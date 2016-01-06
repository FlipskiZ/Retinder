#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import bottle
from bottle import *
import bottle_mysql

os.chdir(os.path.dirname(__file__))

install(bottle_mysql.Plugin(dbuser='root', dbpass='', dbname='tinder', dbhost='localhost', charset='utf8')) #Connects to the database

def set_to_encoding(string, startEncoding='latin1', endEncoding='utf8'): #To reverse utf-8 symbols that became encoded in latin-1
	string = string.encode('latin1')
	string = string.decode('utf8')
	return string

def mysql_real_escape_string(string): #Used to remove some possibilites for errors
    return string\
		.replace("\\", "\\\\")\
        .replace('"', '\\"')\
        .replace("'", "\\'")

def mysql_real_escape_string_delete(string): #Used to remove disallowed characters for the login
    return string\
		.replace("\\", "")\
        .replace('"', '')\
        .replace("'", "")
		
def checkLogin(username, password, db, admin=False): #Checks if there exists a row with the specified login credentials. Also if the user is an admin if specified.
	if username and password:
		username, password = mysql_real_escape_string_delete(username), mysql_real_escape_string_delete(password)
		db.execute("SELECT username, password FROM accounts WHERE username='{0}' AND password='{1}'".format(username, password))
		row = db.fetchall()
		if row:
			if admin and not checkAdmin(username, db):
				return False;
			return True
	return False

def checkAdmin(username, db):
	username = mysql_real_escape_string_delete(username)
	db.execute("SELECT administrator FROM accounts WHERE username='{0}' AND administrator = 1".format(username))
	row = db.fetchall()
	if row:
		return True
	return False
	
def loginForm(error=0, message=""): #The login site. Different errors append different messages at the end, preferably explaining the error.
	return	'''
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8"/>
				<link rel="stylesheet" href="/css/style.css">
				<title>Tinder Remake</title>
			</head>
			<body>
				<div id="login_wrapper">
					<header id="top_header">
						<h2>Login</h2>
					</header>
					
					<form method="post" action="/">
						Username: <input type="text" name="username" required="required"/>
						<br>
						Password: <input type="password" name="password" required="required"/>
						<br>
						Keep Logged In? (24h): <input type="checkbox" name="keepLogged"/>
						<br>
						<button type="submit">Submit</button>
					</form>
					<a href="/registration">Don't have an account?</a>
					{0} 
					{1}
					
					<footer id="bottom_footer">
						
					</footer>
				</div>
			</body>
		</html>
	'''.format("<br><p>Error: Incorrect Username/Password combination<p>" if error==1 else "", "<br><p>{0}<p>".format(message) if message else "")

def registrationForm(error=0):#The registration site. Error system same as above
	return '''
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8"/>
				<link rel="stylesheet" href="/css/style.css">
				<title>Tinder Remake</title>
			</head>
			<body>
				<div id="login_wrapper">
					<header id="top_header">
						<h2>Registration</h2>
					</header>
					
					<form method="post" action="registration">
						Username: <input type="text" name="username" required="required"/>
						<br>
						Password: <input type="password" name="password" required="required"/>
						<br>
						Repeat the password: <input type="password" name="passwordRepeat" required="required"/>
						<br>
						<button type="submit">Submit</button>
					</form>
					<a href="/">Already have an account?</a>
					{0}
					
					<footer id = "bottom_footer">
						
					</footer>
				</div>
			</body>
		</html>
		'''.format("<br><p>Error: Passwords don't match<p>" if error==1 else "<br><p>Error: Username already in use<p>" if error==2  else "<br><p>Error: Disallowed characters inputted<p>" if error == 3 else "")

def hubPage(db, username):
	username = mysql_real_escape_string_delete(username)
	return '''
		<!DOCTYPE html>
			<html lang="en">
				<head>
					<meta charset="utf-8"/>
					<link rel="stylesheet" href="/css/style.css">
					<title>Tinder Remake</title>
				</head>
				<body>
					<header id="top_header">
						<h1>Hub</h1>
					</header>
					<div id="main_wrapper">
						<nav id="nav_menu">
							<ul>
								<li><a href="/app/hub">Home</a></li>
								<li><a href="/app/app">Application</a></li>
								<li><a href="/app/info">Account Info</a></li>
								<li><a href="/app/logout">Logout</a></li>
								{adminLink}
							</ul>
						</nav>
						
						<p>Welcome!</p>
						
						<footer id="bottom_footer">
							
						</footer>
					</div>
				</body>
			</html>
		'''.format(adminLink=("""<li><a href="/app/admin">Admin Panel</a></li>""" if checkAdmin(username, db) else ""))
		
