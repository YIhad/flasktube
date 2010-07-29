import os
import flask
from flask import Flask, request, redirect, url_for, abort, session, escape
from werkzeug import secure_filename
#import bottle
#from bottle import route, run, redirect, abort, request
from time import time, sleep
import subprocess
#import bikcmpdb
ip_address="192.168.1.13"
maintmode="0"
UPLOAD_FOLDER = '/home/jason/fossvideo/temp/'
STATIC_FOLDER = "/home/jason/fossvideo/static/"
VIDEO_FOLDER = "/home/jason/fossvideo/video/"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) #Not really used...yet.

app = Flask(__name__)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
	return redirect(url_for('upload'))

@app.route('/upload')
def upload():
	if 'username' in session:
		return '''
		<!doctype html>
		<title>Upload new File</title>
		<h1>Upload new File</h1>
		<form action="/do/upload" method=post enctype=multipart/form-data>
		<p><input type=file name=file>
		<input type=submit value=Upload>
		</form>
		'''
	return "Please login."
@app.route('/do/upload', methods=['POST'])
def do_upload():
	vidid=int(time())
    #return datafile.file.read()
	#f = open('/home/jason/fossvideo/temp/'+str(vidid), 'w')
	#if 'username' in session:
	
	#if maintmode == "0":
	if request.method == 'POST':
		file = request.files['file']
		if 'username' in session:
			if file: #and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(UPLOAD_FOLDER, str(vidid)))
	#f.write(datafile.file.read())
	#f.close()
            
              	subprocess.Popen(["/usr/bin/ffmpeg", "-i", str(vidid), VIDEO_FOLDER+str(vidid)+".flv"], cwd=UPLOAD_FOLDER)
                print "Converted video"
                subprocess.Popen(["/bin/cp", STATIC_FOLDER+"default.html", STATIC_FOLDER+str(vidid)+".html.tmp"], cwd=STATIC_FOLDER)
                sleep(1)
                f = open(STATIC_FOLDER+str(vidid)+'.html.tmp', 'r')
                fread=f.read()
                freplaced=fread.replace('replacewithvideo',"http://"+ip_address+":5000/raw_video/"+str(vidid)+".flv").replace('uploaderuser',escape(session['username']))
                f.close()
                f = open(STATIC_FOLDER+str(vidid)+'.html', 'w')
                f.write(freplaced)
                f.close()
                return 'Video uploaded sucessfully.</br></br>Your video is at: <A HREF="http://'+ip_address+':5000/video/'+str(vidid)+'">http://'+ip_address+':5000/video/'+str(vidid)+'</A>'
        else:
			return "You are not logged in."
            #return "OK"

@app.route('/video/<vidid>')
def play_video(vidid):
	try:
		f = open(STATIC_FOLDER+vidid+".html", 'r')
		fread=f.read()
		#return template('default', content=fread)
		return fread#+"<br></br><p>Submitted by: "+username+"</p>"
	except IOError:
	#	abort(404, "File not found.")
		abort(404)
@app.route('/raw_video/<raw_file>')
def rawvideo(raw_file):
	try:
		f = open(VIDEO_FOLDER+raw_file, 'r')
		fread=f.read()
		#return template('default', content=fread)
		return fread
	except IOError:
		abort(404)#, "File/video not found.")
	
#logins (added by bikcmp, Jul 29, 2010)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        #return redirect(url_for('index'))
        return "You are now logged in."
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
	
@app.route('/logout')
def logout():
    # remove the username from the session if its there
    session.pop('username', None)
    #return redirect(url_for('index'))
    return "You are now logged out."


app.secret_key = 'HJFHGSYUKEYTW786F7I675jkyftehyas6a7'
app.run(debug=True,host='0.0.0.0')