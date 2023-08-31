# %%
#! This module is used to read the wilson loop data from the out.xml file of the pure gauge measurement, choose the wloop1 block and return the ns * ns matrix for different shapes of the loop: 1 * 1, 1 * 2, ... ns * ns.
import re
import numpy as np

def find_which_line(file_path, str_to_find):
    """
    Reads the file at the given file_path and returns a list of line numbers where the given str_to_find is found.

    Args:
        file_path: The path to the file to read.
        str_to_find: The string to search for in the file.

    Returns:
        A list of line numbers where the given str_to_find is found.
    """
    matching_lines = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if str_to_find in line:
                matching_lines.append(line_num)
    return matching_lines


def extract_data(file_path, start_line, end_line, Ns, Nt):
    with open(file_path, 'r') as file:
        content = file.readlines()

    if end_line is None:
        end_line = len(content)

    pattern = r'<loop>(.*?)</loop>' #! each line is varying nt with fixed nr
    matches = []

    for line_num, line in enumerate(content, start=1):
        if start_line <= line_num <= end_line:
            match = re.search(pattern, line)
            if match:
                numbers = match.group(1).split()
                matches.extend(numbers)

    matches = np.array([float(match) for match in matches]).reshape(int(Ns), int(Nt/2))

    return matches


def read_wilslp(file_path, Ns, Nt):
    #* firstly find out the line number of the line start to search and the line end to search
    str_to_start = '<wloop2>' #! wloop2 is the time like loops
    matching_lines = find_which_line(file_path, str_to_start)
    start_line = matching_lines[0]

    print("Find " + str_to_start + " in line " + str(start_line) + ".")


    str_to_end = '</wloop2>'
    matching_lines = find_which_line(file_path, str_to_end)
    end_line = matching_lines[0]

    print("Find " + str_to_end + " in line " + str(end_line) + ".")


    #* secondly find out the string between start_string and end_string, which is the data we want
    wloop = extract_data(file_path, start_line, end_line, Ns, Nt)

    return wloop


#! Usage: read the file at "file_path" and get the 2pt data for gamma_value = "gamma_val"

if __name__ == "__main__":
    file_path = 'out_xml/pure_gauge_wilslp_cfg1.out.xml'  
    wloop1 = read_wilslp(file_path)
    print(wloop1)


# %%
