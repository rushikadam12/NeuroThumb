import logging
import os

# ---- Basic logger setup ----
logger = logging.getLogger("thumb_logger")
logger.setLevel(logging.DEBUG)  # DEBUG shows all messages

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Formatter for timestamps + log level + message
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

# Optional: log to file
log_file = os.path.join(os.getcwd(), "thumb_debug.log")
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
