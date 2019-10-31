set assert_stop_level never
simvision -input encoder_simvision_commands.tcl

database -open waves -into waves.shm -default
probe -create -database waves ebpc_encoder_tb.dut_i.clk_i ebpc_encoder_tb.dut_i.rst_ni ebpc_encoder_tb.dut_i.data_i ebpc_encoder_tb.dut_i.last_i ebpc_encoder_tb.dut_i.vld_i ebpc_encoder_tb.dut_i.rdy_o ebpc_encoder_tb.dut_i.bpc_data_o ebpc_encoder_tb.dut_i.bpc_vld_o ebpc_encoder_tb.dut_i.bpc_rdy_i ebpc_encoder_tb.dut_i.znz_data_o ebpc_encoder_tb.dut_i.znz_vld_o ebpc_encoder_tb.dut_i.znz_rdy_i ebpc_encoder_tb.dut_i.idle_o ebpc_encoder_tb.dut_i.block_cnt_d ebpc_encoder_tb.dut_i.block_cnt_q ebpc_encoder_tb.dut_i.bpc_idle ebpc_encoder_tb.dut_i.data_reg_d ebpc_encoder_tb.dut_i.data_reg_en ebpc_encoder_tb.dut_i.data_reg_q ebpc_encoder_tb.dut_i.data_to_bpc ebpc_encoder_tb.dut_i.flush ebpc_encoder_tb.dut_i.is_one_to_znz ebpc_encoder_tb.dut_i.last_d ebpc_encoder_tb.dut_i.last_q ebpc_encoder_tb.dut_i.rdy_from_bpc ebpc_encoder_tb.dut_i.rdy_from_znz ebpc_encoder_tb.dut_i.state_d ebpc_encoder_tb.dut_i.state_q ebpc_encoder_tb.dut_i.vld_to_bpc ebpc_encoder_tb.dut_i.vld_to_znz ebpc_encoder_tb.dut_i.wait_rdy_d ebpc_encoder_tb.dut_i.wait_rdy_q ebpc_encoder_tb.dut_i.znz_idle ebpc_encoder_tb.dut_i.bpc_encoder_i.data_i ebpc_encoder_tb.dut_i.bpc_encoder_i.vld_i ebpc_encoder_tb.dut_i.bpc_encoder_i.rdy_o ebpc_encoder_tb.dut_i.bpc_encoder_i.data_o ebpc_encoder_tb.dut_i.bpc_encoder_i.vld_o ebpc_encoder_tb.dut_i.bpc_encoder_i.rdy_i ebpc_encoder_tb.dut_i.bpc_encoder_i.flush_i ebpc_encoder_tb.dut_i.bpc_encoder_i.idle_o ebpc_encoder_tb.dut_i.bpc_encoder_i.vld_enc_to_coder ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_idle ebpc_encoder_tb.dut_i.bpc_encoder_i.rdy_coder_to_enc ebpc_encoder_tb.dut_i.bpc_encoder_i.flush_dbp_dbx_to_coder ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_enc_to_coder ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_idle ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.data_i ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.vld_i ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.rdy_o ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.dbp_block_o ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.vld_o ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.rdy_i ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.flush_i ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.flush_o ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.idle_o ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.dbp ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.diffs_d ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.diffs_q ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.fill_cnt_d ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.fill_cnt_q ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.last_item_d ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.last_item_q ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.shift ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.state_d ebpc_encoder_tb.dut_i.bpc_encoder_i.dbp_dbx_i.state_q ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.dbp_block_i ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.vld_i ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.rdy_o ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.data_o ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.vld_o ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.rdy_i ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.flush_i ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.idle_o ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.code_symb ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.data ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.dbp_block_from_fifo ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.dbx_cnt_d ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.dbx_cnt_q ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.flush ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.last_was_zero_d ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.last_was_zero_q ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.rdy_to_slice ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.shift ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.shift_rdy ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.shift_vld ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.state_d ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.state_q ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.streamer_idle ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.vld_from_slice ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.zero_cnt_d ebpc_encoder_tb.dut_i.bpc_encoder_i.seq_coder_i.zero_cnt_q
run