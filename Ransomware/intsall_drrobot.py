import os
import shutil
import platform

def logo():
    logo = """
    \033[91m
                       ⠀⠀⠀⠀⠀⣀⣀⣀⣀⣠⣤⣤⣄⣀⣀⣀⣀⠀⠀⠀⠀⠀
                       ⢀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⡀
                       ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
                       ⣿⣿⣿⡿⠛⠉⠉⠙⠿⣿⣿⣿⣿⠿⠋⠉⠉⠛⢿⣿⣿⣿
                       ⣿⣿⣿⣶⣿⣿⣿⣦⠀⢘⣿⣿⡃⠀⣴⣿⣿⣿⣶⣿⣿⣿
                       ⣿⣿⣿⣏⠉⠀⠈⣙⣿⣿⣿⣿⣿⣿⣋⠁⠀⠉⣹⣿⣿⣿
                       ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                       ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                       ⢸⣿⣿⣎⠻⣿⣿⣿⣿⡿⠋⠙⢿⣿⣿⣿⣿⠟⣱⣿⣿⡇
                       ⠀⢿⣿⣿⣧⠀⠉⠉⠉⠀⢀⡀⠀⠉⠉⠉⠀⣼⣿⣿⡿⠀
⠀                       ⠈⢻⣿⣿⣷⣶⣶⣶⣶⣿⣿⣶⣶⣶⣶⣾⣿⣿⡟⠁⠀
⠀                       ⠀⠀⠹⣿⣿⣿⣿⣿⣿⠉⠉⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀
   ⠀⠀⠀                    ⠀⠈⠻⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
                       ⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣦⣴⡿⠟⠋⠀⠀⠀⠀⠀⠀⠀

    .------.------.------.     .------.------.------.------.------.
    |D.--. |R.--. |..--. |.-.  |R.--. |O.--. |B.--. |O.--. |T.--. |
    | :/\: | :(): | :(): ((5)) | :(): | :/\: | :(): | :/\: | :/\: |
    | (__) | ()() | ()() |'-.-.| ()() | :\/: | ()() | :\/: | (__) |
    | '--'D| '--'R| '--'.| ((1)| '--'R| '--'O| '--'B| '--'O| '--'T|
    `------`------`------'  '-'`------`------`------`------`------'
"""

    # ANSI escape sequence for red color
    red_color = "\u001b[31m"
    # ANSI escape sequence to reset color to default
    reset_color = "\u001b[0m"

    # Add color formatting to the logo
    colored_logo = red_color + logo + reset_color

    print("\033[91m" + logo + "\033[0m")
    
def get_platform():
    system = platform.system()
    if system == 'Linux':
        return 'linux'
    elif system == 'Darwin':
        return 'macos'
    elif system == 'Windows':
        return 'windows'
    else:
        return None

def install_hashtag():
    # Define the paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    drrobot_script = os.path.join(current_dir, 'drrobot.py')
    platform_name = get_platform()

    if platform_name is None:
        print("Unsupported operating system.")
        return

    if platform_name == 'linux':
        destination_dir = '/usr/local/bin'
    elif platform_name == 'macos':
        destination_dir = '/usr/local/bin'
    elif platform_name == 'windows':
        destination_dir = os.path.join(os.environ['ProgramFiles'], 'Drrobot')

    destination_file = os.path.join(destination_dir, 'drrobot')

    try:
        # Copy the hashtag.py script to the destination directory
        shutil.copy2(drrobot_script, destination_file)

        # Set the copied file's permissions to be executable (Linux and macOS)
        if platform_name in ['linux', 'macos']:
            os.chmod(destination_file, 0o755)

        print("Installation complete. You can now use 'drrobot' as a command.")
    except Exception as e:
        print(f"An error occurred during installation: {str(e)}")

if __name__ == "__main__":
    logo()
    print("Welcome to the Dr. Robot installer!")
    install_hashtag()



