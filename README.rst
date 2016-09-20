==============
WHAT IS THIS ?
==============

**mcpartools** is a software simplifying time consuming simulation of particle transport using Monte Carlo codes
(Fluka, SHIELDHIT12A). We assume user has access to a computing cluster with batch processing software installed
(i.e. slurm, torque) and wants to parallelize simulation by running it simultaneously on many computing nodes.
**mcpartools** simplifies this process by generating necessary directory structures and scripts for starting calculations
and collecting the results.

**mcpartools** provides a command line application called ``generatemc`` which works under Linux operating system
(interpreter of Python programming language has to be also installed).
No programming knowledge is required from user, but basic skills in working with terminal console are needed.


Quick installation guide
------------------------

First be sure to have Python framework installed, then type::

    pip install mcpartools

This command will automatically download and install **mcpartools** for all users in your system.
In case you don't have administrator rights, add ``--user`` flag to ``pip`` command.
In this situation converter will be probably installed in ``~/.local/bin`` directory.

For more detailed instruction, see `installation guide <INSTALL.rst>`__.

Short documentation
-------------------

Let us start with simple simulation of 10^6 of particles using Fluka MC code.
Such simulation would probably take few hours when running on single CPU.
It can be however faster, when you submit 100 parallel jobs, each running simulation of 10^4 particles.
We assume that:

* you are logged in to the computing cluster, all commands are executed there
* **mcpartools** is installed on the cluster
* Fluka in installed on the cluster and ``rfluka`` is available as a command
* cluster has working ``slurm`` batch job software
* an example Fluka input file is located in ``$HOME/sample.inp``

First step is to generate necessary scripts and directory structure. To accomplish this, type in terminal::

    generatemc --jobs_no 100 --particle_no 100000 $HOME/sample.inp

New directory with a name similar to ``$HOME/run_20160913_084601`` will be created. To start simulation, we call
appriopriate script::

    $HOME/run_20160913_084601/submit.sh

After the simulation is done (it may take few minutes), run following script to gather the results in a single directory::

    $HOME/run_20160913_084601/collect.sh

Output files from 100 parallel jobs will be saved in ``$HOME/run_20160913_084601/output`` directory,
ready to be analyzed or merged.
In case the output is not satisfactory, new workspace can be created and whole process repeated from scratch.


More documentation dealing with advanced options can be found here https://mcpartools.readthedocs.io/

Features
--------

* user-friendly parallelisation of particle transport simulations
* output collected in single directory
* workspace with logs and input files saved for bookkeeping
* Monte-Carlo codes support: SHIELD-HIT12A and Fluka
* cluster batch software support: slurm
* python2 and python3 compatible
* no external libraries needed

More documentation
------------------

Full documentation can be found here:
https://mcpartools.readthedocs.io/

If you would like to download the code and modify it, read first `contribution guide <CONTRIBUTING.rst>`__.