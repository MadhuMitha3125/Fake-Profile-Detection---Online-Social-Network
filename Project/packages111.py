import subprocess
import time
pip_commands=[
    "pip list",
    "python -m pip install --upgrade pip",
    "pip install seaborn",
    "pip install plotly",
    "pip install imagehash",
    "pip install opencv-python",
    "pip install flask",
    "pip install mysql-connector",
    "pip install cryptography",
    "pip install scikit-learn",
    "pip install scikit-image",

    "pip list",

    ]
print(
"""

░█████╗░██████╗░██╗░░░██╗
██╔══██╗██╔══██╗██║░░░██║
███████║██████╦╝██║░░░██║
██╔══██║██╔══██╗██║░░░██║
██║░░██║██████╦╝╚██████╔╝
╚═╝░░╚═╝╚═════╝░░╚═════╝░

                        -DEVELOPER
"""


    )
time.sleep(7)
for commands in pip_commands:
    if commands==pip_commands[0]:
        print("==============| YOUR PREVIOUS PIP LIST |=============")
    elif commands==pip_commands[7]:
        print("==========| YOUR INSTALLED PIP LIST  |===========")
    subprocess.run(commands,shell=True)
print("developer:\>abu")
#developed by abu>>developer

"""
THIS IS FOR PACKAGES INSTALLER
WRITE SINGLE LINE COMMAND TO DO EXECUTE MORE PIP COMMANDS


C:\>python packages.py

"""
