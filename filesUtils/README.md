# File Utils

This directory contains utilities for handling file operations in the assembler project.

## Files

### file_utils.py
This file contains functions to perform various file operations required by the assembler. Below is a detailed explanation of each function and its usage.

## Functions

### `read_file(file_path)`
This function reads the content of a file and returns it.

**Parameters:**
- `file_path`: The path to the file to be read.

**Returns:**
- `content`: The content of the file.

**Usage:**
```python
from file_utils import read_file

content = read_file("path/to/file")
```

### `write_file(file_path, content)`
This function writes the given content to a file.

**Parameters:**
- `file_path`: The path to the file to be written.
- `content`: The content to be written to the file.

**Usage:**
```python
from file_utils import write_file

write_file("path/to/file", "content to write")
```

### `append_to_file(file_path, content)`
This function appends the given content to a file.

**Parameters:**
- `file_path`: The path to the file to be appended.
- `content`: The content to be appended to the file.

**Usage:**
```python
from file_utils import append_to_file

append_to_file("path/to/file", "content to append")
```

## Usage

To perform file operations, you can use the functions provided in `file_utils.py` as shown below:

```python
from file_utils import read_file, write_file, append_to_file

# Read content from a file
content = read_file("path/to/file")

# Write content to a file
write_file("path/to/file", "content to write")

# Append content to a file
append_to_file("path/to/file", "content to append")
```

This will allow you to handle file operations efficiently in your assembler project.