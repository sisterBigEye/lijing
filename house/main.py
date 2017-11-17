#-*- coding:utf-8 -*-
import logging
import logging.config
#多模块日志的使用

logging.config.fileConfig('logging.conf')
root_logger = logging.getLogger('root')
root_logger.debug('test root logger...')

logger = logging.getLogger('main')
logger.info('test main logger')
logger.info('start import mould \'mod\'....')

import mod
logger.debug('let\'s test mod testLogger()')
mod.testLogger()

root_logger.info('finish test...')


