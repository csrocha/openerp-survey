#!/usr/bin/python

import psycopg2
import re
import sys

re_path = re.compile(r'(\w+):(\w+)\.(\w+)')

def main(source, target):
    parameters = zip(['src_db', 'src_table', 'src_field'], re_path.match(source).groups())
    parameters.extend(zip(['tar_db', 'tar_table', 'tar_field'], re_path.match(target).groups()))
    parameters=dict(parameters)

    src_conn = psycopg2.connect("dbname={src_db}".format(**parameters))
    dst_conn = psycopg2.connect("dbname={tar_db}".format(**parameters))

    src_cur = src_conn.cursor()
    dst_cur = dst_conn.cursor()

    src_cur.execute('select {src_field},id from {src_table}'.format(**parameters))
    src_data = src_cur.fetchall()
    
    dst_cur.executemany('update {tar_table} set {tar_field}=%s where id=%s'.format(**parameters), src_data)

    dst_conn.commit()

    src_cur.close()
    dst_cur.close()

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
