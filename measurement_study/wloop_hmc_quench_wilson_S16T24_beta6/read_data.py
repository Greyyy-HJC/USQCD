# %%
#! read the 2pt real part from out.xml file and plot the effective mass

import gvar as gv
import lsqfit as lsf
from read_wilslp_module import *

data_list = []

#! about SaveInterval = 48, nsteps = 75
for conf_num in range(48, 12288 + 48, 48):
    file_path = "out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml".format(conf_num)

    temp = read_wilslp(file_path, Ns=16, Nt=24)
    data_list.append(temp)


Ns = 16
Nt = int(24 / 2)


print(np.shape(data_list))

data_output = np.array(data_list).reshape(256, Ns * Nt)
print(np.shape(data_output))

file_name = "wilson_S16_T24_beta6.txt"
np.savetxt(file_name, data_output, fmt="%.8e", delimiter=" ")


# %%
#! plot the wilson loop W(Lt, Lz)

import matplotlib.pyplot as plt
from liblattice.preprocess import resampling as resam
from liblattice.general import general_plot_funcs as gplt
from liblattice.general.plot_settings import *

# * time like Wilson loops
data_resam = resam.bootstrap(data_list, samp_times=300)
data_avg = gv.dataset.avg_data(data_resam, bstrap=True)
# data_avg = gv.dataset.avg_data(data_list, bstrap=False)

print(np.shape(data_avg))


x_ls = [np.arange(1, Nt + 1) for i in range(Ns)]
y_ls = [gv.mean(data_avg[i]) for i in range(Ns)]
yerr_ls = [gv.sdev(data_avg[i]) for i in range(Ns)]
label_ls = ["Lz={}".format(i) for i in range(1, Ns + 1)]
title = "Wilson Loop (pure gauge)"


plt_axes = [0.12, 0.12, 0.8, 0.8]  # left, bottom, width, height


fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_ls_plot(
    x_ls, y_ls, yerr_ls, label_ls, title, ylim=[10**-6, 10**0], save=False, head=ax
)
plt.yscale("log")
plt.xlabel("Lt")
plt.show()


# %%
#! plot the linear potential aV(nz*a)

data_V = []
for i in range(Ns):
    potential = [np.log(data_avg[i][j] / data_avg[i][j + 1]) for j in range(Nt - 1)]
    data_V.append(potential)

Ns_show = 6

x_ls = [np.arange(1, Nt) for i in range(Ns_show)]
y_ls = [gv.mean(data_V[i]) for i in range(Ns_show)]
yerr_ls = [gv.sdev(data_V[i]) for i in range(Ns_show)]
label_ls = ["Lz={}".format(i) for i in range(1, Ns_show + 1)]
title = "Linear Potential (pure gauge)"

plt_axes = [0.12, 0.12, 0.8, 0.8]  # left, bottom, width, height

fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_ls_plot(x_ls, y_ls, yerr_ls, label_ls, title, save=False, head=ax)
plt.xlabel("Lt")
plt.ylim([-1, 2])
plt.show()


# %%
#! fix nt plot the linear potential aV(nz*a)

if True:
    fix_nt = 5
    nz_range = np.arange(1, 6 + 1)

    aV_fix_nt = [data_V[i][4] for i in nz_range - 1]
    fig = plt.figure(figsize=fig_size)
    ax = plt.axes(plt_axes)
    ax.errorbar(
        nz_range,
        [v.mean for v in aV_fix_nt],
        [v.sdev for v in aV_fix_nt],
        fmt="o",
        label="fix nt={}".format(fix_nt),
        **errorb
    )
    plt.legend()
    plt.xlabel("Lz")
    plt.show()


#! fit aV to get the lattice spacing a
fit_nt = 5  # take fix nt, not index
fit_nz_range = np.arange(1, 6 + 1)  # nz range, not index

avg_V = [data_V[i][fit_nt - 1] for i in fit_nz_range - 1]
print(avg_V)

priors = gv.BufferDict()
priors["a"] = gv.gvar(0.1, 0.5)
priors["A"] = gv.gvar(1, 5)
priors["B"] = gv.gvar(1, 5)


def fcn(x, p):
    nz = x

    val = p["A"] * p["a"] * 1 + p["B"] / nz + 4 * p["a"] ** 2 * (1.65 + p["B"]) * nz

    return val


data_x = fit_nz_range
data_y = avg_V

fit_res = lsf.nonlinear_fit(data=(data_x, data_y), fcn=fcn, prior=priors)

print(fit_res.format(100))


# %%
#! check the correlation with bin

check_point_ns = 1
bin_list = np.arange(1, 33)


check_list = []
for conf_num in range(48, 12288 + 48, 48):
    file_path = "out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml".format(conf_num)

    temp = read_wilslp(file_path, Ns=16, Nt=24, quiet=True)
    check_list.append(temp)

