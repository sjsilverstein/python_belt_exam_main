# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from django.contrib import messages

from models import *

# Create your views here.


def index(request):
	return render (request, "login_app/index.html")

def register(request):
	errors = User.objects.register(request.POST)
	if len(errors) == 0:
		request.session['id'] = User.objects.get(email=request.POST['email']).id
		return redirect('/quotes')
	for i in errors:
		messages.add_message(request, messages.INFO, i)

	return redirect('/main')

def login(request):
	if User.objects.login(request.POST):
		request.session['id'] = User.objects.get(email=request.POST['email']).id
		return redirect('/quotes')
	messages.add_message(request, messages.INFO, 'Invalid User / Pwd')
	return redirect('/main')

def logout(request):
	request.session.clear()
	return redirect('/main')

def landing(request):
	context = {
		'name' : User.objects.get(id=request.session['id']).name,
		'quotelist' : Quote.objects.all(),
		'favoriteslist' : Favorites.objects.filter(user = User.objects.get(id=request.session['id']))
	}
	return render(request, 'login_app/landing.html', context)

def newquote(request):
	errors = Quote.objects.newquote(request.POST, request.session['id'])
	for i in errors:
		messages.add_message(request, messages.INFO, i)
	return redirect('/quotes')

def addFavorite(request):
	errors = Favorites.objects.addFavorite(request.POST, request.session['id'])
	for i in errors:
		messages.add_message(request, messages.INFO, i)
	return redirect('/quotes')

def removeFavorit(request):
	removeFavorit = Favorites.objects.removeFavorit(request.POST)
	return redirect('/quotes')

def userspage(request, userID):
	user = User.objects.get(id=userID)
	context = {
	'userID' : user,
	'quotes' : Quote.objects.filter(user=user),
	'count' : len(Quote.objects.filter(user=user)),
	}
	return render(request, 'login_app/user.html', context)