def applicationSite(db, username, error=0): #The main application page where you choose pictures. IT gets a random row from the pictures and sends it's id over with the like or dislike of the user.
	username = mysql_real_escape_string_delete(username)
	db.execute('''
	SELECT pictures.id, pictures.name, pictures.imagePath
	FROM pictures
    	INNER JOIN(
            SELECT RAND()*(
                SELECT MAX(id) 
                FROM pictures 
                WHERE id NOT IN (
        	SELECT likes.receiverId
       		FROM likes
        	WHERE likes.likerId = (
                SELECT accounts.id 
                FROM accounts 
                WHERE username = '{0}'
            )
        )) AS ID) AS t ON pictures.ID >= t.ID
	WHERE pictures.id NOT IN (
        SELECT likes.receiverId
        FROM likes
        WHERE likes.likerId = (
            SELECT accounts.id 
            FROM accounts 
            WHERE username = '{0}'
        )
    )
	LIMIT 1
	'''.format(username)) #This long query gets a semi-random row that the user has not liked or disliked yet.
	
	row = db.fetchall()
	
	if not row: #Checks if there aren't any rows left, if there isn't it says to the user that he has gone through all the pictures.
		return '''
			<!DOCTYPE html>
			<html lang="en">
				<head>
					<meta charset="utf-8"/>
					<link rel="stylesheet" href="/css/style.css">
					<title>Tinder Remake</title>
				</head>
				<body>
					<header id="top_header">
						<h1>Application</h1>
					</header>
					<div id="main_wrapper">
						<nav id="nav_menu">
							<ul>
								<li><a href="/app/hub">Home</a></li>
								<li><a href="/app/app">Application</a></li>
								<li><a href="/app/info">Account Info</a></li>
								<li><a href="/app/logout">Logout</a></li>
								{adminLink}
							</ul>
						</nav>
						
						<p>You have gone through all the pictures! Do you feel a bit concerned?<p>
						
						<footer id="bottom_footer">
							
						</footer>
					</div>
				</body>
			</html>
		'''.format(adminLink=("""<li><a href="/app/admin">Admin Panel</a></li>""" if checkAdmin(username, db) else ""))
	#If there are pictures left, show it, together with it's name and encode the id in the page URL for the next page.
	return	'''
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8"/>
				<link rel="stylesheet" href="/css/style.css">
				<title>Tinder Remake</title>
			</head>
			<body>
				<header id="top_header">
					<h1>Application</h1>
				</header>
					
				<div id="main_wrapper">
					<nav id="nav_menu">
						<ul>
							<li><a href="/app/hub">Home</a></li>
							<li><a href="/app/app">Application</a></li>
							<li><a href="/app/info">Account Info</a></li>
							<li><a href="/app/logout">Logout</a></li>
							{adminLink}
						</ul>
					</nav>
					
					<section id="image_section">
						<form method="post" action="/app/app?receiverId={id}">
							<button type="submit" name="liked" value="liked">Like</button>
							<button type="submit" name="liked" value="disliked">Dislike</button>
						</form>
						
						{error}
						
						<p>{name}<p>
						<img src="{path}" alt="{name}"/>
					</section>
					<footer id="bottom_footer">
						
					</footer>
				</div>
			</body>
		</html>
	'''.format(name=row[0]['name'], path=row[0]['imagePath'], id=row[0]['id'], error=("" if error==1 else ""), adminLink=("""<li><a href="/app/admin">Admin Panel</a></li>""" if checkAdmin(username, db) else ""))

