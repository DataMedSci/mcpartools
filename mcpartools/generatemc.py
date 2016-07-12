import argparse
import logging
import sys

from mcpartools.generator import Generator
from mcpartools.generator import Options


def main(args=sys.argv[1:]):
    """
    Main function, called from CLI script
    :return:
    """
    import mcpartools
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose',
                        action='count',
                        default=0,
                        help='Give more output. Option is additive, '
                             'and can be used up to 3 times')
    parser.add_argument('-q', '--quiet',
                        action='count',
                        default=0,
                        help='Be silent')
    parser.add_argument('-V', '--version',
                        action='version',
                        version=mcpartools.__version__)
    parser.add_argument('-p', '--particle_no',
                        dest='particle_no',
                        metavar='particle_no',
                        type=int,
                        default=10000,
                        help='number of primary particles per job')
    parser.add_argument('-j', '--jobs_no',
                        type=int,
                        default=10,
                        help='number of parallel jobs')
    parser.add_argument('-m', '--mc_run_template',
                        type=str,
                        default=None,
                        help='path to optional MC run script')
    parser.add_argument('-s', '--scheduler_options',
                        type=str,
                        default=None,
                        help='path to optional scheduler options file')
    parser.add_argument('input',
                        type=str,
                        help='path to input configuration')
    # TODO add grouping of options
    args = parser.parse_args(args)

    if args.quiet:
        if args.quiet == 1:
            level = "WARNING"
        if args.quiet == 2:
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
    generator.run()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
