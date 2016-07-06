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
    parser.add_argument('--verbose',
                        action='store_true',
                        help='be verbose')
    parser.add_argument('--version',
                        action='version',
                        version=mcpartools.__version__)
    parser.add_argument('-p', '--particle_no',
                        type=int,
                        default=10000,
                        help='number of primary particles per job')
    parser.add_argument('-j', '--jobs_no',
                        type=int,
                        default=10,
                        help='number of parallel jobs')
    parser.add_argument('input',
                        type=str,
                        help='path to input configuration')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    opt = Options(args)
    generator = Generator(options=opt)
    generator.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
