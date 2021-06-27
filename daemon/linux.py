import os
import subprocess
import shutil

try:
    import apt
    import apt_pkg
except:
    print("not running in linux")
from consts import app_name, dev

home_dir = os.path.expanduser("~")
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
    dirs = ".config .var .local/share/gnome-shell .local/share/fonts \
    .local/share/backgrounds .local/share/applications .local/share/icons .local/share/keyrings snap".split()
    dirs[:] = [f"{home_dir}/" + d for d in dirs]
    os.popen(f'cp -Rpu {" ".join(dirs)} {repo_location}')


def get_apt_packages():
    # Apt repos and keys
    run_shell(f'cp -Rpu /etc/apt/sources.list.d/ {repo_location}')
    run_shell(f'cp -Rpu /etc/apt/sources.list {repo_location}')
    write_output('repo.keys', 'apt-key exportall')
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


def install_apt_packages():
    os.system(f'sudo cp -Rpu {repo_location}/source.list.d /etc/apt/sources.list.d/')
    os.system(f'sudo cp -Rpu {repo_location}/sources.list /etc/apt/sources.list ')
    os.system(f'sudo apt-key add {repo_location}/repo.keys')
    os.system(f'sudo xargs -a packageList.txt apt-get install --ignore-missing -y -q')


def restore_app_data():
    os.chdir(repo_location)
    subdirs = next(os.walk('.'))[1]
    subdirs.remove('sources.list.d')
    for dir in subdirs:
        run_shell(f'rsync --recursive {dir} {home_dir}/{dir}')


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
    write("snap.list", os.popen("snap list | awk '!/disabled/{print $1}' | awk '{if(NR>1)print}'").read())
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
    try:
        os.chdir(repo_location)
    except:
        load_repo(git_remote, username, password)
        try:
            os.chdir(repo_location)
        except:
            exit(1)
    step = 1
    install_apt_packages()
    with open(f'{repo_location}/flatpak.list', 'r') as file:
        for line in file.readlines():
            while line != '':
                run_shell(f'flatpak install flathub {line} -y --noninteractive')
    with open(f'{repo_location}/snap.list', 'r') as file:
        for line in file.readlines():
            while line != '':
                run_shell(f'sudo snap install {line} --classic')
    step = 2
    restore_app_data()
    run_shell("dconf load / < donf-backup.txt")
    step = 3

# load_repo('url', 'username', 'password')
