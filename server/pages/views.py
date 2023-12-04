from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
import sqlite3
from django.contrib.auth.models import User
import random


def homePageView(request):
	con = sqlite3.connect("db.db")
	cur = con.cursor()
	messages = cur.execute("SELECT * FROM message").fetchall()
	return render(request, 'pages/home.html',  {"messages": messages})


def insertMessageView(request):
	con = sqlite3.connect("db.db")
	cur = con.cursor()
	user = request.POST.get("username")
	text = request.POST.get("textmessage")

	# UNSAFE QUERY (not SQL INJECTION proof)
	q = f"INSERT INTO message (user, message) VALUES ('{user}', '{text}');"
	cur.executescript(q)

	# SAFER VARIANT (OR use ORM instead)
	# cur.execute("INSERT INTO message (user, message) VALUES (?, ?);", user, text)
	con.commit()

	cur = con.cursor()
	cur.execute(q)
	messages = cur.execute("SELECT * FROM message").fetchall()
	return render(request, 'pages/home.html', {"messages": messages})
