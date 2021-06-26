import subprocess
import re
from pathlib import Path
import os
from consts import app_name, dev
import urllib.request
from linux import create_repo, push_repo, load_repo

home_dir = str(Path.home())

repo_location = os.getcwd() + "\\cache_windows" if dev else f"{home_dir}\\{app_name}"


def backup(git_remote, username, password):
    # applications
    try:
        os.mkdir(repo_location)
    except:
        pass
    create_repo(git_remote, username, password, repo_location)
    apps = subprocess.run(
        "powershell.exe Get-ChildItem 'HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\App Paths' "
        "| Select-Object name",
        stdout=subprocess.PIPE, text=True).stdout
    regex = r"\\(\w*).(?:exe|EXE)"
    apps = re.findall(regex, apps)
    apps = [app.lower() for app in apps]
    url = f'https://ninite.com/{"-".join(apps)}/ninite.exe'
    urllib.request.urlretrieve(url, f"{repo_location}\\installer.exe")
    # appdata
    dir = home_dir + "\\AppData\\Roaming"
    os.system(f"powershell.exe Copy-Item -Recurse {dir} {repo_location}")
    push_repo(repo_location)


def restore(git_remote, username, password):
    try:
        os.chdir(repo_location)
    except:
        load_repo(git_remote, username, password)
        try:
            os.chdir(repo_location)
        except:
            exit(1)
    os.system(f"{repo_location}\\installer.exe")
    dir = home_dir + "\\AppData\\Roaming"
    appdata = repo_location + "\\AppData\\Roaming"
    os.system(f"powershell.exe Copy-Item -Recurse {repo_location} {dir}")


