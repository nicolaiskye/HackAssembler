# This script is responsible for taking a parsed file and mapping
# locations in memory for static and user-defined symbols

import sys
import re


def resolve_symbols(file):
    print("Resolving symbols...")

    file_labels_mapped = list()
    file_symbols_mapped = list()
    static_symbols = {
        'SP': 0x0000,
        'LCL': 0x0001,
        'ARG': 0x0002,
        'THIS': 0x0003,
        'THAT': 0x0004,
        'R0': 0x0000,
        'R1': 0x0001,
        'R2': 0x0002,
        'R3': 0x0003,
        'R4': 0x0004,
        'R5': 0x0005,
        'R6': 0x0006,
        'R7': 0x0007,
        'R8': 0x0008,
        'R9': 0x0009,
        'R10': 0x000a,
        'R11': 0x000b,
        'R12': 0x000c,
        'R13': 0x000d,
        'R14': 0x000e,
        'R15': 0x000f,
        'SCREEN': 0x4000,
        'KBD': 0x6000
    }
    user_defined_symbols = dict()
    memory_pointer = 0x0400
    remove_lines = 0

    # Firstly, find and map LABELS
    for i in range(0, len(file)):
        if file[i].startswith("("):
            label = file[i].lstrip("(").rstrip(")")
            print("\t- Label detected: ", label)
            if not contains_prohibited_characters(label):
                user_defined_symbols.update({label: i-remove_lines})
                remove_lines += 1
            else:
                print("\n\nError: Label '", label, "' contains non-alphabet characters. Quitting.")
                sys.exit("")
        else:
            file_labels_mapped.append(file[i])

    # Secondly, add unique user defined symbols to a dictionary
    for line in file_labels_mapped:

        resolved = False
        if line.startswith("@"):

            current_symbol = line.lstrip("@")
            print("\t- Symbol detected: ", current_symbol)

            # Check if symbol is a constant
            if is_constant(current_symbol) and not resolved:
                print("\t\t-> is a constant. Ignoring.")
                resolved = True

            # Check if symbol breaks any rules
            if not current_symbol[0].isalpha() and not resolved:
                print("\n\nError: First letters of symbols must be an alphabet character.")
                print("[", current_symbol, "] does not comply.")
                sys.exit()

            if contains_prohibited_characters(current_symbol) and not resolved:
                print("\n\nError: Symbol [", current_symbol, "] contains prohibited characters. Symbols can "
                                                             "only contain\nletters, numbers, periods, "
                                                             "underscores, dollar signs, and colons.")
                sys.exit()

            # Check if symbol exists as static symbol
            if not resolved:
                for key in static_symbols:
                    if current_symbol == key and not resolved:
                        print("\t\t-> is in static symbol database.")
                        resolved = True
                        break

            # Check if user-defined symbol already mapped
            if not resolved:
                for key in user_defined_symbols:
                    if current_symbol == key and not resolved:
                        print("\t\t-> user defined symbol already exist.")
                        resolved = True
                        break

            # Symbol appears to be new and unmapped. Map it
            if not resolved:
                print("\t\t-> new user defined symbol detected. Allocating space in memory.")
                user_defined_symbols.update({current_symbol: memory_pointer})
                memory_pointer += 1
                resolved = True

    # This message is for debug purposes only .. Delete later!
    print("These symbols have been mapped to memory:")
    for key, value in user_defined_symbols.items():
        print("\t- ", key, " : ", value)

    # Thirdly, replace all symbols with their mapped memory locations
    for line in file_labels_mapped:
        resolved = False
        if line.startswith("@"):
            current_symbol = line.lstrip("@")

            if is_constant(current_symbol) and not resolved:
                mapped_symbol = "@" + current_symbol
                file_symbols_mapped.append(mapped_symbol)
                resolved = True

            if not resolved:
                for key, value in static_symbols.items():
                    if current_symbol == key and not resolved:
                        mapped_symbol = "@" + str(value)
                        file_symbols_mapped.append(mapped_symbol)
                        resolved = True
                        break

            if not resolved:
                for key, value in user_defined_symbols.items():
                    if current_symbol == key and not resolved:
                        mapped_symbol = "@" + str(value)
                        file_symbols_mapped.append(mapped_symbol)
                        resolved = True
                        break
        else:
            file_symbols_mapped.append(line)

    return file_symbols_mapped


def is_constant(symbol):
    return symbol.isnumeric()


def contains_prohibited_characters(strg, search=re.compile(r'[^a-zA-Z0-9\_\.\$\:]').search):
    return bool(search(strg))
