# Project Manager

# Introduction

This is a simple project manager that allows you to create projects and tasks. It's written in Python, and is divided in few simple scripts.

It helps you to import quickly your projects presets, and to automatically do some tasks.

# Installation

It's a simple Python script, so you need to install Python 3.6 or higher.

Then, you need to install the requirements:
```bash
pip3 install argparse
```

## Linux and Mac

Then put the script in your `HOME` directory, and add the following line in your `.bashrc` file (for Linux) or `.bash_profile` file (for Mac):

```bash
cp program-manager.py ~/pm.py
echo "alias pm='python3 ~/pm.py'" >> ~/.bashrc
# or
echo "alias pm='python3 ~/pm.py'" >> ~/.bash_profile
```

## Windows

For Windows, you need to add the script to your `PATH` environment variable.

# Usage

Arguments:
```bash
usage: pm.py [-h] [-tp] [-g {html,java,python,c,javascript,processing}] [-utp] [-git] [-utils] [-processing-import] [-processing-delete] [-clear-folder]
```

## Options

<!-- 
 -h, --help            show this help message and exit
  -tp, --move-last-downloads
                        Move the last downloads to the Desktop
  -g {html,java,python,c,javascript,processing}, --generate {html,java,python,c,javascript,processing}
                        Generate a file in the specified language
  -utp, --undo-move-last-downloads
                        Undo the last move of the last downloads
  -git                  Initialize a git repository and initialize the first commit
  -utils                Add utils folder to the project
  -processing-import    Add the import of the processing library to the project
  -processing-delete    Delete the processing library from the project
  -clear-folder         Clear the folder

Make a table with the options (commands are between "`")

 -->

| Command | Description |
| --- | --- |
| `-h`, `--help` | Show the help message |
| `-tp`, `--move-last-downloads` | Move the last downloads to the Desktop |
| `-g {html,java,python,c,javascript,processing}`, `--generate {html,java,python,c,javascript,processing}` | Generate a file in the specified language |
| `-utp`, `--undo-move-last-downloads` | Undo the last move of the last downloads |
| `-git` | Initialize a git repository and initialize the first commit |
| `-utils` | Add utils folder to the project |
| `-processing-import` | Add the import of the processing library to the project |
| `-processing-delete` | Delete the processing library from the project |
| `-clear-folder` | Clear the folder |

