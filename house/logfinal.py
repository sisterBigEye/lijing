'''
Created on 2012-8-12

@author: walfred
@module: loggingmodule.FinalLogger
'''

import logging.handlers
import logging


class FinalLogger:
    logger = None

    levels = {"n" : logging.NOTSET,"d" : logging.DEBUG,"i" : logging.INFO,"w" : logging.WARN,
    "e" : logging.ERROR,
    "c" : logging.CRITICAL}

    log_level = "d"
    log_file = "final_logger.log"
    log_max_byte = 10 * 1024 * 1024;
    log_backup_count = 5

    @staticmethod
    def getLogger():
        if FinalLogger.logger is not None:
            return FinalLogger.logger
        FinalLogger.logger = logging.Logger("loggingmodule.FinalLogger")
        log_handler = logging.handlers.RotatingFileHandler(filename = FinalLogger.log_file,maxBytes = FinalLogger.log_max_byte,backupCount = FinalLogger.log_backup_count)
        log_fmt = logging.Formatter("[%(levelname)s][%(funcName)s][%(asctime)s]%(message)s")
        log_handler.setFormatter(log_fmt)
        FinalLogger.logger.addHandler(log_handler)
        FinalLogger.logger.setLevel(FinalLogger.levels.get(FinalLogger.log_level))
        return FinalLogger.logger

if __name__ == "__main__":
    logger = FinalLogger.getLogger()
    logger.debug("this is a debug msg!")
    logger.info("this is a info msg!")
    logger.warn("this is a warn msg!")
    logger.error("this is a error msg!")
    logger.critical("this is a critical msg!")
