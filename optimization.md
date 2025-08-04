---
kernelspec:
  name: python3
  display_name: 'Python 3'
---
# Optimization and benchmarking

> Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We **should** forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil.
> 
> Yet we should not pass up our opportunities in that critical 3%. A good programmer will not be lulled into complacency by such reasoning, he will be wise to look carefully at the critical code; but only **after** that code has been identified. It is often a mistake to make a priori judgments about what parts of a program are really critical, since the universal experience of programmers who have been using measurement tools has been that their intuitive guesses fail.

— {cite}`10.1145/356635.356640`

## Definitions

Benchmarking 
: Running code (usually multiple times) and measuring the resources (CPU time, memory, disk space, and/or network usage) necessary to execute it. If the code takes inputs, benchmarking usually involves testing inputs of different sizes or types.

Optimization
: Modifying code to reduce its resource consumption. Note that reduced consumption may vary with the size or type of input; optimizing a function to be really efficient for small 1-dimensional array input is unhelpful if the typical user will be passing in large 3-dimensional arrays.

## When to optimize

It is generally encouraged to optimize code only *after* the program has been written (i.e., all features are implemented, and the code is tested and believed to be bug-free) and *after* it has been benchmarked. If you optimize before the code is finished (e.g., as you're writing it), you risk wasting that effort (by later re-writing that part of the code) because your partial implementation was buggy, or because it didn't account for all the planned features. As the quote from {cite}`10.1145/356635.356640` makes clear, it is also considered a best practice to optimize only after benchmarking: programmer instincts are often wrong about about which lines of code are the performance bottleneck.

## Simple benchmarking

Here's an example script that we'll use for benchmarking practice.

```{include} script.py
:lang: python
```

### Measuring speed

Often a good first-pass benchmark is seeing how long it takes to run some code, without worrying (yet) about parallelization or memory usage. There are several ways to do this; which you choose depends mostly on what your code is like (a self-contained Python script, a function, an expression, or a sequence of expressions).

#### POSIX builtin `time`
Most command-line shells have a built-in `time` utility that will report the execution time for whatever commands follow it. Use this when you have a self-contained Python script and want to benchmark execution of the entire file. For example:

```{code-cell} ipython
%%bash

time python script.py
```

Here, `real` refers to total elapsed time ("wall clock time"); `user` is the time that the CPU spent executing the `python` process; and `sys` refers to things that the CPU needed to do in order to execute the process but that the process itself isn't allowed to do for security reasons (e.g., network access, memory allocation, *etc*). Generally speaking, `user+sys` gives the total amount of CPU time used, which may be greater than `real` if the process uses multiple CPU cores in parallel.

The results above show a total execution time of ~1.4 s. There is no rule of thumb: whether that is "fast enough to not care" or "slow enough to be worth optimizing" is a judgment call.

#### Python `timeit` module
If your code is a function that can't easily be made into a standalone script (e.g., a function that's part of MNE-Python), the Python `timeit` module can be a good option. It has both a command-line interface and a Python API. The command line interface has a nice feature of automatically choosing a number of repetitions of your code (which you can control yourself with the `-n` flag), chosen to make the benchmark not take too long.

```{code-cell} ipython
%%bash

python -m timeit -s "from script import ARR, my_func" "my_func(ARR)"
```

Here, we see it ran the statement `my_func(ARR)` 2 times ("2 loops") within one timing cycle, repeated that process 5 times ("best of 5"), and reports the duration of the fastest cycle divided by the number of loops (i.e., the average time it took to execute the statement once). Notice that the result is almost an order of magnitude faster than what we saw when timing the entire script, because here we're measuring only the time needed to perform the function call (not the time needed to import numpy and create the input array).

You can achieve the same thing within Python; the main difference is that you *must* decide the number of loops yourself, and you only get out the total (you have to divide by the number of loops yourself):

```{code-cell} ipython
import timeit
n_loops = 3

total = timeit.timeit(
    stmt="my_func(ARR)",
    setup="from script import ARR, my_func",
    number=n_loops,
)

f"average time to execute statement: {total / n_loops:6f} seconds"
```

#### Jupyter `timeit` magic

If you're working in a Jupyter notebook, there are "magic" commands that wrap the `timeit` module too:

```{code-cell} ipython
from script import ARR, my_func

%timeit my_func(ARR)  # single-% version for one-liners
```

```{code-cell} ipython
%%timeit import time; time.sleep(0.01)  # this line is setup code, and is not timed

my_func(ARR)
```

