import csv
from avlTree.avl_tree import AVLTree
from helper.entries import OpcodeInstruction 
import re

def read_assembly_code_from_file(filename):
    """Reads the assembly code from a file, removing comments and empty lines."""
    with open(filename, 'r') as file:
        lines = []
        for line in file:
            # Remove comments
            line = re.sub(r';.*', '', line)
            # Remove extra blank lines by checking if the line is non-empty after stripping whitespace
            if line.strip():  # Only add non-empty lines
                lines.append(line.rstrip())
        return lines

def create_opcode_tree_from_file(filename,error_table):
    opcode_tree = AVLTree()
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            key = f"{row['instruction']}:{row['param1']}:{row['param2']}"
            opcode_data = OpcodeInstruction(
                opcode=row['opcode'],
                instruction=row['instruction'],
                num_params=int(row['num_params']),
                param1=row['param1'],
                param2=row['param2'],
                size=int(row['size']),
                is_modr=bool(int(row['is_modr'])),
                rd=row['+rd']
            )
            
            # Insert opcode data into the opcode tree
            opcode_tree.root = opcode_tree.insert(opcode_tree.root, key, opcode_data,error_table)
    
    return opcode_tree

def save_file(filename, data,mode="text",format="string"):
    if mode == "binary":
        mode = "wb"
    elif mode == "text":
        mode = "w"
    with open(filename, mode) as file:
        if format == "list":
            for line in data:
                file.write(line)
        else:
            file.write(data)
    


def store_symbol_table(node,symbol_table_list=None):
    if symbol_table_list is None:
        symbol_table_list =[]
    if node:
        store_symbol_table(node.left,symbol_table_list)
        symbol_table_list.append([
            node.data.Symbol_Name,
            node.data.Type,
            node.data.Size,
            node.data.Value,
            node.data.Scope,
            node.data.Address
        ])
        store_symbol_table(node.right,symbol_table_list)
    return symbol_table_list