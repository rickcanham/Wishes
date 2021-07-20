from django.db import models
from django.db.models.fields import BooleanField, CharField, DateTimeField, EmailField, TextField
import datetime
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):


    def login_validator(self,postData):

        errors = {}

        all_users = User.objects.all()
        user_id = -1

        for user in all_users:
            if user.email == postData['login_email']:
                user_id = user.id
            if user_id > 0:
                break
            
        if user_id != -1:
            user_obj = User.objects.get(id=user_id)

            hash1 = user_obj.pw_hash

            if bcrypt.checkpw(postData['login_password'].encode(), hash1.encode()):
                user.logged_in = True
                user.save()
            else:
                errors['user_password'] = "Error: Incorrect password."
        else:
            errors['user_email'] = "Error: User not found. Please check your email or register."

        return errors, user_id


    def register_validator(self,postData):

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        errors = {}

        if len(postData['register_first_name']) < 2:
            errors['first_name'] = "Error: First name must be at least 2 characters."
        if len(postData['register_last_name']) < 2:
            errors['last_name'] = "Error: Last name must be at least 2 characters."       

        if not(re.match(regex, postData['register_email'])): 
            errors['email'] = "Error: Invalid email address." 
        else:
            try:
                user_obj = User.objects.all()   
                for i in user_obj:
                    if postData['register_email'] == i.email:
                        errors['email'] = "Error: E-mail address is already in database. Please enter a different e-mail."
                        break
            except User.DoesNotExist:
                pass

        if len(postData['register_password']) < 8:
            errors['password'] = "Error: Password must be at least 8 characters."

        if postData['register_password'] != postData['register_confirm_password']:
            errors['password_match'] = "Error: Password and confirm password do not match."

        return errors



class WishManager(models.Manager):

    def wish_validator(self,postData):

        errors = {}

        if len(postData['wish_for']) < 3:
            errors['wish_for'] = "Error: I wish for must be at least 3 characters."
        if len(postData['wish_desc']) < 3:
            errors['wish_desc'] = "Error: Wish description must be at least 3 characters."  

        return errors



# Create your models here.
class User(models.Model):
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    email = EmailField(max_length=254)
    pw_hash = CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #wish_for = 
    #wish_granted = 
    #liked_wishes

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Wish(models.Model):
    item = CharField(max_length=255)
    desc = TextField()
    granted = BooleanField(default=False)
    date_granted = DateTimeField(default=datetime.time(0,0))
    wisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wish_for") #OneToMany - One user can make many wishes, but each wish can only be made by one user
    granted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wish_granted") #OneToMany - One user can grant many wishes, but each wish can only be granted by one user
    like_by = models.ManyToManyField(User, related_name="liked_wishes") #ManyToMany - Many users can like a wish, and many wishes can be liked by a user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

