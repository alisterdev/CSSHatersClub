#!/usr/bin/env python                                      
import cgi, cgitb, os, sys
cgitb.enable()

print "Content-type: text/html\n\n"

form = cgi.FieldStorage()

# Get values form the form and initialize necessary variables
currentUser = form.getvalue('username')
comment = form.getvalue('comment')
friendSearch = form.getvalue('friendSearch')

usersList=[]
friendsList=[]
friendsPosts=[]

# Populates userList variable with all 
# currently registered users
def GetUsers():
	global usersList
	try:
		input = open('members.csv', 'r')
		s = input.readlines()
		InputTuple = []
		for line in s:
			singleLine = line.rstrip()			
			list = singleLine.split()
			usersList.append(list[1])
	except:
		print "GetUsers(): An error has occured! Sorry for the inconvienience!"
	input.close()

# Populates friendsList variable with all 
# friends of currently logged in user
def GetFriends():
	global friendsList
	try:
		input = open('members.csv', 'r')
		s = input.readlines()
		InputTuple = []
		for line in s:
			singleLine = line.rstrip()
			InputTuple.append(singleLine)				
			list = singleLine.split()
			if (list[1] == currentUser):									
				for index in range(len(list)):						
					if (index > 2):
						friendsList.append(list[index])
	except:
		print "GetFriends(): An error has occured! Sorry for the inconvienience!"
	input.close()

# Populates friendsPosts variable with all 
# posts of currently logged in user friends
def GetFriendsPosts():
	global friendsList
	global friendsPosts
	copyFriendsList = list(friendsList)
	copyFriendsList.append(currentUser)
	try:		
		input = open('topics.csv', 'r')
		lines = input.readlines()
		InputTuple = []	
		for (line_index, line) in enumerate(lines):
			singleLine = line.rstrip()
			InputTuple.append(singleLine)				
			fList = singleLine.split("\n")
			if (line_index % 2 == 0):				
				for friend in copyFriendsList:
					if (friend == fList[0]):
						friendsPosts.append( (lines[line_index + 1], friend) )													
	except:
		print "GetFriendsPosts(): An error has occured! Sorry for the inconvienience!"
	input.close()

# Adds a comment posted by current user
def AddComment():
	try:
		topics = open('topics.csv', 'a')
		topics.write(currentUser + "\n")
		comment.strip()
		topics.write(comment + "\n")
		topics.close()
	except:
		print "AddComment(): An error has occured while opening 'topics.csv'! Sorry for the inconvienience!"

# Check if searched user exists
def UserExists():
	friendFound=0
	try:
		input = open('members.csv', 'r')
		s = input.readlines()
		for line in s:
			singleLine = line.rstrip()						
			list = singleLine.split()			
			if (list[1] == friendSearch and list[1] != currentUser):
				friendFound=1
		input.close()		
		return friendFound
	except:
		print "UserExists(): An error has occured while opening 'topics.csv'! Sorry for the inconvienience!"

# Add a user to current user friends list
def AddFriend():
	try:
		file_name = "members.csv"						
		file_lines = ""		
		str = " ";

		with open(file_name, 'r') as f:
			for x in f.readlines():
				list = x.split()
				if (list[1] == currentUser and friendSearch not in list):			
					seq = (x.strip(), friendSearch, "\n")
					file_lines += str.join(seq)
				else:
					file_lines += x

		with open(file_name, 'w') as f:
		    f.writelines(file_lines) 
	except:
		print "AddFriend(): An error has occured while opening 'topics.csv'! Sorry for the inconvienience!"

# Appropriate method calls depending on the scenario
userAddedHTML=""
if friendSearch:	
	friendSearch.strip()
	userFound = UserExists()
	if (userFound == 1):
		AddFriend()
		userAddedHTML = "User added!"
	else:
		userAddedHTML = "Sorry, this user doesn't exist! Try something else!"

if comment:
	comment = cgi.escape(comment)
	AddComment()

GetUsers()
GetFriends()
GetFriendsPosts()

# Generates all necessary HTML to be added to the page
usersHTML=""
for user in usersList:
	usersHTML += "<tr><td>" + user + "</td></tr>"

friendsHTML=""
if friendsList:
	for friend in friendsList:
		friendsHTML += "<tr><td>" + friend + "</td></tr>"
else:
	friendsHTML = "<tr><td>You don't have any friends at the moment!<br/>Add someone in the form below!</td></tr>" 

postsHTML=""
if friendsPosts:
	postCount = 0
	for post in reversed(friendsPosts):
		if (postCount < 10):		
			postsHTML += "<tr><td><blockquote><p>" + post[0] + "</p><i>by " + post[1] + "</i></blockquote></td></tr>"
			postCount += 1
else:
	postsHTML = "<tr><td>There are no posts from your friends at the moment!</td></tr>"


page = '''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Live Feed | CSS Haters Club</title>	
</head>
<body bgcolor="#0070e0">
	<font color="white" face="Helvetica Neue, Arial">		
		<table align="center" width="60%">
			<tr>		
				<td align="center" colspan="2">
					<a href="../index.html" align="center">
						<img src="../images/logo.png" alt="CSS Haters Club Logo"/>
					</a>
					<hr size="5px" color="#fff">					
				</td>				
			</tr>
			<tr>
'''

page += '<td align="right" colspan="2" height="50px"><h3>Welcome, %s </h3><a href="../index.html"><font color="#fff">Logout</font></a></td>' %currentUser
page += '''
			</tr>	
			<tr valign="top">		
				<td bgcolor="#0050A0" width="70%">														
					<table cellpadding="5" border="#fff" width="100%">
						<tr><td><h3 align="center">Recent news from fellow haters</h3></td></tr>
'''
page += postsHTML
page += '''					<tr>	<td colspan="2">				
					<form action="./MyFacebookPage.py" method="POST">
						Leave a comment, hater:<br/>
						<textarea name="comment" rows="5" cols="85" placehodler="Enter your message here" required></textarea> <br/>
'''
page += '<input type="hidden" name="username" value="%s" />' % currentUser
page +=	'''			
						<input type="submit" value="Comment!">
					</form>
				</td></tr>
					</table>								
				</td>
				<td bgcolor="#b00211" width="30%">
					<table cellpadding="5" border="#fff" width="100%">
					<tr>
						<td><h3 align="center">Active Users</h3></td>
					</tr>
'''
page += usersHTML
page += ''' 
						<tr>
							<td><h3 align="center">Your Friends</h3></td>
						</tr>					
'''
page += friendsHTML
page += '''
						<tr><td><h3 align="center">Add a new friend</h3></td></tr>								
						<tr>
							<td align="center">
								<form action="./MyFacebookPage.py" method=POST>
									<input type="text" placeholder="Enter a username" name="friendSearch"/>
									<input type="submit" value="Add!">
'''
page += '<input type="hidden" name="username" value="%s" />' % currentUser
page += userAddedHTML
page += '''
								</form>																
							</td>
						</tr>	
						<tr>
							<td><br></td>
						</tr>
					</table>															
				</td>
			</tr>
		</table>
		<div class="footer">
			<hr width="60%" size="3px" color="#fff">
			<font size="2"><p align="center">&copy; Copyright 2015 - Alex I. - Team CSS Haters</p></font>
		</div>		
	</font>
</body>
</html>'''

print page 