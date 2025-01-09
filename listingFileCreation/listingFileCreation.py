from listingFileCreation.textSection.formatTextSection import format_instruction_textSection
import re


def extract_values(instruction, instruction_type):
    result = []

    if instruction_type == "db":
        # Extract ASCII values from quoted strings and append any numbers
        quoted_strings = re.findall(r'"([^"]*)"', instruction)
        for string in quoted_strings:
            result.extend([ord(char) for char in string])
        numbers = re.findall(r'\d+', instruction)
        result.extend([int(num) for num in numbers])

    elif instruction_type == "dw":
        # Extract numbers as 2-byte values
        numbers = re.findall(r'\d+', instruction)
        for num in numbers:
            value = int(num)
            result.extend([value & 0xFF, (value >> 8) & 0xFF])  # Split into 2 bytes

    elif instruction_type == "dd":
        # Extract numbers as 4-byte values
        numbers = re.findall(r'\d+', instruction)
        for num in numbers:
            value = int(num)
            result.extend(
                [
                    value & 0xFF,
                    (value >> 8) & 0xFF,
                    (value >> 16) & 0xFF,
                    (value >> 24) & 0xFF,
                ]
            )

    elif instruction_type == "dq":
        # Extract numbers as 8-byte values
        numbers = re.findall(r'\d+', instruction)
        for num in numbers:
            value = int(num)
            result.extend(
                [
                    value & 0xFF,
                    (value >> 8) & 0xFF,
                    (value >> 16) & 0xFF,
                    (value >> 24) & 0xFF,
                    (value >> 32) & 0xFF,
                    (value >> 40) & 0xFF,
                    (value >> 48) & 0xFF,
                    (value >> 56) & 0xFF,
                ]
            )

    return result


def format_instruction(line_num, address, instruction,opcode=-1):
   
    parts = instruction.split()
    machine_instructions = []
    label = parts[0] if len(parts) > 1 else ""
    instruction_type = parts[1] if len(parts) > 1 else ""

    if instruction.startswith("section"):
        # Section headers are formatted directly
        return f"    {instruction}",''

    if instruction_type.startswith("res"):
        # Reserved memory instructions
        size = int(re.search(r'\d+', instruction).group())
        if instruction_type == "resb":
            size_int = size
        elif instruction_type == "resw":
            size_int = size * 2
        elif instruction_type == "resd":
            size_int = size * 4
        elif instruction_type == "resq":
            size_int = size * 8
        else:
            size_int = size
        size_hex = f"{size_int:X}h"  # Keeping for display purposes
        return f"{line_num:3} {address:08X} <res {size_hex:>3}>", size_int


    elif instruction_type in ["db", "dw", "dd", "dq"]:
        # Data instructions
        values = extract_values(instruction, instruction_type)
        hex_values = "".join(f"{value:02X}" for value in values)
        return f"{line_num:3} {address:08X} {hex_values}",hex_values

    else:
        # Handle .text instructions (e.g., mov, add)
        #opcode = instruction.split()[0]  # Simplified for now
        #operands = instruction[len(opcode):].strip()
        # For simplicity, let's return the opcode and operands as-is
        # Extend this logic for binary translation if needed
        print(f"Opcode is {opcode}")
        #return f"{line_num:3} {address:08X} {opcode:<6} {operands}"
        return f"{opcode}",''

def process_intermediate_code(intermediate_table,symbol_table,literal_table):
    result = []
    machineCode_text= []
    machineCode_Data=[]
    machineCode_Bss =[]
    current_section = None
    address = 0
    counter = 0
    for entry in intermediate_table:
        # Check for section declarations
        if entry.Instruction.startswith("section"):
            current_section = entry.Instruction.split()[1]  # e.g., '.text', '.data'
            address = 0  # Reset address for new section
            result.append('') 
            continue

        # Handle .text section instructions
        if current_section == ".text":
           #print(entry.Address)
            formatted,mc = format_instruction_textSection(entry, symbol_table,counter)
            machineCode_text.append(mc)
            if formatted == '':
                counter -= 1
            result.append(formatted)
            address += entry.Size  # Update address based on instruction size
            counter+=1

        # Handle .data or .bss sections (already implemented)
        elif current_section in [".data", ".bss"]:
            formatted,mc = format_instruction(entry.Line_Number, address, entry.Instruction)
            if current_section == ".data":
                machineCode_Data.append(mc)
            elif current_section == ".bss":
                machineCode_Bss.append(mc)
        
            result.append(formatted)

            # Update the address based on the instruction type
            if "res" in entry.Instruction:
                if "resb" in entry.Instruction:
                    address += int(re.search(r'\d+', entry.Instruction).group())
                elif "resw" in entry.Instruction:
                    address += 2 * int(re.search(r'\d+', entry.Instruction).group())
                elif "resd" in entry.Instruction:
                    address += 4 * int(re.search(r'\d+', entry.Instruction).group())
                elif "resq" in entry.Instruction:
                    address += 8 * int(re.search(r'\d+', entry.Instruction).group())
            else:
                address += entry.Size

    return result,machineCode_text,machineCode_Data,machineCode_Bss 


def listing_File_Creation(intermediate_table, symbol_tree, literal_tree):
    # Process the intermediate table to generate the output
    output_lst,machine_code_text,machine_code_data,machine_code_bss= process_intermediate_code(intermediate_table,symbol_tree,literal_tree)    

    return output_lst,machine_code_text,machine_code_data,machine_code_bss
