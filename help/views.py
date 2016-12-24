from django.shortcuts import render
from .models import Order, Comment, Profile,Counter
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils import timezone
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.utils import timezone
import datetime

def index(request):
    ord_id = None
    has_error = False

    if Counter.objects.filter(date = datetime.date.today()).exists():
        a = Counter.objects.get(date = datetime.date.today())
        a.count = a.count + 1
        a.save()
    else:
        a = Counter()
        a.count = 1
        a.save()
    
    if request.method == "POST":
        if "ok_button" in request.POST:
            telephone = request.POST["telephone"]
            problem   = request.POST["problem"]
            if problem != "" and telephone != "":

                orr = Order()

                orr.telephone = telephone
                orr.problem   = problem
                orr.pub_date  = timezone.now()
                orr.profile   = request.user.profile

                orr.save()

                ord_id = orr.id
            else:
                has_error = True

    latest_order_list = Order.objects.all()[::-1]

    paginator = Paginator(latest_order_list,10)

    page = request.GET.get('page')
    
    try:
        latest_order_list = paginator.page(page)
    except PageNotAnInteger:
        latest_order_list = paginator.page(1)
    except EmptyPage:
        latest_order_list = paginator.page(paginator.num_pages)

    if request.user.is_authenticated():
        is_auth = True
        user = request.user
        profile = request.user.profile
        context = {"latest_order_list":latest_order_list,"paginator":paginator,"is_auth":is_auth,"user":user,"has_error":has_error}
    else:
        is_auth = False
        context = {"latest_order_list":latest_order_list,"paginator":paginator,"is_auth":is_auth,"has_error":has_error}
    
    
    response = render(request, "help/index.html",context)
    
    return response

def order(request, order_id):
    has_error = False
    if request.method == "POST":
        if request.user.is_authenticated(): 
            if "ok_button" in request.POST:
                comment_text     = request.POST["comment_text"]
                if comment_text != '':
                    orr              = Order.objects.get(id=order_id)

                    cmt              = Comment()

                    cmt.order   = orr
                    cmt.comment_text = comment_text
                    cmt.save()
                else:
                    has_error = True
            
                

    latest_cmt_list = Comment.objects.all()[::-1]
    order = Order.objects.get(id = order_id)
    if request.user.is_authenticated():
        is_auth = True
        user = request.user
        context = {"latest_cmt_list":latest_cmt_list,"order":order,"user":user,"is_auth":is_auth,"has_error":has_error}
    else:
        is_auth = False
        context = {"latest_cmt_list":latest_cmt_list,"order":order,"is_auth":is_auth,"has_error":has_error}
    response = render(request, "help/order.html", context)

    return response 

def registrations(request):
    false_message = False
    false_login   = False

    if request.method == "POST":
        if "register_button" in request.POST:
            username     = request.POST["login"]
            password     = request.POST["password"]
            
            if username !='' and password !='':
                try:
                    user = User.objects.create_user(username = username, password = password)
                    user.save()

                except IntegrityError:
                    false_login = True
                    response = render(request, 'registration/registrations.html',{"false_login":false_login,"false_message":false_message})
                    return response

                profile = Profile(user = user)
                profile.save()      

                user = authenticate(username = username, password = password)

                if user is not None and user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect("/loginned")
            else:
                false_message = True

    is_auth = False
   
    context = {'is_auth':is_auth,"false_message":false_message}
    response = render(request, 'registration/registrations.html',context)
    return response

def edit(request, edit_order_id):
    if request.method == "POST":
        if "ok_button" in request.POST:
            telephone       = request.POST["telephone"]
            problem         = request.POST["problem"]

            order           = Order.objects.get(id = edit_order_id)
            order.telephone = telephone
            order.problem   = problem
            
            if "status" not in request.POST:
                order.status = False
            else:
                order.status = True

            order.save() 

            return redirect('/')
    user = request.user
    order = Order.objects.get(id = edit_order_id)
    if request.user.is_authenticated():
        is_auth = True
    else:
        is_auth = False
    context = {"user":user,"order":order,"is_auth":is_auth}
    response = render(request, 'help/edit.html',context)
    return response

def profile(request,views_profile_id):
    user = request.user
    profile = Profile.objects.get(id = views_profile_id)

    if request.user.is_authenticated():
        is_auth = True
    else:
        is_auth = False

    context = {"user":user,"order":order,"is_auth":is_auth,"profile":profile}
    response = render(request, 'help/profile.html',context)
    return response


def editprofile(request, edit_profile_id):
    if request.method == "POST":
        if "ok_button" in request.POST:
            address    = request.POST["address"]
            telephone  = request.POST["telephone"]
            last_name  = request.POST["last_name"]
            first_name = request.POST["first_name"]

            profile    = request.user.profile
            user       = request.user

            profile.address = address
            profile.telephone = telephone
            
            user.last_name = last_name
            user.first_name = first_name

            profile.save()
            user.save()

            return redirect('/')

    user = request.user
    profile = Profile.objects.get(id = edit_profile_id)

    if request.user.is_authenticated():
        is_auth = True
    else:
        is_auth = False

    context = {"user":user,"order":order,"is_auth":is_auth,"profile":profile}
    response = render(request, 'help/editprofile.html',context)
    return response

def login(request):
    false_message=False
    false_login  =False
    if request.method == "POST":

        if "ok_button" in request.POST:
            login    = request.POST["login"]
            password = request.POST["password"]
            if login != "" and password != "":
                user = authenticate(username = login, password = password)

                if user is not None and user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    false_login = True
            else:
                false_message = True
                
    context = {"false_login":false_login,"false_message":false_message}
    response = render(request, 'registration/login.html',context)

    return response

def logginned(request):
    break_message = False
    if request.method == "POST":
        if "ok_button" in request.POST:
            first_name = request.POST["first_name"]
            last_name  = request.POST["last_name"]
            address    = request.POST["address"]
            telephone  = request.POST["telephone"]
            if first_name != "" and last_name != "":
                profile = request.user.profile
                user = request.user
                user.first_name = first_name
                user.last_name  = last_name
                profile.address         = address
                profile.telephone       = telephone
                user.save()
                profile.save()
                return redirect("/")
            else:
                break_message = True

    return render(request, 'registration/logginned.html',{"break_message":break_message})

def logout(request):
    auth.logout(request)
    return redirect("/")

