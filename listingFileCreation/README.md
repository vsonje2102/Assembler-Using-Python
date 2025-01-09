# Listing File Creation

This directory contains scripts for creating and managing listing files in the assembler project. Listing files provide a detailed view of the assembly process, including the original source code, intermediate representations, and final machine code.

## Files

### `combine_and_save_lst.py`
This script combines various components of the assembly process and saves them into a listing file.

#### Functions

- `combine_and_save_lst(intermediate_code, symbol_table, error_list, file_path)`: Combines the intermediate code, symbol table, and error list into a single listing file and saves it.
    - **Parameters:**
        - `intermediate_code`: The intermediate code to be included in the listing file.
        - `symbol_table`: The symbol table to be included in the listing file.
        - `error_list`: The list of errors to be included in the listing file.
        - `file_path`: The path to the file where the listing will be saved.
    - **Usage:**
        ```python
        from combine_and_save_lst import combine_and_save_lst

        combine_and_save_lst(intermediate_code, symbol_table, error_list, "path/to/listing_file.lst")
        ```

### `listingFileCreation.py`
This script handles the creation of listing files by orchestrating the combination of various components and managing the output format.

#### Functions

- `create_listing_file(assembly_code, file_path)`: Creates a listing file from the given assembly code.
    - **Parameters:**
        - `assembly_code`: The assembly code to be processed.
        - `file_path`: The path to the file where the listing will be saved.
    - **Usage:**
        ```python
        from listingFileCreation import create_listing_file

        create_listing_file(assembly_code, "path/to/listing_file.lst")
        ```

## Summary

The listing file creation scripts are essential for generating comprehensive listing files that provide insights into the assembly process. These files include the original source code, intermediate representations, symbol tables, and error lists, facilitating debugging and optimization.