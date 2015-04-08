# web_chat_flask

Short description:
This is simple web chat that has the following functionality:
- User authentification
- Authenticated users can create chat rooms and send messages
- Latest news from http://stackoverflow.com/ are listed on main page


Folders structure
Directories content:
 - myapp - WEB application folder.
 - \myapp\templates -  Jinja2 Templates location 
 - run.py - startup script 

Features
Few main features:
 - Flask-SQLAlchemy ORM was used to create Users and Rooms models 
 - Flask-Login library was used for user authentification
 - flask-socketio extension was used for bi-directional communications between the clients and the server(sending chat messages)
 - The client-side application uses the SocketIO Javascript library to establish connection to the server.

