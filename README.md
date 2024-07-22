# Project Manager

# Introduction

This is a simple project manager that allows you to create projects and tasks. It's written in Python, and is divided in few simple scripts.

It helps you to import quickly your projects presets, and to automatically do some tasks.

# TODO

- [ ] Add documentation for the program itself
- [ ] Add documentation for programming languages
- [ ] Add a tool to easily add presets (with a GUI ?) (maybe with a web interface ?)
- [ ] Reconfigure the program with a GUI (Django ?)
- [ ] Add presets for other languages
- [ ] Cross-platform support (Nearly done)
- [ ] Add tool downloaders (for example, download LaTeX, Processing, etc.) (maybe with a web interface as well ?)

Globally : 

- [ ] Add a web interface to manage the program


# Installation

It's a simple Python script, so you need to install Python 3.6 or higher.

Then, you need to install the requirements:
```bash
pip3 install argparse
pip3 install parse
```

First of all, you need to clone the repository:
```bash
git clone https://gitlab.isima.fr/rovandemer/project-manager.git
```

## Linux and Mac

Add the following line in your `.bashrc` file (for Linux) or `.bash_profile` file (for Mac):

```bash
echo "alias pm='python3 /PATH/TO/program-manager.py'" >> ~/.bashrc
# or
echo "alias pm='python3 /PATH/TO/program-manager.py'" >> ~/.bash_profile

# Source the file
source ~/.bashrc
# or
source ~/.bash_profile
```

## Windows

For Windows, you need to add the script to your `PATH` environment variable.

# Usage

Arguments:
```bash
usage: program-manager.py [-h] [-tp] [-g {[languages]}] [-utp] [--git] [--utils]
                          [--processing-import] [--processing-delete] [--clear-folder] [-lg]
                          [--pandoc-compile FILE_NAME] [-ctp]
```

## Options

<!-- 
 options:
  -h, --help            show this help message and exit
  -tp, --move-last-downloads
                        Move the last downloads to the Desktop
  -g {processing,latex,java,html,c}, --generate {processing,latex,java,html,c}
                        Generate a file in the specified language
  -utp, --undo-move-last-downloads
                        Undo the last move of the last downloads
  --git                 Initialize a git repository and initialize the first commit
  --utils               Add utils folder to the project
  --processing-import   Add the import of the processing library to the project
  --processing-delete   Delete the processing library from the project
  --clear-folder        Clear the folder
  -lg, --list-generators
                        List the available generators
  --pandoc-compile PANDOC_COMPILE
                        Compile the markdown file to pdf

Make a table with the options (commands are between "`")

 -->

| Command | Description |
| --- | --- |
| `-h`, `--help` | Show the help message |
| `-tp`, `--move-last-downloads` | Move the last downloads to the Desktop |
| `-g {[languages]}`, `--generate {[languages]}` | Generate a file in the specified language |
| `-utp`, `--undo-move-last-downloads` | Undo the last move of the last downloads |
| `--git` | Initialize a git repository and initialize the first commit |
| `--utils` | Add utils folder to the project |
| `--processing-import` | Add the import of the processing library to the project |
| `--processing-delete` | Delete the processing library from the project |
| `--clear-folder` | Clear the folder |
| `-lg`, `--list-generators` | List the available generators |
| `--pandoc-compile PANDOC_COMPILE` | Compile the markdown file to pdf |
| `-ctp`, `--clear-tp` | Clear the TP log file |


## Personalization

You can personalize the script by adding your own presets in the `presets` folder :

- The `presets` contains different folders, each one containing a programming language.
- In each of them, you can add a folder with the name of the preset, and inside it, you can add the files you want to add to the project.
  - You can add a `DESC.txt` file to add a description of the preset.
  - You can name some folders / files with the following syntax: `NAMEX`, where `X` is a number. The script will replace `X` by a string that you will enter when you will create the project.

### Example

Let's say you want to create a preset for a `C` project, with a `main.c` file, and a `utils` folder. You can create a folder `c` in the `presets` folder, and inside it, a folder `my-preset`, with the following structure:

```
presets
└───c
    └───my-preset
        │   main.c
        │   DESC.txt (optional)
        │
        └───utils
```

In the `DESC.txt` file, you can add a description of the preset. In the `main.c` file, you can add code, and in the `utils` folder, you can add some files that you want to add to each project created with this preset.

Then, to generate your preset, you can run the following command :

```bash
pm -g c
```

Command prompt will ask you to choose a preset, and done ! You have a new project with your working files.

