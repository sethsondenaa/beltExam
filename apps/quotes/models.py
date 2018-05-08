# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
	def validate_data(self, request_data):
		valid = True
		errors = []
		if request_data['name'] == "":
			valid = False
			errors.append('Name cannot be empty')
		if request_data['alias'] == "":
			valid = False
			errors.append('Alias cannot be empty')
		if request_data['email'] == "":
			valid = False
			errors.append('Email cannot be empty')
		if len(request_data['password']) < 8:
			valid = False
			errors.append('Password must be at least 8 characters')
		elif request_data['password'] != request_data['confirm_pw']:
				valid = False
				errors.append('Password and confirm password do not match')
		if request_data['birth_date'] == "":
			valid = False
			errors.append('Birth date cannot be empty')
		return (valid, errors)

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	birth_date = models.DateTimeField()
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

	def __str__(self):
		return self.name

class QuoteManager(models.Manager):
	def validate_data(self, request_data):
		valid = True
		errors = []
		if len(request_data['quoted_by']) < 4:
			valid = False
			errors.append('Quoted by must be at least 4 characters')
		if len(request_data['content']) < 11:
			valid = False
			errors.append('Quote must be more than 10 characters')
		return(valid, errors)

class Quotes(models.Model):
	author = models.CharField(max_length=255)
	content = models.CharField(max_length=255)
	user = models.ForeignKey(User, related_name="user")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = QuoteManager()

class Favorites(models.Model):
	quote = models.ForeignKey(Quotes, related_name="quote")
	posted_by = models.ForeignKey(User, related_name="posted_by")
	user = models.ForeignKey(User, related_name="favorited_by")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)