def accountInfo(db, username):
	username = mysql_real_escape_string_delete(username)
	return '''
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8"/>
				<link rel="stylesheet" href="/css/style.css">
				<title>Tinder Remake</title>
			</head>
			<body>
				<header id="top_header">
					<h1>Account Information</h1>
				</header>
				<div id="main_wrapper">
					<nav id="nav_menu">
						<ul>
							<li><a href="/app/hub">Home</a></li>
							<li><a href="/app/app">Application</a></li>
							<li><a href="/app/info">Account Info</a></li>
							<li><a href="/app/logout">Logout</a></li>
							{adminLink}
						</ul>
					</nav>
					<br><br>
					<nav id="nav_menu">
						<ul>
							<li><a href="/app/info/liked">Liked Images</a></li>
							<li><a href="/app/info/disliked">Disliked Images</a></li>
						</ul>
					</nav>
					
					<footer id="bottom_footer">
						
					</footer>
				</div>
			</body>
		</html>
	'''.format(adminLink=("""<li><a href="/app/admin">Admin Panel</a></li>""" if checkAdmin(username, db) else ""))

def showLiked(db, username, liked, page):
	likedRows = ""
	dislikeRows = ""
	likeTable = ""
	dislikeTable = ""
	
	username = mysql_real_escape_string_delete(username)
	if page < 0:
		page = 0
	
	if liked:
		db.execute('''
			SELECT name, imagePath
			FROM pictures 
			WHERE id IN (
				SELECT receiverId 
				FROM likes 
				WHERE liked = 1
				AND likerId = (
					SELECT id FROM accounts WHERE username = '{0}'
				)
			)
			ORDER BY timestamp DESC
		'''.format(username))
		
		likedRows = db.fetchall()
	else:
		db.execute('''
			SELECT name, imagePath, timestamp
			FROM pictures 
			WHERE id IN (
				SELECT receiverId 
				FROM likes 
				WHERE liked = 0
				AND likerId = (
					SELECT id FROM accounts WHERE username = '{0}'
				)
			) 
			ORDER BY timestamp DESC
		'''.format(username))
		
		dislikedRows = db.fetchall()
	
	moreResults = False
	
	if liked:
		if likedRows:
			likeTable += """<table id="like_table">"""
			for row in range(5*page, 5+5*page):
				if row >= len(likedRows):
					break
				likeTable += """<tr><td><a href="{imagePath}">{name}</a><br><a href="{imagePath}"><img src={imagePath} alt={name}/></a></td></tr>""".format(name=likedRows[row]['name'], imagePath=likedRows[row]['imagePath'])
			likeTable += "</table><br>"
		if not 5+5*page >= len(likedRows):
			moreResults = True
	else:
		if dislikedRows:
			dislikeTable += """<table id="dislike_table">"""
			for row in range(5*page, 5+5*page):
				if row >= len(dislikedRows):
					break
				dislikeTable += """<tr><td><a href="{imagePath}">{name}</a><br><a href="{imagePath}"><img src={imagePath} alt={name}/></a></td></tr>""".format(name=dislikedRows[row]['name'], imagePath=dislikedRows[row]['imagePath'])
			dislikeTable += "</table><br>"
		if not 5+5*page >= len(dislikedRows):
			moreResults = True
	return '''
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8"/>
				<link rel="stylesheet" href="/css/style.css">
				<title>Tinder Remake</title>
			</head>
			<body>
				<header id="top_header">
					<h1>Account Information</h1>
				</header>
				<div id="main_wrapper">
					<nav id="nav_menu">
						<ul>
							<li><a href="/app/hub">Home</a></li>
							<li><a href="/app/app">Application</a></li>
							<li><a href="/app/info">Account Info</a></li>
							<li><a href="/app/logout">Logout</a></li>
							{adminLink}
						</ul>
					</nav>
					
					{like}
					{dislike}
					
					<footer id="bottom_footer">
						<nav id="nav_menu">
							<ul>
								{prevPage}
								{nextPage}
							</ul>
						</nav>
					</footer>
				</div>
			</body>
		</html>
	'''.format(like=likeTable, dislike=dislikeTable, adminLink=("""<li><a href="/app/admin">Admin Panel</a></li>""" if checkAdmin(username, db) else ""), prevPage = ("""<li><a href="/app/info/{0}liked?page={1}">Previous Page</a></li>""".format("dis" if not liked else "", page-1) if page > 0 else ""), nextPage = ("""<li><a href="/app/info/{0}liked?page={1}">Next Page</a></li>""".format("dis" if not liked else "", page+1) if moreResults else ""))
		
