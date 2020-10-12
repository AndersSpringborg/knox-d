def line_wrapper(input_file, wrap_length):
    with open(input_file, 'r') as input_file, open('Data/output.txt', 'w') as output_file:
        for line in input_file:
            words = line.split()
            for i in range(0, len(words)):
                output_file.write('%s ' % words[i])
                if i != 0 and i % (wrap_length - 1) == 0:
                    output_file.write("\n")


def split_file(file_name, lines_per_smallfile):
    num = 0
    smallfile = None
    with open(file_name) as bigfile:
        for line_number, line in enumerate(bigfile):
            if line_number % lines_per_smallfile == 0:
                if smallfile:
                    smallfile.close()

                small_filename = f'Data/small_file_{num}.txt'
                smallfile = open(small_filename, "w")
                num += 1
            smallfile.write(line)
        if smallfile:
            smallfile.close()
