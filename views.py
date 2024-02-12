from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from .models import Contact,Blogs
#below import is done for sending mail
from django.conf import settings
from django.core import mail
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if not request.user.is_authenticated:
        messages.warning(request,'hey login and use website')
        return redirect('/login')
    if request.method=="POST":
        fphone=request.POST['phone']
        fname = request.POST['name']
        femail = request.POST['email']
        desc=request.POST['message']
        query=Contact(phone=fphone,name=fname,email=femail,description=desc)
        query.save()
      






        messages.info(request,"Your message has been sent successfully will get back.")
        return redirect('/contact')
    
    return render(request, 'contact.html')

def service(request):
    return render(request, 'service.html')

def search(request):
    query=request.GET['search']
    if len(query) > 100:
      allposts=Blogs.objects.none()
    else:
        allpoststitle=Blogs.objects.filter(title__icontains=query)
        allpostsdescription=Blogs.objects.filter(description__icontains=query)
        allpostsposted=Blogs.objects.filter(authorname__icontains=query)
        allposts=allpoststitle | allpostsdescription | allpostsposted
    if allposts.count()==0:
        messages.warning(request,'no result found')
    params={'allposts' : allposts,'query':query}
    return render(request, 'search.html',params)

def handlelogin(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=uname, password=pass1)
        if myuser is not None:
            auth_login(request, myuser)  # Corrected login() call
            messages.success(request, "You are now logged in!")
            return redirect('/')
        else:
            messages.error(request, 'Username or Password is incorrect!')
            return redirect("/login")
    return render(request, 'login.html', {'messages': messages.get_messages(request)})
   

def handlelogout(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect( '/login' )

def handleblog(request):
    if not request.user.is_authenticated:
        messages.warning(request,'hey login and use website')
        return redirect('/login')
    allposts=Blogs.objects.all()
    context={'allposts':allposts}
    print(allposts)
    return render(request, 'blog.html',context)

def handlesignup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('Email')
        password = request.POST.get('inputPassword3')
        confirmpass = request.POST.get('confirmPassword')

        if password != confirmpass:
            messages.warning(request, "Passwords do not match")
            return redirect('/signup')

        if User.objects.filter(username=uname).exists():
            messages.info(request, "Username is already taken")
            return redirect('/signup')

        if User.objects.filter(email=email).exists():
            messages.info(request, "This email has already been registered")
            return redirect('/signup')

        myuser = User.objects.create_user(uname, email, password)
        myuser.save()
        messages.success(request, "Signup successful")
        return redirect('/login')

    return render(request, 'signup.html')
