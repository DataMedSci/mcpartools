import logging
import os

logger = logging.getLogger(__name__)


class Engine:
    """
    Base class for all MC engines
    """
    def __init__(self, input_path, mc_run_script, collect_method, mc_engine_options):
        """
        :param input_path: Path to the input file(s): to the directory or to a single file
        :param mc_run_script:  Path to the binary file with Monte-Carlo code executable
        :param collect_method:  String denoting result collection method (i.e. 'mv', 'cp', 'image')
        :param mc_engine_options: String which may be either list of MC engine options, enclosed in square brackets
        or path to the file with options (in case of very long text)
        """
        self.input_path = input_path
        self.run_script_path = mc_run_script
        self.collect_method = collect_method
        self.engine_options = mc_engine_options

        if not mc_engine_options:  # check if options were provided
            self.engine_options = ""
            logger.debug("No engine options")
        elif os.path.exists(mc_engine_options):  # check if we have file with options content
            opt_fd = open(mc_engine_options, 'r')
            options_file_content = opt_fd.read()
            opt_fd.close()
            self.engine_options = options_file_content
            logger.debug("Engine options file contents: " + options_file_content)
        else:  # assume options are inside the square brackets and unpack them
            self.engine_options = mc_engine_options[1:-1]
            logger.debug("Engine options arguments: " + self.engine_options)

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
