'''
'''
import json
import sys, getopt

# global settings
import config
# utility collection
import utils
# threaded worker
import thread

def test( x ): print( "Hello world!! " + str(x) )
# def test( x ): print( "Hello world!! " + x )

def try_retrieval( obj, key ):
    try:    return obj[ key ]
    except: return None

# parse the input data points
def parse( obj ):
    # connect to the database
    db, cur = utils.db_connect()
    cur.execute( '''use {};'''.format( config.mdb_db ) )

    ### Comments
    cid = try_retrieval( obj, 'id' )
    # this data point doesn't even have an id, just ignore it!
    if( cid == None ): return
    link_id = try_retrieval( obj, 'link_id' )
    parent_id = try_retrieval( obj, 'parent_id' )

    ups = try_retrieval( obj, 'ups' )           # None != 0
    downs = try_retrieval( obj, 'downs' )       # None != 0
    score = try_retrieval( obj, 'score' )
    gilded = try_retrieval( obj, 'gilded' )
    controversiality = try_retrieval( obj, 'controversiality' )
    permalink = try_retrieval( obj, 'permalink' )
    created_utc = utils.datetime_to_str( utils.unix_to_datetime( try_retrieval( obj, 'created_utc' ) ) )
    retrieved_on = utils.datetime_to_str( utils.unix_to_datetime( try_retrieval( obj, 'retrieved_on' ) ) )

    ### CommentDetails
    name = try_retrieval( obj, 'name' )
    body = try_retrieval( obj, 'body' )
    archived = try_retrieval( obj, 'archived' )     # None != False
    edited = try_retrieval( obj, 'edited' )         # None != False
    stickied = try_retrieval( obj, 'stickied' )     # None != False
    distinguished = try_retrieval( obj, 'distinguished' )
    removal_reason = try_retrieval( obj, 'removal_reason' )
    score_hidden = try_retrieval( obj, 'score_hidden' )

    ### Subreddit
    subreddit_id = try_retrieval( obj, 'subreddit_id' )
    subreddit = try_retrieval( obj, 'subreddit' )
    subreddit_name_prefixed = try_retrieval( obj, 'subreddit_name_prefixed' )
    subreddit_type = try_retrieval( obj, 'subreddit_type' )

    ### Author
    author = try_retrieval( obj, 'author' )
    author_fullname = try_retrieval( obj, 'author_fullname' )
    author_created_utc = try_retrieval( obj, 'author_created_utc' )
    if( author_created_utc != None ):
        author_created_utc = utils.datetime_to_str( utils.unix_to_datetime( author_created_utc ) )
    # author_flair_css_class = try_retrieval( obj, 'author_flair_css_class' )
    # author_flair_text = try_retrieval( obj, 'author_flair_text' )

    '''
    insertion ordering: Author/Subreddit -> Comment -> CommentDetail
    '''
    ### insert into Author
    cur.execute( '''
        INSERT INTO Author (author, author_fullname, author_created_utc) VALUES
        (%s, %s, %s) ON DUPLICATE KEY UPDATE    
        author_fullname=%s, author_created_utc=%s
    ''', (author, author_fullname, author_created_utc,
            author_fullname,
            author_created_utc) )

    ### insert into Subreddit
    cur.execute( '''
        INSERT INTO Subreddit (id, subreddit_name, subreddit_name_prefixed, subreddit_type) VALUES
        (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE    
        subreddit_name=%s, subreddit_name_prefixed=%s, subreddit_type=%s
    ''', (subreddit_id, subreddit, subreddit_name_prefixed, subreddit_type, subreddit, subreddit_name_prefixed, subreddit_type) )

    ### insert into Comment
    cur.execute( '''
        INSERT IGNORE INTO Comment (id, link_id, parent_id, subreddit_id, author, score, gilded, ups, downs, controversiality, created_utc, retrieved_on, permalink) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (cid, link_id, parent_id, subreddit_id, author, score, gilded, ups, downs, controversiality, created_utc, retrieved_on, permalink) )

    ### insert into CommentDetail
    cur.execute( '''
        INSERT IGNORE INTO CommentDetail (id, name, body, archived, edited, stickied, distinguished, removal_reason, score_hidden) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (cid, name, body, archived, edited, stickied, distinguished, removal_reason, score_hidden) )

    # close the database connection
    utils.db_close( db )

def main( argv ):
    # command line arguments
    opts, args = getopt.getopt( argv, "hi:s:", [ "ifile=", "start=" ] )
    # input file pointer
    inputfile = None
    # default value for start idx
    start = 0
    for opt, arg in opts:
        if opt == '-h':
            print( 'insertion.py -i <input_file> -s <start_idx>' )
            sys.exit()
        elif opt in ( "-i", "--ifile" ): inputfile = arg
        elif opt in ( "-s", "--start" ):
            try: start = int(arg)
            except:
                print( "Parameter start should be int!" )
                sys.exit()

    if( inputfile is not None and utils.is_file_exist( inputfile ) ):
        # init the worker class
        w = thread.init_worker( concurrent=config.concurrent, timeout=config.timeout )

        with open( inputfile, 'r', buffering=config.read_buffer ) as f:
            data = []
            idx, c = 0, 0
            for l in f:
                if( idx >= start ):
                    try: dpoint = json.loads( l )
                    except: continue

                    c += 1

                    data.append( dpoint )
                    if( c == config.partition ):
                        print( f"insert_{idx - config.partition}-{idx}" )
                        thread.run_worker( w, f"insert_{idx - config.partition}-{idx}", data, parse )
                        # clear
                        c = 0
                        data = []
                idx += 1
            if( len( data ) ):
                print( f"insert_{idx-len(data)}-{idx}" )
                thread.run_worker( w, f"insert_{idx-len(data)}-{idx}", data, parse )
    else:
        print( "[WARNING] File not exists or not specified!" )

if __name__ == '__main__': main( sys.argv[1:] )