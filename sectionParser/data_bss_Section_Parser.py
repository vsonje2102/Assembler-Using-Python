import re
from helper.entries import SymbolEntry, IntermediateCodeEntry ,LiteralEntry,ErrorEntry
from avlTree.avl_tree import AVLTree



def parse_text_section(text_section, symbol_tree, intermediate_code, opcode_tree, literal_tree,error_table):
    sr_no = 0
    address = 0
    literal_sr_no = 1  # For assigning serial numbers to literals

    # Regular expressions for operand types
    reg_pattern = re.compile(r'^(eax|ebx|ecx|edx|esi|edi|ebp|esp)$')  # Register pattern
    #mem_pattern = re.compile(r'^\[.*\]$')  # Memory access pattern
    mem_pattern = re.compile(r'^\[.+\]$')
    mem_pattern_with_disp = re.compile(r'^\[.+\+\d+\]$')
    imm_pattern = re.compile(r'^(\d+|0x[0-9a-fA-F]+|".*?")$')  # Immediate values (numbers or strings)

    for line in text_section:
        condn=0
        line = line.strip()
        if 'global main' in line or 'section .text' in line:
            intermediate_entry = IntermediateCodeEntry(
                Line_Number=-1,
                Size=-1,
                Opcode=-1,
                Instruction=f"{line}" , 
                Address=-1
            )
            intermediate_code.append(intermediate_entry)
            continue

        # Skip empty lines and comments
        if not line or line.startswith(';'):
            continue

        # Check for label
        if ':' in line:
            label_parts = line.split(':', 1)
            label = label_parts[0].strip()
            rest_of_line = label_parts[1].strip() if len(label_parts) > 1 else ""

            # Add label to symbol tree
            symbol_entry = SymbolEntry(
                Symbol_Name=label,
                Type="label",
                Size=0,
                Address=address
            )
            symbol_tree.root = symbol_tree.insert(symbol_tree.root, label, symbol_entry,error_table)
            #print(f"Added label: {label}, Address: {address}")  # Debug info

            # If there's an instruction after the label, continue parsing it
            line = rest_of_line

        if not line:
            intermediate_entry = IntermediateCodeEntry(
                Line_Number=-1,
                Size=-1,
                Opcode=-1,
                Instruction=label,
                Address=-1
            ) 
            intermediate_code.append(intermediate_entry)
            continue

        # Split the instruction and operands
        parts = line.split(maxsplit=1)
        instruction = parts[0]
        operands = parts[1].split(',') if len(parts) > 1 else []
        #print(f"Operands are {operands}")

        # Determine operand types
        param1_type = ""
        param2_type = ""
        flag = 0            # if 1st  paramter is eax then flag  =1 else 0 
        if len(operands) > 0:
            operand1 = operands[0].strip()
            operand2=""
            if operand1 == 'eax':
                flag=1
            if reg_pattern.match(operand1):
                param1_type = 'reg'
            elif mem_pattern_with_disp.match(operand1):
                param1_type = 'mem'
            elif mem_pattern.match(operand1):
                param1_type = 'mem'
                if instruction != 'jmp':
                    condn=4
                elif instruction == 'jmp' and  reg_pattern.match(operand1.strip('[]')):
                    condn=4
            elif imm_pattern.match(operand1):
                param1_type = 'imm32'
                # Add immediate to literal table
                literal_entry = LiteralEntry(
                    SrNo=literal_sr_no,
                    Literal=operand1,
                    Type="imm32",
                    Size=len(operand1),
                    Value=operand1
                )
                literal_tree.root = literal_tree.insert(literal_tree.root, operand1, literal_entry,error_table,0)
                #print(f"Added literal: {operand1}")  # Debug info
                literal_sr_no += 1
            instruction_str = f"{instruction} {operand1}"

        if len(operands) > 1:
            operand2 = operands[1].strip()
            if reg_pattern.match(operand2):
                param2_type = 'reg'
            elif mem_pattern_with_disp.match(operand2):
                param2_type = 'mem'
            elif mem_pattern.match(operand2):
                param2_type = 'mem'
                condn=4
            elif imm_pattern.match(operand2):
                param2_type = 'imm32'
                if flag == 1:
                    param1_type = 'eax'
                # Add immediate to literal table
                literal_entry = LiteralEntry(
                    SrNo=literal_sr_no,
                    Literal=operand2,
                    Type="imm32",
                    Size=len(operand2),
                    Value=operand2
                )
                literal_tree.root = literal_tree.insert(literal_tree.root, operand2, literal_entry,error_table,0)
                #print(f"Added literal: {operand2}")  # Debug info
                literal_sr_no += 1
            instruction_str = f"{instruction} {operand1}, {operand2}"
        #print(instruction)
        #print(param1_type)
        #print(param2_type)
    
        # Generate key for opcode lookup
        key = f"{instruction}:{param1_type}:{param2_type}"
        opcode_entry = opcode_tree.search(opcode_tree.root, key)

        if opcode_entry is None:
            error_table.append(ErrorEntry(
                Error_no=len(error_table) + 1,
                Error_Message=f"Unknown instruction: '{instruction}'.",
                Address=address
            ))
            continue
        sz=opcode_entry.data.size - condn
        op=opcode_entry.data.opcode
        #print(sz)
        #print(op)
        #print(line)    
        # Add to intermediate code
        intermediate_entry = IntermediateCodeEntry(
            Line_Number=sr_no,
            Size=sz,
            Opcode=op,
            Instruction=instruction_str,
            Address=address
       )
        intermediate_code.append(intermediate_entry)

        # Update address and serial number
        address += sz
        sr_no += 1

    return literal_tree,intermediate_code

