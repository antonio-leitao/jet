# JET

## _Fail Fast, Test Faster_

<img alt="JET demo" src="assets/run.gif" width="600" />

## Installation

> **Note**
> JET requires [`gum`](https://github.com/charmbracelet/gum) to be installed and available on your `PATH`.

Use pip:

```sh
pip install jet
```

# Usage

## Running Tests

```sh
jet run <option>
```

JET searches for the `tests` folder in your working directory and runs all tests that start with `test_*` from the modules named as: `test_<something>.py`. JET starts by prompting you to choose wich modules to run. You can run all of them by selecting "Run All" or use the [`--all`](#run) flag, check the [`run`](#run) command for more options.
<img alt="JET demo" src="assets/run.gif" width="600" />

Specific options for the `run` command:

<img alt="JET demo" src="assets/one_liner.gif" width="600" />

- `--all`: Run all test modules. Skips initial module selection.
- `--dir`: Path to tests directory. Defaults to /tests when not supplied.
- `--files`: List of modules to consider instead of entire directory.
- `--quiet`: Disable test ouput verbose as they run.
- `--n-jobs`: Number of processes to use in parallel when running tests. Defaults to one.
- `--percentage`: Whether to show progress as a percentage instead of count.

## Reading Reports

```sh
jet see <option>
```

All tests that did not conclude with a "pass" can be further inspected. To see a detailed report including, captured standard output, local variables, source code and error description run the `see` command. The report is colapsable as to display as much information as possible without cluttering your terminal.
<img alt="JET demo" src="assets/see.gif" width="600" />

Specific options for the `see` command:

- `--dir`: Path to tests directory. Defaults to /tests when not supplied.
- `--doc-width`: Width (number of columns collumns) of report doc.
- `--text-width`: Width (number of columns collumns) of text blocks in report.
- `--buffer`: Number of lines of code to show in the report.

# Mastering Verbosity

JET displays the result of each test after it has been run.

- **if it passes** : It displays the tests's `doc`. If no `doc` is available, it shows the test's name.
- **else** : Display's the error/warning/failing condition descritption. If no description is provided, it shows the `doc` or name of test. This behaviour is specially usefull of a test has more than one failing condition, for example:

```python
#tests have to start with test_
def test_example():
   """This is the text that will be display if the test passes"""
   a = 1
   b = 2
   assert a == 1, "Text displayed if a is not equal to 1"
   assert b == 2, "Text displayed if b is not equal to 2"
```

<img alt="JET demo" src="assets/verbosity.gif" width="600" />

# Custom Fail Conditions

Suppose you want a test to fail if it's running time exceeds 0.5 seconds. We do that by creating a wrapper that raises a custom error when the condition is failed.

```python
def timebounded(test_function):
    """Example wrapper for a custom suport.
    Throws an error if the wrapped function exceeds a certain amount of time to run"""

    @wraps(test_function)
    def wrappee():
        elapsed = timeit.timeit(test_function, number=1)
        if elapsed > 0.5:
            raise PatienceError(
                f"CUSTOM ERROR: The function called {test_function.__name__} exceded my patience"
            )

    return wrappee


@timebounded
def test_timings_of_calculation():
    """The function should not exeed 0.5 seconds."""
    time.sleep(1)
```

The custom error and description and variables will show up both on the run erbose but also in the error report. This example can easily be expanded to add different and more complex failing conditions such as memory allocation and network usage etc.

<img alt="JET demo" src="assets/custom_error.gif" width="600" />

# Further Customizations

Global JET customization options:

```sh
jet <option> <command>
```

<img alt="JET demo" src="assets/colors.gif" width="600" />

- `--foreground`: color (hex, rgb or terminal256) for foreground elements.
- `--background`: color (hex, rgb or terminal256) for foreground elements.
- `--pass-color`: color (hex, rgb or terminal256) for foreground elements.
- `--failed-color`: color (hex, rgb or terminal256) for foreground elements.
- `--error-color`: color (hex, rgb or terminal256) for foreground elements.
- `--warning-color`: color (hex, rgb or terminal256) for foreground elements.
