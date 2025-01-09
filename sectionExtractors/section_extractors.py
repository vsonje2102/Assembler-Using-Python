import re
def extract_text_section(assembly_code):
    text_section = []
    in_text_section = False
    for line in assembly_code:
        line = line.strip()
        if re.match(r"section\s+\.text", line, re.IGNORECASE):
            in_text_section = True
        if in_text_section:
            text_section.append(line)
    return text_section

def extract_data_section(assembly_code):
    data_section = []
    in_data_section = False
    for line in assembly_code:
        line = line.strip()
        if re.match(r"section\s+\.data", line, re.IGNORECASE):
            in_data_section = True
        if re.match(r"section\s+\.(bss|text)", line, re.IGNORECASE):
            in_data_section = False
            break
        if in_data_section:
            data_section.append(line)
    return data_section

def extract_bss_section(assembly_code):
    bss_section = []
    in_bss_section = False
    for line in assembly_code:
       # print(line)
        line = line.strip()
        if re.match(r"section\s+\.bss", line, re.IGNORECASE):
            in_bss_section = True
        if re.match(r"section\s+\.(text)", line, re.IGNORECASE):
            in_bss_section = False
            break
        if in_bss_section:
            bss_section.append(line)
    return bss_section

