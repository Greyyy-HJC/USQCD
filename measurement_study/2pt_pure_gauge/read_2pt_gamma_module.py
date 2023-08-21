# %%
#! This module is used to read the 2pt data from the out.xml file of the pure gauge measurement, choose a specific gamma value and return the real part for the 2pt data.


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


def select_specific_strings(file_path, start_string, end_string, start_line, end_line):
    """
    Reads the file at the given file_path and selects the strings that are between the start_string and end_string
    on the lines between start_line and end_line. The selected strings are converted to floats and returned as a list.

    Args:
        file_path: The path to the file to read.
        start_string: The string that marks the beginning of the selected string.
        end_string: The string that marks the end of the selected string.
        start_line: The line number to start selecting strings from.
        end_line: The line number to stop selecting strings at.

    Returns:
        A list of floats that were selected from the file.
    """
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


def read_real_data_for_gamma(file_path, gamma_val):
    """
    Reads the file at the given file_path and returns a list of real data for the given gamma_val.

    Args:
        gamma_val: The gamma value to get the real data for.
        file_path: The path to the file to read.

    Returns:
        A list of real data for the given gamma_val.
    """

    #* firstly find out the line number of the line start to search and the line end to search
    str_to_start = '<gamma_value>' + str(gamma_val) + '</gamma_value>'
    matching_lines = find_which_line(file_path, str_to_start)
    start_line = matching_lines[0]

    print("Find " + str_to_start + " in line " + str(start_line) + ".")


    if gamma_val == 15:
        #* if gamma_val = 15, then the end_line is the last line of the file

        total_lines = sum(1 for line in open(file_path)) # total number of lines in the file
        end_line = total_lines

    else:
        str_to_end = '<gamma_value>' + str(gamma_val + 1) + '</gamma_value>'
        matching_lines = find_which_line(file_path, str_to_end)
        end_line = matching_lines[0]

        print("Find " + str_to_end + " in line " + str(end_line) + ".")


    #* secondly find out the string between start_string and end_string, which is the data we want
    start_string = "<re>" # real part
    end_string = "</re>"

    #* search for the line between start_line and end_line
    real_data = select_specific_strings(file_path, start_string, end_string, start_line, end_line)

    return real_data


#! Usage: read the file at "file_path" and get the 2pt data for gamma_value = "gamma_val"

if __name__ == "__main__":
    file_path = 'out_xml/pure_gauge_meson_2pt_cfg1.out.xml'  
    data = read_real_data_for_gamma(file_path, gamma_val=15)
    print(data)


# %%
