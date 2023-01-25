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

PROGRAMMING_LANGUAGES = {
    "python",
    "c",
    "java",
    "javascript",
    "html"
}


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

        self.environment = ENVIRONMENTS.get(self.language, {})

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

            isDir = os.path.isdir(s)

            # If the file / directory to copy is called "NAMEX.extension" for a file or "NAMEX" for a directory,
            # Ask the user if he wants to change the name
            # (extension could be whatever, it doesn't matter)
            # The X is a number, it's the Xth file / directory with the same name
            # Every file / directory with the same X will have the same name
            itemName = item.split(".")[0]
            if itemName.startswith("NAME") and itemName[4:].isdigit():

                if not itemName[4:] in names.keys():

                    # Ask the user to change the name
                    itemType = "directory" if isDir else "file"
                    newName = input(
                        f"Enter a new name for {item} ({itemType}) : ")
                    t = os.path.join(target, newName + "." +
                                     item.split(".")[1])

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

    def generate_file(self, language: str, name: str = "default"):
        """
        Generate a file in the specified language
        """

        # Get directory to clone
        source = currentPath + "/presets/{0}/{1}/".format(language, name)

        # Copy the files
        self.copy_recursive(source, "./")


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
        choices=PROGRAMMING_LANGUAGES
    )

    parser.add_argument(
        "-utp",
        "--undo-move-last-downloads",
        dest="utp",
        action="store_true",
        help="Undo the last move of the last downloads"
    )

    parser.add_argument(
        "-git",
        dest="git",
        action="store_true",
        help="Initialize a git repository and initialize the first commit"
    )

    parser.add_argument(
        "-utils",
        dest="utils",
        action="store_true",
        help="Add utils folder to the project"
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

            elif arg == "g":

                # Generate files
                program_manager.generate_file(value)

            elif arg == "utp":

                # Undo the last move of the last downloads
                program_manager.undo_move_last_downloads()

            elif arg == "git":

                # Initialize git repository
                os.system("git init")
                os.system("git add .")
                os.system("git commit -m 'Project Initialisation'")

            elif arg == "utils":

                # Create the utils folder
                os.mkdir("utils")
                
    if not used:
        print("No argument used, use -h to see the help")
        sys.exit(1)

    print("Done")
