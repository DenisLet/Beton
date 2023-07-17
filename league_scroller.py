import os

folder_path = "./records"  # Путь к папке records (можно указать абсолютный путь)
txt_files = [file for file in os.listdir(folder_path) if file]
files = st = 0
for file_name in txt_files:
    file_path = os.path.join(folder_path, file_name)
    files+=1
    with open(file_path, "r") as file:
        for line in file:
            st += 1

print(files,st)


def extract_details(line):
    half1 = line[0][0]
