
def create_object_file_header():
    # Header components
    magic_number = b"vsonje"  # 6-byte magic number
    version = 0x01  # Version byte (1 byte)
    
    # Combine architecture (2 bits), section table offset (4 bits), section count (2 bits)
    architecture = 0b00  # Architecture: x86 (2 bits)
    section_table_offset = 0b1000  # Section table offset: 8 (4 bits)
    section_count = 0b11  # Section count: 3 sections (2 bits)

    # Pack architecture, offset, and section count into a single byte
    combined_byte = (architecture << 6) | (section_table_offset << 2) | section_count

    # Print binary and hex representation of combined byte
    #print(f"Combined Byte (Binary): {bin(combined_byte)}")
    #print(f"Combined Byte (Hex): {hex(combined_byte)}")

    # Construct the header
    header = bytearray()
    header.extend(magic_number)  # Add magic number
    header.append(version)       # Add version
    header.append(combined_byte)  # Add combined byte

    return header


def create_object_file(machine_code_text, machine_code_data, machine_code_bss, symbol_table_list):
    machine_code_text = [code for code in machine_code_text if code and all(c in '0123456789ABCDEFabcdef' for c in code)]
    # Generate the header and save to file
    header = create_object_file_header()
    #print("Generated Header (Hex):", header.hex())

    # Add machine code to .text section
    text_section = bytearray()
    for code in machine_code_text:
        text_section.extend(bytes.fromhex(code))
    #print(f"text Section is {text_section}")
    #print(len(text_section))
    

    # Add machine code to .data section
    data_section = bytearray()
    for code in machine_code_data:
        data_section.extend(bytes.fromhex(code))
    #print(len(data_section))
    #print(f"data section is {data_section}")
    

    # Add machine code to .bss section
    bss_section = bytearray()
    for size_str in machine_code_bss:
        size = int(size_str) 
        bss_section.extend(bytearray(size))
    #print(len(bss_section)) 
    #print(f"bss_section is {bss_section}")


# Add symbol table to .symtab section
    symtab_section = bytearray()
    #print(symbol_table_list)
    for symbol in symbol_table_list:
        for entry in symbol:
            if isinstance(entry, str):
                # Handle empty string
                if entry == "":
                    symtab_section.extend((0).to_bytes(2, byteorder='little'))  # Add length as 0
                else:
                    symtab_section.extend(len(entry).to_bytes(2, byteorder='little'))  # Add length as 2 bytes
                    symtab_section.extend(entry.encode('utf-8'))
            elif isinstance(entry, int):
                # Handle integer entry (including 0 as valid value)
                symtab_section.extend(entry.to_bytes(4, byteorder='little'))
            elif isinstance(entry, list):
                # Handle empty list
                if not entry:
                    symtab_section.extend((0).to_bytes(2, byteorder='little'))  # Add length as 0
                else:
                    symtab_section.extend(len(entry).to_bytes(2, byteorder='little'))  # Add length of list
                    for item in entry:
                        if isinstance(item, str):
                            # Handle empty string in list
                            if item == "":
                                symtab_section.extend((0).to_bytes(2, byteorder='little'))  # Add length as 0
                            else:
                                symtab_section.extend(len(item).to_bytes(2, byteorder='little'))  # Add length of string
                                symtab_section.extend(item.encode('utf-8'))
                        elif isinstance(item, int):
                            symtab_section.extend(item.to_bytes(4, byteorder='little'))
                        else:
                            raise TypeError(f"Unsupported list entry type: {type(item)}")
            elif entry is None:
                # Encode None as a placeholder (e.g., 4 zero bytes)
                symtab_section.extend((0).to_bytes(4, byteorder='little'))
            else:
                raise TypeError(f"Unsupported symbol table entry type: {type(entry)}")
            #print(symtab_section)
            #print(len(symtab_section))
            #print("")
    # At this point, symtab_section contains the encoded symbol table
    # You can verify it by printing or saving the content
    #print(symtab_section)

    # Create the section table with offsets
    section_table = bytearray()
    section_offsets = {
        "text": 40,  # 4 sections, each 4 bytes for offset
        "data": 0,  # Placeholder, will be updated later
        "bsss": 0,   # Placeholder, will be updated later
        "symt": 0  # Placeholder, will be updated later
    }

    # Calculate actual offsets for each section
    section_offsets["data"] = section_offsets["text"] + len(text_section)
    section_offsets["bsss"] = section_offsets["data"] + len(data_section)
    section_offsets["symt"] = section_offsets["bsss"] + len(bss_section)

    # Add section names and offsets to the section table
    for section, offset in section_offsets.items():
        section_table.extend(section.encode('utf-8'))
        section_table.extend(offset.to_bytes(4, byteorder='little'))
    
   # Print offsets stored in section table
   # print("Section Table Offsets:")
    #for section, offset in section_offsets.items():
    #    print(f"{section}: {offset}")

    # Combine header, section table, and sections
    #print("Combining file contents")
    object_file_content = header + section_table + text_section + data_section + bss_section + symtab_section

    return object_file_content
       