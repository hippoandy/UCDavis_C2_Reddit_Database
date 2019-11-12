'''
'''

# database connection settings ------------------------------
mdb_addr = '127.0.0.1'
mdb_port = 3306
mdb_user = 'andy'
mdb_pass = 'test'
# ------------------------------ database connection settings

# file opertions --------------------------------------------
read_buffer = 10000

path_data = r'./data/'
path_failed = r'./error/'


encoding_default = 'utf-8'
# -------------------------------------------- file opertions

# thread settings -------------------------------------------
concurrent = 10
timeout = 10

partition = 100
# ------------------------------------------- thread settings