'''
'''

# database connection settings ------------------------------
mdb_addr = '127.0.0.1'
mdb_port = 3306
mdb_user = 'andy'
mdb_pass = 'test'
# mdb_addr = '127.0.0.1'
# mdb_port = 8889
# mdb_user = 'reddit'
# mdb_pass = 'test'

mdb_db = 'reddit_comments'
# ------------------------------ database connection settings

# file/data/value opertions ---------------------------------
read_buffer = 10000

path_data = r'./data/'
path_failed = r'./error/'


encoding_default = 'utf-8'

tsstr_default = '%Y-%m-%d %H:%M:%S'
# -------------------------------------------- file opertions

# thread settings -------------------------------------------
concurrent = 10
timeout = 10

partition = 1000
# ------------------------------------------- thread settings