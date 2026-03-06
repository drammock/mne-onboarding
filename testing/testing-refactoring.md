---
kernelspec:
  name: python3
  display_name: 'Python 3'
---
# Refactoring large tests

TODO INTRODUCTION

General approach:

1. read through the test and take thematic notes about what each line or group of lines is doing. The goal is to help you spot similar checks at different points in the test function, that might make sense to group together and refactor out into a separate test function.

2. run the whole test file and record coverage of the submodule that it resides in. For example, if your over-large test is in `mne/time_frequency/tests/test_tfr.py`, then run like this: `pytest mne/time_frequency/tests/test_tfr.py --cov=mne/time_frequency --cov-report=term-missing`.  This tells pytest to (1) only record coverage of library code within the `time_frequency` submodule, and (2) write the coverage info to the terminal with line numbers for any missed lines.

3. run the coverage command again, but first decorate the over-large test function with `@pytest.mark.skip("TEMPORARY SKIP TO ASSESS COVERAGE")`.

4. Compare the results of steps (2) and (3). In particular, find the lines that are covered in the "baseline" coverage from step (2) but are not covered when the long test is omitted as in step (3).  This will help you determine what parts of the long test *should not be eliminated* because they would reduce coverage.

5. For each line (or line span) of coverage that would be lost, look them up in the source file and see what they do. Annotate the list of missed lines with that information. Example: `tfr.py:3957 -> combine_tfr(..., weights="equal")`. This info will help you identify which line(s) of the over-long test are the ones underpinning the coverage difference.


# NOTES
scott: doc setup (numpydoc, sphinx-autodoc, autoapi, sphinx-gallery + mini-galleries, etc)
