import os
import sys
import apt

repo_location = sys.argv[1]


def install_apt_packages():
    os.system(f'sudo cp -Rp {repo_location}/sources.list.d /etc/apt/')
    os.system(f'sudo cp -Rp {repo_location}/sources.list /etc/apt/sources.list ')
    os.system(f'sudo apt-key add {repo_location}/repo.keys')
    os.system(f'sudo apt update')
    packages = apt.Cache()
    available = []
    with open(f'{repo_location}/packageList.txt', 'r') as file:
        for p in file.readlines():
            p = p.strip()
            if p in packages.keys() and not packages[p].is_inst_broken:
                available.append(p.strip())
    available = " ".join(available)
    os.system(f'sudo apt-get install {available} --ignore-missing -y -q')


def install_snaps():
    with open(f'{repo_location}/snap.list', 'r') as file:
        for line in file.readlines():
            os.system(f'sudo snap install {line.strip()} --classic')


install_apt_packages()
install_snaps()
