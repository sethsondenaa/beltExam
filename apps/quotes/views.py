# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from models import User, Quotes, Favorites
import bcrypt

# Create your views here.
def index(request):
	return render(request, 'quotes/index.html')

def login(request):
	if request.POST.get('submit') == 'Register':
		valid = User.objects.validate_data(request.POST)
		if valid[0] == True:
			User.objects.create(name=request.POST['name'],
				alias=request.POST['alias'],
				birth_date=request.POST['birth_date'],
				email=request.POST['email'],
				password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			)
			user = User.objects.filter(email=request.POST['email'])
			request.session['id'] = user[0].id
			request.session.modified = True
			return redirect('/quotes')
		else:
			for message in valid[1]:
				messages.error(request, message, "register error")
			return redirect('/main')
	else:
		user = User.objects.filter(email=request.POST['email'])
		if len(user) > 0:
			user = user[0]
			if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
				request.session['id'] = user.id
				request.session.modified = True
				return redirect('/quotes')
			else:
				messages.error(request, "Incorrect password")
				return redirect('/main')
		else: 
			messages.error(request, "Email not found")
			return redirect('/main')

def home(request):
	if not request.session.keys():
		return redirect('/main')
	user =  User.objects.filter(id=request.session['id'])
	if request.POST.get('add_favorite', False) == 'Add to My List': # If user wants to add to favorites list
		quote = Quotes.objects.filter(id=request.POST['favorite'])
		posted_user = User.objects.filter(id=request.POST['posted_by'])
		Favorites.objects.create(quote=quote[0],
			posted_by=posted_user[0],
			user=user[0]
		)
	elif request.POST.get('remove_favorite', False) == 'Remove from My List': #If user wants to remove from users list
		Favorites.objects.filter(id=request.POST.get('favorite', False)).delete()
	all_quotes = Quotes.objects.all()
	user_favorites = Favorites.objects.filter(user=user[0])
	for each in all_quotes:
		for favorite in user_favorites:
			if favorite.quote.id == each.id:
				all_quotes = all_quotes.exclude(id=each.id)			
	context = {
		'user': user[0],
		'quotes': all_quotes,
		'favorites': user_favorites
	}
	return render(request, 'quotes/home.html', context)

def add(request):
	valid = Quotes.objects.validate_data(request.POST)
	if valid[0] == True:
		user = User.objects.filter(id=request.session['id'])
		Quotes.objects.create(user=user[0],
			author=request.POST['quoted_by'],
			content=request.POST['content']
		)
	else:
		for message in valid[1]:
			messages.error(request, message)
	return redirect('/quotes')

def users(request, posted_by):
	posted_user = User.objects.filter(id=posted_by)
	context = {
		'quotes': Quotes.objects.filter(user=posted_user[0]),
		'count': len(Quotes.objects.filter(user=posted_user[0])),
		'posted_by': posted_user[0]
	}
	return render(request, 'quotes/quote.html', context)

def logout(request):
	request.session.clear()
	request.session.modified = True
	return redirect('/main')