import os
import sys

repo_location = sys.argv[1]


def install_apt_packages():
    os.system(f'sudo cp -Rp {repo_location}/sources.list.d /etc/apt/')
    os.system(f'sudo cp -Rp {repo_location}/sources.list /etc/apt/sources.list ')
    os.system(f'sudo apt-key add {repo_location}/repo.keys')
    os.system(f'sudo apt update')
    os.system(f'sudo xargs -a {repo_location}/packageList.txt apt-get install --ignore-missing -y -q')


def install_snaps():
    with open(f'{repo_location}/snap.list', 'r') as file:
        for line in file.readlines():
            os.system(f'sudo snap install {line.strip()} --classic')


install_apt_packages()
install_snaps()
