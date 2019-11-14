'''
'''

import mysql.connector
import errno
import os
import json, textwrap

from datetime import datetime

# global settings
import config

# database operations --------------------------------------------------
def db_connect():
    # connect to mysql
    mydb = mysql.connector.connect(
        host=config.mdb_addr,
        port=config.mdb_port,
        user=config.mdb_user,
        passwd=config.mdb_pass
    )
    mycur = mydb.cursor()
    mydb.autocommit = True
    return (mydb, mycur)

def db_close( db ): db.close()
# -------------------------------------------------- database operations

# equivalent to UNIX command: '$ mkdir -p'
def mkdir_p( path ):
    try: os.makedirs( path )
    except OSError as exc:
        if( exc.errno == errno.EEXIST and os.path.isdir( path ) ): pass
        else: raise IOError( f'Error while creating the folder with path: {path}' )

# create the folder for a given folder path
def create_dir( path ): mkdir_p( path )

# create the parent folder for a given file path
def create_parent_dir( path ):
    if( not is_parent_dir_exist( path ) ):
        path_parent = os.path.dirname( path )
        mkdir_p( path_parent )

# check if dir exist
def is_dir_exist( path ):
    if( os.path.exists( path ) ): return True
    else: return False

# check if parent dir exist
def is_parent_dir_exist( path ):
    path_parent = os.path.dirname( path )
    if( not os.path.exists( path_parent ) ): return False
    else: return True

# saver file to json
def write_to_json( path, data, encode=config.encoding_default ):
    ''' write json to current dir, path="out path", data="json serializable data" '''
    create_parent_dir( path )
    with open( path, 'w+', encoding=encode, errors='ignore' ) as f:
        json.dump( data, f )

def create_thread_report( len_data, finished, len_err, msg="Finished" ):
    print(textwrap.dedent(f'''\
        {msg}:
            Totally: {len_data}
            Number of data completed: {finished}
            Number of failure: {len_err}
    '''))

def clean_str( str ): return str.replace( '\n', '' ).replace( '\r', '' ).replace( '\t', '' )

def unix_to_datetime( ts ):
    ts = clean_str( str(ts) )
    return datetime.utcfromtimestamp( int(ts) )

def datetime_to_str( dt, format=config.tsstr_default ): return dt.strftime( format )