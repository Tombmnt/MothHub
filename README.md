# MothHub
Raspberry Pi software suite to run a data collection hub on a moth sailboat.

## Installing the suite
You will need python, at least version 3.7 to run this suite.

1) Clone the repo to your computer.
2) Open a comand line in the projet's folder (../MothHub/)
3) Create a virtual environment for python in the .env folder.

    Windows:
    > py -m venv .env
    
    Linux:
    > python3 -m venv .env
4) Activate the environment. (You're going to have to do this every time you open a command prompt in the project folder)

    Windows (cmd):
    > .env\Scripts\activate.bat

    Windows (PowerShell):
    > .\.env\Scripts\Activate.ps1

    Linux:
    > source my-project-env/bin/activate
5) Installe the requirements.

    For a dev setup, able to run the mock modules:
    
    Windows:
    > py -m pip install -r dev_requirements.txt

    Linux:
    > python3 -m pip install -r dev_requirements.txt

    On the Pi or for a headless setup, only able to run the real suite (only linux):
    > python3 -m pip install -r requirements.txt

6) Enjoy!

## Running the suite
To run the full hub on the Pi manually, use:
> ./MothHub.sh

To run the mock setup on windows, use:
> run_mock_setup.bat

To run the mock setup on linux, use: (Note: this will NOT work on the Pi as it requires a display and a desktop.)
> ./run_mock_setup.sh