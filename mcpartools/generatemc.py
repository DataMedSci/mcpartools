import argparse
import logging
import sys

from mcpartools.generator import Generator
from mcpartools.generator import Options
from mcpartools.scheduler.common import SchedulerDiscover


def main(args=sys.argv[1:]):
    """
    Main function, called from CLI script
    :return:
    """
    import mcpartools
    parser = argparse.ArgumentParser()

    general_args = parser.add_argument_group(title=None, description='General options')
    config_args = parser.add_argument_group(title=None, description='Generator configuration options')
    mc_args = parser.add_argument_group(title=None, description='Monte Carlo options')
    smart_args = parser.add_argument_group(title=None, description='Smart submit options.')

    parser.add_argument('input',
                        type=str,
                        help='path to input configuration')

    general_args.add_argument('-V', '--version',
                              action='version',
                              version=mcpartools.__version__)
    general_args.add_argument('-v', '--verbose',
                              action='count',
                              default=0,
                              help='Give more output. Option is additive, '
                                   'and can be used up to 3 times')
    general_args.add_argument('-q', '--quiet',
                              action='count',
                              default=0,
                              help='Be silent')

    config_args.add_argument('-w', '--workspace',
                             type=str,
                             help='workspace directory')

    config_args.add_argument('-m', '--mc_run_template',
                             type=str,
                             default=None,
                             help='path to optional MC run script')
    config_args.add_argument('-s', '--scheduler_options',
                             type=str,
                             default=None,
                             help='optional scheduler options: path to a file or list of options in square brackets')
    config_args.add_argument('-e', '--mc_engine_options',
                             type=str,
                             default=None,
                             help='optional MC engine options: path to a file or list of options in square brackets')
    config_args.add_argument('-x', '--external_files',
                             nargs='+',  # list may be empty
                             type=str,
                             help='list of external files to be copied into each job working directory')
    config_args.add_argument('-b', '--batch',
                             type=str,
                             default=None,
                             choices=[b.id for b in SchedulerDiscover.supported],
                             help='Available batch systems: {}'.format([b.id for b in SchedulerDiscover.supported]))
    config_args.add_argument('-c', '--collect',
                             type=str,
                             default='mv',
                             choices=Options.collect_methods,
                             help='Available collect methods')

    mc_args.add_argument('-p', '--particle_no',
                         dest='particle_no',
                         metavar='particle_no',
                         type=int,
                         required=True,
                         help='number of primary particles per job')
    mc_args.add_argument('-j', '--jobs_no',
                         type=int,
                         required=True,
                         help='number of parallel jobs')

    smart_args.add_argument('--smart',
                            action='store_true',
                            help='smart mode on (only for slurm)')
    smart_args.add_argument('--partition',
                            default="plgrid",
                            help='partition (default: %(default)s)')
    smart_args.add_argument('--utilisation',
                            type=float,
                            default=0.5,
                            help='cluster node utilisation (default: %(default)s), 1 stands for 100%%')
    smart_args.add_argument('--ratio',
                            type=float,
                            default=1.08,
                            help='multiply utilisation by ratio (default: %(default)s) to contain all jobs')

    args = parser.parse_args(args)

    if args.quiet:
        if args.quiet == 1:
            level = "WARNING"
        elif args.quiet == 2:
            level = "ERROR"
        else:
            level = "CRITICAL"
    elif args.verbose:
        level = "DEBUG"
    else:
        level = "INFO"

    logging.basicConfig(level=level)

    opt = Options(args)
    generator = Generator(options=opt)
    ret_code = generator.run()

    return ret_code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