def adminPanelSite(success=0, error=0): #The admin panel. The only thing you can do here for now is adding a new item. Later on there will be more functions added on to here, but this is a relatively low-priority feature.
	return	'''
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="utf-8"/>
				<link rel="stylesheet" href="/css/style.css">
				<title>Tinder Remake</title>
			</head>
			<body>
				<header id="top_header">
					<h1>Admin Panel</h1>	
				</header>
				<div id="main_wrapper">
					
					<nav id="nav_menu">
						<ul>
							<li><a href="/app/hub">Home</a></li>
							<li><a href="/app/app">Application</a></li>
							<li><a href="/app/info">Account Info</a></li>
							<li><a href="/app/logout">Logout</a></li>
							<li><a href="/app/admin">Admin Panel</a></li>
						</ul>
					</nav>
					
					{error}
					{success}
					
					<p>Insert a new image<p>
					<form method="post" action="/app/admin" enctype="multipart/form-data">
						Image name: <input type="text" name="name" required="required"/>
						<br>
						Image Location (Max 5MB): <input type="file" name="data" required="required"/>
						<br>
						<button type="submit" name="formType" value="0"/>Submit</button>
					</form>
					<br>
					<p>Delete an image<p>
					<form method="post" action="/app/admin">
						Image name: <input type="text" name="imageName" required="required"/>
						<br>
						<button type="submit" name="formType" value="1"/>Submit</button>
					</form>
					<br>
					<p>Change account username<p>
					<form method="post" action="/app/admin">
						Current user's username: <input type="text" name="currentUsername" required="required"/>
						<br>
						New username: <input type="text" name="newUsername" required="required"/>
						<br>
						<button type="submit" name="formType" value="2"/>Submit</button>
					</form>
					<br>
					<p>Change account password<p>
					<form method="post" action="/app/admin">
						User's username: <input type="text" name="username" required="required"/>
						<br>
						New password: <input type="password" name="newPassword" required="required"/>
						<br>
						<button type="submit" name="formType" value="3"/>Submit</button>
					</form>
					<br>
					<p>Delete a user's account<p>
					<form method="post" action="/app/admin">
						User's username: <input type="text" name="username" required="required"/>
						<br>
						<button type="submit" name="formType" value="4"/>Submit</button>
					</form>
					<br>
					<p>Delete a users like/dislike<p>
					<form method="post" action="/app/admin">
						User's username: <input type="text" name="username" required="required"/>
						<br>
						Image name: <input type="text" name="imageName" required="required"/>
						<br>
						<button type="submit" name="formType" value="5"/>Submit</button>
					</form>
					<br>
					<p>Reset user likes/dislikes<p>
					<form method="post" action="/app/admin">
						User's username: <input type="text" name="username" required="required"/>
						<br>
						<button type="submit" name="formType" value="6"/>Submit</button>
					</form>
					<br>
					<p>Add/remove admin privileges to user<p>
					<form method="post" action="/app/admin">
						User's username: <input type="text" name="username" required="required"/>
						<br>
						Add/Remove admin? (checked=add, unchecked=remove): <input type="checkbox" name="setAdmin"/>
						<br>
						<button type="submit" name="formType" value="7"/>Submit</button>
					</form>
					<footer id="bottom_footer">
						
					</footer>
				</div>
			</body>
		</html>
	'''.format(success = ("<h2>Successfully added a new row</h2><br>" if success==1 else"<h2>Successfully deleted a row</h2><br>" if success==2 else"<h2>Successfully changed username</h2><br>" if success==3 else"<h2>Successfully changed password</h2><br>" if success==4 else"<h2>Successfully deleted the account</h2><br>" if success==5 else"<h2>Successfully deleted the like</h2><br>" if success==6 else"<h2>Successfully reset the likes</h2><br>" if success==7 else"<h2>Successfully set admin privileges</h2><br>" if success==8 else ""),\
	error=("Error: Unknown Error" if error==-1 else "<h2>Error: File size over 1MB</h2><br>" if error==1 else "<h2>Error: File is not an image (or unrecognizable format)</h2><br>" if error==2 else "<h2>Error: Image name already exists</h2><br>" if error==3 else "<h2>Error: Image name doesn't exist</h2><br>" if error==4 else "<h2>Error: Username doesn't exist</h2><br>" if error==5 else "<h2>Error: Username already exists</h2><br>" if error==6 else "<h2>Error: Like doesn't exist</h2><br>" if error==7 else ""))
	#Successes - 0=nothing/no success, 1=successfull upload, 2=successful image delete, 3=successful username change, 4=successful password change, 5=successful account delete, 6=successful user's like/dislike delete, 7=successful user's like/dislike reset, 8=successful admin privileges set
	#Errors - 0=nothing/no error, -1=unexpected error, 1=too large file upload, 2=file is not an image, 3=image name already exists, 4=image name doesn't exist, 5=username doesn't exist, 6=username already exists, 7=like doesn't exist
