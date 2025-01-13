
# Assembler Project

This project is a simple assembler that processes assembly code, generates intermediate code, creates object files, and produces various outputs based on flags. It integrates several utilities for parsing, generating code, and displaying results in various formats.

## Makefile

A `Makefile` is provided to compile all dependencies and manage the build process efficiently. The `Makefile` includes targets for compiling individual components and generating the final executable. To use the `Makefile`, navigate to the project directory and run `make`.

### Example Usage

```bash
make all
```

This command will compile all the necessary files and create the final executable.

### Makefile Targets

- `all`: Compiles all source files and links them to create the executable.
- `clean`: Removes all compiled files and the executable.
- `test`: Runs any tests defined for the project.

## Workflow

1. **Input Assembly Code**: The program takes an assembly code file as input (`.asm` format). You can provide flags to customize the output (e.g., for generating a symbol table or listing file).
2. **Parsing Sections**: The assembly code is divided into different sections: Data, BSS, and Text. Each section is parsed to extract relevant information.
3. **Generate Intermediate Code**: After parsing, intermediate code is generated for the three sections.
4. **Create Opcode Tree**: A tree structure is created from the opcode instructions to assist in generating machine code.
5. **Symbol Table**: The symbol table is populated with symbols found during parsing, including their types, sizes, and addresses.
6. **Listing File and Object File Creation**: Machine code is generated and combined with the listing file, object file, and other output files based on flags.
7. **Final Output**: The program generates the following outputs depending on flags:
    - Object File (`-o` flag)
    - Listing File (`-l` flag)
    - Symbol Table (`-s` flag)
    - Intermediate Code (`-i` flag)
    
## Directory Structure

```plaintext
.
├── Makefile
├── avlTree/
│   ├── avl_tree.py
│   └── README.MD
├── elfUtils/
│   ├── elf_utils.py
│   └── README.md
├── filesUtils/
│   ├── file_utils.py
│   └── README.md
├── helper/
│   ├── assembly_code.asm
│   ├── ecnodings_regIncDecMulDiv.py
│   ├── entries.py
│   ├── filterInput.py
│   ├── opcode_instructions.csv
│   ├── printSymbolTable.py
│   ├── headerInfo.py
│   ├── README.md
├── intermediateCodeFile/
│   ├── intermediateCodeFile.py
│   └── README.md
├── listingFileCreation/
│   ├── combine_and_save_listing.py
│   ├── listingFileCreation.py
│   ├── README.md
│   └── textSection/
│       └── formatTextSection.py
├── sectionExtractors/
│   └── section_extractors.py
├── sectionParser/
│   ├── data_bss_Section_Parser.py
│   └── README.md
├── selfNM/
│   ├── README.md
│   └── self_nm.py
└── main.py
```
## Header Structure
- Total size of header is 8 byte
- Header has 1) 'Magic no'
	     2) 'Version'
	     3) 'Architecture'
	     4) 'Section Table Offset'
	     5) 'Section Count '


## `main.py` Overview

### Input Handling
- The script takes an assembly file (`*.asm`) as input.
- Flags can be provided for additional functionality, such as:
  - `-n` to generate the symbol table.
  - `-l` to generate a listing file.
  - `-s` to print the symbol table.
  - `-i` to generate intermediate code.
  - `-h` to show the help message.

### Initialization
- Various trees and structures are initialized:
  - `symbol_tree`: Holds symbol information.
  - `literal_tree`: Stores literal values.
  - `opcode_tree`: Contains opcode instructions.
  - `error_table`: Collects errors encountered during parsing.
  - `intermediate_code`: Stores intermediate code after parsing.

### File Parsing
- The program reads the input assembly file and extracts the data, BSS, and text sections using helper functions.
- The data, BSS, and text sections are parsed, and intermediate code is generated for each.

### Output Generation
- Based on the flags provided, the script generates the following:
  - **Object File**: Contains binary machine code.
  - **Listing File**: Contains detailed assembly code and machine code.
  - **Symbol Table**: Displays the table of symbols.
  - **Intermediate Code**: Writes the intermediate code generated during parsing.

## Usage

```bash
python main.py <file.asm> [-flags]
```

### Flags:
- `-n`: Generate the symbol table.
- `-l`: Generate the listing file.
- `-s`: Print the symbol table.
- `-i`: Write intermediate code to a file.
- `-m`: Display headerInfo Magic number  information.
- `-h`: Display help information.

### Example:
```bash
python main.py example.asm -nl
```
This will process the `example.asm` file, generate a symbol table, and create a listing file.

## Additional Notes:
- Ensure that the input assembly file is valid and follows the correct syntax.
- The script will stop execution if errors are found during the parsing phase.

---

