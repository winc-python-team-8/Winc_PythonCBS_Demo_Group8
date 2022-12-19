import logging
import CBS_Logging.Constants as lOC

logging.basicConfig(filename=lOC.LOGGING_FILE_NAME,
                    filemode='a',
                    format='%(asctime)s %(levelname)s-%(message)s',
                    level=logging.INFO,
                    datefmt=lOC.LOGGING_DATE_FORMAT)

print('logging is enabled for the project')
logging.info('started with logging class')

