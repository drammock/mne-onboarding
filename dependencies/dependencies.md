---
kernelspec:
  name: python3
  display_name: 'Python 3'
---
# Dependencies

## Why not add them all?

### Dependency resolution
One reason to avoid adding dependencies is that it can make it harder for environment managers to "solve" the environment.
In the worst case, environment constraints may become unsatisfiable if, for example, dependency A requires `package_C < 2.0`, while dependency B requires `package C >= 2.0`.

### Managed IT environments
In both research and commercial contexts, it may not be simple to "just install another package".
Some private companies have long approval processes for getting new packages added to their company software stacks.
Academic {abbr}`HPC (high-performance computing)` systems may also be managed environments, where individual users are not allowed to install new packages (or their disk usage quota precludes large installations).

### Import overhead
When a module is imported, its code gets executed, and any objects it defines are added to the global namespace; this takes time and memory.
If a package has many very large dependencies, a simple `import mypackage` line can take hundreds of milliseconds or even several seconds.
There are some workarounds discussed below, but it bears mentioning that the workarounds are not needed if you can simply avoid large dependencies in the first place. For example, if all your package uses Pandas for is reading CSVs, consider whether you could get by with the standard library's `csv` module instead.

There are two common workarounds for mitigating the impact of heavy dependencies.
The first is *import nesting* and the second is *lazy loading*.[^nesting_is_lazy]

#### Import nesting
Import nesting means moving the `import` statements for large dependencies _inside_ your module's function definitions, so that the import only happens if that particular function gets called by a user's script (or during an interactive session).
The effect is that initial `import mypackage` calls are somewhat faster, and in sessions where the heavy dependency is not needed, its import overhead is avoided completely.
There are two main downsides:

1. Your package is a bit harder to maintain, because the module files don't necessarily have all the imports grouped together at the top of the file.
   Moreover, if you have a test to ensure that certain pre-defined heavy dependencies are always nested, your contributors may have extra work dealing with those test failures if they don't know (or forgot) about your import nesting policy.
   On the other hand, if you *don't* test to insure import nesting, it shifts the burden to maintainers to catch those mistakes during PR review, and you run the risk of import overhead creeping up unnoticed.
1. If the heavy dependency is used many times during a session, there is actually slightly *more* overhead when it's nested, as the `import heavy_dependency` call incurs some cost each time it is called (checking whether the package has already been imported).

#### Lazy loading
The other main workaround for heavy dependencies is *lazy loading*, which yields similar effects to import nesting while keeping the `import heavy_dependency` lines more or less in-place.
The most prominent approaches are the `lazy_loader` module (created by the Scientific Python community), and `importlib.util.LazyLoader`.
There is also an in-progress {abbr}`PEP (Python Enhancement Proposal)` to add lazy loading to the standard library.
The details of how they each work are beyond the scope of this tutorial, other than to say that there are basically two steps to the import process (looking up the module spec, and executing its `__init__` code); if an approach to lazy loading delays *both* steps (not just the latter one) then things like editor tab completion on module namespace objects become much harder to achieve.

## Supported versions of dependencies
As dependencies (including Python itself) are developed and maintained, their APIs may change.
This can lead to changes in the behavior of your package, possibly including warnings or errors as parts of the dependency's API are deprecated or removed.
Experience tells us that supporting *every version* of *every dependency* is quite often a maintenance nightmare (as it requires writing a lot of extra code triaging your package's behavior depending on which version of your dependencies a user has installed), so most packages define minimum and/or maximum versions (often called "version pins") for some (or all) of their dependencies.

The Scientific Python community has collectively articulated a *suggested* policy for dependency support windows, called [SPEC-0](https://scientific-python.org/specs/spec-0000/).
By adopting SPEC-0 in your project, you can avoid some cognitive overhead by never needing to *decide* when to drop old versions of dependencies.

One practice not often seen is running documentation builds (especially tutorials) on the full range of supported package versions.
Tutorial documentation could be considered a form of end-to-end or integration testing; as such, a comprehensive approach to testing would suggest ensuring that all tutorials can be executed on the full range of supported dependency versions.


## Platform-specific dependencies

platform-specific deps (pyobjc-framework-cocoa)

## Lockfiles

new PEP defines standard format; uv/pixi have their own formats.




[^nesting_is_lazy]: Technically, import nesting could be considered a form of lazy loading, but more often "lazy loading" means other (non-nesting) approaches to avoiding (or delaying) import overhead.
