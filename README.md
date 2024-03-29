<br/>
<div align="center">
  <a href="https://cs-insights.uni-goettingen.de">
    <img src="logo.png" alt="Logo" width="600">
  </a>
</div>
<br/>
<p align="center">
<a href="https://codecov.io/gh/jpwahle/cs-insights-prediction-endpoint" > 
 <img src="https://codecov.io/gh/jpwahle/cs-insights-prediction-endpoint/branch/dev/graph/badge.svg?token=KF9ZW8HSJB"/> 
 </a>
<a href="https://github.com/jpwahle/cs-insights-prediction-endpoint/actions/workflows/release.yml"><img alt="Actions Status" src="https://github.com/jpwahle/cs-insights-prediction-endpoint/actions/workflows/release.yml/badge.svg?branch=dev">    
<a href="https://github.com/jpwahle/cs-insights-prediction-endpoint/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/jpwahle/cs-insights-prediction-endpoint/actions/workflows/main.yml/badge.svg?branch=dev">
<a href="https://github.com/jpwahle/cs-insights-prediction-endpoint/releases"><img alt="Actions Status" src="https://img.shields.io/github/v/release/jpwahle/cs-insights-prediction-endpoint"></a>
<a href="https://jpwahle.github.io/cs-insights-prediction-endpoint/"><img alt="Docs" src="https://img.shields.io/badge/Docs-gh--pages-blue"></a>
<a href="https://github.com/jpwahle/cs-insights-prediction-endpoint/blob/master/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://jpwahle.github.io/cs-insights-uptime/"><img alt="All-time uptime 100.00%" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjpwahle%2Fcs-insights-uptime%2FHEAD%2Fapi%2Fprediction-endpoint%2Fuptime.json"></a>
<a href="https://jpwahle.github.io/cs-insights-uptime/"><img alt="Response time 773" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjpwahle%2Fcs-insights-uptime%2FHEAD%2Fapi%2Fprediction-endpoint%2Fresponse-time.json"></a>
</p>
<br/>

> Starting from version 1.0.0, this project is using [semantic versioning](https://semver.org/). For more infos about the features supported, see the [releases](https://github.com/jpwahle/cs-insights-prediction-endpoint/releases).

## Installation & Setup

This project is part of the `cs-insights`-ecosystem. Please refer to the readme [here](https://github.com/jpwahle/cs-insights) to spin up the development and production system.

## Code quality and tests

To maintain a consistent and well-tested repository, we use unit tests, linting, and typing checkers with GitHub actions. We use pytest for testing, pylint for linting, and pyright for typing.
Every time code gets pushed to our repository these checks are executed and have to fullfill certain requirements before you can merge the code to our master branch.

We also use naming conventions for branches, commits, and pull requests to leverage GitHub workflow automation and keep the repository clean.

In the following we will describe how to run checks locally and which naming conventions we use.

### CI

Whenever you create a pull request against the default branch, GitHub actions will create a CI job executing unit tests and linting.

### Pre-commit

To make sure the code requirements are satisfied before you push code to the repository, we use pre-commit hooks.

Install the pre-commit hooks using:

```console
poetry run pre-commit install
```

These hooks are automatically checked before you make a commit. To manually run the pre-commit checks, run:

```console
poetry run pre-commit run --all-files
```

### Replicate CI locally

You can run each of the commands checked in `.github/workflows/main.yml`:

```console
poetry run poe lint
poetry run poe type
poetry run poe test
```

### Repository and naming conventions

Each feature request, bug, enhancement, etc. has to be related to an issue. We have templates for bugs and features requests when you create an issue on GitHub.
An issue should be a closed component that can be implemented by one developer in 1 day. If the issue is larger than that, split it into smaller components.

We group issues using a task list in another issue that has the `Epic` label. These issues are larger components that need to be developed.
Each issue with the `Epic` label has a task list with each element of the task list being a issue (e.g., this one [#47](https://github.com/gipplab/cs-insights-crawler/issues/47)).
Whenever a pull request with the above convention gets merged, the corresponding issue gets closed, and the task in the Epic gets checked.

When a branch is assigned to you, a new issue will be created from the `dev` branch including the issue number.

To indicate whether the PR is a patch, minor, or major update, please use #patch, #minor, #major in the last commit message of the PR and in the PR description.
See [here](https://github.com/anothrNick/github-tag-action) for more information.

To build changelogs, each pull-request needs one of the labels "fix", "feature", or "test". See [here](https://github.com/mikepenz/release-changelog-builder-action) for more information.

## Contributing
Fork the repo, make changes and send a PR. We'll review it together!

Commit messages should follow [Angular's conventions](https://github.com/conventional-changelog/conventional-changelog/tree/master/packages/conventional-changelog-angular).

## License
This project is licensed under the terms of Apache 2.0 license. For more information, please see the [LICENSE](LICENSE) file.

## Citation
If you use this repository, or use our tool for analysis, please cite our work:

```bib
@inproceedings{Wahle2022c,
  title        = {D3: A Massive Dataset of Scholarly Metadata for Analyzing the State of Computer Science Research},
  author       = {Wahle, Jan Philip and Ruas, Terry and Mohammad, Saif M. and Gipp, Bela},
  year         = {2022},
  month        = {July},
  booktitle    = {Proceedings of The 13th Language Resources and Evaluation Conference},
  publisher    = {European Language Resources Association},
  address      = {Marseille, France},
  doi          = {},
}
```
