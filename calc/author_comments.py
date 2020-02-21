import sys, getopt
# read the excel file
import xlrd

def read_and_create_query( input_file ):
    # read the file
    wb = xlrd.open_workbook( input_file )
    sheet = wb.sheet_by_index( 0 )

    '''
    SELECT
        id, link_id, parent_id, subreddit_id, author, created_utc, permalink,
        CommentDetail.body
    FROM
        Comment
    WHERE
        author = '' AND
        ...
        ...
    INNER JOIN
        CommentDetail
    ON
        Comment.id = CommentDetail.id
    ;
    '''

    # forming the SQL command
    sql = str("SELECT "
        "id, link_id, parent_id, subreddit_id, author, created_utc, permalink, "
        "CommentDetail.body "
        "FROM Comment "
        "INNER JOIN "
        "CommentDetail "
        "ON Comment.id = CommentDetail.id "
        "WHERE "
    )

    for i in range( 0, sheet.nrows ):
        sql = "{} {} '{}'".format( sql, "author = ", str(sheet.cell_value( i, 0 )) )
        if( i != sheet.nrows - 1 ):
            sql = "{} {}".format( sql, "AND" )
    print( sql )

def main( argv ):
    # command line arguments
    opts, args = getopt.getopt( argv, "hi:", [ "ifile=" ] )

    input_file = None

    for opt, arg in opts:
        if opt == '-h':
            print( '[HELP] author_comments.py -i <excel_file>' )
            sys.exit()
        elif opt in ( "-i", "--ifile" ):
            input_file = arg

    if( input_file is None ):
        print( "[ERROR] Please specify the path of the excel file!" )
        sys.exit()
    else:
        read_and_create_query( input_file )

if __name__ == '__main__':
    main( sys.argv[1:] )