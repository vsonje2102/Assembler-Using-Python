from avlTree.avl_tree import AVLTree
from helper.ecnodings_regIncDecMulDiv import inc_opcodes,dec_opcodes,mul_modrm,div_modrm,register_encoding
# Register encoding for ModR/M byte


def encode_modrm(mod, reg, rm):
    return f"{(mod << 6) | (reg << 3) | rm:02X}"

def encode_immediate(value, size):
    if value is None:
        print("Cannot encode None as immediate value.")
    return ''.join(f"{(value >> (8 * i)) & 0xFF:02X}" for i in range(size))

def resolve_symbol(symbol, symbol_tree):
    #print(f"Symbol is {symbol}")
    symbol_node = symbol_tree.search(symbol_tree.root, symbol)  # Search for the symbol node
    #print(f"Symbol node is {symbol_node}")
    if symbol_node:
        symbol_entry = symbol_node.data
        return symbol_entry.Address  # Return the Address from the SymbolEntry object
    print(f"Symbol '{symbol}' not found in symbol tree.")

def resolve_memory_address(operand, symbol_tree):
    if operand in register_encoding:
        return register_encoding[operand]

    if "+" in operand:
        symbol, offset = operand.strip("[]").split("+")
        #print(f"Symbol is {symbol}")
        offset = int(offset)
        #print(f"Offset is {offset}")
        if symbol in register_encoding:
            return register_encoding[symbol] + offset
        else:
            symbol_address = resolve_symbol(symbol, symbol_tree)
            #print(f"Symbol address is {symbol_address}")
            return symbol_address + offset
    elif "[" in operand:
        symbol = operand.strip("[]")
        #print(symbol)
        if symbol in register_encoding:
            return register_encoding[symbol]
        else:       
            return resolve_symbol(symbol, symbol_tree)
    return None

