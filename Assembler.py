# This is a script designed to assemble programs written in assembly language
# for the Hack CPU architecture into executable ".hack" files

import sys
import Parser
import SymbolsManager
import OpcodesGenerator


def main():

    if len(sys.argv)-1 > 0:
        filename = ""
        found_asm = False
        quiet_mode = False
        arguments = []
        for argument in sys.argv:
            arguments.append(argument)
            if sys.argv[argument].count(".asm") > 0 and not found_asm:
                filename = strip_asm(sys.argv[argument])
                found_asm = True

        if not found_asm:
            print("Arguments were given, but no file name found. Please provide a [.asm] file.")
            sys.exit()


        if not quiet_mode:
            print("Beginning compilation...")
        file = get_file(filename)
        file = Parser.parse(file)
        file = SymbolsManager.resolve_symbols(file)
        file = OpcodesGenerator.return_binary(file)
        save_hack(file)
        if not quiet_mode:
            print("\nCompilation complete.")

    else:
        print("This script compiles [name].asm files into 'HACK' CPU machine code")
        print("Usage:")
        print("\t> Assembler.py name-of-file.asm")
        sys.exit()


def get_file(filename):
    print("Opening [.asm] file...")
    f = open(filename, "r")
    if f.mode == 'r':
        print("File opened successfully.")
        return f
    else:
        print("Error finding file named: " + filename)


def save_hack(finished_translation, filename):
    print("Writing compiled code to .hack file...")
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(0, len(finished_translation)):
            if i != len(finished_translation)-1:
                current_line = finished_translation[i] + "\n"
            else:
                current_line = finished_translation[i]
            f.write(current_line)
    print("Done writing file.")


def strip_asm(filename):
    return filename.split(".")[0]


def add_hack_extension(filename):
    return filename + ".hack"


if __name__ == "__main__":
    main()
