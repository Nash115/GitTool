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
if not(os.path.exists("userPreferences.json")):
    with open("userPreferences.json","w") as f:
        f.write(str(json.dumps({"repoFolder": ""}, indent=4)))

with open("param.json", "r") as f:
    param = json.load(f)
    git_folder = param["gitPath"]
    folder = git_folder
with open("userPreferences.json", "r") as f:
    pref = json.load(f)
while os.system(folder + " --version") != 0:
    folder = simpledialog.askstring("GitTool settings", "Git exe / Git command :", initialvalue="git")
    if folder is None:
        crash("No git given")
param["gitPath"] = folder
with open("param.json","w") as f:
    f.write(str(json.dumps(param, indent=4)))
GIT_FOLDER = git_folder

if pref["repoFolder"] == "":
    pre_github_folder = Path.home() / "Documents" / "GitHub"
    if not(os.path.exists(pre_github_folder)):
        pre_github_folder = Path.home() / "OneDrive" / "Documents" / "GitHub"
        if not(os.path.exists(pre_github_folder)):
            pre_github_folder = ""
            while not(os.path.exists(pre_github_folder)):
                pre_github_folder = simpledialog.askstring("GitTool settings", "Github folder :", initialvalue="C:\\")
                if pre_github_folder is None:
                    crash("No github dir given")
            pref["repoFolder"] = pre_github_folder
            with open("userPreferences.json","w") as f:
                f.write(str(json.dumps(param, indent=4)))
else:
    pre_github_folder = pref["repoFolder"]
GITHUB_FOLDER = pre_github_folder
list_in_github_folder = os.listdir(GITHUB_FOLDER)
github_folders = [element for element in list_in_github_folder if os.path.isdir(os.path.join(GITHUB_FOLDER, element))]
github_folders.append("---SELECT---")

def clone_repo():
    dialog = CustomDialog(window, title="Repo url :")
    repo_url = dialog.result
    command(GITHUB_FOLDER, f"{GIT_FOLDER} clone {repo_url}")

def refresh_repos():
    list_in_github_folder = os.listdir(GITHUB_FOLDER)
    github_folders = [element for element in list_in_github_folder if os.path.isdir(os.path.join(GITHUB_FOLDER, element))]
    github_folders.append("---SELECT---")
    selection.set(github_folders[-1])
    dropdown["menu"].delete(0, "end")
    for option in github_folders:
        dropdown["menu"].add_command(label=option, command=tk._setit(selection, option))

window = tk.Tk()
window.title("GitTool")
window.geometry("800x450")
window.config(background="#424242")

repo_location = tk.Frame(window, bd=3, relief="groove", bg="#424242")
label = tk.Label(repo_location, text=f"Repo floder : {GITHUB_FOLDER}", bg="#424242", fg="#ffffff")
label.pack(side="left", padx=5)
refresh_button = tk.Button(repo_location, text="Refresh", command=refresh_repos)
refresh_button.pack(side="left", padx=5)
repo_location.pack(anchor="nw")

repo_selection = tk.Frame(window, bd=3, relief="groove", bg="#424242")
label = tk.Label(repo_selection, text="Repo :", bg="#424242", fg="#ffffff")
label.pack(side="left", padx=5)
selection = tk.StringVar(repo_selection)
selection.set(github_folders[-1])
dropdown = tk.OptionMenu(repo_selection, selection, *github_folders)
dropdown.pack(side="left", padx=5)
clone_bouton = tk.Button(repo_selection, text="Clone a repo", command=clone_repo)
clone_bouton.pack(side="left", padx=5)
repo_selection.pack(anchor="nw")

window.mainloop()