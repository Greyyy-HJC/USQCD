# %%
import numpy as np
import matplotlib.pyplot as plt

def select_specific_strings(file_path, start_string, end_string):
    selected_nums = []

    with open(file_path, 'r') as file:
        for line in file:
            if start_string in line and end_string in line:
                selected_string = line.split(start_string)[1].split(end_string)[0]
                selected_num = float(selected_string)
                selected_nums.append(selected_num)

    return selected_nums


plt.figure()

for start_string, end_string in zip(["<w_plaq>", "<s_plaq>", "<t_plaq>"], ["</w_plaq>", "</s_plaq>", "</t_plaq>"]):
    selected_nums = select_specific_strings("pure_gauge_gen.out.xml", start_string, end_string)

    plt.scatter(np.arange(len(selected_nums)), selected_nums, label=start_string, marker="x", s=10)

plt.legend()
plt.show()


plt.figure()

for start_string, end_string in zip(["<plane_01_plaq>", "<plane_02_plaq>", "<plane_12_plaq>", "<plane_03_plaq>", "<plane_13_plaq>", "<plane_23_plaq>", "<link>"], ["</plane_01_plaq>", "</plane_02_plaq>", "</plane_12_plaq>", "</plane_03_plaq>", "</plane_13_plaq>", "</plane_23_plaq>", "</link>"]):
    selected_nums = select_specific_strings("pure_gauge_gen.out.xml", start_string, end_string)

    plt.scatter(np.arange(len(selected_nums)), selected_nums, label=start_string, marker="x", s=10)

plt.legend()
plt.show()



# %%
