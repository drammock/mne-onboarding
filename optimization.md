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

```{include} my_script.py
:lang: python
```

### Measuring speed

Often a good first-pass benchmark is seeing how long it takes to run some code, without worrying (yet) about parallelization or memory usage. There are several ways to do this; which you choose depends mostly on what your code is like (a self-contained Python script, a function, an expression, or a sequence of expressions).

#### POSIX builtin `time`
Most command-line shells have a built-in `time` utility that will report the execution time for whatever commands follow it. Use this when you have a self-contained Python script and want to benchmark execution of the entire file. For example:

```{code-block} bash
$ time python my_script.py
# [[284972184 202504466]
#  [202504466 285022249]]
# 
# real	0m0.185s
# user	0m0.138s
# sys	0m0.047s
```

Here, `real` refers to total elapsed time ("wall clock time"); `user` is the time that the CPU spent executing the `python` process; and `sys` refers to things that the CPU needed to do in order to execute the process but that the process itself isn't allowed to do for security reasons (e.g., network access, memory allocation, *etc*). Generally speaking, `user+sys` gives the total amount of CPU time used, which may be greater than `real` if the process uses multiple CPU cores in parallel.

The results above show a total execution time of ~185 ms. There is no rule of thumb: whether that is "fast enough to not care" or "slow enough to be worth optimizing" is a judgment call.

#### Python `timeit` module
If your code is a function that can't easily be made into a standalone script (e.g., a function that's part of MNE-Python), the Python `timeit` module can be a good option. It has both a command-line interface and a Python API. The command line interface has a nice feature of automatically choosing a number of repetitions of your code (which you can control yourself with the `-n` flag), chosen to make the benchmark not take too long.

```{code-block} bash
python -m timeit -s "from my_script import ARR, my_func" "my_func(ARR)"
# 5 loops, best of 5: 63.2 msec per loop
```

Here, we see it ran the statement `my_func(ARR)` 5 times ("5 loops") within one timing cycle, repeated that process 5 times ("best of 5"), and reports the duration of the fastest cycle divided by the number of loops (i.e., the average time it took to execute the statement once). Notice that the result is about ⅓ of what we saw when timing the entire script, because here we're measuring only the time needed to perform the function call (not the time needed to import numpy and create the input array).

You can achieve the same thing within Python; the main difference is that you *must* decide the number of loops yourself, and you only get out the total (you have to divide by the number of loops yourself):

```{code-cell} ipython
import timeit
n_loops = 7

total = timeit.timeit(
    stmt="my_func(ARR)",
    setup="from my_script import ARR, my_func",
    number=n_loops,
)

f"average time to execute statement: {total / n_loops:6f} seconds"
```

#### Jupyter `timeit` magic

If you're working in a Jupyter notebook, there are "magic" commands that wrap the `timeit` module too:

```{code-cell} ipython
from my_script import ARR, my_func

%timeit my_func(ARR)  # for one-liners
```

```{code-cell} ipython
%%timeit from time import sleep  # this line is setup code, and is not timed

sleep(0.1)
my_func(ARR)
```

```{note}
In data analysis contexts, it can sometimes be helpful to log the execution time of each step in an analysis pipeline (this is usually done as `start = time.time(); ...; print(time.time() - start)`). This is a bit different from benchmarking: usually the goal is to help you estimate how much longer the pipeline will take to complete. For example, if your pipeline logs `Subject 1 preprocessing completed in 00:04:55` then you can quickly estimate: *100 subjects × 5 minutes/subject = 500 minutes* (or a bit over 8 hours). But this kind of logging can *also* help you identify the slowest steps in your pipeline, showing you where it might be worthwhile to do some more detailed benchmarking and optimization.
```


### Measuring CPU usage

TODO
`kernprof`

### Measuring memory usage

TODO
`memprof`
