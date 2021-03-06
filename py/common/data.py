# Copyright (c) 2019 ETH Zurich, Lukas Cavigelli, Georg Rutishauser, Luca Benini
# This file, licensed under Apache 2.0 was adapted from
# https://github.com/lukasc-ch/ExtendedBitPlaneCompression,
# commit 0b175d0d35937b3f2724fe59b0c6cc82802556f6

import torch
import torchvision as tv
import numpy as np
import random
import math
import common.bpc as bpc
from common.util import zero_pad_list, write_sim_file, split_str


import os
import glob
import csv

import sys
sys.path.append('./quantLab')

def getModel(modelName, epoch=None):
#    import torchvision as tv
#    import quantlab.ImageNet.topology as topo

#    loss_func =  torch.nn.CrossEntropyLoss()
    model = None

    if modelName == 'alexnet':
        model = tv.models.alexnet(pretrained=True)
    elif modelName == 'squeezenet':
        model = tv.models.squeezenet1_1(pretrained=True)
    elif modelName == 'resnet34':
        model = tv.models.resnet34(pretrained=True)
    elif modelName == 'vgg16':
        model = tv.models.vgg16_bn(pretrained=True)
    elif modelName == 'mobilenet2':
        model = tv.models.mobilenet_v2(pretrained=True)

    device = torch.cuda.current_device() if torch.cuda.is_available() else torch.device('cpu')
    model = model.to(device)
    assert(model != None)
    return model, device


def getFMs(model, device, datasetPath, numBatches=1, batchSize=10, safetyFactor=1.0, frac=0.01):

    # CREATE DATASET LOADERS
    #import quantLab.quantlab.ImageNet.preprocess as pp
    #datasetTrain, datasetVal, _ =
    #pp.load_datasets('/scratch/datasets/ilsvrc12/', augment=False)
    transform = tv.transforms.Compose([
        tv.transforms.Resize(256),
        tv.transforms.RandomCrop(224),
        tv.transforms.ToTensor()
    ])
    dataset = tv.datasets.ImageFolder(datasetPath, transform=transform)
#    dataset = datasetVal
    model.eval()

    dataLoader = torch.utils.data.DataLoader(dataset, batch_size=batchSize, shuffle=True)

    # SELECT MODULES
    msReLU = list(filter(lambda m: type(m) == torch.nn.modules.ReLU or type(m) == torch.nn.modules.ReLU6, model.modules()))

    def filter_fmaps(tens4, frac):
        # select filt proportion of random channels of 4dim tensor
        if (tens4.dim()==4):
            num_chans = list(tens4.size())[1]
            indices = random.sample(range(num_chans), math.ceil(frac * num_chans))
            return tens4[:, indices, :, :]
        return tens4

    #register hooks to get intermediate outputs:
    def setupFwdHooks(modules):
      outputs = []
      outputs_f = []
      def hook(module, input, output):
          fm = output.detach().contiguous().clone()
          #fm_q, _, dtype = bpc.quantize(fm, quant='fixed{}'.format(quant), safetyFactor=safetyFactor, normalize=True)
          outputs_f.append(filter_fmaps(fm, frac))
          outputs.append(fm)
      for m in modules:
          m.register_forward_hook(hook)
      return outputs_f, outputs

    outputsReLU, outputsReLU_complete = setupFwdHooks(msReLU)

    # PASS IMAGES THROUGH NETWORK
    dataIterator = iter(dataLoader)

    for _ in range(numBatches):
      (image, target) = next(dataIterator)
      image, target = image.to(device), target.to(device)
      model.eval()
      outp = model(image)

    outputs_max = [outp.max().item() for outp in outputsReLU_complete]
    for op, opmax in zip(outputsReLU, outputs_max):
        op.mul_(safetyFactor/opmax)

    return outputsReLU



