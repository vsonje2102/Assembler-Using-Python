# Self NM

This directory contains the `self_nm.py` script, which is responsible for analyzing and displaying the symbol table of an assembly program. The script provides detailed information about symbols, including their names, addresses,

Gives ouput like a bin/utils nm

## Files

### `self_nm.py`

- **Description:**
    - Analyzes the symbol table of an assembly program.
    - Displays detailed information about each symbol.

- **Parameters:**
    - `assembly_code`: The assembly code from which the symbol table will be extracted and analyzed.

- **Usage:**
    ```python
    from self_nm import analyze_symbol_table

    symbol_table = analyze_symbol_table(assembly_code)
    ```

## Summary

The `self_nm.py` script is essential for understanding the structure and organization of symbols within an assembly program. By providing detailed information about each symbol, it aids in debugging and optimizing the assembly code.