import argparse

from mcpartools.generator import Generator
from mcpartools.generator import Options


def main():
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
    args = parser.parse_args()

    print("number of particles", args.particle_no)
    print("number of jobs", args.jobs_no)

    opt = Options(args)
    generator = Generator(option=opt)
    generator.run()

if __name__ == '__main__':
    main()
