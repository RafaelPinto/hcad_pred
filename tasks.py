import os
from sys import platform

from dotenv import load_dotenv, find_dotenv

from invoke import task


# Set
ENV_NAME = 'hcad_pred'

# Get the SHELL from the environment variable
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
SHELL = os.environ.get("SHELL")

# https://github.com/pyinvoke/invoke/pull/407
if not SHELL:
    if platform == 'win32':
        SHELL = os.environ['COMSPEC']  # default win shell is cmd.exe
    else:
        SHELL = '/bin/bash'


# Environment

# Run this first
# conda env create --name hcad_pred --file .\environment.yml
# conda activate hcad_pred


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
