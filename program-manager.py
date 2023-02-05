import os
import argparse
import sys
import logging
import parse
import shutil

# Get the current path
currentPath = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(
    filename=f'{currentPath}/moves.log',
    filemode='a',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

ENVIRONMENTS = {
    "English": {
        "Desktop": "Desktop",
        "Documents": "Documents",
        "Downloads": "Downloads"
    },
    "Spanish": {
        "Desktop": "Escritorio",
        "Documents": "Documentos",
        "Downloads": "Descargas"
    },
    "French": {
        "Desktop": "Bureau",
        "Documents": "Documents",
        "Downloads": "Téléchargements"
    }
}

LANGUAGES = {
    "en_US.UTF-8": "English",
    "es_ES.UTF-8": "Spanish",
    "fr_FR.UTF-8": "French",
    "en_GB.UTF-8": "English"
}

PROGRAMMING_LANGUAGES = {}

# List folders from presets folder : its the languages
# For each language, list folders from presets folder : its the different environments

# List languages
for language in os.listdir(f"{currentPath}/presets"):

    # List environments
    for environment in os.listdir(f"{currentPath}/presets/{language}"):

        # Check if the environment is already in the dictionary
        if not language in PROGRAMMING_LANGUAGES.keys():
            PROGRAMMING_LANGUAGES[language] = {}

        # Add the environment to the dictionary
        # Check first if there is "DESC.txt" file, if so, use it as description
        description = "No description"

        if os.path.exists(f"{currentPath}/presets/{language}/{environment}/DESC.txt"):
            with open(f"{currentPath}/presets/{language}/{environment}/DESC.txt", "r") as f:
                description = f.read()

        PROGRAMMING_LANGUAGES[language][environment] = {
            "name": environment, "path": f"{currentPath}/presets/{language}/{environment}", "description": description}


class ProgramManager:
    """
    Class that handles the programs
    """

    def __init__(self):
        """
        Constructor
        """

        self.language = ""
        self.environment = {}
        self.homePath = os.path.expanduser("~")

        self.set_language()
        self.set_environment()

    def set_language(self) -> str:
        """
        Returns the language of the system
        """

        self.language = LANGUAGES.get(os.environ.get("LANG"), "Unknown")

    def set_environment(self) -> dict:
        """
        Returns the environment of the system
        """

        self.environment = ENVIRONMENTS.get(
            self.language, {"Documents": "Documents"})

    def newestFile(self, path: str) -> str:
        files = os.listdir(path)

        paths = [os.path.join(path, basename) for basename in files]

        return max(paths, key=os.path.getctime)

    def move_last_downloads(self):
        """
        Move the last downloads to the Desktop
        """

        # Get the paths
        downloads = "{0}/{1}/".format(
            self.homePath,
            self.environment.get("Downloads")
        )

        if downloads:
            # Get the last download
            newestFile = self.newestFile(downloads)

            # Move the file to the folder where the user is
            target = "./{0}".format(newestFile.split("/")[-1])
            os.rename(newestFile, target)

            logging.info(
                "[{0}]->[{1}]".format(
                    newestFile,
                    target
                )
            )

            print(
                f"Moved \x1b[1;32m{newestFile}\x1b[0m to \x1b[1;32m{target}\x1b[0m")

        else:
            print("The environment is not set")
            sys.exit(1)

    def undo_move_last_downloads(self):
        """
        Undo the last move of the last downloads
        """

        # Check if the log file exists
        if os.path.exists(f"{currentPath}/moves.log"):

            # Check if the log file is empty
            if os.stat(f"{currentPath}/moves.log").st_size == 0:
                print("The log file is empty")
                sys.exit(1)

            # Get the last line
            last_line_non_parsed = open(
                f"{currentPath}/moves.log").readlines()[-1].strip()
            # Line is like : 2023-01-01 00:00:00,000 - [path1]->[path2]
            last_line_non_parsed = last_line_non_parsed.split(" - ")[1]

            # Get the last line
            last_line = parse.parse(
                "[{0}]->[{1}]",
                last_line_non_parsed
            )

            # Move the file to the original folder
            os.rename(last_line[1], last_line[0])

            # Delete the last line
            with open(f"{currentPath}/moves.log", "r") as f:
                lines = f.readlines()

            with open(f"{currentPath}/moves.log", "w") as f:
                f.writelines(lines[:-1])

    def copy_recursive(self, source: str, target: str, names: dict = {}):
        """
        Copy everything recursively from source to target
        """

        # Check if the source exists
        for item in os.listdir(source):

            # Get the paths
            s = os.path.join(source, item)
            t = os.path.join(target, item)

            if s.startswith("."):
                continue

            # Check if exists
            if os.path.exists(t):
                print(f"\x1b[3;34m{t} already exists\x1b[0m")
                continue

            isDir = os.path.isdir(s)

            # If the file / directory to copy is called "NAMEX.extension" for a file or "NAMEX" for a directory,
            # Ask the user if he wants to change the name
            # (extension could be whatever, it doesn't matter)
            # The X is a number, it's the Xth file / directory with the same name
            # Every file / directory with the same X will have the same name
            itemName = item.split(".")[0]

            # Check for DESC.txt
            if itemName.startswith("DESC"):
                continue

            # Check if the name is NAMEX
            if itemName.startswith("NAME") and itemName[4:].isdigit():

                if not itemName[4:] in names.keys():

                    # Ask the user to change the name
                    itemType = "directory" if isDir else "file"

                    newName = ""

                    while newName == "":

                        newName = input(
                            f"Enter a new name for {item} ({itemType}) : ")

                        if newName == "":
                            print("\x1b[3;34mName cannot be empty\x1b[0m")

                    # Check if item.split(".")[1] exists
                    if len(item.split(".")) > 1:
                        t = os.path.join(
                            target, newName + "." + item.split(".")[1])
                    else:
                        t = os.path.join(target, newName)

                    names[itemName[4:]] = newName

                else:

                    t = os.path.join(
                        target, names[itemName[4:]] + "." + item.split(".")[1])

            # Check if it is a directory
            if isDir:

                # Create the directory
                os.mkdir(t)
                self.copy_recursive(s, t)

            else:
                # Check if file exists
                i = 1
                while os.path.exists(t):
                    t = os.path.join(target, item.split(
                        ".")[0] + f"({i})." + item.split(".")[1])
                    i += 1

                # Copy the file
                shutil.copy2(s, t)

    def generate_file(self, language: str, name: str = "default", path: str = "./"):
        """
        Generate a file in the specified language
        """

        # Get directory to clone
        source = currentPath + "/presets/{0}/{1}/".format(language, name)

        # Copy the files
        self.copy_recursive(source, path)

    def import_processing_dependencies(self):
        """
        Import the processing dependencies
        """

        # Create code folder
        # Check if the folder exists
        if not os.path.exists("./code"):
            os.mkdir("./code")

        # List folders in Processing/libraries
        documentsPath = self.environment["Documents"]

        folderPath = f"{self.homePath}/{documentsPath}/Processing/libraries"

        libraries = os.listdir(folderPath)

        # Copy the libraries
        for library in libraries:

            if library.startswith("."):
                continue

            folder = f"{folderPath}/{library}"

            # If folder
            print(f"Copying {folder}/library/ to ./code/...")
            self.copy_recursive(f"{folder}/library/", "./code")

    def clear_folder(self, folder: str):
        """
        Clear a folder
        """

        # Check if the folder exists
        if not os.path.exists(folder):
            print(f"{folder} doesn't exist")
            return

        # Check if the folder is empty
        if len(os.listdir(folder)) == 0:
            print(f"{folder} is already empty")
            return

        # Clear the folder
        for item in os.listdir(folder):
            path = os.path.join(folder, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    def compile_markdown_to_pdf(self, file: str):
        """
        Compile a markdown file to pdf
        """

        # Check if the file exists
        if not os.path.exists(file):
            print(f"\x1b[3;31m{file} doesn't exist\x1b[0m")
            exit()

        # Check if the file is a markdown file
        if not file.endswith(".md") or file.startswith("."):
            print(f"\x1b[3;31m{file} is not a markdown file\x1b[0m")
            exit()

        # Check if listings-setup.tex exists at HOME
        if not os.path.exists(f"{self.homePath}/listings-setup.tex"):
            print("\x1b[3;31mlistings-setup.tex doesn't exist at HOME\x1b[0m")
            # Create the file
            self.generate_file("latex", "listings-setup", self.homePath)

        # Compile the file
        # Base command : pandoc -f markdown -t pdf --mathjax --table-of-contents -o "rapport.pdf" --listings -H ./listings-setup.tex --pdf-engine=xelatex "tonmarkdown.md"
        os.system(
            f"pandoc -f markdown -t pdf --mathjax --table-of-contents -o \"{file.split('.')[0]}.pdf\" --listings -H {self.homePath}/listings-setup.tex --pdf-engine=xelatex \"{file}\"")

    def clear_tp_log(self):
        """ 
        Clear the tp (moves.log) log in the program folder
        """

        # Check if the file exists
        if not os.path.exists(f"{currentPath}/moves.log"):
            print("\x1b[3;31mFile moves.log doesn't exist\x1b[0m")
            return

        # Clear the file
        open(f"{currentPath}/moves.log", "w").close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-tp',
        '--move-last-downloads',
        dest='tp',
        action='store_true',
        help="Move the last downloads to the Desktop"
    )

    parser.add_argument(
        '-g',
        '--generate',
        dest='g',
        action='store',
        help="Generate a file in the specified language",
        choices=PROGRAMMING_LANGUAGES.keys()
    )

    parser.add_argument(
        "-utp",
        "--undo-move-last-downloads",
        dest="utp",
        action="store_true",
        help="Undo the last move of the last downloads"
    )

    parser.add_argument(
        "--git",
        dest="git",
        action="store_true",
        help="Initialize a git repository and initialize the first commit"
    )

    parser.add_argument(
        "--utils",
        dest="utils",
        action="store_true",
        help="Add utils folder to the project"
    )

    parser.add_argument(
        "--processing-import",
        dest="processing_import",
        action="store_true",
        help="Add the import of the processing library to the project"
    )

    parser.add_argument(
        "--processing-delete",
        dest="processing_delete",
        action="store_true",
        help="Delete the processing library from the project"
    )

    parser.add_argument(
        "--clear-folder",
        dest="clear_folder",
        action="store_true",
        help="Clear the folder"
    )

    parser.add_argument(
        "-lg",
        "--list-generators",
        dest="lg",
        action="store_true",
        help="List the available generators"
    )

    parser.add_argument(
        "--pandoc-compile",
        dest="pandoc_compile",
        action="store",
        help="Compile the markdown file to pdf"
    )

    parser.add_argument(
        "-ctp",
        "--clear-tp",
        dest="ctp",
        action="store_true",
        help="Clear the TP log file"
    )

    args = parser.parse_args()

    # Create a ProgramManager object
    program_manager = ProgramManager()

    # Loop through the arguments
    used = False

    for arg in vars(args):
        value = getattr(args, arg)

        if value:

            used = True

            if arg == "tp":
                program_manager.move_last_downloads()

                print(
                    "\x1b[33m[+] \x1b[39mThe last downloads have been moved from the Downloads folder\x1b[39m")

            elif arg == "g":

                # Ask the user for the environment
                print(f"Available Environments for {value} :")

                availableEnvironments = PROGRAMMING_LANGUAGES[value].keys()

                for i, environment in enumerate(availableEnvironments):
                    print(f"\t\x1b[33m[{i}] - {environment}\x1b[39m")

                    # Check if the environment has a description
                    if "description" in PROGRAMMING_LANGUAGES[value][environment]:
                        print(
                            f"\t\t\x1b[34m{PROGRAMMING_LANGUAGES[value][environment]['description']}\x1b[39m")

                # Get the environment
                userInput = input(
                    "\n\x1b[32mChoose an Environment : (Default 0) \x1b[39m")

                choice = 0

                try:
                    choice = int(userInput)
                except:
                    pass

                if not choice in range(len(availableEnvironments)):
                    choice = 0
                    print(
                        "\n\x1b[31m\t[!]\x1b[39m Invalid choice, defaulting to 0")

                # Get the environment
                environment = list(availableEnvironments)[choice]

                print(f"\n\x1b[33mEnvironment : {environment}\x1b[39m")

                # Generate files
                program_manager.generate_file(value, environment)

                print(
                    "\x1b[33m[+] \x1b[39mThe files have been generated\x1b[39m")

            elif arg == "utp":

                # Undo the last move of the last downloads
                program_manager.undo_move_last_downloads()

                print(
                    "\x1b[33m[+] \x1b[39mThe last downloads have been moved back to the Downloads folder\x1b[39m")

            elif arg == "git":

                # Initialize git repository
                os.system("git init")
                os.system("git add .")
                os.system("git commit -m 'Project Initialisation'")

                print(
                    "\x1b[33m[+] \x1b[39mThe git repository has been initialized\x1b[39m")

            elif arg == "utils":

                # Create the utils folder
                os.mkdir("utils")

                print(
                    "\x1b[33m[+] \x1b[39mThe utils folder has been created\x1b[39m")

            elif arg == "processing_import":

                program_manager.import_processing_dependencies()

                print(
                    "\x1b[33m[+] \x1b[39mThe processing library has been imported to the project")

            elif arg == "clear_folder":

                program_manager.clear_folder()

                print("\x1b[33m[+] \x1b[39mThe folder has been cleared\x1b[39m")

            elif arg == "processing_delete":

                program_manager.clear_folder("code")

                print(
                    "\x1b[33m[+] \x1b[39mThe processing library has been deleted from the project")

            elif arg == "lg":

                # List the available generators
                for language in PROGRAMMING_LANGUAGES:
                    print(f"-> \x1b[33m{language}\x1b[39m")

                    for environment in PROGRAMMING_LANGUAGES[language]:
                        print(f"\t=> \x1b[34m{environment}\x1b[39m")

                        # Check if the environment has a description
                        if "description" in PROGRAMMING_LANGUAGES[language][environment]:
                            print(
                                f"\t\t\x1b[35m{PROGRAMMING_LANGUAGES[language][environment]['description']}\x1b[39m")

            elif arg == "pandoc_compile":

                program_manager.compile_markdown_to_pdf(value)

                print(
                    "\x1b[33m[+] \x1b[39mThe markdown file has been compiled to pdf\x1b[39m")

            elif arg == "ctp":

                program_manager.clear_tp_log()

                print(
                    "\x1b[33m[+] \x1b[39mThe TP log file has been cleared\x1b[39m")

    if not used:
        print("No argument used, use -h to see the help")
        sys.exit(1)

    print("\x1b[32m[+] Done\x1b[39m")
