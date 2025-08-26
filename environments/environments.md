---
kernelspec:
  name: python3
  display_name: 'Python 3'
---
# Environments and environment managers

Broadly speaking, an *environment* (or *virtual environment*) is a collection of software programs that get used together for a common purpose. In a scientific context, this can mean the software packages needed to analyze a dataset or reproduce a published finding, or the dependencies needed to use a particular software tool.

*Environment managers* are tools that help create and manage multiple environments on a single computer, so that different projects can potentially use different versions of the same software. Typically, the desired environment is "activated" before use; when active, its programs are automatically preferred over other versions of the same programs. Some environment managers (but not all) also serve as *package installers*.

## Terminology

:::{glossary}
Package index (or package registry)
: A database of metadata about software packages (release date, version, author/maintainer, URL of source code, project website, *etc*).

Package repository
: A storehouse of software packages, from which they can be downloaded and installed.
:::

## `venv`: the Python built-in environment manager

:::{sidebar} Where do Python packages get installed?
When you're not using an environment manager, there will be two default locations where installed Python packages end up. The first is `/usr/lib/pythonX.Y/site-packages` (or on Debian-based systems like Ubuntu, `.../dist-packages`). This is where packages go if installed via `sudo pip install` (or on Linux, if installed using a system package manager like `apt` or `synaptic`).  The second location is `~/.local/lib/pythonX.Y/site-packages`, where `~` is the home folder of the logged-in user. For either of these locations, "X" and "Y" are major and minor version numbers, so if the system-level Python installation is version 3.12, the path will be `.../python3.12/...`.  On Windows, the path might be `C:\Users\%USERNAME%\AppData\Local\Programs\Python\PythonXY\Lib\site-packages` or so; you can find it with `python -m site --user-site`.

Nowadays, users can have many different versions of Python installed at once. Each Python version will have its own `site-packages` directory where installed packages go; this is what it means to have different *Python environments*. Each environment can have a different set of installed packages (and/or different installed package versions).
:::

The Python standard library includes a module called `venv`, which can be used to create virtual environments. It does this by creating a folder, and whenever the virtual environment is *active*, any Python package installations (done via `pip install`) go into that folder. Then, when you run Python and `import` a package, Python will look in that folder to find it.
When using `venv`, the environment folder for a project can go anywhere; it is conventional to place the folder *in the project directory* and give it a name like `.env`, `.venv` or `venv`.

To create a new virtual environment, run `python -m venv /path/to/env/folder`.  To *activate* an environment, run `source /path/to/env/folder/bin/activate`. Activating an environment puts its `bin/` folder at the front of the system's `PATH` variable, meaning it will be the first place the system looks for any invoked commands. That `bin/` folder will have a link to the Python executable that was used to create the virtual environment, so this ensures that `python` will get invoked from `/path/to/env/folder/bin/python` and will consequently use `/path/to/env/folder/lib/pythonX.Y/site-packages` as its source for importing modules at runtime, and also as the destination for installing new modules via `pip`. To deactivate a venv-managed virtual environment, run the command `deactivate`.

:::{important}
For the `venv` module to work, you need to already have Python installed, and whatever version of Python you used when creating the virtual environment will be the one used by that virtual environment.
:::

To specify a reproducible environment using `venv`, dependencies and their version constraints are listed in a text file (conventionally called `requirements.txt`) for use with `pip`. See [the pip documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/) for more info.


## Conda and Mamba

:::{sidebar} Mamba
`mamba` is a community-created rewrite of (most of) `conda`'s functionality. Its main advantage was much faster "solving" of environment specifications (i.e., finding a set of package versions that satisfy the compatibility constraints of all listed dependencies, and their dependencies, and their dependencies' dependencies...). Nowadays, `conda` uses the `mamba` solver internally, so the differences are much smaller and the choice is more based on personal taste.
:::

`conda` is a *language-agnostic* packaging tool and installer, meaning it can manage environments that include software written in other languages (C, FORTRAN, R, etc). This is important because often, such programs are *dependencies* of packages written in Python. `conda` also allows installing Python itself into conda-managed environments, meaning it's easier than with `venv` to use different Python versions for different projects.

Another difference between `conda` and `venv` is that by default, `conda` stores all conda-managed environments in one place: the `envs/` folder within the conda "base" folder (find it with `conda info --base`). Users must give each environment a unique *name*, however.

