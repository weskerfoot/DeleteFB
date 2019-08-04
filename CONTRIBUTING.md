### How to contribute

## Dependencies
If you are adding any new dependencies, please make sure that both `requirements.txt` and `setup.py` have been updated. Please read [this](https://caremad.io/posts/2013/07/setup-vs-requirement/) if you are confused about the difference between `requirements.txt` and the `install_requires` section.

## Virtualenv
Always develop with virtualenv, as well as test with `pip install --user .`. This helps make sure implicit dependencies aren't accidentally introduced, and makes sure the average user will be more likely to run it without issues.

## Pull requests
Feel free to make a pull request! Make sure to give a brief overview of what you did, and why you think it is useful. If you are fixing a specific bug or resolving an issue, then make sure to reference it in your PR.

## Coding style
Try to be consistent with the existing codebase as much as possible. Things should be modularized. Don't repeat yourself if possible, but don't add needless complexity. Straightforward is often better than clever and optimized.