def getStimuli(model, dataset_path, data_w, num_batches, batch_size, signed=True, safety_factor=0.75, fmap_frac=0.01, num_stims=10000, block_size=8):
    assert data_w in [8, 16, 32]
    def get_dtype(q):
        dt_dict = {8:np.int8, 16:np.int16, 32:np.int32}
        return dt_dict[q]
    if model not in ['all_zeros', 'random', 'last_test']:
        model, device = getModel(model)
        fms = getFMs(model, numBatches=num_batches, batchSize=batch_size, datasetPath=dataset_path, device=device, frac=fmap_frac, safetyFactor=safety_factor)
        fms_flat = torch.tensor([])
        for fm in fms:
            #safety_factor is already applied in getFMs
            fm_quant, _, dtype = bpc.quantize(fm, safetyFactor=1.0, normalize=False, quant='fixed{}'.format(data_w))
            fms_flat = torch.cat([fms_flat, fm_quant.to(torch.device('cpu')).view(-1)])

        #fms_q, _, dtype = bpc.quantize(fms_flat, normalize=True, quant='fixed{}'.format(data_w))
        #data = fms_q.numpy().astype(dtype).tolist()
        data = fms_flat.numpy().astype(get_dtype(data_w)).tolist()
    elif model == 'all_zeros':
        data = [0] * num_stims
    elif model == 'random':
        data = [np.random.randint(-2**(data_w-1), 2**(data_w-1)) for l in range(num_stims)]
    elif model == 'last_test':
        num_stims = num_stims + (-num_stims % block_size)
        # construct a case where there are no zeros, an integer number of
        # blocks of nonzero values and a bunch of zeros afterwards
        data = [np.random.randint(1, 2**(data_w-1)) for l in range(num_stims)] + 100 * [0]
    return data

def write_stats(f, stat_dict):
    with open(f, 'w') as fh:
        for stat in stat_dict:
            fh.write("{:<20}:{:>20.2f}\n".format(stat, stat_dict[stat]))

def genStimFiles(file_prefixes, data_w, *args, modules=['encoder', 'decoder'], max_zrle_len=16, block_size=8, debug_file=None, num_words_w=24, **kwargs):
    fms_q = getStimuli(*args, data_w=data_w, **kwargs)
    fms_q = np.array(fms_q)
    fms_bin = bpc.valuesToBinary(fms_q, data_w)
    fms_bin = split_str(fms_bin, data_w)
    last_bin = ['0']*(len(fms_q)-1) + ['1']
    nz_data = [el for el in fms_q if el != 0]
    nz_data_padded = zero_pad_list(nz_data, block_size)
    bpc_vals, mod_bpc_len = bpc.BPC_words(np.array(nz_data_padded), block_size=block_size, variant='paper', word_w=8, dbg_fn=debug_file, return_mod_len=True)
    while kwargs['model']=='last_test' and mod_bpc_len != 0:
        fms_q = getStimuli(*args, data_w=data_w, **kwargs)
        fms_q = np.array(fms_q)
        fms_bin = bpc.valuesToBinary(fms_q, data_w)
        fms_bin = split_str(fms_bin, data_w)
        last_bin = ['0']*(len(fms_q)-1) + ['1']
        nz_data = [el for el in fms_q if el != 0]
        nz_data_padded = zero_pad_list(nz_data, block_size)
        bpc_vals, mod_bpc_len = bpc.BPC_words(np.array(nz_data_padded), block_size=block_size, variant='paper', word_w=8, dbg_fn=debug_file, return_mod_len=True)

    znz_vals = bpc.ZRLE_words(fms_q, max_burst_len=max_zrle_len, wordwidth=data_w)
    nw_bin = bpc.valuesToBinary(np.array([len(fms_q)-1]), num_words_w)
    compr_ratio = len(fms_q)/(len(bpc_vals)+len(znz_vals))
    sparsity = 1 - len(nz_data)/len(fms_q)
    znz_last = ['0']*(len(znz_vals)-1) + ['1']
    bpc_last = ['0']*(len(bpc_vals)-1) + ['1']
    stat_dict = {'Compression Ratio':compr_ratio, 'Sparsity':sparsity, '# of Stimuli':len(fms_q)}
    if 'encoder' in modules:
        write_sim_file(data=zip(fms_bin, last_bin), filename=file_prefixes['encoder']+'_input.stim', length=len(fms_bin))
        write_sim_file(zip(bpc_vals, bpc_last), file_prefixes['encoder']+'_bpc.expresp', len(bpc_vals))
        write_sim_file(zip(znz_vals, znz_last), file_prefixes['encoder']+'_znz.expresp', len(znz_vals))
        write_stats(file_prefixes['encoder']+'_stats.log', stat_dict)
    if 'decoder' in modules:
        write_sim_file(data=zip([nw_bin]), filename=file_prefixes['decoder']+'_num_words_input.stim', length=1)
        write_sim_file(zip(bpc_vals, bpc_last), file_prefixes['decoder']+'_bpc_input.stim', len(bpc_vals))
        write_sim_file(zip(znz_vals, znz_last), file_prefixes['decoder']+'_znz_input.stim', len(znz_vals))
        write_sim_file(zip(fms_bin, last_bin), file_prefixes['decoder']+'_data_output.expresp', len(fms_q))
        write_stats(file_prefixes['decoder']+'_stats.log', stat_dict)
