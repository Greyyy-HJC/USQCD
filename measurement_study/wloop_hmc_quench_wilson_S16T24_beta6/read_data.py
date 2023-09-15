# %%
#! read the 2pt real part from out.xml file and plot the effective mass

import gvar as gv
import lsqfit as lsf
from read_wilslp_module import *

data_list = []

#! about SaveInterval = 48, nsteps = 75
for conf_num in range(48, 1536+48, 48):
    file_path = 'out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml'.format(conf_num)

    temp = read_wilslp(file_path, Ns=16, Nt=24)
    data_list.append(temp)

print(np.shape(data_list))

Ns = 16
Nt = int(24 / 2)




# %%
#! plot the wilson loop W(Lt, Lz)

import matplotlib.pyplot as plt
from liblattice.preprocess import resampling as resam
from liblattice.general import general_plot_funcs as gplt
from liblattice.general.plot_settings import *

#* time like Wilson loops
data_resam = resam.bootstrap(data_list, samp_times=100)
data_avg = gv.dataset.avg_data(data_resam, bstrap=True) 
# data_avg = gv.dataset.avg_data(data_list, bstrap=False)

print( np.shape(data_avg) ) 


x_ls = [ np.arange(1, Nt+1) for i in range(Ns) ]
y_ls = [ gv.mean(data_avg[i]) for i in range(Ns) ]
yerr_ls = [ gv.sdev(data_avg[i]) for i in range(Ns) ]
label_ls = [ 'Lz={}'.format(i) for i in range(1, Ns+1) ]
title = 'Wilson Loop (pure gauge)'


plt_axes = [0.12, 0.12, 0.8, 0.8]  # left, bottom, width, height


fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_ls_plot(x_ls, y_ls, yerr_ls, label_ls, title, ylim=[10**-6,10**0], save=False, head=ax)
plt.yscale('log')
plt.xlabel('Lt')
plt.show()

print(yerr_ls[11])


# %%
#! plot the linear potential aV(nz*a)

data_V = []
for i in range(Ns):
    potential = [np.log( data_avg[i][j] / data_avg[i][j + 1] ) for j in range(Nt-1)]
    data_V.append(potential)

Ns_show = 6

x_ls = [ np.arange(1, Nt) for i in range(Ns_show) ]
y_ls = [ gv.mean(data_V[i]) for i in range(Ns_show) ]
yerr_ls = [ gv.sdev(data_V[i]) for i in range(Ns_show) ]
label_ls = [ 'Lz={}'.format(i) for i in range(1, Ns_show+1) ]
title = 'Linear Potential (pure gauge)'

plt_axes = [0.12, 0.12, 0.8, 0.8]  # left, bottom, width, height

fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_ls_plot(x_ls, y_ls, yerr_ls, label_ls, title, save=False, head=ax)
plt.xlabel('Lt')
plt.ylim([-1, 2])
plt.show()

#! take Lt = {...} to average to get the aV
avg_V = [ np.sum(data_V[i][4:8]) / 4 for i in range(8) ]
print(avg_V)


# %%
#! fit aV to get the lattice spacing a

priors = gv.BufferDict()
priors['a'] = gv.gvar(0.1, 0.5)
priors['A'] = gv.gvar(1, 5)
priors['B'] = gv.gvar(1, 5)


def fcn(x, p):
    nz = x

    val = p['A'] * p['a'] + p['B'] / nz + 4 * p['a']**2 * ( 1.65 + p['B'] ) * nz

    return val


data_x = np.arange(3, 7)
data_y = avg_V[2:-2]

fit_res = lsf.nonlinear_fit(data=(data_x, data_y), fcn=fcn, prior=priors)

print(fit_res.format(100))



# %%
#! check the correlation
fs_p = {"fontsize": 13}  # font size of text, label, ticks

check_point_ns = 15
check_point_nt = 11
gap_list = np.arange(1, 6)

check_ls = []

for gap in gap_list:
    temp_ls = []

    #! about SaveInterval = 24, nsteps = 75
    for conf_num in range(48, 1536+48, 48*gap):
        file_path = 'out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml'.format(conf_num)

        temp = read_wilslp(file_path, Ns=16, Nt=24, quiet=True)
        temp_ls.append(temp)


    temp_resam = resam.bootstrap(temp_ls, samp_times=50)
    temp_avg = gv.dataset.avg_data(temp_resam, bstrap=True) 

    check_ls.append(temp_avg[check_point_ns][check_point_nt])


fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_plot(gap_list, gv.sdev(check_ls), np.zeros_like(check_ls), title='Wloop with Ls={}, Lt={}, error v.s. steps'.format(check_point_ns, check_point_nt), ylim=None, save=False, head=ax)
plt.xlabel('steps', **fs_p)
plt.ylabel('error', **fs_p)
plt.show()



# %%
#! check the autocorrelation with tsa
import statsmodels.api as sm
import statsmodels.graphics.tsaplots as tsa_plots

def core(data: np.ndarray, plot: bool) -> np.ndarray:
    """
    Computes the autocorrelation function (ACF) of the given data and returns it as an array.
    If plot is True, also plots the ACF using the tsa_plots.plot_acf function.

    Args:
        data: A 1D numpy array of data to compute the ACF for.
        plot: A boolean indicating whether to plot the ACF.

    Returns:
        A 1D numpy array containing the ACF of the given data.
    """
    acf = sm.tsa.acf(data, nlags=data.shape[0], fft=False)
    if plot:
        tsa_plots.plot_acf(data, lags=len(data) - 1)
        plt.ylim(-1.1, 1.1)
        plt.show()
    return acf

data_list = []
#! about SaveInterval = 48, nsteps = 75
for conf_num in range(48, 1536+48, 48):
    file_path = 'out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml'.format(conf_num)

    temp = read_wilslp(file_path, Ns=16, Nt=24, quiet=True)
    data_list.append(temp)

check_data = np.array( [data_list[i][check_point_ns][check_point_nt] for i in range(len(data_list))] )
acf = core(check_data, plot=True)

# %%
