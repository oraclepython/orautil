import logging
import sys

__LOG_FORMAT = f"%(asctime)s %(levelname)8s: %(message)s"


def initialize_logging(caller: str, log_format: str = __LOG_FORMAT) -> logging:
    """
    Initialize a logger
    :param caller: The callers name as a fallback if the target is not found.
    :type caller: str
    :param log_format: logging format with a default value
    :type log_format: str
    :return: logger
    :rtype: :class:`logging.logger
    """
    try:
        if caller in logging.Logger.manager.loggerDict:
            logger = logging.getLogger(caller)
        else:
            logger = logging.getLogger(caller)

            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)

            logger.addHandler(handler)
    except Exception as e:
        raise RuntimeError(f"Unable to initialize logger {caller}: {e}")
    return logger