meff = [
    np.log(temp[check_point_ns][:-1] / temp[check_point_ns][1:]) for temp in check_list
]

print(np.shape(meff))

# average the data with bin
avg_ls_ls = []
for nt in range(2, 9):
    avg_ls = []
    for bin_num in bin_list:
        largest_mul = int( (len(meff) // bin_num) * bin_num )

        temp = np.mean(np.array(meff)[:largest_mul, nt].reshape(-1, bin_num), axis=1)

        avg = gv.gvar( np.std(temp) / np.sqrt(len(temp)), 0 )

        avg_ls.append(avg)
    avg_ls_ls.append(avg_ls)

gplt.errorbar_ls_plot(
    [bin_list for nt in range(12)],
    [gv.mean(avg_ls) for avg_ls in avg_ls_ls],
    [gv.sdev(avg_ls) for avg_ls in avg_ls_ls],
    label_ls=["nt={}".format(nt) for nt in range(2, 9)],
    title="aV, bin test with ns = {}".format(check_point_ns),
    save=False,
)



# %%
#! check the correlation with correlation matrix

gap = 8

check_list = []
for conf_num in range(48, 12288 + 48, 48 * gap):
    file_path = "out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml".format(conf_num)

    temp = read_wilslp(file_path, Ns=16, Nt=24, quiet=True)
    check_list.append(temp)

check_list = resam.bootstrap(check_list, samp_times=200)

print(np.shape(check_list))

check_list = check_list.reshape(200, 16 * int(24/2))
check_list_avg = gv.dataset.avg_data(check_list, bstrap=True)

if True:
    import matplotlib.pyplot as plt
    import liblattice.preprocess.resampling as resamp

    # * generate a random data set
    test = np.random.normal(size=(int(256 / gap), 16 * 12))
    test_bs = resamp.bootstrap(test, samp_times=200)
    test_bs_avg = resamp.bs_ls_avg(test_bs)

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax[0].imshow(gv.evalcorr(test_bs_avg))
    ax[1].imshow(gv.evalcorr(check_list_avg))

    # add the colorbar for both plots
    fig.colorbar(ax[0].imshow(gv.evalcorr(test_bs_avg)), ax=ax[0])
    fig.colorbar(ax[1].imshow(gv.evalcorr(check_list_avg)), ax=ax[1])

    # add the title for both plots
    ax[0].set_title("Random data")
    ax[1].set_title("Correlation matrix of {} data".format(int(256 / gap)))

    plt.show()


















# %%
'''
Not so good methods below.
'''

#! check the correlation
fs_p = {"fontsize": 13}  # font size of text, label, ticks

check_point_ns = 8
check_point_nt = 6
gap_list = np.arange(1, 32)

check_ls = []

for gap in gap_list:
    temp_ls = []

    #! about SaveInterval = 24, nsteps = 75
    for conf_num in range(48, 12288 + 48, 48 * gap):
        file_path = "out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml".format(conf_num)

        temp = read_wilslp(file_path, Ns=16, Nt=24, quiet=True)
        temp_ls.append(temp)

    temp_resam = resam.bootstrap(temp_ls, samp_times=50)
    temp_avg = gv.dataset.avg_data(temp_resam, bstrap=True)

    check_ls.append(temp_avg[check_point_ns][check_point_nt])


fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
gplt.errorbar_plot(
    gap_list,
    gv.sdev(check_ls),
    np.zeros_like(check_ls),
    title="Wloop with Ls={}, Lt={}, error v.s. steps".format(
        check_point_ns, check_point_nt
    ),
    ylim=None,
    save=False,
    head=ax,
)
plt.xlabel("steps", **fs_p)
plt.ylabel("error", **fs_p)
plt.show()


# %%
#! check the correlation with gv.evalcorr
#! evalcorr is not a good test

check_point_ns = 8
check_point_nt = 6
gap_list = np.arange(1, 4)

check_ls = []

for gap in gap_list:
    temp_ls = []

    #! about SaveInterval = 24, nsteps = 75
    for conf_num in range(48, 4608 + 48, 48 * gap):
        file_path = "out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml".format(conf_num)

        temp = read_wilslp(file_path, Ns=16, Nt=24, quiet=True)
        temp_ls.append(temp)

    temp_resam = resam.bootstrap(temp_ls, samp_times=50)
    temp_avg = gv.dataset.avg_data(temp_resam, bstrap=True)

    print(np.shape(temp_avg))
    corr = gv.evalcorr(temp_avg)
    print(corr[0][0])


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
for conf_num in range(48, 1536 + 48, 48):
    file_path = "out_xml/wilson_S16_T24_beta6_cfg_{}.out.xml".format(conf_num)

    temp = read_wilslp(file_path, Ns=16, Nt=24, quiet=True)
    data_list.append(temp)

check_data = np.array(
    [data_list[i][check_point_ns][check_point_nt] for i in range(len(data_list))]
)
acf = core(check_data, plot=True)


# %%
