import logging

import logfire

logfire.configure(send_to_logfire=False, metrics=False)
logging.basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
