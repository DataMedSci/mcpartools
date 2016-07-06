class Options:
    def __init__(self, args):
        self.particle_no = args.particle_no
        self.jobs_no = args.jobs_no


class Generator:
    def __init__(self, options):
        self.options = options

    def run(self):

        # generate main dir according to date
        self.generate_main_dir()

        # generate submit script
        self.generate_submit_script()

        # generate tmp dir with workspace
        self.generate_workspace()

        # copy input files
        self.copy_input()

        # save logs
        self.save_logs()

    def generate_main_dir(self):
        pass

    def generate_submit_script(self):
        pass

    def generate_workspace(self):
        pass

    def copy_input(self):
        pass

    def save_logs(self):
        pass
