import sys
import numpy as np
import pandas as pd
import os

def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def write_to_file(dir, file_name, data, ext: str = "csv"):
    with open(f"{dir}/{file_name}.{ext}", "w") as f:
        f.write(data)

def validate_question(copy: list, i: int, l: int):
    print(f"[CURRENT CHOICE]::{copy[i:i+l]}")
    if i+l < len(copy):
        print(f"[NEXT CHOICE]::{copy[i+l]}")
    return input("Is this a valid choice? (y/n/t/q)")

class Extractor:
    def __init__(self, filename: str):
        self.filename = filename
        self.raw_data = None
        self.output = {}

    def __repr__(self):
        return f"{self.raw_data}"

    def ask_column_name(self):
        for i, col in enumerate(self.raw_data.columns):
            print(f"{i}: {col}")
        col_idx = int(input("Enter the column index: "))
        return self.raw_data.columns[col_idx]

    def good_question(self, copy, i: int, l: int, tab: list):
        a = ", ".join(copy[i:i+l])
        tab[a] = 1
        for _ in range(i, i+l):
            copy.pop(i)
        return a

    def multichoice_col(self, col_name: str = None, ask_overwrite: bool = False):
        create_dir("ans")
        answers = []
        if col_name is None:
            col_name = self.ask_column_name()
        if self.raw_data[col_name].dtype == int:
            return
        
        if os.path.exists(f"ans/{col_name}.csv"):
            
            if ask_overwrite:
                print("File already exists. Overwrite? (y/n/q)")
                overwrite = input()
                if overwrite == "n":
                    with open(f"ans/{col_name}.csv", "r") as f:
                        answers = f.read().split("; ")
                if overwrite == "q":
                    return
            else:
                with open(f"ans/{col_name}.csv", "r") as f:
                    answers = f.read().split("; ")
        tab = {}
        quit = False
        for raw_answer in self.raw_data[col_name]:
            if isinstance(raw_answer, float):
                print(f"{raw_answer} is a float. Skipping.")
                continue
            if quit:
                break
            for answer in answers:
                if answer in raw_answer:
                    print("Found answer:", answer)
                    raw_answer = raw_answer.replace(answer, "")
                    if tab.get(answer) is None:
                        tab[answer] = 0
                    tab[answer] += 1
            copy = raw_answer.split(", ")
            i = 0
            l = 1
            while copy:
                if copy[i] == "":
                    copy.pop(i)
                    l = 1
                    continue
                if copy[i:i+l] in answers:
                    self.good_question(copy, i, l, tab)
                    l = 1
                q = validate_question(copy, i, l)
                if q == "y":
                    a = self.good_question(copy, i, l, tab)
                    answers.append(a)
                    l = 1
                if q == "n":
                    l += 1
                if q == "t":
                    copy.pop(i)
                    l = 1
                if q == "q":
                    quit = True
                    break

        self.output[col_name] = pd.DataFrame.from_dict(tab, orient="index")
        write_to_file("ans", col_name, "; ".join(answers))


    def label_all(self):
        for col in self.raw_data.columns[1:]:
            self.multichoice_col(col)

    def read_data(self):
        with open(self.filename, "r") as f:
            self.raw_data = pd.read_csv(self.filename)

    def save_all(self):
        if not os.path.exists("output"):
            os.mkdir("output")
        for col in self.output:
            self.output[col].to_csv(f"output/{col}.csv")


def main():
    if len(sys.argv) < 2:
        print("Usage: extract.py <filename>")
        exit(1)
    filename = sys.argv[1]
    extractor = Extractor(f"data/{filename}.csv")
    extractor.read_data()
    extractor.label_all()
    extractor.save_all()
    

if __name__ == "__main__":
    main()