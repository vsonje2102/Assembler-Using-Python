def print_header_info(header):
        # Extract magic number (first 6 bytes)
        magic_number = header[:6].decode('utf-8')
        
        # Extract version (7th byte)
        version = header[6]
        
        # Extract combined byte (8th byte)
        combined_byte = header[7]
        
        # Decode combined byte
        architecture = (combined_byte >> 6) & 0b11
        section_table_offset = (combined_byte >> 2) & 0b1111
        section_count = combined_byte & 0b11
        
        # Print header information
        print(f"Magic Number: {magic_number}")
        print(f"Version: {version}")
        print(f"Architecture: {architecture}")
        print(f"Section Table Offset: {section_table_offset}")
        print(f"Section Count: {section_count}")
        
