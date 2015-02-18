from flask import Flask, request,  flash, redirect, session
from myapp import app 
from flask import render_template
from myapp.forms import RegistrationForm,  loginForm, RegisterRoomForm
from myapp import database
from myapp.database import db_session
from myapp.models import User, Room, Message
from werkzeug import secure_filename
from flask.ext.login import LoginManager
from flask.ext.login import login_user , logout_user , current_user , login_required
import datetime
from flask.ext.socketio import SocketIO, emit

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
	userid = session['user_id']
	load_user(userid)
	room_list = []
	if current_user.is_authenticated():
		print ("test", current_user.name)
	form = RegisterRoomForm()
	# list of avalible rooms
	room_list = Room.query.all()
	
	if request.method == 'POST' and form.validate_on_submit():
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
			return redirect('/index')
			
	return render_template("index.html", form=form, rooms= room_list)
	
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST'and form.validate_on_submit():		
		filename = secure_filename(form.photo.data.filename)
		user = User(form.username.data, form.email.data, form.password.data, filename)
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
	if request.method == 'POST': # and form.validate_on_submit():
		print  ('time', form.message.data)
	return render_template('room.html', room_name=name, messages= messages)    

@socketio.on('client message sent', namespace= '/room-socket')
def clent_message_receive(message):  
	now = datetime.datetime.utcnow()
	userid = session['user_id']
	user_name= User.query.filter_by(id=userid).first().name
	emit('server message sent', {'message': message['data'], 'room': message['room'], 'time_received' : now, 'user': user_name}, broadcast=True)
	room = Room.query.filter_by(name= message['room']).first()		
	message = Message(room.id,  message['data'], user_name)	
	db_session.add(message)
	try:
		db_session.commit()
	except:
		db_session.rollback()
		raise
	finally:
	   db_session.close()  