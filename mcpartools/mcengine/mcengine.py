import os


class Engine:
    """
    TODO
    """
    def __init__(self, input_path, mc_run_script, collect_method):
        self.input_path = input_path
        self.run_script_path = mc_run_script
        self.collect_method = collect_method

    _collect_action = {
        'mv': """TRANSPORT_COMMAND=mv
for INPUT_FILE in $INPUT_WILDCARD; do
  $TRANSPORT_COMMAND $INPUT_FILE $OUTPUT_DIRECTORY
done""",
        'cp': """TRANSPORT_COMMAND=cp
for INPUT_FILE in $INPUT_WILDCARD; do
  $TRANSPORT_COMMAND $INPUT_FILE $OUTPUT_DIRECTORY
done""",
        'image': "convertmc image --many \"$INPUT_WILDCARD\" $OUTPUT_DIRECTORY -q",
        'plotdata': "convertmc plotdata --many \"$INPUT_WILDCARD\" $OUTPUT_DIRECTORY -q"
    }

    def write_collect_script(self, output_dir):
        output_dir_abs_path = os.path.abspath(output_dir)

        collect_action = self._collect_action.get(self.collect_method, "")
        contents = self.collect_script_content.format(output_dir=output_dir_abs_path,
                                                      collect_action=collect_action)
        out_file_name = "collect.sh"
        out_file_path = os.path.join(output_dir, out_file_name)
        out_fd = open(out_file_path, 'w')
        out_fd.write(contents)
        out_fd.close()
        os.chmod(out_file_path, 0o750)

    def find_external_files(self, run_input_dir):
        """Returns paths to found external files"""
        raise NotImplementedError()
