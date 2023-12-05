# App with many security flaws

The app allows users to send messages to a board.

to run:
```Python
pip install -r requirements.txt  # (or just pip install django)
python3 create_db.py  #Needed for the project to run
python3 manage.py runserver
```

## Vulnerability 1.  INJECTION
[sql injection](./server/pages/views.py#L25) | [XSS](./server/pages/templates/pages/home.html#L18)  
#### 1.1 SQL injection  
In an SQL injection the attacker is able to manipulate the SQL query that the server sends to the database. This application is vulnerable in the following way:
```Python
user = request.POST.get("username")
text = request.POST.get("textmessage")
q = f"INSERT INTO message (user, message) VALUES ('{user}', '{text}');"
```

where the attacker can now freely control what goes into the slots “user” and “text”. For example they could input: text=); DROP TABLE message” would drop the “message” table. The attacker  has the freedom freedom to do more or less any query. There are many ways to combat this type of attack. One solution would be to use an object-relation mapper. Another fix would be to use to use parameterized queries. For example in sqlite we could use c.execute("SELECT * FROM DATA WHERE NAME = ?", new_data).

#### 1.1 XSS  
In xss the server does not sanitize input from an user and the user is able to send for example javascript to other users that will then get rended in the victims browser.

The raw input is also subject to Cross-site scripting. The raw message is taken from the user and rendered to other users as is. An attacker could now send anything to the message boards chat and it would be rendered to all users.

The issue is here: {{message|safe}}  
By default Django protects against this, but by adding | safe to it we can bypass it and make our website more dangerous. To fix it we simply remove the |safe from the message and all is good.

You can try this out by creating a message like this to the board; <script>alert("xss")<script>


## Vulnerability 2. Lack of logging
[Logging](server/config/settings.py#L33)  

Logging is essential for spotting users trying to attack your website. It’s essential to have logging of security critical-parts, like logins/registers of users, but also more trivial things. Preferably the logger would alert admins when enough suspicious activity is detected. The app has no logging currently. You can see an example of how to turn on logging here: 



## Vulnerability 3. Cross-Site Request Forgery
[How to add CSRF token](server/pages/templates/pages/home.html#L4)  [Disable CSRF check in django](server/config/settings.py#L70)  

Cross-Site Request Forgery works like this:
1. The victim is logged into the website we are targeting (for example a bank)
2. The attacker lures the victim to their website.
3. The attackers website now creates valid looking request, from the victims browser, to the real website. This works because the victim is still logged into the real website.

An example post request body could have the following info:
From: ?  
To: ?  
Amount?  

The attackers would figure out exactly what the real request looks like and send it on behalf of the victim, when they get lured into the attacker website. Now the real website cannot possibly know if the request is valid, as the request is identical to a “valid” request.

To combat this we add a new field:  

From: ?  
To: ?  
Amount?  
Csrf_Token?  

We create a new token each time a user wants to send a post message (when the form is sent to the user). Now the attacker cannot create a correct looking, invalid request, as they cannot possibly guess what token the victim currently has. This more or less solves the CSRF vulnerability. There’s not much the attacker can do now.

Fixing this in Django is very easy. All you need to do is add a {% csrf_token %} to each form.

This project is maybe not the best for demonstrating CSRF because it does not use accounts at all, but the principle is the same.



## Vulnerability 4. Vulnerable and outdated components
[django version](requirements.txt#L2)  

This one is especially problematic in the js/python world where there are lots of poorly maintained libraries. One needs to make sure the libraries you use are of high standard. For this project in particular, the Django verison is frozen at 3.0, which is an insecure version. You can just check any of djangos official docs and it will have a banner stating: “This document is for an insecure version of Django that is no longer supported. Please upgrade to a newer release!” This is mainly problematic because new vulnerabilities won’t be patched in the older versions. 

Another insecure thing is the usage of execute-script in SQLite [execute-script](server/pages/views.py#L26). This is done as the default execute only allows one query per string, while this one is much more dangerous. Switching to execute would make it slightly more secure, but by no means protected against SQL injections.



## Vulnerability 5. Security Misconfiguration
[turn debug off here](server/config/settings.py#L26)

The application runs in debug mode by default. The main issue with it is that it exposes detailed errors and in worst case exposes credentials. For example you can see some info regarding your settings.py and from there see if any vulnerable components are used in the server. Django is known to filter some stuff out, but certainly not a good idea to leave it in debug mode. This one is also very easy to fix. Just turn debug off.  

You could also add many of the above vulnerabilities in here as many of them are currently possible because I use “dangerous” features and these are not needed at all. Things like making the XSS possible by adding the |safe to the rendering could also fit this category. 