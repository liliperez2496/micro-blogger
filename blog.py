from bottle import route, run, template, response, request, view, redirect

from datetime import datetime

@route('/')
@view('home.html')
def home():
	username = request.get_cookie('Username')
	archive = open("entries")
	entries = []

	for line in archive:
		parts = line.split("\t")
		if len(parts) == 3:
			user, message, timestamp = parts
			entry = { "user": user, "message": message, "timestamp": timestamp }
			entries.append(entry)

	archive.close()
	entries.reverse()

	return {"entries":entries, 'username':username}

@route('/new_entry', method="POST")
def new_entry():
	username=request.params["Username"]
	username=username.replace("\t"," ")
	username=username.replace("\n"," ")

	entry=request.params["Entry"]
	entry=entry.replace("\t"," ")
	entry=entry.replace("\n"," ")

	if len(entry) >= 140 or len(entry) == 0:
		redirect('/')

	timestamp = datetime.now()

	write_entry(username, entry, timestamp)

	redirect('/')

def write_entry(username, entry, timestamp):
	f = open("entries", "a")
	f.write(username + "\t" + entry + "\t" + str(timestamp) + "\n")
	f.close()

@route('/log_in', method='POST')
@view('login.html')
def log_in():
	entered_user=request.params["Username"]

	entered_pw=request.params["Password"]

	a = open("info")
	
	for line in a:
		parts = line.split("\t")
		username, password = parts
	
		if entered_user == username and entered_pw == password:
			response.set_cookie("Username", username)
			redirect('/')




@route('/log_in')
@view('login.html')
def loginpage():
	pass


@route('/log_out')
def logoutpage():
	response.set_cookie("Username", "")
	redirect("/")


@route('/sign_up')
@view('signup.html')
def signuppage():
	pass


@route('/sign_up', method="POST")
@view('signup.html')
def signup():
	 user = request.params["username"]
	 pass1 = request.params["password1"]
	 pass2 = request.params["password2"]
	 if is_username_taken(user):
	 	return dict(error="Username taken")

	 if pass1 != pass2:
	 	return dict(error="Passwords don't match")
	 write_user(user, pass1)
	 response.set_cookie("Username", user)
	 redirect('/')




def write_user(user, password):
	c = open('info', 'a')
	c.write(user + '\t' + password + '\n')
	c.close


def is_username_taken(user):
	 	b = open("info")

	 	for line in b:
	 		parts = line.split('\t')
	 		username, password = parts
	 		if user == username:
	 			return True
	 		
	 	return False



run(host='0.0.0.0', port=8080, debug=True, reloader = True)






