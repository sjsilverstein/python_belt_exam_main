# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.


#********* User Table ********
class UserManager(models.Manager):
	def register (self, postData):
		error = []
		if not postData['name'].isalpha():
			print "Error Names must Be all Alpha characters"
			error.append("Error First and Last Names must Be all Alpha characters")
		if not EMAIL_REGEX.match(postData['email']):
			print "Regex doesn't like the email"
			error.append("Please enter a email format: <string>@<string>.<string>")
		if len(postData['password']) < 8 or postData['password'] != postData['confirm_password']:
			print "Passwords must be more then eight character long and match with your confirmed password."
			error.append("Passwords must be more then eight character long and match with your confirmed password.")
		if len(User.objects.filter(email=postData['email'])) > 0:
			print "email is already in use"
			error.append("email is already in use")
		#REMINDER HASH PASSWORDS LATER
		if len(error) == 0:
			hashpass = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
			User.objects.create(name=postData['name'], alias = postData['alias'], email= postData['email'], password = hashpass)
		return error
	def login(self, postData):
		valid = False
		user = User.objects.filter(email=postData['email'])
		if len(user) == 1:
			test = postData['password']
			if bcrypt.checkpw(test.encode(), user[0].password.encode()):
				valid = True;
		return valid
class User (models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	objects = UserManager()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __repr__(self):
		return "User ID: {} USER NAME : {}".format (self.id, self.name)


#*********END User Table *****

#********Quotes Table **********
class QuoteManager(models.Manager):
	def newquote(self, postData, user):
		errors = []
		
		message = postData['message']
		author = postData['author']
		user = User.objects.get(id=user)

		if len(author) < 3:
			errors.append("The author should be more then 3 characters long")
		if len (message) < 10:
			errors.append("The Message should be at least 10 characters long")
		if len (errors) == 0:
			newquote = Quote.objects.create(author = author, message = message, user = user)
			newFavorit = Favorites.objects.create(user = user, quote = newquote)

		return errors

class Quote(models.Model):
	author = models.CharField(max_length=255)
	message = models.TextField(default = "")
	user = models.ForeignKey(User, related_name = "creator")
	objects = QuoteManager()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	def __repr__(self):
		return "<Quote ID : {} , Author : {} , User FK : {}>".format( self.id, self.author, self.user)

#*********END Quotes Table ****

#*********Favorit Quote Table*****
class FavoritesManager(models.Manager):
	def addFavorite(self, postData, user):
		errors = []
		user = User.objects.get(id=user)
		quote = Quote.objects.get(id=postData['quoteID'])
		lookup = Favorites.objects.filter(user=user, quote=quote)
		if len(lookup) == 0:
			newFavorite = Favorites.objects.create(user = user, quote = quote)
			return errors
		errors.append("Sorry! You cannot Favorit a Quote more then once.")

		return errors
	def removeFavorit(self, postData):
		delete_Favorit = Favorites.objects.get(id=postData['favoritID'])
		delete_Favorit.delete()
		return True
class Favorites(models.Model):
	user = models.ForeignKey(User, related_name = "user_id")
	quote = models.ForeignKey(Quote, related_name = "quote_id")
	objects = FavoritesManager()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
#**********END Favorit Quotes Table ***