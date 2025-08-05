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
: Modifying code to reduce its resource consumption. Note that reduced consumption may vary with the size or type of input; optimizing a function to be really efficient for small 1-dimensional array input is unhelpful if the optimizations aren't as effective for the sizes and shapes of arrays that users typically pass to the function.

## When to optimize

It is generally encouraged to optimize code only *after* the program has been written (i.e., all features are implemented, and the code is tested and believed to be bug-free). If you optimize before the code is finished (e.g., as you're writing it), you risk wasting that effort (by later re-writing that part of the code) because your partial implementation was buggy, or because it didn't account for all the planned features. And as the quote from {cite}`10.1145/356635.356640` makes clear, it is also considered a best practice to optimize only after benchmarking: programmer instincts are often wrong about about which lines of code are the performance bottleneck.

## Simple benchmarking

Here's an example script that we'll use for benchmarking practice.

```{include} script.py
:lang: python
:linenos:
:caption: Our starting point: the unoptimized script
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

The results above show a total execution time of ~1.4 s. ***There is no rule of thumb:*** whether that is "fast enough to not care" or "slow enough to be worth optimizing" is a judgment call.

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

To get line-by-line CPU usage for Python code, install [line_profiler](https://github.com/pyutils/line_profiler) (available via `pip` or `conda`). Selecting portions of code to profile is done in one of three ways:

- `import line_profiler` and then decorate a function with `@line_profiler.profile`.
- `from line_profiler import profile` and then call `profile.enable()` and `profile.disable()` to start/stop profiling.
- `from line_profiler import profile` and use the `with profile:` context manager.

Here we'll use the function decorator:

```{include} script_lprof.py
:lang: python
:linenos:
:lineno-match:
:end-line: 16
:emphasize-lines: 2,8
```

Next, call the script like this: `LINE_PROFILE=1 python script.py`. This will write some files to the current working directory (`profile_output.lprof` and `profile_output.txt`, plus a timestamped version of the `.txt` file so you can review changes to the profiling when you run it multiple times).

```{code-cell} ipython
:tags: [hide-output]

%%bash

LINE_PROFILE=1 python script_lprof.py
```

The terminal output mostly just tells you which filenames have been written to, but the last lines say:

```
To view details run:
python -m line_profiler -rtmz profile_output.lprof
```

Doing so gives you a line-by-line estimate of compute time:

```{code-cell} ipython
%%bash

python -m line_profiler -rtmz profile_output.lprof > lprof_output.txt
# file redirection is just for nicer formatting    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
```

```{literalinclude} lprof_output.txt
:label: lprof-orig
:caption: CPU profiling of the initial (unoptimized) script
:filename: false
:enumerated: false
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

To get line-by-line memory usage for Python code, install [memory_profiler](https://github.com/pythonprofilers/memory_profiler) (available via `pip` or `conda`). As with `line_profiler`, you need to decorate the function(s) that you want to profile with a `@profile` decorator; unlike with `line_profiler`, the decorator doesn't need to be imported for it to work:

```{include} script_mprof.py
:lang: python
:lines: 1-16
:linenos:
:lineno-match:
:emphasize-lines: 7
```

```{code-cell} ipython
%%bash

python -m memory_profiler script_mprof.py > mprof_output.txt
# redirection → nicer output formatting   ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
```

```{literalinclude} mprof_output.txt
:filename: false
```

Here the results are not very interesting, because the output array we're allocating is too small to notice (a 2 × 2 array of `int`s is only 32 *bytes*, or 0.00003 MiB), and the (larger) input array was allocated *outside* the function call, so it just shows up in the baseline `Mem usage` at the start of the function.

If you want to generate a graph of the memory usage over time, you can run `mprof plot`; it will automatically use the most recent `mprofile_*.dat` file in the current directory. If you *only* want the graph (not the line-by-line info) you can also use the shorter command `mprof run script_mprof.py` to just write out the `*dat` file, instead of the longer `python -m memory_profiler script_mprof.py` as above.

```{code-cell} ipython
%%bash

mprof run script_mprof.py
mprof plot --output mprof.png
```

![plot of memory usage on the vertical axis and time on the horizontal axis. The line shows a steady increase from 0 to 63 MiB from 0 to about 0.3 seconds, then holds constant at 63 MiB until 0.5 seconds. Brackets indicate that the function `my_func` executed between 0.3 and about 0.46 seconds.](mprof.png)

## Optimizing with NumPy

Now that we've benchmarked our script, how can we optimize it? There are a few strategies to pursue, given here in rough order from easiest to most difficult.

### Use NumPy builtins

In our script we're manually accumulating the sum of $r_i \times c_j$ products in a for-loop:

```{include} script_lprof.py
:lang: python
:linenos:
:lineno-match:
:lines: 13-16
:emphasize-lines: 15-16
:filename: false
```

We can eliminate the innermost for-loop using the built-in `np.sum` function:

```{include} script_sum.py
:lang: python
:linenos:
:lineno-match:
:lines: 13-15
:emphasize-lines: 15
:filename: false
```

```{code-cell} ipython
:tags: [remove-output]

%%bash

LINE_PROFILE=1 python script_sum.py
python -m line_profiler -rtmz profile_output.lprof > lprof_sum.txt
```

```{literalinclude} lprof_sum.txt
:label: lprof-sum
:caption: CPU profiling after switching to use np.sum
:filename: false
:enumerated: false
```

We went from 0.43 *seconds* runtime for [the original script](#lprof-orig) to around 750 *microseconds* just by using `np.sum`!

### Use NumPy broadcasting

We could try to go further and use [broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) to eliminate another level of for-loop nesting:

```{include} script_broadcast.py
:lang: python
:linenos:
:lineno-match:
:lines: 13-15
:emphasize-lines: 14
:filename: false
```

```{code-cell} ipython
:tags: [remove-output]

%%bash

LINE_PROFILE=1 python script_broadcast.py
python -m line_profiler -rtmz profile_output.lprof > lprof_broadcast.txt
```

```{literalinclude} lprof_broadcast.txt
:label: lprof-bcast
:caption: CPU profiling after eliminating a loop with broadcasting
:filename: false
```

This time we went from 750 microseconds for [the version using np.sum](#lprof-sum) to around 1 *millisecond* — a slowdown! Let's see how the memory performance looks:

```{code-cell} ipython
%%bash

python -m memory_profiler script_bcast_mprof.py > mprof_bcast.txt
```

```{literalinclude} mprof_bcast.txt
:caption: Memory profiling after eliminating a loop with broadcasting
:filename: false
```

It uses more memory too! (Note the increment on line 13). The code is also arguably less readable, so we should probably abandon this approach. In practice, after the initial *huge* speedup due to `np.sum`, most experienced programmers would have said "good enough" and stopped there. Again, there is no one-size-fits-all criterion; when to optimize (and when to stop further optimization attempts) is always a judgment call.

At this point, you're probably screaming "but what about `@`!!" Indeed, just using the built-in NumPy matrix multiplication is *much much* better than anything we've done so far, if for no other reason than the improved readability of the code:

```{include} script_dot.py
:lang: python
:linenos:
:lineno-match:
:lines: 9-12
:filename: false
:emphasize-lines: 11
:caption: The obvious approach, using `@` (the `np.dot` infix operator)
```

At this point we wouldn't even need to define our own function anymore. So how does it stack up?

```{code-cell} ipython
:tags: [remove-output]

%%bash

LINE_PROFILE=1 python script_dot.py
python -m line_profiler -rtmz profile_output.lprof > lprof_dot.txt
```

```{literalinclude} lprof_dot.txt
:label: lprof-dot
:caption: CPU profiling using the `@` infix operator
:filename: false
```

Down from 750 microseconds to around 250 microseconds. So in case the `np.sum` results above weren't convincing, here's further evidence that using NumPy built-in functions will almost always yield more efficient code than implementing the same computations yourself.

### Some pitfalls to avoid

Generally speaking, there are a few patterns that (almost) always work to speed up scientific Python code and/or reduce memory usage:

- *Pre-allocate arrays instead of growing them incrementally*. Avoid using `np.concatenate`, `np.stack`, *etc.* inside for-loops.
- *Re-use the input array*. If you aren't going to need the input array and it's already the shape you need for your output: many NumPy functions have an `out=` parameter, that specifies an *existing* array to write into (instead of allocating and returning a new array). For very large arrays, this can cut down on memory usage considerably.
- *Don't be fooled by `np.vectorize`*. You may be tempted by the name, but `np.vectorize` is built for broadcasting convenience, not for speed. In most cases it won't speed up complex computations that don't have a built-in NumPy equivalent.
- *Consider `np.einsum`*. An explanation of how `np.einsum` works is beyond the scope of this tutorial, but in some cases it can reduce computation and memory usage, usually by re-ordering computations so that operations that reduce the dimensionality happen earlier (thereby eliminating some of the broadcasting that would otherwise have occurred).

## Optimizing with Numba

For complex computations that need to be called repeatedly (e.g., a computation applied to a window, where the window slides along a time series), rewriting the function to use Numba might be worth the effort. Numba JIT (just-in-time) compiles code once based on its input arguments (e.g., dimensionality and dtypes), which can be slow—but any subsequent call with matching type and dimensionality will use that compiled code immediately. Unfortunately, Numba only allows a subset of the NumPy API in functions that it compiles, so some re-writing may be necessary.

### Using numba.jit

Let's try it with our example above, starting with the naive two-loop code, but adding the decorator `@numba.jit(nopython=True)` and tweaking the `result` `dtype` in the function (which is otherwise unchanged):

```{include} script_numba.py
:lang: python
:filename: false
:end-line: 16
:linenos:
:lineno-match:
:emphasize-lines: 2,8,12
```

```{code-cell} ipython
%%bash

python -m timeit -s "from script_numba import ARR, my_func, np; my_func(np.ones([1, 1], dtype=np.int64))" "my_func(ARR)"
```
There are a few notable things here:

1. First, the speed is faster than the [naive](#lprof-orig), [`sum`](#lprof-sum), and [`broadcast`](#lprof-bcast) results, rivaling [using NumPy's `@`](#lprof-dot) directly. The `@` operator in NumPy calls highly optimized BLAS linear algebra routines, utilizing SIMD (single-instruction multiple-data) CPU instructions and multiple threads, so it can in some situations beat Numba. But Numba also can make use of SIMD instructions, so results can vary!
2. We had to tweak the `dtype=int` to be `dtype=np.int64` for the `result` inside the loop. This is because `nopython` mode needs explicit NumPy dtypes. Another (maybe better) option here would be to use `dtype=input.dtype`.
3. In the `timeit` call, we call the function once in the *setup* phase. This triggers the JIT compilation. From then on, it can be used by the repeated calls to `my_func` that `timeit` will do under the hood. Without this step, the JIT compilation time would (misleadingly) be included in the `timeit` stats.

### A more complex example

You can see a more complex example of this in the MNE-Python code for computing the SNR of {abbr}`cHPI (continuous Head Position Indicator)` coils:

```{code-block} python
:linenos:
:emphasize-lines: 7,11-12,22

@jit()
def _fast_fit_snr(this_data, n_freqs, model, inv_model, mag_picks, grad_picks):
    # first or last window
    if this_data.shape[1] != model.shape[0]:
        model = model[: this_data.shape[1]]
        inv_model = np.linalg.pinv(model)
    coefs = np.ascontiguousarray(inv_model) @ np.ascontiguousarray(this_data.T)
    # average sin & cos terms (special property of sinusoids: power=A²/2)
    hpi_power = (coefs[:n_freqs] ** 2 + coefs[n_freqs : (2 * n_freqs)] ** 2) / 2
    resid = this_data - np.ascontiguousarray((model @ coefs).T)
    # can't use np.var(..., axis=1) with Numba, so do it manually:
    resid_mean = np.atleast_2d(resid.sum(axis=1) / resid.shape[1]).T
    squared_devs = np.abs(resid - resid_mean) ** 2
    resid_var = squared_devs.sum(axis=1) / squared_devs.shape[1]
    # output array will be (n_freqs, 3 * n_ch_types). The 3 columns for each
    # channel type are the SNR, the mean cHPI power and the residual variance
    # (which gets tiled to shape (n_freqs,) because it's a scalar).
    snrs = np.empty((n_freqs, 0))
    # average power & compute residual variance separately for each ch type
    for _picks in (mag_picks, grad_picks):
        if len(_picks):
            avg_power = hpi_power[:, _picks].sum(axis=1) / len(_picks)
            avg_resid = resid_var[_picks].mean() * np.ones(n_freqs)
            snr = 10 * np.log10(avg_power / avg_resid)
            snrs = np.hstack((snrs, np.stack((snr, avg_power, avg_resid), 1)))
    return snrs
```

A few things to note:

- *There are several calls to `np.ascontiguousarray`*. Many NumPy functions are faster if performed on arrays stored in C-contiguous order in memory. Numba will warn you if it detects those functions being called on non-contiguous arrays.
- *The `axis` parameter might not be allowed*. The comment on line 11 calls out one such case, so that future developers don't recognize the familiar formula for variance and try to speed things up by using `np.var`. Note that it's not *always* forbidden; on line 22 we see the `.sum(axis=1)` method called on an array. The Numba documentation is fairly clear about what is allowed, but in any case the Numba compiler will complain if you try to use a NumPy feature that it doesn't support.
- *The `@jit` decorator is a wrapper*. In MNE-Python, we re-define Numba's decorator to still work even if the user doesn't have Numba installed. We also set `nopython=True, nogil=True, fastmath=True, cache=True` in all in-repo `jit` calls by default. [See how we do it](https://github.com/mne-tools/mne-python/blob/f04fcaa851e64b379a1a107f18cf3fd5b6b18f42/mne/fixes.py#L600-L640).
