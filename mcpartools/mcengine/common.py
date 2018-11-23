import logging
import os

from mcpartools.mcengine.fluka import Fluka
from mcpartools.mcengine.shieldhit import ShieldHit

logger = logging.getLogger(__name__)


class EngineDiscover:
    def __init__(self):
        pass

    @classmethod
    def get_mcengine(cls, input_path, mc_run_script, collect_method, mc_engine_options, dump_opt):
        if os.path.isfile(input_path) and input_path.endswith('.inp'):
            logger.debug("Discovered MC engine FLUKA")
            return Fluka(input_path, mc_run_script, collect_method, mc_engine_options, dump_opt)
        elif os.path.isdir(input_path):
            logger.debug("Discovered MC engine SHIELDHIT")
            return ShieldHit(input_path, mc_run_script, collect_method, mc_engine_options, dump_opt)
        else:
            logger.error("Input file doesn't match available MC codes")
            return None
