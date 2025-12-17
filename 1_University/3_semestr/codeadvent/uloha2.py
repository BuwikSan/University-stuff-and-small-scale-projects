import os

current_dir = os.path.dirname(__file__)
os.chdir(current_dir)


with open('resources/input2.txt', 'r', encoding='utf-8') as f:
    obsah = f.read()

print(obsah)

