#!/usr/bin/python
import cgi
import psycopg2
import json

def main():
    form = cgi.FieldStorage()

    db = psycopg2.connect(database='student23', user='student23')
    c = db.cursor()

    response = {}
    response['posts'] = []
    parent = int(form.getvalue('post', '0'))
    skip = int(form.getvalue('skip', '0'))
    if parent != 0:
        c.execute('SELECT id, name, title, timestamp, image, filename, comment, parent FROM board WHERE id = %s ORDER BY lastupdate DESC', (parent,))
        postQuery = c.fetchone()
        post = queryToObj(postQuery)
        post['parent'] = postQuery[7]
        response['posts'].append(post)

    #Get a list of all of the posts
    if parent == 0:
        c.execute('SELECT id, name, title, timestamp, image, filename, comment FROM board WHERE parent = 0 ORDER BY lastupdate DESC')
    else:
        c.execute('SELECT id, name, title, timestamp, image, filename, comment FROM board WHERE parent = %s ORDER BY lastupdate ASC', (parent,))
    if parent == 0:
        if skip > 0:
            c.fetchmany(skip)
        # rows = c.fetchmany(10)
        rows = c.fetchall()
    else:
        rows = c.fetchall()

    #For each row in the table, print XML for an entry
    for row in rows:
        post = queryToObj(row)
        if parent == 0:
            post['posts'] = []
            c.execute('SELECT id, name, title, timestamp, image, filename, comment FROM board WHERE parent = %s ORDER BY lastupdate ASC', (row[0],))
            children = c.fetchmany(5)
            for child in children:
                childPost = queryToObj(child)
                post['posts'].append(childPost)
        response['posts'].append(post)
    db.close()

    print("Content-type: application/json\n")
    print(json.dumps(response))

def queryToObj(row):
    post = {}
    post['id'] = row[0]
    post['name'] = row[1]
    post['title'] = row[2]
    post['timestamp'] = str(row[3])
    post['image'] = row[4]
    post['filename'] = row[5]
    post['comment'] = row[6]

    return post

if (__name__ == '__main__'):
    main()

