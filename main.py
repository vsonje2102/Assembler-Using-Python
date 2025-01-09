## importing utils (necessary fubction written in other file)

from filesUtils.file_utils import read_assembly_code_from_file, create_opcode_tree_from_file,store_symbol_table , save_file
from sectionExtractors.section_extractors import extract_data_section, extract_bss_section , extract_text_section
from sectionParser.data_bss_Section_Parser import parse_data_section, parse_bss_section ,parse_text_section
from avlTree.avl_tree import AVLTree
from listingFileCreation.listingFileCreation import listing_File_Creation
from elfUtils.elf_utils import create_object_file
from selfNM.self_nm import binutils_nm
from intermediateCodeFile.intermediateCodeFile import write_IntermediateCode
from listingFileCreation.combine_and_save_listing import combine_and_save_files
from helper.printSymbolTable import print_symbol_table
from helper.displayHelper import display_help
import sys

#-------------------------------------------------------------------------------------------------------
# input  and ouput files

if len(sys.argv) < 2:
    print("Usage: python script.py <file> [-flags]")
    display_help()
    exit(1)

ip_assembly_file = None
flags = None
file_count = 0

for arg in sys.argv[1:]:
    if arg.startswith('-'):
        if flags:  
            print("Error: Multiple flags detected. Only one flag is allowed.")
            exit(1)
        flags = arg 
    elif arg.endswith('.asm'):
        file_count += 1
        if ip_assembly_file: 
            print("Error: Multiple files detected. Only one file is allowed.")
            exit(1)
        ip_assembly_file = arg
    else:
        print(f"Error: Invalid argument '{arg}'. Must be a .asm file or a flag starting with '-'.")
        exit(1)

if not ip_assembly_file:
    print("Error: No valid .asm file provided.")
    display_help()
    exit(1)

print(f"Input assembly file: {ip_assembly_file}")
print(f"Flags provided: {flags}")

opcode_file = "helper/opcode_instructions.csv"
base_file_name_without_ext = ip_assembly_file.split('/')[-1].rsplit('.', 1)[0]
op_obj_file = base_file_name_without_ext + '.o'
intermediate_file = base_file_name_without_ext + '.i'


#-------------------------------------------------------------------------------------------------------
#Inintalization  and declaration
# flag status 

nm_status = 0
lst_status = 0
symTable_status = 0
int_status = 0

if flags:

    if flags.startswith('-'):
        for char in flags[1:]:
            if char == 'n':
                nm_status = 1
            elif char == 'l':
                lst_status = 1
            elif char == 's':
                symTable_status = 1
            elif char == 'i':
                int_status = 1
            elif char == "h":
                 display_help()
                 exit()
            else:
                print(f"Error: Invalid flag '{char}'")
                exit(1)
    else:
        print("Error: Flags should start with '-'")
        exit(1)

symbol_tree = AVLTree()
literal_tree = AVLTree()
opcode_tree = AVLTree()
error_table = []
intermediate_code = []


#-------------------------------------------------------------------------------------------------------
# Ceate the opcode tree from file 

opcode_tree = create_opcode_tree_from_file(opcode_file,error_table)

#-------------------------------------------------------------------------------------------------------
# Read assembly code from file and extract sections from it

assembly_code = read_assembly_code_from_file(ip_assembly_file)
data_section = extract_data_section(assembly_code)
bss_section = extract_bss_section(assembly_code)
text_section = extract_text_section(assembly_code)


#--------------------------------------------------------------------------------------------------------
# Process data,bss and text section and create Intermeddiate code (PARSE ONE)

symbol_tree, intermediate_code = parse_data_section(data_section, symbol_tree, intermediate_code,error_table)
if len(error_table) > 0:
    print("Errors found in data section:")
    for error in error_table:
        print(error)
    exit()
symbol_tree, intermediate_code  = parse_bss_section(bss_section, symbol_tree, intermediate_code,error_table)
if len(error_table) > 0:
    print("Errors found in bss section:")
    for error in error_table:
        print(error)
    exit()

literal_tree,intermediate_code = parse_text_section(text_section, symbol_tree, intermediate_code , opcode_tree,literal_tree,error_table)
if len(error_table) > 0:
    print("Errors found in text section:")
    for error in error_table:
        print(error)
    exit()

symbol_table_list = store_symbol_table(symbol_tree.root)

#-------------------------------------------------------------------------------------------------------------
# getting Listing file and object file Creation (Parse TWO)

lst,machine_code_text,machine_code_data,machine_code_bss=listing_File_Creation(intermediate_code,symbol_tree,literal_tree)
object_code = create_object_file(machine_code_text,machine_code_data,machine_code_bss,symbol_table_list)


#--------------------------------------------------------------------------------------------------------------
# Final output according to flags

save_file(op_obj_file,object_code,"binary") 
if lst_status:
    combine_and_save_files(lst,assembly_code,"p.lst")
    print("Listing File Written in p.lst")
if nm_status:
    binutils_nm(object_code)
if int_status:
    write_IntermediateCode(intermediate_code,intermediate_file)
if symTable_status:
    print_symbol_table(symbol_table_list)
