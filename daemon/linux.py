import os
import subprocess
import shutil
import sys

try:
    import apt
    import apt_pkg
except:
    print("not running in linux")
from consts import app_name, dev

home_dir = os.path.expanduser("~")


def self_dir():
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    return base_path


repo_location = os.getcwd() + "/cache" if dev else f"{home_dir}/.cache/{app_name}"
step = 0


# Helper functions
def run_shell(cmd):
    return subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, text=True).stdout


def write(file_name, string):
    with open(f'{repo_location}/{file_name}', 'w') as f:
        f.write(string)


def write_output(file_name, cmd):
    with open(f'{repo_location}/{file_name}', 'w') as f:
        f.write(run_shell(cmd))


def create_repo(git_remote, username, password, repo):
    os.chdir(repo)
    os.system(f'git init')
    write(".gitignore", "**/*Cache*\n**/*cache*")
    # Format: https://username:password@myrepository.biz/file.git
    credential_url = f'{git_remote.split("//")[0]}//{username}:{password}@{git_remote.split("//")[1]}'
    os.system('git remote rm origin')
    os.system(f'git remote add origin {credential_url}')
    os.system("git pull --all --allow-unrelated-histories")


def push_repo(repo):
    os.chdir(repo)
    branch = os.path.basename(run_shell("git branch -r"))
    os.system('git add .')
    os.system('git commit -am "commit"')
    os.system(f'git merge --allow-unrelated-histories -m "" -s ours origin/{branch}')
    os.system('git commit -am "commit"')
    os.system(f'git branch -M {branch}')
    os.system(f'git push --set-upstream origin {branch}')


def get_app_data():
    dirs = ".config .var .themes snap .local/share/gnome-shell .local/share/fonts \
    .local/share/backgrounds .local/share/applications .local/share/icons .local/share/keyrings".split()
    dirs[:] = [f"{home_dir}/" + d for d in dirs]
    os.popen(f'cp -Ru {" ".join(dirs)} {repo_location}')


def get_apt_packages():
    # Apt repos and keys
    run_shell(f'cp -Ru /etc/apt/sources.list.d/ {repo_location}')
    run_shell(f'cp /etc/apt/sources.list {repo_location}')
    write_output('repo.keys', 'apt-key exportall')
    # Apt packages
    packages = apt.Cache()
    with open(f'{repo_location}/packageList.txt', 'w') as file:
        for name in packages.keys():
            pk = packages[name]
            if pk.is_installed and not (pk.is_now_broken or pk.is_auto_removable):
                file.write(name + '\n')
    file.close()


def restore_app_data():
    os.chdir(repo_location)
    subdirs = next(os.walk('.'))[1]
    subdirs.remove('sources.list.d')
    subdirs.remove('.git')
    share_dir = ['gnome-shell', 'fonts', 'backgrounds', 'applications', 'icons', 'keyrings']
    for dir in subdirs:
        if dir.split('/')[len(dir.split('/')) - 1] in share_dir:
            run_shell(f'rsync --recursive {dir} {home_dir}/.local/share')
        else:
            run_shell(f'rsync --recursive {dir} {home_dir}')


# Non-helper functions
def backup(git_remote, username, password):
    global step
    step = 0
    try:
        os.mkdir(repo_location)
    except:
        pass
    create_repo(git_remote, username, password, repo_location)
    step = 1
    write_output('dconf-backup.txt', 'dconf dump /')
    get_apt_packages()
    write_output('flatpak.list', 'flatpak list --app --columns application')
    write("sudo snap.list", os.popen("snap list | awk '!/disabled/{print $1}' | awk '{if(NR>1)print}'").read())
    step = 2
    get_app_data()
    step = 3
    push_repo(repo_location)
    step = 4


def load_repo(git_remote, username, password):
    try:
        os.mkdir(repo_location)
    except:
        pass
    os.chdir(repo_location)
    # Format: https://username:password@myrepository.biz/file.git
    credential_url = f'{git_remote.split("//")[0]}//{username}:{password}@{git_remote.split("//")[1]}'
    remote = run_shell('git config --get remote.origin.url').strip()
    if credential_url == remote:
        os.system('git pull')
    else:
        pass
        os.chdir("..")
        shutil.rmtree(repo_location)
        os.mkdir(repo_location)
        os.chdir(repo_location)
        os.system(f'git clone {credential_url} .')


def restore(git_remote, username, password):
    global step
    step = 0
    load_repo(git_remote, username, password)
    step = 1
    os.system(f'pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY python3 {self_dir()}/linux_admin.py {repo_location}')
    with open(f'{repo_location}/flatpak.list', 'r') as file:
        for line in file.readlines():
            run_shell(f'flatpak install flathub {line.strip()} -y --noninteractive')
    step = 2
    restore_app_data()
    os.system(f"dconf load / < {repo_location}/dconf-backup.txt")
    step = 3

# load_repo('url', 'username', 'password')