def checkOverSize(data, maxSize): #Checks if a file is not too large. It seeks the start of the data in memory, checks it's lenght, and then sets the pointer at it's start again. Then returns the lenght.
	data.file.seek(0, 2)
	size = data.file.tell()
	data.file.seek(0)
	if size > maxSize:
		return True
	return False
	
@route('/') #The login page. This checks if the user is not already logged in. AKA has the username/password cookies. If so, go to the hub. Warning: This site never meant to have strong security, username and password and everything is stored in plain text.
def login(db): #When you have bottle_mysql imported and use 'db' as one of the function parameters after a route, bottle_mysql automatically connects to th emysql database and uses the db variable as the mysql cursor.
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if checkLogin(username, password, db):
		return '''<meta http-equiv="Refresh" content="0; url=/app/hub">'''
	message = request.query.message or "" #Checks if there is a message encoded in the URL. Used for saying that account registration was successfull.
	return loginForm(0, message)

@route('/', method='POST')
def doLogin(db): #Checking if the inputted login credentials match with a row in the database. And then creates cookies keeping you logged in.
	username = request.forms.get('username')
	password = request.forms.get('password')
	keepLogged = request.forms.get('keepLogged')
	username, password = set_to_encoding(username), set_to_encoding(password)
	
	if checkLogin(username, password, db):
		if keepLogged:
			response.set_cookie("username", username, max_age=86400, path="/")
			response.set_cookie("password", password, max_age=86400, path="/")
		else:
			response.set_cookie("username", username, path="/")
			response.set_cookie("password", password, path="/")
		return '''<meta http-equiv="Refresh" content="0; url=/app/hub">'''
	else:
		return loginForm(1)

@route('/registration')
def register(): #Registration page. It returns the registration page function.
	return registrationForm(0)

@route('/registration', method='POST')
def doRegister(db): #Gets the inputted username and passwords, checks if the username isn't used, then if the passwords match. If both pass, add the information to the database and go back to the login page.
	username = request.forms.get('username')
	password = request.forms.get('password')
	passwordRepeat = request.forms.get('passwordRepeat')
	username, password, passwordRepeat = mysql_real_escape_string(username), mysql_real_escape_string(password), mysql_real_escape_string(passwordRepeat)
	username, password, passwordRepeat = set_to_encoding(username), set_to_encoding(password), set_to_encoding(passwordRepeat)
	
	if (any(x == '\\' or x == '"' or x == "'" for x in username) or any(x == '\\' or x == '"' or x == "'" for x in password)):
		return registrationForm(3)
	if password != passwordRepeat:
		return registrationForm(1)
	db.execute("SELECT username FROM accounts WHERE username='{0}'".format(username))
	row = db.fetchall()
	if row:
		return registrationForm(2)
	db.execute("INSERT INTO accounts(username, password) VALUES('{0}','{1}')".format(username, password))
	return '''<meta http-equiv="Refresh" content="0; url=/?message=Account registration successful">'''

@route('/app/hub') #The hub, all pages from this and down check if the user is logged in (cookies). If not return him to the login page.
def hub(db): #This page is the main page of the site. It's intended to be the go to page for information, links etc.
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if not checkLogin(username, password, db):
		return '''<meta http-equiv="Refresh" content="0; url=/">'''
	return hubPage(db, username)

@route('/app/app')
def application(db): #The page where you like/dislike pictures.
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if not checkLogin(username, password, db):
		return '''<meta http-equiv="Refresh" content="0; url=/">'''
	return applicationSite(db, username, 0)
	
@route('/app/app', method='POST')
def applicationLike(db): #Checks if the user pressed the like, or the dislike button and adds the result in the database.
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if not checkLogin(username, password, db):
		return '''<meta http-equiv="Refresh" content="0; url=/">'''
	username, password = mysql_real_escape_string(username), mysql_real_escape_string(password)
	db.execute("SELECT id FROM accounts WHERE username='{0}'".format(username))
	usernameId = db.fetchall()[0]['id']
	liked = 1 if request.forms.get('liked') == "liked" else 0
	receiverId = int(request.query.receiverId)
	db.execute("INSERT INTO likes(likerId, liked, receiverId) VALUES({0},{1},{2})".format(usernameId, liked, receiverId))
	return applicationSite(db, username, 0)	

