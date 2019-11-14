import threading
import queue
import time
import textwrap
from traceback import format_exc
import os

# global settings
import config
# utility collection
import utils

# general settings --------------------
msg_title = '[worker]'
# -------------------- general settings

# self-defined classes ---------------------------------------------
class worker():
    # constructor
    def __init__( self, name="worker", path_data=config.path_data, timeout=10, concurrent=10 ):
        
        # name of the task
        self.name = name
        self.path_err = os.path.join( config.path_failed, f'{name}_failed.json' )

        self.timeout = timeout
        self.concurrent = concurrent
        self.work_funct = None

        self.obj_list = []
        self.err_list = []

        self.job_queue = queue.Queue()
        self.lock = threading.Lock()
        self.finished = 0
        self._spawn()

    ''' clear temp storages and parameters used by this class '''
    def reset( self ):
        self.obj_list = []
        self.err_list = []
        self.finished = 0

    ''' assign the name of the task. Simultaneously, the pathes for data commitment are created '''
    def name_with( self, name ):
        ''' consume name and reconfigure paths '''
        self.name = name
        self.path_err = os.path.join( config.path_failed, f'{name}_failed.json' )
        return self

    ''' setting the working function '''
    def work_with( self, funct ):
        self.work_funct = funct
        return self

    ''' set the data to be parsed '''
    def input( self, obj_list ):
        self.reset()
        self.obj_list = obj_list
        return self

    ''' ignitiate '''
    def run( self ):
        # print( f'''{msg_title} Number of items: {len( self.obj_list )}''')
        # for obj in self.obj_list: self.job_queue.put( obj )
        # self.job_queue.join()

        # print( f'''{msg_title} Operations finished!''' )

        # retrieve only the obj from the failure list
        def create_list( l ): return list( map( lambda x: x[ 'obj' ], l ) )

        # record the previous status
        pre_list = None

        # still have item in both of the list
        while( self.obj_list or self.err_list ):
            # re-append the failed item to the obj list and try again
            if( len( self.err_list ) ): self.obj_list.extend( create_list( self.err_list ) )

            # items that keep failed!
            if( pre_list and sorted( self.obj_list, key=lambda i: i[ 'id' ] ) == pre_list ):
                self._record_failure()
                utils.create_thread_report( len(self.obj_list), \
                                            self.finished, \
                                            len(self.err_list), \
                                            msg="{} Encountered errors".format( msg_title ) )
                return
            
            # record the current status for the next iteration
            pre_list = sorted( self.obj_list, key=lambda i: i[ 'id' ] )
            # clear failure list
            self.err_list.clear()

            print( f'''{msg_title} Number of items: {len( self.obj_list )}''')
            for obj in self.obj_list: self.job_queue.put( obj )
            self.job_queue.join()

            # reset
            self.obj_list.clear()
            self.finished = 0

        print( f"{msg_title} Operation finished successfully!" )


    ''' save the failed list of obj '''
    def _record_failure( self ): utils.write_to_json( self.path_err, self.err_list )

    ''' things for the thread to do '''
    def _job( self ):
        while True:
            obj = self.job_queue.get()
            try:
                self.work_funct( obj )
                self.lock.acquire()
            except Exception as err:
                # append the failed item with error msg to error record list
                self.err_list.append( { 'obj': obj, 'err': str(err) } )
                self.lock.acquire()
            finally:
                self.finished += 1
                print( f'''{msg_title} Process: {100 * self.finished / len( self.obj_list ):.2f}%''', end='\r' )
                self.lock.release()
                self.job_queue.task_done()

    ''' creating the threads '''
    def _spawn( self ):
        for _ in range( 0, self.concurrent ):
            t = threading.Thread( target=self._job )
            t.daemon = True
            t.start()
# --------------------------------------------- self-defined classes

def run_worker( name, data, work_funct ):

    w = worker( name="test", concurrent=config.concurrent, timeout=config.timeout )

    w.name_with( name )
    w.input( data )
    w.work_with( work_funct ).run()