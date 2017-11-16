## Getting Started

These instructions assume that you are running Linux. If you are a developer running Windows or MacOS, please feel free to open an [issue](https://github.com/jmwright/cqcad/issues) and ask that these instructions be updated for those operating systems. Pull requests are also welcome, and can be submitted for these docs as well.

### Before Starting
It is highly recommended that you set up a [virtual environment](https://docs.python.org/3/tutorial/venv.html) for CQCad development. Once you have activated the virtual environment you can follow the procedure below to get the app up and running.

### Clone
Clone this repository to your local system.
```bash
git clone --recursive https://github.com/jmwright/cqcad.git
```
Notice the `recursive` option in the line below. Extensions and layouts are often included in this repository as git submodules. Without the recursive clone you will not get everything that is needed for the applicaiton to run properly. Downloading the zip of the repo from GitHub will not provide you with all the submodules either.

### Install Pre-Requisites
Change into the `cqcad` root directory and install the pre-requisite Python packages.
```bash
cd cqcad/
pip3 install -r requirements.txt
```
PyQt5 is one of the pre-requisites installed, and is the framework used to create the GUI portion of CQCad.

### Run CQCad
`cqcad/cqcad/cqcad.py` is the entry point for the application.
```bash
cd cqcad/
./cqcad.py
```

### Looking Around
- The main application window is set up by `cqcad/cqcad/CQCadWindow`.
- Other widgets for the user interface are in `cqcad/cqcad/components`. These include the script editor and 3D view widgets.
- Items such as images and icons for buttons are stored in `cqcad/cqcad/content`.
- There is a `cqcad/cqcad/tests` directory, and it is asked that all new contributions come with the appropriate tests.
- The `cqcad/cqcad/layouts` and `cqcad/cqcad/extensions` directories hold dynamically loaded modules that extend the core GUI.
- The `cqcad/cqcad/collections` directory holds user selected collections of parts, assemblies and operations.