def format_instruction_textSection(entry, symbol_tree,line_num):
    #print(f"Entry is {entry}")
    if entry.Opcode == -1 or entry.Size == -1 or entry.Address == -1:
        return '',''  # Skip non-instruction entries

    opcode = entry.Opcode
    instruction = entry.Instruction
    parts = instruction.split(maxsplit=1)
    #print(f"Opcode is {opcode}")
    #print(f"Instruction is {instruction}")
    #print(f"Parts are {parts}")
    #print(len(parts))
    if len(parts) < 2:
        return opcode,''  # No operands

    mnemonic, operands = parts
    operand_parts = [op.strip() for op in operands.split(",")]

    if len(operand_parts) == 2:
        #print("entered in first if where len(operand_part == 2)")
        #print(f"Operand parts are {operand_parts}")   
        dest, src = operand_parts

        # Special cases for add, sub, cmp with eax and imm32
        if mnemonic in ["add", "sub", "cmp","xor"] and dest == "eax" and src.isdigit():
            immediate = encode_immediate(int(src), 4)
            machine_code = f"{opcode}{immediate}"
            return f"{line_num:3} {entry.Address:08X} {opcode}{immediate}",machine_code

        # Register-to-register
        if dest in register_encoding and src in register_encoding:
            modrm = encode_modrm(0b11, register_encoding[src], register_encoding[dest])
            machine_code = f"{opcode}{modrm}"
            return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}",machine_code

        # Immediate-to-register
        if dest in register_encoding and src.isdigit():
            modrm = encode_modrm(0b11, 0b000, register_encoding[dest])
            immediate = encode_immediate(int(src), entry.Size - 2)
            machine_code = f"{opcode}{modrm}{immediate}"
            return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}{immediate}",machine_code

        # Memory-to-register or Register-to-memory
        if "[" in src or "[" in dest:
            if "[" in src:
                mem_operand = src.strip("[]")
                reg = register_encoding[dest]
                #print(f"Register is {reg}")
            else:
                mem_operand = dest.strip("[]")
                reg = register_encoding[src]
                #print(f"Register is {reg}")

            
            if "+" in mem_operand:
                base, offset = mem_operand.split("+")
                offset = int(offset)
                disp = encode_immediate(offset, 4)
                if base in register_encoding:
                    base_reg = register_encoding[base]
                    mod=0b10
                    modrm = encode_modrm(mod, reg, base_reg)
                    machine_code = f"{opcode}{modrm}{disp}"
                    return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}{disp}",machine_code
                else:
                    mem_address = resolve_memory_address(mem_operand, symbol_tree)
                    disp = encode_immediate(mem_address, 4)
                    base_reg = 0b101
                    mod=0b00
                    modrm = encode_modrm(mod, reg, base_reg) 
                    machine_code = f"{opcode}{modrm}[{disp}]"
                    return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}[{disp}]",machine_code
            elif mem_operand in register_encoding:
                mem_address = register_encoding[mem_operand]
                #print(f"Memory address is {mem_address}")
                modrm = encode_modrm(0b00, reg, mem_address)
                machine_code = f"{opcode}{modrm}"
                return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}",machine_code
            
            else:
                mem_address = resolve_memory_address(mem_operand, symbol_tree)
                #print(f"Memory address is {mem_address}")
                disp = encode_immediate(mem_address, 4)
                #print(reg)
                modrm = encode_modrm(0b00, reg, 0b101)  # 0b101 for direct address mode
                machine_code = f"{opcode}{modrm}{disp}"
                return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}{disp}",machine_code
    elif len(operand_parts) == 1:
        #print("entered in second if where len(operand_part == 1)")
        #print(f"Operand parts are {operand_parts}")
        op = operand_parts[0]
        
        if mnemonic == "jmp":
            if '0' <= op[0] <= '9':
                immediate = encode_immediate(int(op), entry.Size - 1)
                machine_code = f"{opcode}({immediate})"
                return f"{line_num:3} {entry.Address:08X} {opcode}({immediate})",machine_code
            elif op in register_encoding:
                modrm = encode_modrm(0b11, 0b100, register_encoding[op])
                machine_code= f"{opcode}{modrm}"
                return f"{line_num:3} {entry.Address:08X} {opcode}{modrm:<24}",machine_code
            else:
                
                if "[" in op:
                        if "+" in op:
                            base, offset = op.strip("[]").split("+")
                            offset = int(offset)
                            disp = encode_immediate(offset, 4)
                            if base in register_encoding:
                                base_reg = register_encoding[base]
                                mod=0b10
                                modrm = encode_modrm(mod, 0b100, base_reg)
                                machine_code = f"{opcode}{modrm}{disp}"
                                return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}{disp}",machine_code
                            else:
                                mem_address = resolve_memory_address(op, symbol_tree)
                                disp = encode_immediate(mem_address, 4)
                                base_reg = 0b101
                                mod=0b00
                                modrm = encode_modrm(mod, 0b100, base_reg)
                                machine_code= f"{opcode}{modrm}[{disp}]"
                                return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}[{disp}]",machine_code
                        else:
                            op = op.strip("[]")
                            #print(f"Operand is {op}")
                            if op in register_encoding:
                                mem_address = register_encoding[op]
                                modrm = encode_modrm(0b00, 0b100, mem_address)
                                machine_code = f"{opcode}{modrm}"
                                return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}",machine_code
                            else:
                                mem_address = resolve_symbol(op, symbol_tree)
                                #print(f"Memory address is {mem_address}")
                                disp = encode_immediate(mem_address, 4)
                                modrm = encode_modrm(0b00, 0b100, 0b101)
                                machine_code = f"{opcode}{modrm}[{disp}]"
                                return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}[{disp}]",machine_code
                else:
                    mem_address = resolve_memory_address(op, symbol_tree)
                    machine_code = f"{opcode}({mem_address})"
                    return f"{line_num:3} {entry.Address:08X} {opcode}{mem_address}",machine_code
        elif mnemonic == "inc" and op in inc_opcodes:
            opcode = encode_immediate(inc_opcodes[op],1)
            machine_code= f"{opcode}"
            return f"{line_num:3} {entry.Address:08X} {opcode}",machine_code
        elif mnemonic == "dec" and op in dec_opcodes:
            opcode = encode_immediate(dec_opcodes[op],1)
            machine_code= f"{opcode}"
            return f"{line_num:3}  {entry.Address:08X} {opcode}",machine_code
        elif mnemonic == "mul" and op in mul_modrm:
            modrm = encode_immediate(mul_modrm[op],1)
            machine_code= f"{opcode}{modrm}"
            return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}",machine_code
        elif mnemonic == "div" and op in div_modrm:
            modrm = encode_immediate(div_modrm[op],1)
            machine_code= f"{opcode}{modrm}"
            return f"{line_num:3} {entry.Address:08X} {opcode}{modrm}",machine_code
        elif mnemonic=="jz" or mnemonic == "jnz":
            disp = encode_immediate(int(op), 4)
            machine_code = f"{opcode}({disp})"
            return f"{line_num:3} {entry.Address:08X} {opcode}({disp})",machine_code
    machine_code=''
    return f"{entry.Address:08X} {opcode:<24} {instruction}",machine_code  # Default fallback for unknown instructions
