#!/usr/bin/env python3
#
# A quirky server that spits out the right (and the wrong) data
#


from flask import Flask, abort, send_file
import io
import os

SERVE_DIR = './data'
SERVE_FILENAME = 'malham-2877857.jpg'
CHUNK_SIZE = 1024*1024 # 1 Megabyte chunks

g_memfile = None
# read file data to memory
with open(os.path.join(SERVE_DIR, SERVE_FILENAME), 'rb') as bites:
    fulldata = bites.read()



app = Flask(__name__)

# this serves one chunk of maximum 1M at a time.
@app.route('/chunk/<int:n>')
def get_chunk(n):
    g_file = io.BytesIO(fulldata)
    g_file.seek(n*CHUNK_SIZE)
    g_chunk = io.BytesIO(g_file.read(CHUNK_SIZE))
    return send_file(g_chunk,
            attachment_filename=SERVE_FILENAME+f'.part{n}',
            mimetype='application/octet-stream'
            )



# this serves the whole file.
@app.route('/getfile')
def get_complete_file():
    g_file = io.BytesIO(fulldata) 
    return send_file(
                 g_file,
                 attachment_filename=SERVE_FILENAME,
                 mimetype='image/jpg'
           )

if __name__ == '__main__':
    app.run(debug=False)
