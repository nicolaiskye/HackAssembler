def parse(file):
    print("Parsing...")
    new_file = remove_comments(file)
    new_file = remove_whitespaces(new_file)
    new_file = remove_empty_lines(new_file)
    print("File parsed.")

    return new_file


def remove_comments(file):
    print("\t- Removing user comments...")
    new_file = list()
    i = 0
    lines = file.readlines()
    for x in lines:
        if "//" in x:
            s = x.split("//")
            new_file.append(s[0])
            i += 1
        else:
            new_file.append(x)
    # print(len(new_file), " total lines.", i, " comments removed.")

    report_done(file, new_file)
    return new_file


def remove_whitespaces(file):
    print("\t- Removing whitespaces...")
    new_file = list()
    for x in file:
        new_file.append(x.strip())
    # print(len(new_file), " total lines stripped.")

    report_done(file, new_file)
    return new_file


def remove_empty_lines(file):
    print("\t- Removing empty lines...")
    new_file = list(filter(None, file))
    # print(len(file)-len(new_file), " empty lines erased. ")

    report_done(file, new_file)
    return new_file


def report_done(file, new_file):
    if new_file == file:
        print("\t- Nothing to do.")
    else:
        print("\t- Finished.")
