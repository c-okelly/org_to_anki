#! /bin/python3

import os

# This is terrible
def main():

    # Insall
    os.system("python3 setup.py install")
    # Run command
    os.system("org_to_anki > testOutput.txt")

    with open("testOutput.txt") as f:
        data = f.read()
    assert(data.split("\n")[0] == "File was not given. Will upload default file.")

if __name__ == "__main__":
    main()



