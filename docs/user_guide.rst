.. highlight:: bash

.. _user_guide:

.. role:: bash(code)
   :language: bash

User's Guide
============

Directory layout and basic workflow
-----------------------------------

**generatemc** will create following directory structure for each run::

    run_20170219_122904               # main directory, new one is created for each generatemc call
        collect.sh                    # call to copy output files to output directory
        input                         # reference directory with copy of input files
            sample_fluka.inp          # non-modified copy of original Fluka input files
        submit.sh                     # call to submit jobs to the cluster
        workspace                     # workspace used to store modified input files and temporary storage for output
            main_run.sh               # this script will be called by batch system and redirect the execution to specific worker
            job_0001                  # working directory of worker no 1
                sample_fluka.inp      # copy of input file, with adapted RNG seed and output file path
                run.sh                # run script executed by worker no 1
            job_0002
                sample_fluka.inp
                run.sh
            job_0003
                sample_fluka.inp
                run.sh

After executing submit.sh script, output files will be created in the workspace directory.
Each parallel job will store its output in separate directory::

     run_20170219_122904
        collect.sh
        input
            sample_fluka.inp
        submit.sh
        workspace
            main_run.sh
            job_0001
                sample_fluka.inp
                run.sh
                TODO                  # TODO
            job_0002
                sample_fluka.inp
                run.sh
                TODO                  # TODO
            job_0003
                sample_fluka.inp
                run.sh
                TODO                  # TODO



In order to collect all files in a single place,
run `collect.sh` script. This will result in following new files::

    run_20170219_122904
        collect.sh
        input
            sample_fluka.inp
        submit.sh
        output                        # TODO
            TODO                      # TODO
        workspace
            main_run.sh
            job_0001
                sample_fluka.inp
                run.sh
            job_0002
                sample_fluka.inp
                run.sh
            job_0003
                sample_fluka.inp
                run.sh

Advanced options
----------------

There are several advanced options in the generator, customising the workflow.

After executing `generatemc` command a directory will be created (i.e. run_20170219_122904), by default
in the same location as the input configuration files. In order to change the location of generated directory,
use the `--workspace` option. For example after typing::

   generatemc.py -p 10000 -j 20 tests/res/sample_fluka.inp

A directory `tests/res/run_20170717_195410` will be created. Now providing a workspace option::

   generatemc.py -p 10000 -j 20 tests/res/sample_fluka.inp --workspace mydir

will result in new directory `mydir/run_20170717_195557`



Another useful option is the ability to provide additional options for scheduler and for Monte-Carlo binary.
The first one can be used i.e. to specify directly the walltime for job execution::

   generatemc.py -p 10000 -j 20 tests/res/sample_fluka.inp --scheduler_options "[--walltime=2:00:00]"

Not additional square brackets added to distringuish between generatemc and scheduler options.


One could also specify additional options to Monte-Carlo binary files. For example to add an user-defined
particle source in Fluka one can use its `-e` option. If the `flukadpm3_sobp` file is not present
in the PATH enviromental variable, then its location needs to be known. This may
be achieved by a mechanism of creating a link to an external file. Such links
can be created by using `-x` switch, here we provide an example in which
an external source is enabled by `-e` switch and two external files are linked (`sobp.dat` and `flukadpm3_sobp`)::

   generatemc.py -p 10000 -j 20 tests/res/sample_fluka.inp --mc_engine_options "[-e flukadpm3_sobp]" -x ./sobp.dat ./flukadpm3_sobp

When using `-x` option you may also set the absolute paths to the linked files.