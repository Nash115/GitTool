import tkinter as tk
from tkinter import simpledialog
import os
import json
from pathlib import Path
from tkinter import simpledialog
from tkinter import messagebox

actu_repo = ""
actu_repo_folder = ""
branches = {
    "actual":"",
    "others":[]
}
branches_list = ["NO REPO SELECTED"]

# pomme de terre

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
    return os.popen(command).read()

def refresh_actu_repo(event, a, b):
    global actu_repo, actu_repo_folder
    if selection.get() != "---SELECT---":
        actu_repo = selection.get()
        actu_repo_folder = f"{GITHUB_FOLDER}\{actu_repo}"
        actu_repo_title["text"] = selection.get()
    else:
        actu_repo = ""
        actu_repo_folder = ""
        actu_repo_title["text"] = "No repository selected"
    read_branches(0,0,0)

if not(os.path.exists("param.json")):
    crash("param.json not present")
if not(os.path.exists("userPreferences.json")):
    with open("userPreferences.json","w") as f:
        f.write(str(json.dumps({"repoFolder": ""}, indent=4)))

######################
# GIT COMMAND/FOLDER #
######################
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

#################
# GITHUB FOLDER #
#################
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

#####################
# FUNCs USED IN TK  #
#####################
def clone_repo():
    dialog = CustomDialog(window, title="Repo url :")
    repo_url = dialog.result
    command(GITHUB_FOLDER, f"{GIT_FOLDER} clone {repo_url}")

def read_branches(event, a, b):
    global branches, branches_list
    if actu_repo == "":
        return False
    branches = {
        "actual":"",
        "others":[]
    }

    if event != 0 and (branches_list != [] and branches_list != ["NO REPO SELECTED"]):
        branch_name = selection_branch.get()
        command(actu_repo_folder, f"{GIT_FOLDER} checkout {branch_name}")

    result = command(actu_repo_folder,f"{GIT_FOLDER} branch")
    lines = result.split('\n')
    for line in lines:
        if line.startswith('* '):
            branches["actual"] = line.strip().replace("* ","")
        if line.startswith('  '):
            branches["others"].append(line.strip().replace("  ",""))
    
    branches_list = [] # Index  0 => actual branch
    branches_list.append(branches["actual"])
    for i in branches["others"]:
        branches_list.append(i)
    selection_branch.set(branches_list[0])
    dropdown_branch["menu"].delete(0, "end")
    for option in branches_list:
        dropdown_branch["menu"].add_command(label=option, command=tk._setit(selection_branch, option))

    if branches_list == []:
        branches_list = ["NO REPO SELECTED"]
    return branches_list
read_branches(0,0,0)

def create_branch():
    dialog = CustomDialog(window, title="Name of the branch to create:")
    branch_name = dialog.result
    command(actu_repo_folder, f"{GIT_FOLDER} branch {branch_name}")

def delete_branch():
    messagebox.showwarning("GitTool Warning", "WARNING ! Deleting the branch is permanent.")
    dialog = CustomDialog(window, title="Name of the branch to delete:")
    branch_name = dialog.result
    command(actu_repo_folder, f"{GIT_FOLDER} branch -D {branch_name}")

def refresh_repos():
    list_in_github_folder = os.listdir(GITHUB_FOLDER)
    github_folders = [element for element in list_in_github_folder if os.path.isdir(os.path.join(GITHUB_FOLDER, element))]
    github_folders.append("---SELECT---")
    selection.set(github_folders[-1])
    dropdown["menu"].delete(0, "end")
    for option in github_folders:
        dropdown["menu"].add_command(label=option, command=tk._setit(selection, option))

def get_git_status():
    if actu_repo == "":
        return False
    result = command(actu_repo_folder,f"{GIT_FOLDER} add .")
    result = command(actu_repo_folder,f"{GIT_FOLDER} status")
    modified_files = []
    lines = result.split('\n')
    for line in lines:
        if line.startswith('\tmodified:'):
            modified_files.append(("m",line.strip().replace("modified:   ","")))
        if line.startswith('\tnew file:'):
            modified_files.append(("n",line.strip().replace("new file:   ","")))
        if line.startswith('\tdeleted:'):
            modified_files.append(("d",line.strip().replace("deleted:    ","")))
    matchStatusColor = {
        "m":"#0366d6",
        "n":"#2fd04e",
        "d":"#bf0404"
    }
    status_list.delete(0, tk.END)
    for status,file in modified_files:
        status_list.insert(tk.END, file)
        status_list.itemconfig(tk.END, fg=matchStatusColor[status])
    return modified_files

