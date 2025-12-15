
def parse_script(file):
    with open(file, 'r') as f:
        for line in f:
            if "Failed password" in line:
                yield line.strip()



if __name__ == "__main__":

    file_path = "fakelog1.txt"
    parsed = parse_script(file_path)

    print("Res: ")
    for i in parsed:
        print(i)

