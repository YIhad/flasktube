#This code is licensed under the GNU GPL v3 License.
#By bikcmp
import os
import flask
from flask import Flask, request, redirect, url_for, abort, session, escape
from werkzeug import secure_filename
#import bottle
#from bottle import route, run, redirect, abort, request
from time import time, sleep
import subprocess
import re
#import bikcmpdb
ip_address="192.168.1.14"
maintmode="0"
UPLOAD_FOLDER = '/home/jason/fossvideo/temp/'
STATIC_FOLDER = "/home/jason/fossvideo/static/"
VIDEO_FOLDER = "/home/jason/fossvideo/video/"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) #Not really used...yet.
#Make sure to make a blank file named "users", and "comments" (touch users and touch comments)
#Add users by manually editing the 'users' file, and make users each on a seperate line, with the format USERNAME PASSWORD.
DATABASE_FOLDER = "/home/jason/fossvideo/db/"

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
		comid=vidid
		file = request.files['file']
		if 'username' in session:
			uploader=escape(session['username'])
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
                #freplaced=fread.replace('replacewithvideo',"http://"+ip_address+":5000/raw_video/"+str(vidid)+".flv").replace('uploaderuser',escape(session['username']))
                freplaced=fread.replace('replacewithvideo',"http://"+ip_address+":5000/raw_video/"+str(vidid)+".flv").replace('uploadeduser',uploader).replace('replacecommentid',str(vidid))
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
		f = open(STATIC_FOLDER+vidid+".html", 'r')
		fread=f.read()
		#fi = open(DATABASE_FOLDER+'comments','r')
		#return template('default', content=fread)
		#vidcomments = fi.read()
		handle=open(DATABASE_FOLDER+'comments','r')
		#rawcomment=handle.read()
		#print handle.read()
		var = ""
		for line in handle.readlines():
			#var="
			if line.find(vidid+' ')!=-1:
				comment=" ".join(line.split()[2:]).strip('\r\n')
				print comment
				handle.close()
				#fread2=fread.replace("\r\n", "")
				comment_username = "".join(line.split()[1]).strip('\r\n')
				var+="<br></br><b>"+comment_username+"</b> <p>  </p>"+comment
		return fread+"<br></br>Comments: "+var
		#print "Falling back to no comment detected page!"
		#return fread
		#return fread+raw
		#.close()
		#comment=vidcomments.replace(vidid, "<br>")
				
	#except IOError:
	#	abort(404, "File not found.")
		#abort(404)
@app.route('/raw_video/<raw_file>')
def rawvideo(raw_file):
	try:
		f = open(VIDEO_FOLDER+raw_file, 'r')
		fread=f.read()
		#return template('default', content=fread)
		return fread
	except IOError:
		abort(404)#, "File/video not found.")

@app.route('/login', methods=['GET'])#, 'POST'])
def login():
	#if request.method == 'GET':
		return '''
        <form action="/do/login" method="post">
            <p>
            <p>Username</p><input type=text name=username>
            <br>
            <p>Password</p>
            <input type="password" name=password>
            <p><input type=submit value=Login>
        </form>
    '''
	
@app.route('/do/login', methods=['POST'])
def do_login():
	#if request.method == 'POST': Not needed because of methods=
			session['username'] = request.form['username']
			username = session['username']
			password=request.form['password']
			handle=open(DATABASE_FOLDER+'users','r')
			for line in handle.readlines():
				if line.find(username+' ')!=-1:
					realpassword=line.split()[1].strip('\r\n')
					if realpassword == password:
						return "You are now logged in."
					elif realpassword != password:
						return "Login failed."
					else:
						return abort(500)
			return abort(500)
	

@app.route('/logout')
def logout():
    # remove the username from the session if its there
    session.pop('username', None)
    #return redirect(url_for('index'))
    return "You are now logged out."
 
@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
	if request.method == 'POST':
		#username = session['username']
		createUser = request.form['username']
		createPassword = request.form['password']
		password=request.form['password']
		f=open(DATABASE_FOLDER+'users','a')
		f.write(createUser+" "+createPassword+"\n")
		f.close()
		return "User sucessfully added."
	#return '''
	return '''
        <form action="/createAccount" method="post">
            <p><input type=text name=username>
            <input type="password" name=password>
            <p><input type=submit value=Login>
        </form>
    '''
@app.route('/addComment', methods=['POST'])
def addComment():
	if request.method == 'POST':
		if 'username' in session:
			username = session['username']
			commentVid = request.form['vidid']
			commentComments=request.form['comments']
			f=open(DATABASE_FOLDER+'comments','a')
			print username+" "+commentVid+" "+commentComments
			f.write(commentVid+ " "+username+" "+commentComments+"\n")
			f.close()
			return "Added comment."
		return redirect(url_for('login'))
	elif request.method == 'GET':
		return abort(404)
@app.route('/debug/comment')
def show_comment():
	handle=open(DATABASE_FOLDER+'comments','r')
	for line in handle.readlines():
				if line.find('1280552091'+' ')!=-1:
					comment=line.split()[1].strip('\r\n')
					return comment
					
	#debugcomment=f.read()
	f.close()
	#return debugcomment
app.secret_key = 'HJFHGSYUKEYTW786F7I675jkyftehyas6a7'
app.run(debug=True,host='0.0.0.0')
