def write_IntermediateCode(intermediate_code, filename):
    # Calculate the maximum width for each column based on the data and headers
    max_line_number = max(max(len(str(entry.Line_Number)) for entry in intermediate_code), len("Line Number"))
    max_size = max(max(len(str(entry.Size)) for entry in intermediate_code), len("Size"))
    max_opcode = max(max(len(str(entry.Opcode)) for entry in intermediate_code), len("Opcode"))
    max_instruction = max(max(len(entry.Instruction) for entry in intermediate_code), len("Instruction"))
    max_address = max(max(len(str(entry.Address)) for entry in intermediate_code), len("Address"))

    with open(filename, "w") as file:
        # Write headers with dynamic width
        file.write(f"{'Line Number':<{max_line_number}}  {'Size':<{max_size}}  {'Opcode':<{max_opcode}}  {'Instruction':<{max_instruction}}  {'Address':<{max_address}}\n")
        file.write("=" * (max_line_number + max_size + max_opcode + max_instruction + max_address + 20) + "\n")
    
        # Write the intermediate code entries with adjusted column widths
        for entry in intermediate_code:
            file.write(f"{entry.Line_Number:<{max_line_number}}  {entry.Size:<{max_size}}  {entry.Opcode:<{max_opcode}}  {entry.Instruction:<{max_instruction}}  {entry.Address:<{max_address}}\n")
        
        print("")
        print(f"Intermediate code (output of Parse 1) written to {filename}")
        print("")
