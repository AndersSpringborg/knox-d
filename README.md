# MI-Graph

MI-graph (Machine learning graph) is a pip module supporting various configurations for knowledge extraction.

## Usage

To download the module run the following command:

```bash
pip install --extra-index-url https://repos.knox.cs.aau.dk knox-mi-graph
```

### Demo

```bash
python -c "from mi_graph.util import cli; cli()" file -f examples/use_this_grundfos_manual.json --visualisation
```

### List of commandline arguments

MI-Graph supports the following arguments.

```
usage: mi-graph [-h] [-v] [--file] [--visualisation] {file,flask}

positional arguments:
  {file,flask}     Choose if you want to process a file, or run the program as a rest api

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show program's version number and exit
  --file , -f      Please indicate the json file you want to process.
  --visualisation  This option visualizes the graph with plotly, after the script has run
```

### Run under development

There is two alternatives to run the program when developing:

#### Option 1

```
# RdfLib prints their version, because its run from the cli, and not a script
python -c "from mi_graph.util import cli; cli()"
```

#### Option 2

Wrap option 1 into a Python file which then can be executed:

```
from mi_graph.util import cli

cli()

```

Now run the file:

```
python <file path>
```

## Setup: virtualenv environment

Follow [this guide](https://wiki.knox.cs.aau.dk/en/SettingUpPython) to setup a virtual environment for development

## Setup: conda environment

Install conda from [their website](https://docs.anaconda.com/anaconda/install/). (We recommend the mini version /
miniconda)

Initialize the environment with:

- `conda create --name knox-env python=3.8`
- `activate knox-env`
- `pip install -r requirements.txt`

## Test dependencies

For developers, you also need to install the test requirements:

- `pip install -r tests/requirements.txt`

## Pylint

Before you make a pull request to master, you should run branch though pylint.

you can use `pylint_runner` to run all folders in the solution, or with pylint like so Run:

```bash
pip install pylint
```

And then

```bash
pylint folder/
```

## Build module

You cannot be in a virtual environment, when building

- `python3 setup.py sdist bdist_wheel`

Output artifacts:

- `knox-mi-graph-1.0.2.tar.gz`
- `knox_mi_graph-1.0.2-py3-none-any.whl`

---
When the command is finished, it outputs a set of artifacts in a `dist` folder. Copy the artifacts to the knox
server `knox-master02.srv.aau.dk` in the following path: `/srv/web/repos.knox.cs.aau.dk/https/`

The final result after completing the steps above:

- `knox-master02.srv.aau.dk/srv/web/repos.knox.cs.aau.dk/https/knox-mi-graph-1.0.2.tar.gz`
- `knox-master02.srv.aau.dk/srv/web/repos.knox.cs.aau.dk/https/knox_mi_graph-1.0.2-py3-none-any.whl`