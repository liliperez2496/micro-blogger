from bottle import route, run, template, response, request, view, redirect

from datetime import datetime
@route('/')
@view('home.html')
def home():
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
	return {"entries":entries}

@route('/new_entry', method="POST")
def new_entry():
	username=request.params["Username"]
	username=username.replace("\t"," ")
	username=username.replace("\n"," ")

	entry=request.params["Entry"]
	entry=entry.replace("\t"," ")
	entry=entry.replace("\n"," ")

	timestamp = datetime.now()

	f = open("entries", "a")
	f.write(username + "\t" + entry + "\t" + str(timestamp) + "\n")
	f.close()

	redirect('/')

run(host='0.0.0.0', port=8080, debug=True, reloader = True)