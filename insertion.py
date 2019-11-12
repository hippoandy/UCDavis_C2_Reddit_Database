'''
'''

import json
import sys

# global settings
import config
# utility collection
import utils
# threaded worker
import thread

def test( x ): print( "Hello world!! " + str(x) )
# def test( x ): print( "Hello world!! " + x )

# parse the input data points
def parse( x ):
    print( x )

if __name__ == '__main__':

    # # connect to the database
    # db, cur = utils.db_connect()

    # print( db )
    # print( cur )

    # # close the database connection
    # utils.db_close( db )

    with open( './sample_data.json', 'r',buffering=config.read_buffer ) as f:
        for l in f.readlines():
            point = json.loads( l )
            
            parse( point )

            break

    # data = []
    # for i in range( 0, 100 ): data.append( i )

    # w = thread.worker( name="test", concurrent=config.concurrent, timeout=config.timeout )
    # w.input( data )
    # w.work_with( test ).run()