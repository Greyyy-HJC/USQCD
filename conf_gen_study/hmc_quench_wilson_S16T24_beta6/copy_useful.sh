#!/bin/bash

# copy useful results to the new folder
for conf_num in {48..768..48}
do
    cp /home/jinchen/USQCD/config/hmc_quench_wilson_S16T24_beta6_round1/hmc_wilson_S16T24_beta6_nstep75_restart_${conf_num}.xml /home/jinchen/USQCD/config/hmc_quench_wilson_S16T24_beta6_round2/hmc_wilson_S16T24_beta6_nstep75_restart_${conf_num}.xml
done