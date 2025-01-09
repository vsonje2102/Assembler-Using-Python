# Helper Module

This directory contains helper functions and classes used throughout the assembler project. Below is a detailed explanation of each file and its usage.

## Files

### `entries.py`
This file contains classes for handling different types of entries such as symbols, literals, and errors.

#### Classes

- `SymbolEntry`: Represents a symbol entry with attributes like `Symbol_Name`, `Type`, `Size`, and `Address`.
- `LiteralEntry`: Represents a literal entry with attributes like `Literal_Value`, `Address`, and `Length`.
- `ErrorEntry`: Represents an error entry with attributes like `Error_Code`, `Error_Message`, and `Line_Number`.

#### Usage

```python
from helper.entries import SymbolEntry, LiteralEntry, ErrorEntry

# Create a symbol entry
symbol_entry = SymbolEntry(Symbol_Name="example", Type="label", Size=0, Address=0)

# Create a literal entry
literal_entry = LiteralEntry(Literal_Value="100", Address=0x0040, Length=4)

# Create an error entry
error_entry = ErrorEntry(Error_Code=1, Error_Message="Syntax Error", Line_Number=10)
```

### `error_handler.py`
This file contains functions to handle errors during the assembly process.

#### Functions

- `log_error(error_entry)`: Logs an error entry to the error table.
- `display_errors()`: Displays all logged errors.

#### Usage

```python
from helper.error_handler import log_error, display_errors
from helper.entries import ErrorEntry

# Log an error
error_entry = ErrorEntry(Error_Code=1, Error_Message="Syntax Error", Line_Number=10)
log_error(error_entry)

# Display all errors
display_errors()
```

### `utils.py`
This file contains utility functions that assist in various tasks within the assembler project.

#### Functions

- `convert_to_binary(value, bits)`: Converts a given value to its binary representation with the specified number of bits.
- `is_valid_identifier(identifier)`: Checks if the given identifier is valid according to the assembler's rules.

#### Usage

```python
from helper.utils import convert_to_binary, is_valid_identifier

# Convert a value to binary
binary_value = convert_to_binary(10, 8)

# Check if an identifier is valid
is_valid = is_valid_identifier("example_label")
```

### `opcode_instructions

- `OpcodeInstruction`: Represents an opcode instruction with attributes like `Mnemonic`, `Opcode`, `Format`, and `Operands`.


## Summary

The helper module provides essential classes and functions that facilitate the assembly process by managing entries, handling errors, processing opcode instructions, and providing utility functions. These components are crucial for the smooth operation of the assembler project.