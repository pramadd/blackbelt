from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from django.utils import formats
from .models import User,List
import bcrypt


def index(request):
    return render(request, 'belt/index.html')


def register(request):
    Name = request.POST['Name']
    Alias = request.POST['Alias']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    context = {'Name': Name, 'Alias': Alias, 'email': email, 'password': password, 'confirm_password': confirm_password}
    errors = User.objects.validate(context)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(Name=Name, Alias=Alias, email=email, password=hashed_password)
        request.session['id'] = user.id
        request.session.name = user.Name
        print 'UsrName', request.session.name
        lists = List.objects.all()
        context = {
            'lists': lists
        }
        # return redirect("/appointments")
        return redirect('/dashboard')


def login(request):
    email = request.POST['email']
    password = request.POST['password']
    print "inside login"

    errors = User.objects.validateLogin(request.POST)
    print errors
    if errors:
        print "heres"
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        print "redirecting to root"
        return redirect('/')
    else:
        user = User.objects.filter(email=email)[0]

        request.session['id'] = user.id

        request.session.name = user.Name
        request.session['name'] = user.Name
        lists = List.objects.all()
        context = {
            'lists': lists
        }
        print request.session['name']
        # return redirect("/appointments")
        return redirect('/dashboard')

def createItem(request):
    return render(request, 'belt/create.html')

def dashboard(request):
    print 'indashboard method'
    lists = List.objects.all()
    context = {
        'lists' : lists
    }
    return render(request, 'belt/dashboard.html', context)


def deleteItem(request):
    listId = request.POST['listId']
    List.objects.get(id=listId).delete()
    return redirect('/dashboard')

#def removeFromlist(request):

#def addTolist(request):
    # listId = request.POST['listId']
    # listItem = List.objects.get(id=listId)
    # List.objects.create(item=item, uploader=user)
#
# def addItem(request):
#
#
def add(request):
    item = request.POST['itemName']
    context = {'Item': item}
    errors = List.objects.validate(context)
    #print 'In ADd ' , request.session['name']
    user = User.objects.get(id=request.session['id'])
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
    else:
        List.objects.create(item=item, uploader=user)


    return redirect("/dashboard")
#
def viewItem(request, number):
    list = List.objects.get(id=number)
    itemName = list.item;
    context = {'itemsList' : list, 'itemName': itemName}
    return render(request, 'belt/viewItem.html', context)


def logout(request):
    request.session['id'] = ""
    return redirect('/')


