<h1 align="center">
  <img align="center" alt="JET demo" src="assets/banner.png"/>
</h1>

<p align="center">
  [Installation](#installation) • 
  [Basic Usage](#usage) • 
  [Mastering Verbosity](#mastering-verbosity) • 
  [Custom Fail Conditions](#custom-fail-conditions) • 
  [Customization](#custom-fail-conditions)
  <p>Fail Fast, test faster. Jet is testing library for python aimed at being fast to set up, easy to use and above all pleasing to the eye. Because testing does not have to be a chore to set up, hard to understand and ugly to look at.</p>
</p>

<p align="center">
  <img alt="JET demo" src="assets/run.gif" width="600" />
</p>

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

- `--all`: Run all test modules. Skips initial module selection.
- `--dir`: Path to tests directory. Defaults to /tests when not supplied.
- `--files`: List of modules to consider instead of entire directory.
- `--quiet`: Disable test ouput verbose as they run.
- `--n-jobs`: Number of processes to use in parallel when running tests. Defaults to one.
- `--percentage`: Whether to show progress as a percentage instead of count.

<p align="center">
<img alt="JET demo" src="assets/run.gif" width="600" />
</p>

JET searches for the `tests` folder in your working directory and runs all tests that start with `test_*` from the modules named as: `test_<something>.py`. JET starts by prompting you to choose wich modules to run. You can run all of them by selecting "Run All" or use the [`--all`](#run) flag, check the [`run`](#run) command for more options.

<p align="center">
<img alt="JET demo" src="assets/one_liner.gif" width="600" />
</p>

## Reading Reports

```sh
jet see <option>
```

Specific options for the `see` command:

- `--dir`: Path to tests directory. Defaults to /tests when not supplied.
- `--doc-width`: Width (number of columns collumns) of report doc.
- `--text-width`: Width (number of columns collumns) of text blocks in report.
- `--buffer`: Number of lines of code to show in the report.

<p align="center">
<img alt="JET demo" src="assets/see.gif" width="600" />
</p>

All tests that did not conclude with a "pass" can be further inspected. To see a detailed report including, captured standard output, local variables, source code and error description run the `see` command. The report is colapsable as to display as much information as possible without cluttering your terminal.

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

<p align="center">
<img alt="JET demo" src="assets/verbosity.gif" width="600" />
</p>

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

<p align="center">
<img alt="JET demo" src="assets/custom_error.gif" width="600" />
</p>

# Further Customizations

Global JET customization options:

```sh
jet <option> <command>
```

- `--foreground`: color (hex, rgb or terminal256) for foreground elements.
- `--background`: color (hex, rgb or terminal256) for background.
- `--pass-color`: color (hex, rgb or terminal256) for pass tests.
- `--failed-color`: color (hex, rgb or terminal256) for failed tests.
- `--error-color`: color (hex, rgb or terminal256) for tests that result in errors.
- `--warning-color`: color (hex, rgb or terminal256) for tests that throw warnings.

<p align="center">
<img alt="JET demo" src="assets/colors.gif" width="600" />
</p>
