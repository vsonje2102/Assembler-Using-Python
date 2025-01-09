from filesUtils.file_utils import save_file
def combine_and_save_files(lst, assembly_code, output_file):
    max_machine_code_length = max(len(line.strip()) for line in lst)
    combined_lines = []
    for padded_line, asm_line in zip(lst, assembly_code):
        combined_lines.append(f"{padded_line.strip():<{max_machine_code_length}} {asm_line}\n")
    save_file(output_file, combined_lines, "text", "list")