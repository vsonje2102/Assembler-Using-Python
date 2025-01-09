import re

def filter_assembler_code(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Remove comments
            line = re.sub(r';.*', '', line)
            # Remove extra blank lines
            if line.strip():
                outfile.write(line)