@route('/app/logout')
def logout(): #Logging out of the site. Basically deletes the cookies and returns to the login page.
	response.set_cookie('username', '', expires=1, path="/")
	response.set_cookie('password', '', expires=1, path="/")
	
	return '''<meta http-equiv="Refresh" content="0; url=/">'''

@route('/app/info')
def info(db): #The information page. For now it shows a table of all your liked/disliked pictures.
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if not checkLogin(username, password, db):
		return '''<meta http-equiv="Refresh" content="0; url=/">'''
	return accountInfo(db, username)

@route('/app/info/liked')
def infoLiked(db):
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if not checkLogin(username, password, db):
		return '''<meta http-equiv="Refresh" content="0; url=/">'''
	page = request.query.page
	page = int(page if page else 0)
	return showLiked(db, username, True, page)

@route('/app/info/disliked')
def infoDisliked(db):
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if not checkLogin(username, password, db):
		return '''<meta http-equiv="Refresh" content="0; url=/">'''
	page = request.query.page
	page = int(page if page else 0)
	return showLiked(db, username, False, page)

@route("/app/admin")
def adminPanel(db): #Returns the admin panel. Also checks if you are an admin.
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if not checkLogin(username, password, db, True):
		return '''<meta http-equiv="Refresh" content="0; url=/app/hub">'''
	return adminPanelSite(0)
	
