from flask import Flask, request,  flash, redirect, session
from myapp import app 
from flask import render_template, send_from_directory
from myapp.forms import RegistrationForm,  loginForm, RegisterRoomForm
from myapp import database
from myapp.database import db_session
from myapp.models import User, Room, Message
from werkzeug import secure_filename
from flask.ext.login import LoginManager
from flask.ext.login import login_user , logout_user , current_user , login_required
import datetime, os
from flask.ext.socketio import SocketIO, emit
from threading import Thread
from time import sleep

login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)
@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


@app.route('/',  methods=['GET', 'POST'])
@app.route('/index',  methods=['GET', 'POST'])
def index():
	# Use authentication
	form = RegisterRoomForm()
	if 'user_id' in session:
		load_user(session['user_id'])
		room_list = []
		filename=""
		if current_user.is_authenticated():
			
			filename= "uploads/" + current_user.user_image_file
			print ("test", filename)

			if request.method == 'POST' and form.validate():
				room = Room(form.room_name.data)
				if not Room.query.filter_by(name=form.room_name.data).first():
					db_session.add(room)
					try:
						db_session.commit()
					except:
			  			db_session.rollback()
			   			raise
					finally:
					   db_session.close()  # optional, depends on use case
				else:
					message = "Room already exists"
					flash(message, category='error')
				
	
	# list of avalible rooms
	room_list = Room.query.all()
	
			
	return render_template("index.html", form=form, rooms= room_list)
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	filename = None
	form = RegistrationForm()
	if request.method == 'POST'and form.validate_on_submit():		
		filename = secure_filename(form.photo.data.filename)
		user = User(form.username.data, form.email.data, form.password.data, filename, form.accept_tos.data)
		if filename:
			print (app.config['UPLOAD_FOLDER'] )
			form.photo.data.save('uploads/' + filename)		
		db_session.add(user)
		try:
			db_session.commit()
		except:
  			db_session.rollback()
   			raise
		finally:
		   db_session.close()  # optional, depends on use case
		
		flash('Thanks for registering')
		return redirect('/login')
	return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
	form = loginForm()
	if request.method == 'POST' and form.validate_on_submit():
		username = form.user.data
		password = form.password.data		
		registered_user = User.query.filter_by(name=username,password=password).first()
		if registered_user is None:
			flash('Username or Password is invalid' , 'error')
			return redirect('/login')
		else:    
			login_user(registered_user)
			session['user_id']= registered_user.id
			print ("current_user.name", current_user.name, current_user.is_authenticated())
			flash('Logged in successfully')
	        # Check the password and log the user in
			return redirect('/index')
	return render_template('login.html', form=form)    

@app.route('/logout', methods=["GET", "POST"])
def logout():
	session['user_id']= None
	return redirect('/index')


@app.route('/room/<path:name>', methods=['GET', 'POST'])
def room(name):
	room_id=  Room.query.filter_by(name=name).first().id
	messages= Message.query.filter_by(parent_id=room_id)[1:3]
	for i in messages:
		print i.message
	
	return render_template('room.html', room_name=name, messages= messages)    

@socketio.on('client message sent', namespace= '/room-socket')
def clent_message_receive(message):  
	now = datetime.datetime.utcnow()
	userid = session['user_id']
	if userid:
		load_user(userid)
		user_name= User.query.filter_by(id=userid).first().name
		emit('server message sent', {'message': message['data'], 'room': message['room'], 'time_received' : now, 'user': user_name}, broadcast=True)
		room = Room.query.filter_by(name= message['room']).first()	
		print ("room",  message['room'])
		if room:	
			message = Message(room.id,  message['data'], user_name)	
			db_session.add(message)
			try:
				db_session.commit()
			except:
				db_session.rollback()
				raise
			finally:
			   db_session.close()  
@app.route('/user/uploads/<path:filename>')
@app.route('/uploads/<path:filename>')
@app.route('/room/uploads/<path:filename>')
def send_foo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/user/<path:user>')
def user_info(user):
	use_name = user
	requested_user= User.query.filter_by(name=user).first()

	return render_template('user.html', requested_user= requested_user ) 	

class MyThread(threading.Thread):
    def __init__(self, node_port):
        super(MyThread, self).__init__()
        self.node_port = node_port
        self.published_files_list = []
    def run(self):
        while True:
            time.sleep(3)           
            for file in os.listdir("./upload"):
                if file not in self.published_files_list:
                    file_name = file;
                    print file_name
                    self.published_files_list.append(file)

class MyThread(threading.Thread):
    def __init__(self, node_port):
        super(MyThread2, self).__init__()
        self.node_port = node_port
        self.published_files_list = []
    def run(self):
        while True:
            time.sleep(90)
            news_html = urllib2.urlopen("http://stackoverflow.com/").read()
            regex = re.compile('<h3><a\shref="([^>]*>[^<]*</a>)')
            titles = regex.findall(news_html)
            titles = titles[2:12]

            digest_message = ""
            for title in titles:
                digest_message += "<a href=\"http://stackoverflow.com" + title + '<br>'           
                socketio.emit('news',
                {('message': digest_message) },
                namespace= '/news')
                    