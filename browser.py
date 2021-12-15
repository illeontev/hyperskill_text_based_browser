import os
import shutil
import sys
import requests
from bs4 import BeautifulSoup
from colorama import Fore

from collections import deque

if len(sys.argv) < 2:
    exit(0)

dir_for_files = sys.argv[1]

try:
    os.mkdir(dir_for_files)
except:
    pass

prev_page = ""
stack = deque()

while True:
    string = input()
    if string == "exit":
        exit()
    elif string == "back":
        filename = stack.pop()
        with open(dir_for_files + "/" + filename, "r") as fin:
            data = fin.read()
            print(data)
        prev_page = filename
    elif "." not in string:
        print("Error: Incorrect URL")
    else:
        if prev_page != "":
            stack.append(prev_page)
        if not string.startswith("https://"):
            url = "https://" + string
        else:
            url = string
        try:
            respond = requests.request("GET", url)
            if respond:
                bs = BeautifulSoup(respond.text.rstrip(), "html.parser")
                text_output = ""
                for tag in bs.find_all(True):
                    if tag.name == "a":
                        text_output += Fore.BLUE + tag.get_text()
                    else:
                        text_output += Fore.RESET + tag.get_text()
                print(text_output)
                filename = string[:string.index(".")]
                with open(dir_for_files + "/" + filename, "w", encoding="UTF-8") as fout:
                    print(text_output, file=fout)

                prev_page = filename
        except requests.exceptions.ConnectionError:
            print("Incorrect URL")




