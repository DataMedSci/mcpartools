.. highlight:: bash

.. _user_guide:

.. role:: bash(code)
   :language: bash

User's Guide
============

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

