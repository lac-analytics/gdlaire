"""Global settings, can be configured by user with utils.config()."""

import logging as lg

# locations to save data, logs, images, and cache
data_folder = "data"
logs_folder = "logs"

# write log to file and/or to console
log_file = True
log_level = lg.INFO
log_name = "aireGDL"
log_filename = "aireGDL"

# Database settings
url = 'pip-gdl.cxkuumj8eis0.us-west-2.rds.amazonaws.com'
user = 'pipderive'
pw = 'aireGuadalajara'
db = 'postgres'
