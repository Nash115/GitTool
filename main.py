import tkinter as tk
from tkinter import simpledialog
import os
import json
from pathlib import Path
from tkinter import simpledialog

class CustomDialog(simpledialog.Dialog):
    def body(self, master):
        self.entry = tk.Entry(master, width=100)
        self.entry.pack()
        self.entry.insert(0, "https://www.github.com/")
        self.geometry("300x150")
        return self.entry
    def apply(self):
        self.result = self.entry.get()

def crash(pb:str):
    print(50*"#")
    print("The program terminated with the following error:")
    print(f"> {pb}")
    os.system("pause")
    exit()

def command(exFolder, command):
    os.chdir(exFolder)
    os.system(command)
    return True

if not(os.path.exists("param.json")):
    crash("param.json not present")

with open("param.json", "r") as f:
    param = json.load(f)
    git_folder = param["gitPath"]
    folder = git_folder
while os.system(folder + " --version") != 0:
    folder = simpledialog.askstring("GitTool settings", "Git exe / Git command :", initialvalue="git")
    if folder is None:
        crash("No git given")
param["gitPath"] = folder
with open("param.json","w") as f:
    f.write(str(json.dumps(param, indent=4)))
GIT_FOLDER = git_folder

GITHUB_FOLDER = Path.home() / "Documents" / "GitHub"
if not(os.path.exists(GITHUB_FOLDER)):
    os.system(f"mkdir {GITHUB_FOLDER}")
list_in_github_folder = os.listdir(GITHUB_FOLDER)
github_folders = [element for element in list_in_github_folder if os.path.isdir(os.path.join(GITHUB_FOLDER, element))]


def bouton_appuye():
    label.config(text="Le bouton a été appuyé!")

def clone_repo():
    dialog = CustomDialog(window, title="Repo url :")
    repo_url = dialog.result
    command(GITHUB_FOLDER, f"{GIT_FOLDER} clone {repo_url}")

window = tk.Tk()
window.title("GitTool")
window.geometry("800x450")
window.config(background="#424242")

repo_selection = tk.Frame(window, bd=3, relief="groove", bg="#424242")
label = tk.Label(repo_selection, text="Repo :", bg="#424242", fg="#ffffff")
label.pack(side="left", padx=5)
selection = tk.StringVar(repo_selection)
selection.set(github_folders[0])
dropdown = tk.OptionMenu(repo_selection, selection, *github_folders)
dropdown.pack(side="left", padx=5)
clone_bouton = tk.Button(repo_selection, text="Clone a repo", command=clone_repo)
clone_bouton.pack(side="left", padx=5)
repo_selection.pack(anchor="nw")


bouton = tk.Button(window, text="Appuyer", command=bouton_appuye)
bouton.pack()

window.mainloop()