---
kernelspec:
  name: python3
  display_name: 'Python 3'
---
# Packaging

There are already several excellent packaging tutorials online:

- [The Scientific Python packaging tutorial](https://learn.scientific-python.org/development/tutorials/packaging/) is a step-by-step guide to creating a minimal package locally, and installing it locally.
- The ["Packaging Python Projects" tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) from the Python Packaging Authority, and the [Scientific Python "simple" packaging guide](https://learn.scientific-python.org/development/guides/packaging-simple/) both focus on building *distribution packages* (sdists and wheels) from pure Python codebases, and uploading the packages to PyPI.
- [The Scientific Python "compiled" packaging guide](https://learn.scientific-python.org/development/guides/packaging-compiled/) focuses on extra steps needed when the package includes code (C++, FORTRAN, etc) that must be compiled before distribution.
- [The Scientific Python "classic" packaging guide](https://learn.scientific-python.org/development/guides/packaging-classic/) describes how things *used to* be done, mainly helpful if you're dealing with legacy code and want to transition it to a modern packaging process.
- [The Python Packaging Authority's main site](https://packaging.python.org/) covers almost everything in lots of detail.


## Terminology

:::{glossary}
module
: An object that serves as an organizational unit of Python code. Modules have a namespace containing arbitrary Python objects. Modules are loaded into Python by the process of importing. Source: https://docs.python.org/3/glossary.html#term-module

package
: A Python module which can contain submodules or recursively, subpackages. Technically, a package is a Python module with a `__path__` attribute. See also [regular package](https://docs.python.org/3/glossary.html#term-regular-package) and [namespace package](https://docs.python.org/3/glossary.html#term-namespace-package). Source: https://docs.python.org/3/glossary.html#term-package
:::

## Background: ways to run code in Python

- Type Python code directly into the Python REPL
- Write Python code in a file, and:
    - run the file (`python myfile.py`) from a command shell
    - *import* objects defined in that file.
        - Works as long as the file is *at or below* the location of the Python REPL in the folder hierarchy (in other words, only works for "absolute imports").

          :::{admonition} Relative imports
          :class: note
          Attempting to use relative imports (using leading `.`, e.g., `from ..foo.bar import BAZ`) in an interactive REPL or in a script executed from command shell, will fail with `ImportError: attempted relative import with no known parent package`.
          There are hacks around it, but generally speaking, relative imports only work inside a defined package. If you must directly run a script that involves relative imports, you can invoke it as `python -m foo.bar` (to run `bar.py`, which suppose contains a relative import from `foo.baz`), to automatically (effectively) run `import foo` and `import foo.baz` first.
          :::

    - make it a package, and install the package. This means:
        - defining `__init__.py` files in the top level folder and each subfolder where there are Python files you want to be able to import from.
        - running `pip install <packagename>` so that you can import it regardless of where in the filesystem the REPL is.

## background: src layout vs flat layout

- main distinction is whether *importable code* is in a folder `packagename` at the repository root, or if it's instead nested within a `src` folder.
- advantage of `src` layout is that it *guarantees* that when you `import packagename` you're getting the *installed* version of the package, not importing directly from the source tree.

## Basic "installable" package

```
projectroot
├─ pyproject.toml
└─ src
   └─ projectname
      ├─ __init__.py
      ├─ submoduleA.py
      └─ submoduleB
         ├─ __init__.py
         └─ ...
```


## Basic package distribution

nowadays it's all done via CIs / trusted publishing (https://github.com/mne-tools/mne-python/blob/main/.github/workflows/release.yml)


## How we *actually* do it

https://github.com/mne-tools/mne-python/wiki/How-to-make-a-major-or-minor-release


## QUESTIONS

- build backends: what are they, how do we configure them? specifying versions?
- 
