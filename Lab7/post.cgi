#!/usr/bin/python

import psycopg2
import cgi
import os
import imghdr
from hashlib import blake2b
from base64 import b32encode
import json

#Custom Errors:
class NoImage(Exception):
   pass

class NoComment(Exception):
   pass

class InvalidParent(Exception):
   pass

class NameTooLong(Exception):
   pass

class TitleTooLong(Exception):
   pass

class ImageTooLarge(Exception):
   pass

class InvalidImageFormat(Exception):
   pass

class CommentTooLong(Exception):
   pass

SECRET = b'sto_0PRo[Q_8!Ji1`kg:z%L8dps0m%w*^1OY$nuw1`NC!S;+a$JOlP3+UmbaRcX'

def main():
    # Prepare response
    response = {}

    # Connect to the database
    db = psycopg2.connect(database='student23', user='student23')
    c = db.cursor()

    try:
        # Fetch information from the web form
        form = cgi.FieldStorage()
        # TODO: Check DB for Valid Parent with 'SELECT parent FROM board WHERE id = %s'
        parent = int(form.getvalue('parent', '0'))
        if parent != 0:
            c.execute('SELECT parent FROM board WHERE id = %s', (parent,))
            rootParent = c.fetchone()
            if (len(rootParent) < 1 or rootParent[0] != 0):
                raise InvalidParent

        name = form.getvalue('name', 'Anonymous')
        if len(name) > 90:
            raise NameTooLong
        if len(name) < 1:
            name = "Anonymous"

        title = form.getvalue('title', '')
        if len(title) > 80:
            raise TitleTooLong

        comment = ''
        comment = form.getvalue('comment', '')
        if len(comment) < 1:
            raise NoComment

        image = None
        if 'image' in form:
            image = form['image']
        elif parent == 0:
            raise NoImage

        filename = image.filename[:260]
        fname = ''
        image.file.seek(0,2)
        if image.file.tell() == 0 and parent == 0:
            raise NoImage
        elif image.file.tell() < 4000000 and image.file.tell() != 0:
            image.file.seek(0)
            imagedata = image.file.read()
            imageformat = imghdr.what('', imagedata)
            if imageformat in {'png', 'jpeg', 'gif', 'bmp', 'webp'}:
                fname = '{}.{}'.format(b32encode(blake2b(imagedata + SECRET).digest()).decode('utf-8').lower()[:8], imageformat)
                dest = open(os.path.join('usrimg', fname), 'wb')
                image.file.seek(0)
                while 1:
                    copy_buffer = image.file.read(100000)
                    if not copy_buffer:
                        break
                    dest.write(copy_buffer)
            else:
                raise InvalidImageFormat
        elif image.file.tell() != 0:
            raise ImageTooLarge

        # Insert the form data into the database
        c.execute('INSERT INTO board (parent, name, title, image, filename, comment) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id', (parent, name, title, fname, filename, comment))
        response['success'] = c.fetchone()[0]
        if (parent != 0):
            c.execute('UPDATE board SET lastupdate = now(), children = children + 1 WHERE id = %s', (parent,))
        db.commit()
        db.close()
    except NoImage:
        response['error'] = 'Posts Require an Image.'
    except NoComment:
        response['error'] = 'All Posts Require a Message.'
    except InvalidParent:
        response['error'] = 'Invalid Parent Post.'
    except NameTooLong:
        response['error'] = 'Name Too Long. Maximum: 80 characters.'
    except TitleTooLong:
        response['error'] = 'Title Too Long. Maximum: 80 characters.'
    except ImageTooLarge:
        response['error'] = 'Image Too Large. Maximum: 4MB.'
    except InvalidImageFormat:
        response['error'] = 'Invalid Image Format. Supported: PNG, JPEG, GIF, BMP, WEBP.'
    except CommentTooLong:
        response['error'] = 'Comment Too Long. Maximum: 15,000 characters.'
    except Exception as e:
        response['error'] = 'Invalid Submission. Try again.  ' + str(e)

    print('Content-type: application/json\n')
    print(json.dumps(response))

if (__name__ == "__main__"):
    main()
