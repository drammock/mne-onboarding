---
kernelspec:
  name: python3
  display_name: 'Python 3'
---
# Testing with pytest

TODO INTRODUCTION

## Terminology


::::{glossary}
Unit test
: A test of one component of a software project. "Units" are usually defined in terms of software *behavior*, and may or may not cleanly align with functions or classes. When testing a unit, it is considered best practice to *mock* any aspects of the software that are needed for the test to run but are not part of the unit being tested.

  :::{admonition} Mocking in unit tests: an example
  :class: dropdown hint

  Suppose the behavior being tested is matrix multiplication. To test it, you need two arrays to multiply. Now suppose that in your software, the matrix multiplication function allows users to pass *file paths* from which the arrays will be loaded. The unit test for matrix multiplication behavior should *not* include code that loads those arrays from disk or downloads them from a remote server (if it did, the test might fail because of network or file permission problems, which are unrelated to matrix multiplication). Instead, the unit test should *mock* the function that loads arrays so that it never pulls from local or remote storage (for example, by constructing the arrays on-the-fly). That way, the test will only fail if there's a problem with the matrix multiplication behavior.
  :::

Integration test
: A test of the interaction among many components of a software project, to ensure they interoperate as designed. For example, if one function creates a data object by reading from a file, and another function performs some computation or analysis of that data object, an integration test would *pass an object read from file directly to the analysis function* to make sure that the read-from-disk object has all the attributes that the analysis function expects it to have.

System test, end-to-end test, or workflow test
: A test that follows a sequence of actions that typical users might perform when using the software. For many Scientific Python software packages, workflow tests take the form of *example notebooks* or *tutorials* that are executed when building the software's documentation website.

Regression test
: A test created in response to a discovered bug, designed to make sure that bug does not reappear once fixed.

Smoke test
: A fast, high-level test of basic functionality, designed to answer the question "are things basically working, enough so that it's worth the time to run the full test suite?"

  :::{admonition} Etymology of "smoke test"
  :class: dropdown note
  
  Historically, some kinds of machines were tested for leaks by filling their pipes with smoke, and looking for sources of escaping smoke. This was done prior to more comprehensive testing (e.g., with the machine running and the pipes full of scalding steam), which was more costly, risky, and time-consuming.
  
  source: <wiki:Smoke_testing_(software)#Etymology>
  :::
::::

Fixture
: TODO

Monkeypatch
: TODO

Mocking
: TODO

Setup / Teardown
: TODO

# NOTES

- mocking: not clear from given example
- autouse: scope, purpose not clear
- why do we have empty `__init__` files in our test folders?
- terminology: fixture, teardown, not easy for non-native speaker
