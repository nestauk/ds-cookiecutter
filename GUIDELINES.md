# Technical and working style guidelines

_Challenging this documentation is encouraged. Please set up an issue for challenges, additions or corrections. For explanations, please consult the `dev` Slack channel_

In this document we set out some basic "tips" (either mandatory or encouraged) which should guide your way of working, regardless of the task.

- [Foreword](#foreword)
- [Design patterns](#design-patterns)
- [Programming](#programming)
- [Critical thinking](#critical-thinking)
- [Naming conventions](#naming-conventions)
- [Spaces and spacing](#spaces-and-spacing)
- [Comments and docs](#comments-and-docs)

## Foreword

In advance, we recommend installing the linter and autoformatter [ruff](https://pypi.org/project/ruff/) in your IDE.

Hopefully the conventions laid out here are the easy and intuitive set of [pep8](https://www.python.org/dev/peps/pep-0008/).

Code reviewers: it is on you to ensure that this style guide has been followed: there are no points for being lenient, but there [non-redeemable] points for being opinionated! We should all feel pressured into making sure that our code meets an acceptable standard.

## Design patterns

Favour the following design patterns, in this order:

1. Functional programming: using functions to do one thing well, not altering the original data.
2. Modular code: using functions to eliminate duplication, improve readability and reduce indentation.
3. Object-oriented programming: Generally avoid, unless you are customising an API (for example `DataFrame`) or defining your own API.

If you are not, at least, adhering to a modular style then you have gone very wrong.
You should implement unit tests for each of your functions, something which is generally more tricky for object-oriented programming.

## Programming

### Mandatory

_NB: eventually these checks will be automatic_

- Don't compare boolean values to `True` or `False`.
- Favour `is not condition` over `not condition is`
- Don't compare a value to `None` (`value == None`), always favour `value is None`

### Encouraged

- Favour [`logging`](https://docs.python.org/3/howto/logging.html) over `print`
- Favour using configuration files, or (faster/lazier/less good/ok) `GLOBAL_VARIABLES` near the top of your code, rather than repeated use of hard-coded variables in your code, particularly when with URL and file path variables like `s3://path/to/some/fixed/place`, but also for repeated numeric hyperparameters.

## Critical thinking

The following questions should be going through your mind when developing your code. If you don't quite understand the wording or intention of the following questions then we encourage you to ask in the `dev` Slack channel!

- Surely this simple problem already has an elegant solution?
- How many copies of the data am I making in memory?
- Where do my variables go out of scope?
- How can I avoid creating a new variable at all costs? (think iterator, scope, `lru_cache`)
- Have I made sure that I only run expensive or time consuming processes as few times as possible?

## Naming conventions

### Mandatory

- Functions / methods: `function`, `my_function` (snake case)
- Variables / attributes: `variable`, `my_var` (snake case)
- Class: `Model`, `MyClass` (camel case)
- Module / file names / directory names: `module`, `file_name.py`, `dir_name` (camel case)
- Global\* / constants: `A_GLOBAL_VARIABLE` (screaming snake case)

\* here we use "Global" to mean constants in scope at the module level, not the `global` level. Don't use `global`, ever.

### Encouraged

- Keep all names as short and descriptive as possible. Variable names such as `x` or `df` are highly discouraged unless they are genuinely representing abstract concepts.
- Favour good naming conventions over helpful comments

## Spaces and spacing

_NB: that using the autoformatter [black](https://pypi.org/project/black/) in your IDE will resolve almost all of the following_

### Encouraged

- Use the absolute minimum number of indents of your code. You can achieve this by writing modular code, and inverting logic, for example:

```python
def something(args):
    for item_collection in args:         # 1 tab
        if item_collection.exists():     # 2 tabs
            the_sum = 0                  # 3 tabs
            for item in item_collection:
                the_sum += item.value()  # 4 tabs
            print(the_sum)
```

can become:

```python
def sum_values(item_collection):
    the_sum = sum(item.value() for item in item_collection)
    print(the_sum)

def something(args):
    for item_collection in args:         # 1 tab
        if not item_collection.exists(): # 2 tabs
            continue  # 3 tabs, buts unindents following lines
        sum_values(item_collection)      # 2 tabs
```

- Put a space before starting block comments `# like this`, `#not this`
- Inline comments need two spaces before them `a = 2 # like this`
- Keep lines to 88 (officially 79) characters or less. You can achieve this by utilising other parts of this guideline, particularly with regards to creating modular code. Splitting over multiple lines is, of course, permissible so long as it doesn't conflict with legibility.
- When declaring default values, never put spaces around operators like `=`, i.e `def this_is_ok(param=1)`, `def this_is_NOT_ok(param = 1)`. Otherwise, all operators must always have a single space on either side.
- Separate function and class arguments with a comma and a space, i.e. `do_thing(1, b=2)` and not `do_thing(1,b=2)`.

## Comments and docs

### Mandatory

- At least _a basic docstring_ is required for every function/method and class
- Full, explanatory docstrings are required for all function/methods and classes _if_ it will be used in the main body of a code routine.
- Use Google-style: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
- If you are using type hints then then you can write e.g. `my_arg (str): description` as simply `my_arg: description`.

### Encouraged

- Don't state the obvious in comments
- Before writing a comment, consider whether that information would be better be encoded in a useful variable or function name.

## Workflow

This builds on a much greater body of work, laid out in [nestauk/DAP_playbook](https://github.com/nestauk/DAP_playbook/tree/dev/github). For avoidance of doubt, branches must be linked to a GitHub issue and named accordingly:

```bash
{GitHub issue number}_{tinyLowerCamelDescription}
```

For example `14_readme`, which indicates that [this branch](https://github.com/nestauk/ojd_daps/pull/24) refered to [this issue](https://github.com/nestauk/ojd_daps/issues/14).

You should generally favour having a `dev` branch, in addition to your `main` (`master`) branch. Never commit to `dev`, `master` or `main`.

Only pull requests from branches named `{GitHub issue number}_{tinyLowerCamelDescription}` should ever be accepted.

Please make all PRs and issues reasonably small: they should be trying to achieve roughly one task. Inevitably some simple tasks spawn large numbers of utils, and sometimes these detract from the original PR. In this case, you should stack an new PR on top of your "base" PR, for example as `{GitHub issue number}_{differentLowerCamelDescription}`. In this case the PR / Git merging tree will look like:

    dev <-- 123_originalThing <-- 423_differentThing <-- 578_anotherDifferentThing

We can then merge the PR `123_originalThing` into `dev`, then `423_differentThing` into `dev` (after calling `git merge dev` on `423_differentThing`), etc until the chain is merged entirely. The nominated reviewer should review the entire chain, before the merge can go ahead. PRs should only be merged if all tests and a review has been signed off.
