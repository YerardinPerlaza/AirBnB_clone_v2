#!/usr/bin/python3
# Fabric script  (based on the file 1-pack_web_static.py) that
# distributes an archive to your web servers
from fabric.api import *
from os import path
env.host = ['35.190.183.78', '34.226.194.149']


def do_deploy(archive_path):
    '''Distributes an archive to your web servers'''
    if len(archive_path) == 0 or not path.exists(archive_path):
        print("{} doesn’t exist".format(archive_path))
        return False
    file = archive_path.split('/')[1]
    name_of_file = file.split('.')[0]
    folder_web = "/data/web_static/releases/{}".format(name_of_file)
    current = "/data/web_static/current"
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf {}/".format(folder_web)).failed is True:
        return False
    if run("mkdir -p {}/".format(folder_web)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C {}/".format(file, folder_web)).failed is True:
        return False
    if run("rm -rf /tmp/{}".format(file)).failed is True:
        return False
    if run("mv {}/web_static/* {}/".
            format(folder_web, folder_web)).failed is True:
        return False
    if run("rm -rf {}/web_static".format(folder_web)).failed is True:
        return False
    if run("rm -rf {}".format(current)).failed is True:
        return False
    if run("ln -s {}/ {}".format(folder_web, current)).failed is True:
        return False
    return True
