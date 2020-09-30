
def linewrapper(input_file, wrap_length):
    with open(input_file, 'r') as input_file, open('Data/output.txt', 'w') as output_file:
        for line in input_file:
            words = line.split()
            for i in range(0, len(words)):
                output_file.write('%s ' % words[i])
                if i != 0 and i % (wrap_length - 1) == 0:
                    output_file.write("\n")

def splitFile(fname, lnumber):
    lines_per_file = lnumber
    num = 0
    smallfile = None
    with open(fname) as bigfile:
        for lineno, line in enumerate(bigfile):
            if lineno % lines_per_file == 0:
                if smallfile:
                    smallfile.close()
                small_filename = 'Data/small_file_{}.txt'.format(num)
                smallfile = open(small_filename, "w")
                num += 1
            smallfile.write(line)
        if smallfile:
            smallfile.close()