```{admonition} Timing analysis pipelines
:class: dropdown hint

In data analysis contexts, it can sometimes be helpful to log the execution time of each step in an analysis pipeline (this is usually done as `start = time.time(); ...; print(time.time() - start)`). This is a bit different from benchmarking: usually the goal is to help you estimate how much longer the pipeline will take to complete. For example, if your pipeline logs `Subject 1 preprocessing completed in 00:04:55` then you can quickly estimate: *100 subjects × 5 minutes/subject = 500 minutes* (or a bit over 8 hours). But this kind of logging can *also* help you identify the slowest steps in your pipeline, showing you where it might be worthwhile to do some more detailed benchmarking and optimization.
```


### Measuring CPU usage

To get line-by-line CPU usage for Python code, install [line_profiler](https://github.com/pyutils/line_profiler) (available via `pip` or `conda`). The tool *only works on functions*, and is enabled by a 2-step process:

1. in the script where your function is defined, `import line_profiler` and decorate the function with `@line_profiler.profile`
2. call the script like this: `LINE_PROFILE=1 python script.py`

Here's what that looks like:

```{include} script_lprof.py
:lang: python
:class: collapse
```

This will write some files to the current working directory (`profile_output.lprof` and `profile_output.txt`, plus a timestamped version of the `.txt` file so you can review changes to the profiling when you run it multiple times). The terminal output of the command will tell you how to view the results:

```{code-cell} ipython
:tags: [hide-output]

%%bash

LINE_PROFILE=1 python script_lprof.py
```

The output mostly just tells you which filenames have been written to, but the last lines say:
```
To view details run:
python -m line_profiler -rtmz profile_output.lprof
```

Doing so gives you a line-by-line estimate of compute time:

```{code-cell} ipython
%%bash

python -m line_profiler -rtmz profile_output.lprof > _static/lprof.txt
```

```{literalinclude} _static/lprof.txt
:filename: false
```

Some things to notice:

- the `Hits` column shows how many times each line was executed. Lines inside `for` loops are executed more times; if you're profiling a helper function that is called more than once by another function, you may also see multiple hits on lines of the helper function.
- the values in the `Time` and `Per Hit` column are not necessarily in seconds! The first line of output says `Timer unit: 1e-06 s`, so we're seeing microseconds here.
- the `% Time` column is often the best place to look to identify what to consider optimizing.

```{note}
The function that you're profiling doesn't need to be defined in the script you're executing to generate the profile output. This means you could write a short script that loads some data and processes (or plots) it, and then go into the source code of MNE-Python and stick an `@line_profiler.profile` decorator on any function or method in the codebase to see how it performs when given that data.
```

````{admonition} Profiling scripts (not functions)
:class: dropdown hint

If you're trying to profile a script (such as a tutorial for MNE-Python's documentation website), you can (temporarily) indent the whole script, and then add a few lines above and below to make it ready for profiling:

```{code-block} python
import line_profiler

@line_profiler.profile
def my_func():
    # your indented script goes here...

if __name__ == "__main__":
    my_func()
```
````

### Measuring memory usage

```{warning}
For a long time, [memory_profiler](https://github.com/pythonprofilers/memory_profiler) was the go-to choice for measuring memory usage. It is still in widespread use, but is currently unmaintained. You may want to try out [memray](https://bloomberg.github.io/memray/index.html) instead.
```

To get line-by-line memory usage for Python code, install [memory_profiler](https://github.com/pythonprofilers/memory_profiler) (available via `pip` or `conda`). As with `line_profiler`, you need to decorate the function(s) that you want to profile with an `@profile` decorator; unlike with `line_profiler`, the decorator doesn't need to be imported for it to work. Just run:

```{code-cell} ipython
%%bash

python -m memory_profiler script.py
```

Here the results are  not very interesting, because the output array we're allocating is small, and the (larger) input array was allocated *outside* the function call, so it just shows up in the baseline `Mem usage` at the start of the function.

If you want to generate a graph of the memory usage over time, you can run

```{code-cell} ipython
%%bash

mprof run script.py
mprof plot --output _static/mprof.png
```

![plot of memory usage on the vertical axis and time on the horizontal axis, showing ](_static/mprof.png)

The `run` subcommand will generate a file (`mprofile_20250804091557.dat` or so) and the `plot` subcommand automatically plots the data the file with the most recent timestamp.

<!-- TODO insert plot -->

## Optimizing with NumPy

- use NumPy builtins
- cut out for-loops and use broadcasting
- NB: `np.vectorize` doesn't help you here! It's built for broadcasting convenience, not speed (so you can start with a sequence of objects, do your custom operation on them, and end up with an array).
- pre-allocate arrays instead of growing them
- many NumPy functions have an `out=` parameter, that specifies an *existing* array to write into (instead of allocating and returning a new array). For very large arrays, consider overwriting the input array if it's safe to do so.

## Optimizing with Numba

TODO
