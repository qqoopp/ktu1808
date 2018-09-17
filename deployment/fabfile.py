#fab deploy:gateway

from getpass import getpass
from fabric.api import local, run, env, get, put, prompt, open_shell
from fabric.api import execute , roles
from fabric.api import task

env.user = 'osuser'
env.roledefs = {
    'gateway': ['pi@192.168.137.152'],
}

def remote_host():
    print("user : " + str(env.user))
    print("proxy gateway : " + str(env.gateway))

    if env.user == "osuser":
        env.user = prompt('Enter user name: ')
    env.password = getpass('Enter password: ')
    env.home_folder = '/tmp'
    run("pwd")

def upload_file():
    print("Checking remote disk space...")
    #run("df -h")
    default_local_path = "C:/iotschool/ktu1808/IOTServer/"
    default_remote_path = "~/"

    local_path = prompt("Enter the local path : default(" + default_local_path + ") :")
    remote_path = prompt("Enter the remote file path : default(" + default_remote_path + ") :")

    if local_path.strip() == "":
        local_path = default_local_path

    if remote_path.strip() == "":
        remote_path = default_remote_path

    put(remote_path=remote_path, local_path=local_path)
    run("ls %s" %remote_path)

def remote_cmd():
    strcmd = prompt("type cmd : ")
    run(strcmd)

def do_deploy():
    execute(remote_host)
    execute(upload_file)

def do_cmd():
    execute(remote_host)
    execute(remote_cmd)

@task
def deploy(rolename):
    execute(do_deploy, role=rolename)

@task
def remotecmd(rolename):
    execute(do_cmd, role=rolename)
