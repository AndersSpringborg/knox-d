def convertToCsv(input, output, header):
    f = open(input, encoding="latin9")

    outfile = open(output, "w", encoding="utf-8", errors="replace")

    outfile.write(",".join(header) + "\n")
    currentLine = []
    for line in f:

        line = line.strip()
        # need to reomve the , so that the comment review text won't be in many columns
        line = line.replace(',', '')

        if line == "":
            outfile.write(",".join(currentLine))
            outfile.write("\n")
            currentLine = []
            continue
        parts = line.split(":", 1)
        currentLine.append(parts[1])

    if currentLine != []:
        outfile.write(",".join(currentLine))
    f.close()
    outfile.close()