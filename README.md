# [mcpartools](https://github.com/DataMedSci/mcpartools)

[![License: GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://img.shields.io/pypi/v/mcpartools.svg?style=flat)](https://pypi.org/project/mcpartools)
[![CI](https://github.com/DataMedSci/mcpartools/actions/workflows/ci.yml/badge.svg)](https://github.com/DataMedSci/mcpartools/actions/workflows/ci.yml)
[![Docs Status](https://readthedocs.org/projects/mcpartools/badge/?version=stable)](https://mcpartools.readthedocs.io/en/stable/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://mcpartools.readthedocs.io/en/stable/contributing.html)

---

**mcpartools** is a command-line tool that simplifies and accelerates particle transport simulations using Monte Carlo codes like **FLUKA** and **SHIELD-HIT12A**. It’s designed for users with access to HPC clusters (e.g., SLURM, Torque), allowing large-scale simulations to run in parallel across multiple compute nodes with minimal manual setup.

## 🚀 Features

* Generates all necessary directory structures and job scripts
* Supports distributed batch execution and result collection
* Works out-of-the-box with Linux clusters
* No programming required — just basic terminal usage

## 🛆 Installation & Usage

`mcpartools` is a Python-based tool and requires Python and Linux to run.

Install and start using the CLI tool:

```bash
pip install mcpartools
generatemc --help
```

> ✅ Tip: See our [Getting Started guide](https://mcpartools.readthedocs.io/en/stable/getting_started.html) for detailed setup instructions.

## 📚 Documentation

Full documentation is available at:
📖 [https://mcpartools.readthedocs.io/](https://mcpartools.readthedocs.io/)

* [Getting Started](https://mcpartools.readthedocs.io/en/stable/getting_started.html)
* [User Guide](https://mcpartools.readthedocs.io/en/stable/user_guide.html)

## 💡 Example Use Case

You're running FLUKA or SHIELD-HIT12A simulations and want to:

* Distribute workloads over dozens of cluster nodes
* Automatically prepare job scripts and directories
* Collect and organize simulation outputs efficiently

Then `mcpartools` is the automation tool you're looking for.

## 🛠 Development

Contributions are welcome! Feel free to open issues or submit pull requests.

To set up a development environment:

```bash
git clone https://github.com/DataMedSci/mcpartools.git
cd mcpartools
pip install -e .[dev]
```

## 📟 License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0).

---

© [DataMedSci](https://github.com/DataMedSci)
