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
url = 'airegdlpip.cptlhu1n34ei.us-west-1.rds.amazonaws.com'
user = 'postgres'
pw = 'pipguadalajara'
db = 'postgres'
#access_key_id = 'AKIA3BSMXZ65WZYEI3AR'