def parse_bss_section(bss_section, symbol_tree, intermediate_code,error_table):
    sr_no = 0
    address = 0
    pattern = re.compile(r'(\w+)\s+(resb|resw|resd|resq)\s+(\d+)')
    
    for line in bss_section:
        line = line.strip()
        #print(line)

        if 'section .bss' in line:
            intermediate_entry = IntermediateCodeEntry(
                Line_Number=-1,
                Size=-1,
                Opcode=-1,
                Instruction=f"{line}",
                Address=-1    
            )
            intermediate_code.append(intermediate_entry)
            continue
        match = pattern.match(line)
        if match:
            symbol_name = match.group(1)
            data_type = match.group(2)
            count = int(match.group(3))
            size = 0
            total_size = 0

            if data_type == 'resb':
                size = 1
            elif data_type == 'resw':
                size = 2
            elif data_type == 'resd':
                size = 4
            elif data_type == 'resq':
                size = 8

            total_size = count * size

            symbol_entry = SymbolEntry(
                Symbol_Name=symbol_name,
                Type=data_type,
                Size=total_size,
                Value=None,
                Scope='local',
                Address=address
            )

            intermediate_entry = IntermediateCodeEntry(
                Line_Number=sr_no,
                Size=total_size,
                Opcode=-1,
                Instruction=f"{symbol_name} {data_type} {count}",
                Address=address
            )

            # Insert symbol entry into AVL tree
            symbol_tree.root = symbol_tree.insert(symbol_tree.root, symbol_name, symbol_entry,error_table)
            #print(f"Inserted symbol: {symbol_name}, Address: {address}, Size: {total_size}")  # Debug print

            address += total_size
            intermediate_code.append(intermediate_entry)
            sr_no += 1

    return symbol_tree, intermediate_code


def parse_data_section(data_section, symbol_tree, intermediate_code,error_table):
    address = 0
    sr_no=0
    pattern = re.compile(r'(\w+)\s+(db|dd|dw|dq)\s+(.+)') 
    for line in data_section:
        line = line.strip()
        if 'section .data' in line:
            intermediate_entry = IntermediateCodeEntry(
                Line_Number=-1,
                Size=-1,
                Opcode=-1,
                Instruction=f"{line}", 
                Address=-1
            )
            intermediate_code.append(intermediate_entry)
            continue
        match = pattern.match(line)
        if match:
            symbol_name = match.group(1)
            data_type = match.group(2)
            values = match.group(3).split(',')
            size = 0
            total_size = 0
            if data_type == 'db' and '"' in values[0]:
                for value in values:
                    if '"' in value:
                        string_value = value.strip('"')
                        size += len(string_value)
                        total_size += len(string_value)
                    else:
                        size += 1
                        total_size += 1
            else:
                if data_type == 'dd':
                    size = 4
                    total_size = len(values) * size
                elif data_type == 'dw':
                    size = 2
                    total_size = len(values) * size
                elif data_type == 'dq':
                    size = 8
                    total_size = len(values) * size

            symbol_entry = SymbolEntry(
                Symbol_Name=symbol_name,
                Type=data_type,
                Size=total_size,
                Value=values,
                Scope='local',
                Address=address
            )

            intermediate_entry = IntermediateCodeEntry(
                Line_Number=sr_no,
                Size=total_size,
                Opcode=-1,
                Instruction=f"{line}",
                Address=address
            )

            # Insert symbol entry into AVL tree
            symbol_tree.root = symbol_tree.insert(symbol_tree.root, symbol_name, symbol_entry,error_table)
            # print(f"Inserted symbol: {symbol_name}, Address: {address}, Size: {total_size}")  # Debug print

            address += total_size      
            intermediate_code.append(intermediate_entry)
            sr_no += 1

    return symbol_tree, intermediate_code
