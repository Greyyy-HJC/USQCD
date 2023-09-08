# %%
#! read the 2pt real part from out.xml file and plot the effective mass

import numpy as np
import gvar as gv
from read_2pt_gamma_module import *

data_list = []

for conf_num in range(20, 620, 20):
    file_path = 'out_xml/wilson_S16_T16_beta6_nstep10_cfg_{}.out.xml'.format(conf_num)

    data_list.append( read_real_data_for_gamma(file_path, gamma_val=15) )

print(np.shape(data_list))



# %%
from liblattice.preprocess import resampling as resam
from liblattice.general import general_plot_funcs as gplt

data_resam = resam.bootstrap(data_list, samp_times=50)
data_avg = gv.dataset.avg_data(data_resam, bstrap=True)
# data_avg = gv.dataset.avg_data(data_list, bstrap=False)

# meff = [np.log( data_avg[i] / data_avg[i+1] ) for i in range(len(data_avg) - 1)]

meff = np.arccosh( (data_avg[:-2] + data_avg[2:]) / ( 2 * data_avg[1:-1] ) )

print(meff)

x = np.arange(len(meff))
y = [meff[i].mean for i in range(len(meff))]
yerr = [meff[i].sdev for i in range(len(meff))]
title = 'Effective mass for pure gauge theory'
gplt.errorbar_plot(x, y, yerr, title, save=False, ylim=[0.5,4])


# %%
#! check the stability of the uncertainty

def output_error(gap):
    data_list = []

    for conf_num in range(1, 1025, gap):
        file_path = 'out_xml/pure_gauge_meson_2pt_cfg{}.out.xml'.format(conf_num)

        data_list.append( read_real_data_for_gamma(file_path, gamma_val=15) )

    data_resam = resam.bootstrap(data_list, samp_times=200)
    data_avg = gv.dataset.avg_data(data_resam, bstrap=True)

    meff = [np.log( data_avg[i] / data_avg[i+1] ) for i in range(len(data_avg) - 1)]


    # fit the effective mass with lsqfit
    import lsqfit as lsf

    def fcn(x, p):
        return p['m'] + 0 * x
    
    priors = gv.BufferDict()
    priors['m'] = gv.gvar(2, 0.5)

    x_fit = np.arange(len(meff))[4:7]
    y_fit = meff[4:7]

    fit_res = lsf.nonlinear_fit(data=(x_fit, y_fit), fcn=fcn, prior=priors)

    # return fit_res.p['m'], fit_res.Q
    return meff[5], fit_res.Q

# write a for loop to check the uncertainty change of each data point when the gap is varying
gap_list = np.arange(2, 128, 4)
fit_m_ls = []
Q_ls = []

for gap in gap_list:
    fit_m_ls.append(output_error(gap)[0])
    Q_ls.append(output_error(gap)[1])


gplt.errorbar_plot(gap_list, gv.sdev(fit_m_ls), np.zeros_like(fit_m_ls), title='meff fit results', ylim=None, save=False, head=None)

# %%
print(Q_ls)
# %%
