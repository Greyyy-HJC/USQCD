# %%
#! read the 2pt real part from out.xml file and plot the effective mass

import gvar as gv
import lsqfit as lsf
from read_wilslp_module import *

data_list = []

for conf_num in range(20, 620, 20*4):
    file_path = 'out_xml/wilson_S16_T16_beta6_cfg_{}.out.xml'.format(conf_num)

    temp = read_wilslp(file_path, Ns=16, Nt=16)
    data_list.append(temp)

print(np.shape(data_list))

Ns = 16
Nt = int(16 / 2)


# %%
#! plot the wilson loop W(Lt, Lz)

import matplotlib.pyplot as plt
from liblattice.preprocess import resampling as resam
from liblattice.general import general_plot_funcs as gplt
from liblattice.general.plot_settings import *

#* time like Wilson loops
data_resam = resam.bootstrap(data_list, samp_times=50)
# data_avg = gv.dataset.avg_data(data_resam, bstrap=True) 
data_avg = gv.dataset.avg_data(data_list, bstrap=False)

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
#! fit to get aV
if True:
    fit_V = []
    for i in range(4, 7):
        priors = gv.BufferDict()
        priors['C'] = gv.gvar(1, 5)
        priors['V'] = gv.gvar(1, 5)

        def fcn_V(x, p):
            nt = x
            return p['C'] * np.exp(- p['V'] * nt)

        data_t = np.arange(2, 8)
        data_y = data_avg[i][1:-1]

        fit_res = lsf.nonlinear_fit(data=(data_t, data_y), fcn=fcn_V, prior=priors)
        print(fit_res)

        fit_V.append(fit_res.p['V'])

    print(fit_V)

    plt.plot(data_t, gv.mean(data_y), 'o')




#! use fit V
if False:
    priors = gv.BufferDict()
    priors['a'] = gv.gvar(0.1, 0.5)
    priors['A'] = gv.gvar(1, 5)
    priors['B'] = gv.gvar(1, 5)


    def fcn(x, p):
        nz = x

        val = p['A'] * p['a'] + p['B'] / nz + 4 * p['a']**2 * ( 1.65 + p['B'] ) * nz

        return val


    data_x = np.arange(1, 9)
    data_y = fit_V

    fit_res = lsf.nonlinear_fit(data=(data_x, data_y), fcn=fcn, prior=priors)

    print(fit_res.format(100))


# %%
