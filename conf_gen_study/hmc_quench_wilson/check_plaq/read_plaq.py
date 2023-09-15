# %%
#! read the w_plaq from out.xml file and plot

import numpy as np
import gvar as gv

# define a function to select all numbers in lines with a specific string prefix and suffix
def select_specific_num(file_path, start_string, end_string, start_line, end_line):
    selected_nums = []

    with open(file_path, 'r') as file:
        line_num = 0
        for line in file:
            line_num += 1
            if line_num >= start_line and line_num <= end_line:
                if start_string in line and end_string in line:
                    selected_string = line.split(start_string)[1].split(end_string)[0]
                    try:
                        selected_num = float(selected_string)
                        selected_nums.append(selected_num)
                    except ValueError:
                        pass

    return selected_nums


# define a function to recognize the lines with a specific string prefix and suffix, if the middle string is "true", then append 1, if "false", then append 0
def select_specific_bool(file_path, start_string, end_string, start_line, end_line):
    selected_bools = []

    with open(file_path, 'r') as file:
        line_num = 0
        for line in file:
            line_num += 1
            if line_num >= start_line and line_num <= end_line:
                if start_string in line and end_string in line:
                    selected_string = line.split(start_string)[1].split(end_string)[0]
                    if selected_string == 'true':
                        selected_bools.append(1)
                    elif selected_string == 'false':
                        selected_bools.append(0)
                    else:
                        pass

    return selected_bools


# %%
start_string = '<w_plaq>'
end_string = '</w_plaq>'
start_line = 0
end_line = 25000

nstep = 50

# file_path = 'quench_hmc_nstep_{}.out.xml'.format(nstep)
file_path = 'quench_hmc_S16T24_nstep_{}.out.xml'.format(nstep)



plaq_ls = select_specific_num(file_path, start_string, end_string, start_line, end_line)

print(plaq_ls)
print(np.shape(plaq_ls))

import matplotlib.pyplot as plt
from liblattice.general.plot_settings import *
from liblattice.general import general_plot_funcs as gplt

plt_axes = [0.12, 0.12, 0.8, 0.8]  # left, bottom, width, height
fs_p = {"fontsize": 13}  # font size of text, label, ticks
ls_p = {"labelsize": 13}


fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
ax.scatter(np.arange(len(plaq_ls)), plaq_ls, marker='x')
ax.tick_params(direction="in", top="on", right="on", **ls_p)
ax.grid(linestyle=":")
plt.ylim([0.59, 0.60])
plt.title('w_plaq with nstep = {}'.format(nstep), **fs_p)



# %%
start_string = '<AcceptP>'
end_string = '</AcceptP>'
start_line = 4187
end_line = 25000

nstep = 30

file_path = 'quench_hmc_nstep_{}.out.xml'.format(nstep)
# file_path = 'quench_hmc_S16T24_nstep_{}.out.xml'.format(nstep)



bool_ls = select_specific_bool(file_path, start_string, end_string, start_line, end_line)

acc_rate = round(np.sum(bool_ls) / len(bool_ls), 3)

fig = plt.figure(figsize=fig_size)
ax = plt.axes(plt_axes)
ax.plot(np.arange(len(bool_ls)), bool_ls, linewidth=0.7)
ax.tick_params(direction="in", top="on", right="on", **ls_p)
ax.grid(linestyle=":")
plt.ylim([-0.1, 1.1])
plt.title('w_plaq with nstep = {}, accept rate = {}'.format(nstep, acc_rate), **fs_p)

# %%