When installing packages with `conda`, it's important to choose the right *channel* (this is a conda-specific synonym for "registry" or "index" — in other words, a database of package metadata and version info). Versions of `conda` provided by Anaconda, Inc., use the "defaults" channel, which may incur licensing fees to use. The [Miniforge](https://conda-forge.org/download/) installer instead uses the "conda-forge" channel by default, which is gratis and community-maintained (although the hosting infrastructure is provided by Anaconda, Inc.). Other noteworthy channels are [bioconductor](https://bioconductor.org) (focused on bioinformatics packages) and [Scientific Python Nightly Wheels](https://anaconda.org/scientific-python-nightly-wheels/).

:::{sidebar} Changing env location with `conda`
Instead of specifying `--name` you may pass `--prefix /path/to/env/folder/env_name`, to store the environment in a non-default location (such as in the project directory). Doing this means you must use `source activate env_name` from `/path/to/env/folder`, instead of `conda activate env_name` (which could be run from anywhere).
:::

To specify a reproducible environment using `conda`, dependencies (and their version constraints) are written to a YAML file, conventionally named `environment.yaml`. This file can also include a name for the environment, which channel(s) to install packages from, and other metadata.

A third difference (already alluded to) is that conda is both an environment manager *and* a package installer; in other words, it performs the functions of both `venv` and `pip`. That said, it cannot completely replace `pip` in all cases, because not all Python packages are available from conda-compatible sources. In such cases, you can tell conda (in an `environment.yaml` file) which dependencies it should install via `pip` instead of from one of the conda-compatible channels.

## `uv`

`uv` is both a package installer and environment manager, with an empasis on managing environments for *projects*. This means that by default, `uv` writes dependency specifications to a `pyproject.toml` file rather than `requirements.txt` (like `pip`) or `environment.yaml` (like `conda`). By default, `uv` installs dependencies to a `.venv` folder within the project folder, and automatically keeps them up-to-date (within the version constraints specified for each dependency). `uv` automatically creates *lock files* for its environments, which record the exact versions actually installed (as opposed to a range of acceptable versions, as is typical when specifying dependencies). Notably, `uv`'s lock files are *platform agnostic* which (when needed) will specify different dependencies for different platforms, making the environment sharable with users on different OSes.

:::{sidebar} Single-script dependencies
`uv` can also manage dependencies and virtual environments for single-file scripts (as opposed to projects). For example, `uv add --script myscript.py numpy` will add a dependency on NumPy. Dependencies are stored in a special [script metadata section](https://packaging.python.org/en/latest/specifications/inline-script-metadata/) at the top of the file. See the [uv scripts guide](https://docs.astral.sh/uv/guides/scripts/) for more.
:::

Like the `venv`+`pip`+`pipx` combination that it replaces, `uv` only manages Python packages and dependencies (not dependencies written in other languages). By default, it uses [PyPI](https://pypi.org/) as its default index and repository for packages, though (as with `pip`) you can specify other indexes if needed.


## `pixi`



## Summary

```{csv-table} Environment manager comparison and cheat-sheet
:header: "", "Python built-in", "conda", "uv (venv)", "uv (project)", "pixi"
:label: table-env-mgmt

create env       , `python -m venv .venv`           , `conda create --name my_env`              , `uv venv`                                             , `uv init`                             ,
activate env     , `source .venv/bin/activate`      , `conda activate my_env`                   , `source .venv/bin/activate`                           , n/a                                   ,
deactivate env   , `deactivate`                     , `conda deactivate`                        , `deactivate`                                          , n/a                                   ,
install into env , `pip install ...`                , `conda install ...`                       , `uv pip install ...`                                  , `uv add ...`                          ,
install from file, `pip install -r requirements.txt`, `conda env create --file environment.yml` , `uv pip install -r requirements.txt`                  , `uv add -r requirements.txt`          ,
remove from env  , `pip uninstall ...`              , `conda remove ...` [^conda_remove]        , `uv pip uninstall ...`                                , `uv remove ...` (project)             ,
update dependency, `pip install --upgrade ...`      , `conda update ...`                        , `uv pip install --upgrade ...`                        , `uv sync` (also happens automatically),
install globally , `pipx install ...`               , n/a                                       , n/a                                                   , `uv tool install ...`                 ,
run once         , `pipx run ...`                   , `conda run --name my_env ...` [^conda_run], `uvx ...` [^uvx]                                      , `uv run ...` (within a project)       ,
create lockfile  , n/a                              , `conda list --explicit > spec-file.txt`   , `uv pip freeze | uv pip compile - -o requirements.txt`, `uv lock` (also happens automatically),
```

[^conda_remove]: `conda uninstall ...` also works
[^conda_run]: `my_env` must already exist and have `my_executable` installed in it
[^uvx]: alias for `uv tool run`
