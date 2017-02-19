mcpartools
==========

**mcpartools** is a software simplifying time consuming simulation of particle transport using Monte Carlo codes
(Fluka, SHIELDHIT12A). We assume user has access to a computing cluster with batch processing software installed
(i.e. slurm, torque) and wants faster simulation by running it simultaneously on many computing nodes.
**mcpartools** simplifies this process by generating necessary directory structures and scripts for starting calculations
and collecting the results.

**mcpartools** provides a command line application called ``generatemc`` which works under Linux operating system
(interpreter of Python programming language has to be also installed).
No programming knowledge is required from user, but basic skills in working with terminal console are needed.


More documentation
------------------

Full **mcpartools** documentation can be found here: https://mcpartools.readthedocs.io/

See `Getting Started <https://mcpartools.readthedocs.org/en/stable/getting_started.html>`_ for installation and basic
information, and the `User's Guide <https://mcpartools.readthedocs.org/en/stable/user_guide.html>`_ for an overview of
how to use the mcpartools.
