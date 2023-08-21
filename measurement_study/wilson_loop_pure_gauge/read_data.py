# %%
#! read the 2pt real part from out.xml file and plot the effective mass

import gvar as gv
from read_wilslp_module import *

data_list = []

for conf_num in range(1, 11):
    file_path = 'out_xml/pure_gauge_wilslp_cfg{}.out.xml'.format(conf_num)

    data_list.append([])
    data_list[conf_num - 1] = read_wilslp(file_path)

print(np.shape(data_list))



# %%
from liblattice.preprocess import resampling as resam
from liblattice.general import general_plot_funcs as gplt

data_resam = resam.bootstrap(data_list, samp_times=20)
data_avg = gv.dataset.avg_data(data_resam, bstrap=True)

print( np.shape(data_avg) )


# %%
def average_by_sum(lis):
    sums = {}
    counts = {}

    # Iterate over each element in the lis
    for i in range(len(lis)):
        for j in range(len(lis[i])):
            value = lis[i][j]
            key = i + j

            # Update the sum and count for the corresponding key
            if key in sums:
                sums[key] += value
                counts[key] += 1
            else:
                sums[key] = value
                counts[key] = 1

    # Calculate the averages for each key
    averages = {}
    for key in sums:
        averages[key] = sums[key] / counts[key]

    return averages

data_avg_length_avg = average_by_sum(data_avg)

print( data_avg_length_avg )

# %%

x = np.array( [key for key in data_avg_length_avg] )
y = [data_avg_length_avg[key].mean for key in data_avg_length_avg]
yerr = [data_avg_length_avg[key].sdev for key in data_avg_length_avg]
title = 'Wilson Loop (pure gauge)'
gplt.errorbar_plot(x, y, yerr, title, save=False)


# %%
