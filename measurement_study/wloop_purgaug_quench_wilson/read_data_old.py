# %%
#! read the 2pt real part from out.xml file and plot the effective mass

import gvar as gv
import lsqfit as lsf
from read_wilslp_module import *

data_list = []

for conf_num in range(1, 31):
    file_path = 'out_xml/wilson_S16_T16_beta6_cfg{}.out.xml'.format(conf_num)

    temp = read_wilslp(file_path, Ns=16, Nt=16)
    data_list.append(temp)

print(np.shape(data_list))



# %%
#! plot the wilson loop W(Lt, Lz)

import matplotlib.pyplot as plt
from liblattice.preprocess import resampling as resam
from liblattice.general import general_plot_funcs as gplt
from liblattice.general.plot_settings import *

#* time like Wilson loops
data_resam = resam.bootstrap(data_list, samp_times=500)
data_avg = gv.dataset.avg_data(data_resam, bstrap=True) 

print( np.shape(data_avg) ) 


x_ls = [ np.arange(1, 9) for i in range(8) ]
y_ls = [ gv.mean(data_avg[i]) for i in range(8) ]
yerr_ls = [ gv.sdev(data_avg[i]) for i in range(8) ]
label_ls = [ 'Lz={}'.format(i) for i in range(1, 9) ]
title = 'Wilson Loop (pure gauge)'


plt_axes = [0.12, 0.12, 0.8, 0.8]  # left, bottom, width, height


fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_ls_plot(x_ls, y_ls, yerr_ls, label_ls, title, ylim=[10**-6,10**0], save=False, head=ax)
plt.yscale('log')
plt.xlabel('Lt')
plt.show()


# %%
#! plot the linear potential aV(nz*a)

data_V = []
for i in range(8):
    potential = [np.log( data_avg[i][j] / data_avg[i][j + 1] ) for j in range(7)]
    data_V.append(potential)

x_ls = [ np.arange(1, 8) for i in range(8) ]
y_ls = [ gv.mean(data_V[i]) for i in range(8) ]
yerr_ls = [ gv.sdev(data_V[i]) for i in range(8) ]
label_ls = [ 'Lz={}'.format(i) for i in range(1, 9) ]
title = 'Linear Potential (pure gauge)'

plt_axes = [0.12, 0.12, 0.8, 0.8]  # left, bottom, width, height

fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_ls_plot(x_ls, y_ls, yerr_ls, label_ls, title, save=False, head=ax)
plt.xlabel('Lt')
# plt.ylim(0.1, 0.3)
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


data_x = np.arange(1, 9)
data_y = avg_V[:]

fit_res = lsf.nonlinear_fit(data=(data_x, data_y), fcn=fcn, prior=priors)

print(fit_res.format(100))


# %%
#! fit to get aV
if True:
    fit_V = []
    for i in range(8):
        priors = gv.BufferDict()
        priors['C0'] = gv.gvar(1, 5)
        priors['C1'] = gv.gvar(1, 5)
        priors['V'] = gv.gvar(1, 5)
        priors['E1'] = gv.gvar(1, 5)

        def fcn_V(x, p):
            nt = x
            return p['C0'] * np.exp(- p['V'] * nt) * (1 + p['C1'] * np.exp(- p['E1'] * nt) )

        data_t = np.arange(2, 8)
        data_y = data_V[i][1:7]

        fit_res = lsf.nonlinear_fit(data=(data_t, data_y), fcn=fcn_V, prior=priors)
        print(fit_res.format(100))

        fit_V.append(fit_res.p['V'])

    print(fit_V)




#! use fit V
if True:
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
