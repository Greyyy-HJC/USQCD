# %%
import gvar as gv
import lsqfit as lsf
from read_wilslp_module import *

def read_wilslp_milc(file_path, Ns, Nt):
    #* firstly find out the line number of the line start to search and the line end to search
    str_to_start = '<wloop2>' #! wloop2 is the time like loops
    start_lines = find_which_line(file_path, str_to_start)

    str_to_end = '</wloop2>'
    end_lines = find_which_line(file_path, str_to_end)

    num_conf = len(start_lines)

    wloop_ls = []

    for i in range(num_conf):
        start_line = start_lines[i]
        print("Find " + str_to_start + " in line " + str(start_line) + ".")

        
        end_line = end_lines[i]
        print("Find " + str_to_end + " in line " + str(end_line) + ".")

        #* secondly find out the string between start_string and end_string, which is the data we want
        wloop = extract_data(file_path, start_line, end_line, Ns, Nt)
        wloop_ls.append(wloop)

    return wloop_ls


Ns = 24
Nt = 32

file_path = 'a12m310_wlp_200.txt'

wloop_ls = read_wilslp_milc(file_path, Ns, Nt*2)


# %%
#! plot the wilson loop W(Lt, Lz)

import matplotlib.pyplot as plt
from liblattice.preprocess import resampling as resam
from liblattice.general import general_plot_funcs as gplt
from liblattice.general.plot_settings import *

#* time like Wilson loops
data_resam = resam.bootstrap(wloop_ls, samp_times=200)
data_avg = gv.dataset.avg_data(data_resam, bstrap=True)

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


# %%
#! plot the linear potential aV(nz*a)

Ns = 8

data_V = []
for i in range(Ns):
    potential = [np.log( data_avg[i][j] / data_avg[i][j + 1] ) for j in range(Nt-1)]
    data_V.append(potential)

x_ls = [ np.arange(1, Nt) for i in range(Ns) ]
y_ls = [ gv.mean(data_V[i]) for i in range(Ns) ]
yerr_ls = [ gv.sdev(data_V[i]) for i in range(Ns) ]
label_ls = [ 'Lz={}'.format(i) for i in range(1, Ns+1) ]
title = 'Linear Potential (pure gauge)'

plt_axes = [0.12, 0.12, 0.8, 0.8]  # left, bottom, width, height

fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_ls_plot(x_ls, y_ls, yerr_ls, label_ls, title, save=False, head=ax)
plt.xlabel('Lt')
plt.ylim([-1, 2])
plt.show()

#! take Lt = {...} to average to get the aV
avg_V = [ np.sum(data_V[i][7:10]) / 3 for i in range(Ns) ]
print(avg_V)

# %%
#! fit aV to get the lattice spacing a

priors = gv.BufferDict()
priors['a'] = gv.gvar(0.1, 0.5)
priors['A'] = gv.gvar(1, 5)
priors['B'] = gv.gvar(1, 5)


def fcn(x, p):
    nz = x

    val = p['A'] * (nz + 12) * p['a'] + p['B'] / nz + 4 * p['a']**2 * ( 1.65 + p['B'] ) * nz

    return val


data_x = np.arange(1, Ns+1)[1:]
data_y = avg_V[1:]

fit_res = lsf.nonlinear_fit(data=(data_x, data_y), fcn=fcn, prior=priors)

print(fit_res.format(100))


# %%
aV_fix_nt = [ data_V[i][8] for i in range(Ns) ]
fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
ax.errorbar(np.arange(1, Ns+1), [v.mean for v in aV_fix_nt], [v.sdev for v in aV_fix_nt], fmt='o', label='data', **errorb)
plt.legend()
plt.xlabel('Lz')
plt.show()

# %%
