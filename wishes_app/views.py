from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Wish
import bcrypt
import datetime

# Create your views here.
def disp_login(request):
    return render(request, "login.html")


def login(request):
    if request.method == "POST":

        errors, user_id = User.objects.login_validator(request.POST)

        if len(errors) > 0:

            for key, val in errors.items():
                messages.error(request, val)
        
            return redirect("/")

        else:
            request.session['user_id'] = user_id

            return redirect("/wishes")


def register(request):
    if request.method == "POST":

        errors = User.objects.register_validator(request.POST)

        if len(errors) > 0:

            for key, val in errors.items():
                messages.error(request, val)
        
            return redirect("/")
        else:

            register_pw_hash = bcrypt.hashpw(request.POST["register_password"].encode(), bcrypt.gensalt()).decode() 

            User.objects.create(
                first_name = request.POST["register_first_name"],
                last_name = request.POST["register_last_name"],
                email = request.POST["register_email"],
                pw_hash = register_pw_hash,
            )

            user = User.objects.last()      
            user_id = user.id

            request.session['user_id'] = user_id

            return redirect("/wishes")


def log_out(request):

    request.session.clear()
    return redirect("/")


def disp_home(request):
    if 'user_id' in request.session:

        user_id = request.session['user_id']
        user_obj = User.objects.get(id=user_id)
        wishes_obj = Wish.objects.all()

        context = {
            "wishes" : wishes_obj,
            "user" : user_obj,
        }

        return render(request, "dashboard.html", context)
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context)


def disp_new(request):
    if 'user_id' in request.session:

        user = User.objects.get(id = request.session['user_id'])

        context = {
            "user" : user,
        }

        return render(request, "add.html", context)
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context)


def add_wish(request):
    if 'user_id' in request.session:
        if request.method == "POST":

            if 'cancel_wish' not in request.POST:

                errors = Wish.objects.wish_validator(request.POST)

                if len(errors) > 0:

                    for key, val in errors.items():
                        messages.error(request, val)
                
                    return redirect("/wishes/new")

                else:
                    user_obj = User.objects.get(id = request.session['user_id'])

                    wish_obj = Wish.objects.create(
                        item = request.POST['wish_for'], 
                        desc = request.POST['wish_desc'],
                        granted = False,
                        date_granted = datetime.datetime.now(),
                        wisher = user_obj, 
                        granted_by = user_obj,
                    )

        return redirect("/wishes")
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context)   


def disp_edit(request,wish_id):
    if 'user_id' in request.session:

        user = User.objects.get(id = request.session['user_id'])

        context = {
            "user" : user,
            "wish" : Wish.objects.get(id=wish_id)
        }

        return render(request, "edit.html", context)
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context)


def edit_wish(request,wish_id):
    if 'user_id' in request.session:
        if request.method == "POST":

            if 'cancel_wish' not in request.POST:

                errors  = Wish.objects.wish_validator(request.POST)

                if len(errors) > 0:

                    for key, val in errors.items():
                        messages.error(request, val)

                    return redirect("wishes/disp_edit/{wish_id}")

                else:

                    wish_obj = Wish.objects.get(id=wish_id)
                    wish_obj.item = request.POST["wish_for"]
                    wish_obj.desc = request.POST["wish_desc"]
                    wish_obj.save()

        return redirect("/wishes")
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context)  


def remove_wish(request,wish_id):
    if 'user_id' in request.session:
        wish_obj = Wish.objects.get(id = wish_id)
        wish_obj.delete()

        return redirect("/wishes")
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context)   


def grant_wish(request,wish_id):
    if 'user_id' in request.session:

        user_obj = User.objects.get(id = request.session['user_id'])
        wish_obj = Wish.objects.get(id = wish_id)

        wish_obj.granted = True
        wish_obj.granted_by = user_obj
        wish_obj.date_granted = datetime.datetime.now()
        wish_obj.save()

        return redirect("/wishes")
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context)   


def like_wish(request,wish_id):
    if 'user_id' in request.session:

        user_obj = User.objects.get(id = request.session['user_id'])
        wish_obj = Wish.objects.get(id = wish_id)
        user_obj.liked_wishes.add(wish_obj)

        return redirect("/wishes")
    else:
        context = {
            "login_msg" : "Please log in first."
        }

        return render(request, "login.html", context)   








