# %%
#! read the 2pt real part from out.xml file and plot the effective mass

import numpy as np
import gvar as gv
from read_2pt_gamma_module import *

data_list = []

for conf_num in range(1, 11):
    file_path = 'out_xml/pure_gauge_meson_2pt_cfg{}.out.xml'.format(conf_num)

    data_list.append([])
    data_list[conf_num - 1] = read_real_data_for_gamma(file_path, gamma_val=15)

print(np.shape(data_list))



# %%
from liblattice.preprocess import resampling as resam
from liblattice.general import general_plot_funcs as gplt

data_resam = resam.bootstrap(data_list, samp_times=50)
data_avg = gv.dataset.avg_data(data_resam, bstrap=True)

print(data_avg)

meff = [np.log( data_avg[i] / data_avg[i+1] ) for i in range(len(data_avg) - 1)]


x = np.arange(len(meff))
y = [meff[i].mean for i in range(len(meff))]
yerr = [meff[i].sdev for i in range(len(meff))]
title = 'Effective mass for pure gauge theory'
gplt.errorbar_plot(x, y, yerr, title, save=False, ylim=[0.5,4])


# %%
