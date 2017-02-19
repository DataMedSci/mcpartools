class Engine:
    def __init__(self, input_path, mc_run_script):
        self.input_path = input_path
        self.run_script_path = mc_run_script

    def find_external_files(self, run_input_dir):
        """Returns paths to found external files"""
        raise NotImplementedError()
