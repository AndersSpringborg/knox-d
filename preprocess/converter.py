def convert_to_csv(input, output, header):
    input_file = open(input, encoding="latin9")

    outfile_file = open(output, "w", encoding="utf-8", errors="replace")

    outfile_file.write(",".join(header) + "\n")
    current_line = []
    for line in input_file:

        line = line.strip()
        # need to reomve the , so that the comment review text won't be in many columns
        line = line.replace(',', '')

        if line == "":
            outfile_file.write(",".join(current_line))
            outfile_file.write("\n")
            current_line = []
            continue
        parts = line.split(":", 1)
        current_line.append(parts[1])

    if current_line != []:
        outfile_file.write(",".join(current_line))
    input_file.close()
    outfile_file.close()