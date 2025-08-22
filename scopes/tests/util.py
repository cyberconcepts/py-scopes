# scopes.tests.util

import logging

def setup_logging(config):
    hdlr = logging.getLogger().handlers[-1]
    logging.getLogger().removeHandler(hdlr) # remove NullHandler added by testrunner
    logging.basicConfig(filename=config.log_file, level=config.log_level, 
                        format=config.log_format, datefmt=config.log_dateformat)


