# This script compiles the .asm file into the actual binary for the .hack file
import sys


def return_binary(file):

    print("Converting mnemonics to binary codes...")
    new_file = list()

    for line in file:

        computed_string = ""
        resolved = False

        if line.startswith("@") and not resolved:
            clean_line = line.lstrip("@")
            computed_string = format(int(clean_line), "08b").zfill(16)
            resolved = True

        if line.count('=') > 0 and not resolved:
            parts = line.split('=')

            destination = parts[0]
            destination = return_dest_code(destination)
            safety_check(destination, line)

            compute = parts[1]
            compute = return_command_code(compute)
            safety_check(compute, line)

            jump = "000"
            computed_string = "111" + compute + destination + jump
            resolved = True

        if line.count(';') > 0 and not resolved:
            parts = line.split(';')

            compute = parts[0]
            compute = return_command_code(compute)
            safety_check(compute, line)

            jump = parts[1]
            jump = return_jump_code(jump)
            safety_check(jump, line)

            destination = "000"
            computed_string = "111" + compute + destination + jump
            resolved = True

        if not resolved:
            compute = return_command_code(line)
            safety_check(compute, line)
            computed_string = "111" + compute + "000" + "000"

        new_file.append(computed_string)

    print("Finished converting mnemonics.")
    return new_file


def return_command_code(mnemonic):
    switch_comp = {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        'M': '1110000',
        '!M': '1110001',
        '-M': '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101'
    }
    return switch_comp.get(mnemonic, "INVALID")


def return_dest_code(mnemonic):
    switch_dest = {
        'null': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
    }
    return switch_dest.get(mnemonic, "INVALID")


def return_jump_code(mnemonic):
    switch_jump = {
        '0': '000',
        'null': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }
    return switch_jump.get(mnemonic, "INVALID")


def safety_check(command, line):
    if command == "INVALID":
        print("Error: This command is not recognized.")
        print(line)
        sys.exit()