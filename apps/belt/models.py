from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
import datetime


class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['Name']) < 3:
            errors['Name'] = "Name  must be at least 3 characters"

        if len(postData['Alias']) < 1:
            errors['Alias'] = "Alias  must be at least 1 characters"

        if not my_re.match(postData['email']):
            errors['email'] = " enter a valid email id"

        if len(postData['password']) < 8:
            errors['password'] = "password  must be at least 8 characters"

        if postData['password'] != postData['confirm_password']:
            errors['password'] = "passwords must match"

        return errors
        # min_age = 24
        # max_date = date.today()
        # try:
        #     max_date = max_date.replace(year=max_date.year - min_age)
        # except ValueError: # 29th of february and not a leap year
        #     assert max_date.month == 2 and max_date.day == 29
        #     max_date = max_date.replace(year=max_date.year - min_age, month=2, day=28)
        # people = People.objects.filter(birth_date__lte=max_date)

    def validateLogin(self, postData):
        errors = {}
        my_re = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        hash2 = postData['password'].encode()

        if not my_re.match(postData['email']):
            errors['email'] = "Enter a valid email id"
        else:
            # try:
            try:
                user = User.objects.get(email=postData['email'])
                print "user  "
                if (user):
                    if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                        print "logged in"
                    else:
                        errors['password'] = "password do not match"
            except:
                # User.DoesNotExist:
                errors['emailnotexist'] = "email doesn't exist"
                print "user not found"
        print errors
        return errors


class ListManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['Item']) <= 3:
            errors['Item'] = "Item must be at least 3 characters"

        return errors




class User(models.Model):
    Name = models.CharField(max_length = 255)
    Alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.Name, self.Alias, self.email, self.password)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n{}\n".format(self.Name, self.Alias, self.email, self.password)



class List(models.Model):
    item = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name="items")
    wishers = models.ManyToManyField(User, related_name="wishers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ListManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n".format(self.item, self.uploader, self.wishers)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n".format(self.item, self.uploader, self.wishers)