def make_git_fetch():
    command(actu_repo_folder,f"{GIT_FOLDER} fetch")
    get_git_status()

def make_git_commit():
    message = commit_message.get()
    if message == "":
        messagebox.showerror("Commit error", "Summary is required")
        return False
    command(actu_repo_folder,f"{GIT_FOLDER} commit -m \"{message}\"")
    get_git_status()

def make_git_push():
    command(actu_repo_folder,f"{GIT_FOLDER} push origin main") ############################################ ! ONLY FOR MAIN BRANCH !!!!!!!!!!
    get_git_status()

##################
# TKINTER WINDOW #
##################
window = tk.Tk()
window.title("GitTool")
window.geometry("940x500")
window.minsize(300,300)
window.config(background="#424242")

repo_location = tk.Frame(window, bd=3, relief="groove", bg="#424242")
label = tk.Label(repo_location, text=f"Repo floder : {GITHUB_FOLDER}", bg="#424242", fg="#ffffff")
label.pack(side="left", padx=5)
refresh_button = tk.Button(repo_location, text="Refresh", command=refresh_repos)
refresh_button.pack(side="left", padx=5)
repo_location.pack(anchor="nw")

repo_info = tk.Frame(window, bg="#424242")

repo_selection = tk.Frame(repo_info, bd=3, relief="groove", bg="#424242")
label_repo = tk.Label(repo_selection, text="Repo :", bg="#424242", fg="#ffffff")
label_repo.pack(side="left", padx=5)
selection = tk.StringVar(repo_selection)
selection.set(github_folders[-1])
dropdown = tk.OptionMenu(repo_selection, selection, *github_folders)
dropdown.pack(side="left", padx=5)
clone_bouton = tk.Button(repo_selection, text="Clone a repo", command=clone_repo)
clone_bouton.pack(side="left", padx=5)
repo_selection.pack(side="left")

actu_repo_title = tk.Label(repo_info, text="No repository selected", bg="#424242", fg="#ffffff", font=("Times",21))
actu_repo_title.pack(side="left", padx=15)

branch_selection = tk.Frame(repo_info, bd=3, relief="groove", bg="#424242")
label_branch = tk.Label(branch_selection, text="Branch :", bg="#424242", fg="#ffffff")
label_branch.pack(side="left", padx=5)
selection_branch = tk.StringVar(branch_selection)
selection_branch.set(branches_list[0])
dropdown_branch = tk.OptionMenu(branch_selection, selection_branch, *branches_list)
dropdown_branch.pack(side="left", padx=5)
add_branch_bouton = tk.Button(branch_selection, text="New branch", command=create_branch)
add_branch_bouton.pack(side="left", padx=5)
remove_branch_bouton = tk.Button(branch_selection, text="Remove a branch", command=delete_branch)
remove_branch_bouton.pack(side="left", padx=5)
branch_selection.pack(side="left")

repo_info.pack(anchor="nw")

selection.trace_add("write", refresh_actu_repo)
dropdown.bind("<<OptionMenuSelect>>",refresh_actu_repo)

selection_branch.trace_add("write", read_branches)
dropdown_branch.bind("<<OptionMenuSelect>>",read_branches)

command_frame = tk.Frame(window, bg="#424242")

fetch_container = tk.Frame(command_frame, bd=3, relief="groove", bg="#424242")
status_bouton = tk.Button(fetch_container, text="Fetch", command=make_git_fetch)
status_bouton.pack(pady=5)
fetch_container.pack(side="left", padx=5)

status_list_container = tk.Frame(command_frame, bd=3, relief="groove", bg="#424242")
status_bouton = tk.Button(status_list_container, text="Status", command=get_git_status)
status_bouton.pack(pady=5)
status_list = tk.Listbox(status_list_container)
status_list.pack()
status_list_container.pack(side="left", padx=5)

commit_container = tk.Frame(command_frame, bd=3, relief="groove", bg="#424242")
commit_message = tk.Entry(commit_container)
commit_message.pack()
commit_bouton = tk.Button(commit_container, text="Commit", command=make_git_commit)
commit_bouton.pack(pady=5)
commit_container.pack(side="left", padx=5)

push_container = tk.Frame(command_frame, bd=3, relief="groove", bg="#424242")
push_bouton = tk.Button(push_container, text="Push main branch on GitHub", command=make_git_push)
push_bouton.pack(pady=5)
push_container.pack(side="left", padx=5)

command_frame.pack(anchor="n", pady=20)

window.mainloop()