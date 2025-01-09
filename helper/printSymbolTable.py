def print_symbol_table(symbol_table):
    # Calculate maximum length for each column
    max_symbol_name = max(max(len(str(entry[0])) for entry in symbol_table), len("Symbol_Name"))
    max_type = max(max(len(str(entry[1])) for entry in symbol_table), len("Type"))
    max_size = max(max(len(str(entry[2])) for entry in symbol_table), len("Size"))
    max_value = max(max(len(str(entry[3])) for entry in symbol_table), len("Value"))
    max_scope = max(max(len(str(entry[4])) for entry in symbol_table), len("Scope"))
    max_address = max(max(len(str(entry[5])) for entry in symbol_table), len("Address"))

    # Print the header
    print(f"{'Symbol_Name':<{max_symbol_name}}  {'Type':<{max_type}}  {'Size':<{max_size}}  {'Value':<{max_value}}  {'Scope':<{max_scope}}  {'Address':<{max_address}}")
    print("=" * (max_symbol_name + max_type + max_size + max_value + max_scope + max_address + 20))

    for entry in symbol_table:
        # Handle None and list types before printing
        entry_formatted = []
        for item in entry:
            if isinstance(item, list):
                item = str(item)  # Convert list to string representation
            elif item is None:
                item = 'None'  # Convert None to a string 'None'
            entry_formatted.append(item)
        # Now you can safely print the entry with formatted values
        print(f"{entry_formatted[0]:<{max_symbol_name}}  "
              f"{entry_formatted[1]:<{max_type}}  "
              f"{entry_formatted[2]:<{max_size}}  "
              f"{entry_formatted[3]:<{max_value}}  "
              f"{entry_formatted[4]:<{max_scope}}  "
              f"{entry_formatted[5]:<{max_address}}")
    
