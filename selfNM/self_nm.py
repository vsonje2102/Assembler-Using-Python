def binutils_nm(object_file_content):
        header = object_file_content[:8]
        #print(header)
        section_table_offset = ( header[7] & 0x3C) >> 2 # Extract the section table offset from the header
        #print(section_table_offset)
        section_count = header[7] & 0b11                  # Extract the section count
        #print(section_names)

        # Parse the section table
        section_table_start = section_table_offset
        section_table = object_file_content[section_table_start:]
        section_name = object_file_content[32:36]
        offset= object_file_content[36:40]
        #print(offset)
        #print(section_name)
        # Convert bytearray to integer
        symtab_offset = int.from_bytes(offset, byteorder='little')
        #print("Integer:", symtab_offset)

        # Convert bytearray to string
        string_value = section_name.decode('utf-8')
        #print("String:", string_value)


        symtab_content = object_file_content[symtab_offset:]
        #print(symtab_content)

        # Parse symbols from .symtab
        print("")
        print("Symbol Table:")
        i = 0  # Start index
        while(i<len(symtab_content)):
            # Extract `name_length`
            name_length = int.from_bytes(symtab_content[i:i+2], byteorder='little')
            i += 2  # Move index forward
            #print(f"Name Length: {name_length}")
            #print(i)
            # Extract `name`
            name = symtab_content[i:i + name_length].decode('utf-8')
            i += name_length  # Move index forward
            #print(f"Name: {name}")
            #print(i)
            # Extract `type_length`
            type_length = int.from_bytes(symtab_content[i:i+2], byteorder='little')
            i += 2  # Move index forward
            #print(f"Type Length: {type_length}")
            #print(i)
            # Extract `type`
            symbol_type = symtab_content[i:i + type_length].decode('utf-8')
            i += type_length  # Move index forward
            #print(f"Type: {symbol_type}")
            #print(i)
            # Extract `size`
            size = int.from_bytes(symtab_content[i:i+4], byteorder='little')
            i += 4
            #print(f"Size: {size}")
            #print(i)
            # Extract `value_list_length`
            value_list_length = int.from_bytes(symtab_content[i:i+2], byteorder='little')
            i += 2
            #print(f"Value List Length: {value_list_length}")
            #print(i)
            # Extract `value_list` (if any)
            if( value_list_length != 0):
                value_list = []
                for _ in range(value_list_length):
                    # Check each item in the list
                    item_length = int.from_bytes(symtab_content[i:i+2], byteorder='little')
                    i += 2  # Move past the length
                    item = symtab_content[i:i+item_length].decode('utf-8')
                    i += item_length  # Move past the item
                    value_list.append(item)
                #print(f"Value List: {value_list}")
            else :
                i += 2
            #print(i)
            # Extract `scope_length`
            scope_length = int.from_bytes(symtab_content[i:i+2], byteorder='little')
            i += 2
            #print(f"Scope Length: {scope_length}")
            #print(i)
            if(scope_length != 0 ):
                # Extract `scope`
                scope = symtab_content[i:i + scope_length].decode('utf-8')
                i += scope_length  # Move past the scope
                #print(f"Scope: {scope}")
            else:
                i+=2
            #print(i)
            # Extract `address`
            address = int.from_bytes(symtab_content[i:i+4], byteorder='little')
            i += 4
            # Print symbol information in nm-like format
            symbol_type = {
                "dd": "d",
                "db": "d",
                "dq" : "d",
                "dw": "d",
                "resb" : "b",
                "resd" : "b",
                "resq" : "b",
                "resq" : "b",
                "label" : "t",
                "label": "t",
                "main": "T"
            }.get(symbol_type, "t")  # Default to 't' if type is unknown
            if name == "main":
                symbol_type = "T"
            print(f"{address:08x} {symbol_type} {name}")
            #print(i)
