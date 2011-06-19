#!/usr/bin/python
# -*- coding: utf-8 -*

import sys
import MySQLdb
from Config import *
from ArticleParser import *

COLON = u'\uff1a'
ADVANTAGES = u'\u512a\u9ede:'
ATTACHMENT = u'\n\u9644\u4ef6\n'

db = MySQLdb.connect(host=DATABASE_HOST, user=DATABASE_USERID, passwd=DATABASE_PASSWD, db=DATABASE_NAME, charset='utf8', \
				 	use_unicode=True)
				
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER_SET_CLIENT=utf8;')
cursor.execute('SET CHARACTER_SET_CONNECTION=utf8;')
cursor.execute('SET CHARACTER_SET_RESULTS=utf8;')

def get_main_content_from_raw_email(emailid, table_name=EMAIL_TABLE_NAME):
    sql_command = 'select body from %s where id=%s;'%(table_name, emailid)
    cursor.execute(sql_command)
    body_text = cursor.fetchall()[0][0].replace('\r','\n')

    tags_to_remove = TAGS_TO_REMOVE
    tags_to_remove.update({"td":["<td ",">"], "tr":["<tr ",">"], "table":["<table ",">"], \
							'href':['<a href', ">"],'meta':['<meta ','>']})
    body_text = RemoveTags(body_text, tags_to_remove)
    get_rid_of = ['<tr>', '</tr>', '<td>', '</td>', '</center>', '</body>', '</html>','</head>','<body>','<center>']
    for r in get_rid_of:
        body_text = body_text.replace(r,'')
    while '\n\n\n' in body_text:
        body_text = body_text.replace('\n\n\n','\n')

    body_text = body_text.replace(COLON+'\n\n', COLON).replace(COLON+'\n',COLON)
    main_content_begin = body_text[body_text.find(ADVANTAGES)+10:].find('\n\n')+body_text.find(ADVANTAGES) + 10
    main_content_end = body_text.find(ATTACHMENT)
    main_content = body_text[main_content_begin:main_content_end]
    return main_content

