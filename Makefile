# Makefile to run Python files one by one

all:
	python3 -m avlTree.avl_tree
	python3 -m elfUtils.elf_utils
	python3 -m filesUtils.file_utils
	python3 -m helper.ecnodings_regIncDecMulDiv
	python3 -m helper.entries
	python3 -m helper.filterInput
	python3 -m helper.printSymbolTable
	python3 -m intermediateCodeFile.intermediateCodeFile
	python3 -m listingFileCreation.combine_and_save_listing
	python3 -m listingFileCreation.listingFileCreation
	python3 -m listingFileCreation.textSection.formatTextSection
	python3 -m sectionExtractors.section_extractors
	python3 -m sectionParser.data_bss_Section_Parser
	python3 -m selfNM.self_nm
