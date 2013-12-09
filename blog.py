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




run(host='0.0.0.0', port=8080, debug=True, reloader = True)






