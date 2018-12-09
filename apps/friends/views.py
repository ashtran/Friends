from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import *
from django.contrib.messages import error
from django.contrib import messages
from django.db.models import Count

#<--- Homepage --->#
def index(request):
    return render(request, 'friends/index.html')
#<--- Process Create New User --->#
def createuser(request):
    errors= User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.items():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user= User.objects.create_user(request.POST)
        request.session['user_id']=user.id
        return redirect('/friends')
#<--- Process User Login --->#
def login(request):
    errors= User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.items():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user= User.objects.filter(email=request.POST['email'])[0]
        request.session['user_id']=user.id
        return redirect('/friends')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def dashboard(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    user_id=request.session['user_id']
    context={
    'user':User.objects.get(id=request.session['user_id']),
    'friend':User.objects.filter(friends=request.session['user_id']).exclude(id=request.session['user_id']),
    'others':User.objects.exclude(id=request.session['user_id']).exclude(friends=request.session['user_id'])
    }
    return render(request, 'friends/dashboard.html',context)

def user(request,friend_id):
    user= User.objects.get(id=friend_id)
    context={
        'user':user,
    }
    return render(request, 'friends/friends.html',context)

def deletefriend(request,friend_id):
    delete_friend=User.objects.get(id=request.session['user_id']).friends.remove(User.objects.get(id=friend_id))
    return redirect('/user/{}'.format(friend_id))

def addfriend(request,friend_id):
    add_friend=User.objects.get(id=request.session['user_id']).friends.add(User.objects.get(id=friend_id))
    return redirect('/friends')