@route("/app/admin", method='POST')
def adminPanelAdd(db): #Applies the row to the table with an path to the uploaded image, which is saved in the /images directory.
	username, password = request.get_cookie("username"), request.get_cookie("password")
	if not checkLogin(username, password, db, True):
		return '''<meta http-equiv="Refresh" content="0; url=/app/hub">'''
	formType = int(request.forms.get('formType'))
	
	if formType == 0: #0=upload image, 1=delete image, 2=change user's username, 3=change user's password, 4=delete account, 5=delete a user's like/dislike, 6=reset user's likes/dislikes, 7=add/remove admin privileges to user.
		name = request.forms.get('name')
		data = request.files.get('data')
		
		name = mysql_real_escape_string(name)
		set_to_encoding(name)
		
		db.execute("SELECT name FROM pictures WHERE name='{0}'".format(name))
		row = db.fetchall()
		if row:
			return adminPanelSite(0, 3)
			
		temp, ext = os.path.splitext(data.filename)
		if ext not in ('.png','.jpg','.jpeg', '.gif', '.bpg'): #Checks if the extension is valid.
			return adminPanelSite(0, 2)
		
		if checkOverSize(data, 5*1024*1024): #Max size is 5MB
			return adminPanelSite(0, 1)

		db.execute('''
			SELECT `AUTO_INCREMENT`
			FROM  INFORMATION_SCHEMA.TABLES
			WHERE TABLE_SCHEMA = 'tinder'
			AND   TABLE_NAME   = 'pictures';
		''')
		
		incrementId = db.fetchall()[0]['AUTO_INCREMENT'] #Gets this row's to be id
		
		data.filename = "{0}.jpg".format(incrementId) #Names the file to be the same id as its row
		filePath = "images/"
		data.save(filePath, overwrite=True) #Saves the file
		
		db.execute("INSERT INTO pictures(name, imagePath) VALUES('{0}', '{1}')".format(name, "/"+filePath+"{0}.jpg".format(incrementId)))
		return adminPanelSite(1, 0)
	elif formType == 1:
		imageName = request.forms.get('imageName')
		imageName = mysql_real_escape_string(imageName)
		set_to_encoding(imageName)
		
		db.execute("SELECT name FROM pictures WHERE name='{0}'".format(imageName))
		row = db.fetchall()
		if row:
			db.execute("DELETE FROM likes WHERE receiverId=(SELECT id FROM pictures WHERE name='{0}')".format(imageName))
			db.execute("DELETE FROM pictures WHERE name='{0}'" .format(imageName))
			return adminPanelSite(2, 0)
		return adminPanelSite(0, 4)
	elif formType == 2:
		currentName = request.forms.get('currentUsername')
		newName = request.forms.get('newUsername')
		currentName, newName = mysql_real_escape_string(currentName), mysql_real_escape_string(newName)
		currentName, newName = set_to_encoding(currentName), set_to_encoding(newName)
		
		db.execute("SELECT username FROM accounts WHERE username='{0}'".format(currentName))
		row = db.fetchall()
		if row:
			db.execute("SELECT username FROM accounts WHERE username='{0}'".format(newName))
			row = db.fetchall()
			if row:
				return adminPanelSite(0, 6)
			db.execute("UPDATE accounts SET username='{1}' WHERE username='{0}'".format(currentName, newName))
			return adminPanelSite(3, 0)
		return adminPanelSite(0, 5)
	elif formType == 3:
		username = request.forms.get('username')
		newPassword = request.forms.get('newPassword')
		username, newPassword = mysql_real_escape_string(username), mysql_real_escape_string(newPassword)
		
		username, newPassword = set_to_encoding(username), set_to_encoding(newPassword)
		
		db.execute("SELECT username FROM accounts WHERE username='{0}'".format(username))
		row = db.fetchall()
		if row:
			db.execute("UPDATE accounts SET password='{1}' WHERE username='{0}'".format(username, newPassword))
			return adminPanelSite(4, 0)
		return adminPanelSite(0, 5)
	elif formType == 4:
		username = request.forms.get('username')
		username = mysql_real_escape_string(username)
		username = set_to_encoding(username)
		db.execute("SELECT username FROM accounts WHERE username='{0}'".format(username))
		row = db.fetchall()
		if row:
			db.execute("DELETE FROM likes WHERE likerId=(SELECT id FROM accounts WHERE username='{0}')".format(username))
			db.execute("DELETE FROM accounts WHERE username='{0}'".format(username))
			return adminPanelSite(5, 0)
		return adminPanelSite(0, 5)
	elif formType == 5:
		username = request.forms.get('username')
		imageName = request.forms.get('imageName')
		username, imageName = mysql_real_escape_string(username), mysql_real_escape_string(imageName)
		username, imageName = set_to_encoding(username), set_to_encoding(imageName)
		
		db.execute("SELECT username FROM accounts WHERE username='{0}'".format(username))
		row = db.fetchall()
		if row:
			db.execute("""SELECT id FROM likes WHERE likerId=(
					SELECT id FROM accounts WHERE username='{0}'
				) AND receiverId=(
					SELECT id FROM pictures WHERE name='{1}'
				)""".format(username, imageName))
			row = db.fetchall()
			id = row[0]['id']
			if row:
				db.execute("DELETE FROM likes WHERE id='{0}'".format(id))
				return adminPanelSite(6, 0)
			return adminPanelSite(0, 7)
		return adminPanelSite(0, 5)
	elif formType == 6:
		username = request.forms.get('username')
		username = mysql_real_escape_string(username)
		username = set_to_encoding(username)
		
		db.execute("SELECT username FROM accounts WHERE username='{0}'".format(username))
		row = db.fetchall()
		if row:
			db.execute("""SELECT id FROM likes WHERE likerId=(SELECT id FROM accounts WHERE username='{0}')""".format(username))
			row = db.fetchall()
			db.execute("DELETE FROM likes WHERE likerId=(SELECT id FROM accounts WHERE username='{0}')".format(username))
			return adminPanelSite(7, 0)
		return adminPanelSite(0, 5)
	elif formType == 7:
		username = request.forms.get('username')
		setAdmin = bool(request.forms.get('setAdmin'))
		username = mysql_real_escape_string(username)
		username = set_to_encoding(username)
		
		db.execute("SELECT username FROM accounts WHERE username='{0}'".format(username))
		row = db.fetchall()
		if row:
			db.execute("UPDATE accounts SET administrator={1} WHERE username='{0}'".format(username, setAdmin))
			return adminPanelSite(8, 0)
		return adminPanelSite(0, 5)
	
	return adminPanelSite(0, -1)
	
@route('/images/<image>')
def returnImage(image): #Returns the image static file. Required for showing and accessing the pictures.
    return static_file(image, root='./images')

@route('/css/<sheet>')
def returnSheet(sheet): #Returns the css stylesheet static file. Required for showing and accessing the stylesheet of the site.
	return static_file(sheet, root='./css')

application = bottle.default_app() #Used so that mod_wsgi knows what bottle application to use. We are using the default application.