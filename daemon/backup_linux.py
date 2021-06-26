import shutil

import apt
import subprocess
from consts import app_name, dev
import os

home_dir = os.path.expanduser("~")
repo_location = os.getcwd() + "/cache" if dev else f"{home_dir}/.cache/{app_name}"


def run_shell(cmd):
    return subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, text=True).stdout


def write(file_name, string):
    with open(f'{repo_location}/{file_name}', 'w') as f:
        f.write(string)


def write_output(file_name, cmd):
    with open(f'{repo_location}/{file_name}', 'w') as f:
        f.write(run_shell(cmd))


def create_repo(git_remote, username, password):
    os.chdir(repo_location)
    os.system(f'git init')
    write(".gitignore", "**/*Cache*\n**/*cache*")
    # Format: https://username:password@myrepository.biz/file.git
    credential_url = f'{git_remote.split("//")[0]}//{username}:{password}@{git_remote.split("//")[1]}'
    os.system('git remote rm origin')
    os.system(f'git remote add origin {credential_url}')
    os.system("git pull --all --allow-unrelated-histories")


def push_repo(git_remote, username, password):
    os.chdir(repo_location)
    branch = os.path.basename(run_shell("git branch -r"))
    os.system('git add .')
    os.system('git commit -am "commit"')
    # Format: https://username:password@myrepository.biz/file.git
    credential_url = f'{git_remote.split("//")[0]}//{username}:{password}@{git_remote.split("//")[1]}'
    os.system(f'git merge --allow-unrelated-histories -m "" -s ours origin/{branch}')
    os.system('git commit -am "commit"')
    os.system(f'git branch -M {branch}')
    os.system(f'git push --set-upstream origin {branch}')


def run(git_remote, username, password):
    # Git
    create_repo(git_remote, username, password)
    # Gnome registry
    write_output('dconf-backup.txt', 'dconf dump /')
    # Apt packages
    user_installed = []
    packages = apt.Cache()
    packages.open(None)
    with open(f'{repo_location}/packageList.txt', 'w') as file:
        for name in packages.keys():
            pk = packages[name]
            if pk.is_installed and not (pk.is_now_broken or pk.is_auto_removable
                                        or pk.is_auto_installed or 'lib' in name):
                user_installed.append(name)
                file.write(name + '\n')
    file.close()
    # Apt repos and keys
    os.system(f'cp -Rpu /etc/apt/sources.list.d/ {repo_location}')
    os.system(f'cp -Rpu /etc/apt/sources.list {repo_location}')
    write_output('repo.keys', 'apt-key exportall')
    # Flatpaks
    write_output('flatpak.list', 'flatpak list --app --columns application')
    # Snaps
    write("snap.list", os.popen("snap list | awk '!/disabled/{print $1}' | awk '{if(NR>1)print}'").read())
    # Appdata
    dirs = ".config .var .local/share/gnome-shell .local/share/fonts \
    .local/share/backgrounds .local/share/applications .local/share/icons .local/share/keyrings snap".split()
    dirs[:] = [f"{home_dir}/" + d for d in dirs]
    os.popen(f'cp -Rpu {" ".join(dirs)} {repo_location}')
    # Push


create_repo("https://gitlab.com/NeverLucky123/personal.git", "NeverLucky123", "Lol.com135")
push_repo("https://gitlab.com/NeverLucky123/personal.git", "NeverLucky123", "Lol.com135")
