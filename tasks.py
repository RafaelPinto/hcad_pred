from os import environ
from sys import platform

from invoke import task


# Set
ENV_NAME = 'hcad_pred'

# Set the runing shell to PowerShell
# https://github.com/pyinvoke/invoke/pull/407
if False:
    SHELL = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'
else:
    # default was cmd.exe
    if platform == 'win32':
        SHELL = environ['COMSPEC']
    else:
        SHELL = '/bin/bash'


# Environment

# Run this first
# conda env create --name my_env_name --file .\environment.yml
# conda activate


@task
def env_set_jupyter(c):
    print('Setting up jupyter kernel')
    c.run(
        f"ipython kernel install --name {ENV_NAME} --display-name {ENV_NAME} --sys-prefix")
    print('Adding nbextensions')
    c.run("jupyter nbextensions_configurator enable --user")
    print('Done!')


@task
def env_to_freeze(c):
    c.run(f"conda env export --name {ENV_NAME} --file environment_to_freeze.yml",
          shell=SHELL)
    print('Exported freeze environment to: environment_to_freeze.yml')


@task
def env_update(c):
    c.run(f"conda env update --name {ENV_NAME} --file environment.yml --prune",
          shell=SHELL)


@task
def env_remove(c):
    c.run(f"conda remove --name {ENV_NAME} --all",
          shell=SHELL)


# Data

@task
def download_data(c):
    c.run("python src/data/download_hcad_data.py", shell=SHELL)


@task
def select_data(c):
    c.run("python src/data/process_select_data.py", shell=SHELL)
