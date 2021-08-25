from django.shortcuts import render, redirect
from django.http import HttpResponse
from blogapp.models import *
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def Home(request):
    allblogs = BlogModel.objects.all()
    lastblog = allblogs[len(allblogs)-1:][0]
    reverseblog = allblogs[::-1]
    recentfour = reverseblog[1:5]
    d = {"allblogs":allblogs, "lastblog":lastblog, "recentfour":recentfour}
    return render(request, 'index.html', d)

def About(request):
    allcategory = Category.objects.all()

    d = {"allcategory":allcategory}
    return render(request, 'about.html', d)

def Foods(request):
    return render(request, 'foods.html')

def Lifestyle(request):
    return render(request, 'lifestyle.html')

def Contact(request):
    return render(request, 'contact.html')


def Login(request):
    error = False
    if request.method == "POST":
        datadict = request.POST
        username = datadict['username']
        password = datadict['pwd']

        user = authenticate(username = username, password = password)
        if user:
            login(request,user)
            return redirect("home")
        else:
            error = True

    d = {"error":error}
    return render(request, 'login.html', d)

def Logout(request):
    logout(request)
    return redirect("home")

def Signup(request):
    error = False
    if request.method == 'POST':
        datadict = request.POST
        username = datadict['username']
        password = datadict['pwd']
        firstname = datadict['firstname']
        lastname = datadict['lastname']
        email = datadict['email']
        img = request.FILES['profileimg']
        aboutyou = datadict['aboutyou']
        
        #check username same or not
        data = User.objects.filter(username = username)
        if data:
            error = True
        else:
            user = User.objects.create_user(username = username, password = password, first_name = firstname, 
                                            last_name = lastname, email = email)
            UserDetail.objects.create(usr = user, userimage = img, aboutyou = aboutyou) 
            return redirect('login')

    d = {"error":error}
    return render(request, 'signup.html', d)

def BlogDetail(request, bid):
    blog = BlogModel.objects.get(id = bid)
    usrdetail = UserDetail.objects.get(usr = blog.usr)
    allcomments = CommentBLog.objects.filter(blog = blog)
    allcategory = Category.objects.all()
    d = { "blog":blog, "user":usrdetail, "allcategory":allcategory, "allcomments":allcomments }
    return render(request, 'single.html', d)

def categortyBlog(request, cid):
    allcategory = Category.objects.all()
    catedata = Category.objects.get(id = cid)
    cateblog = BlogModel.objects.filter(category = catedata)
    d = {"cateblog":cateblog, "catedata":catedata, "allcategory":allcategory}
    return render(request, 'category_blog.html', d)

def UserPanel(request):
    cateblog = BlogModel.objects.filter(usr = request.user)
    udetail = UserDetail.objects.get(usr = request.user)
    d = {"cateblog":cateblog, "udetail":udetail}
    return render(request, "userpanel.html", d)

def DeleteBlog(request, bid):
    blog = BlogModel.objects.get(id = bid)
    blog.delete()
    return redirect("userpanel")

### when user create new blog they get mail ###

def SenddynamicMail(to_mail,sub,blogdata):
   
    from_mail = settings.EMAIL_HOST_USER
    to_mail = to_mail
    sub = sub
    msg = EmailMultiAlternatives(sub,'',from_mail,[to_mail])
    d = {"title":blogdata.title,"dec":blogdata.short,
            "username":blogdata.usr.first_name}
    html = get_template('addblogmail.html').render(d)
    msg.attach_alternative(html, 'text/html')
    msg.send()
    

def AddBlog(request):
    allcat = Category.objects.all()
    if request.method == "POST":
        datadict = request.POST
        title = datadict["title"]
        short = datadict["short"]
        long = datadict["long"]
        blogimg = request.FILES["blogimg"]
        cid = datadict["cid"]
        catdata = Category.objects.get(id = cid)
        usr = request.user
        todaydate = date.today() 
        blogdata = BlogModel.objects.create(category = catdata, usr = usr, title = title,
                                short = short, long = long, image = blogimg, date = todaydate)
        
        SenddynamicMail(request.user.email,"NEW BLOG CREATED", blogdata)

        return redirect('userpanel')

    d = {"allcat":allcat}
    return render(request,'addblog.html', d)


def Editprofile(request):
    details = UserDetail.objects.get(usr = request.user)
    if request.method == 'POST':
        datadict = request.POST
        firstname = datadict['firstname']
        lastname = datadict['lastname']
        email = datadict['email']
        try:
            img = request.FILES['profileimg']
            details.userimage = img
            details.save()
        except KeyError:
            pass

        aboutyou = datadict['aboutyou']
        user = request.user 
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.save()
        details.aboutyou = aboutyou
        details.save()
        return redirect('userpanel')

    d = { "userdetail":details}

    return render(request,'editprofile.html',d)

def Changepassword(request):
    error = False
    if request.method == "POST":
        datadict = request.POST
        oldpwd = datadict['oldpwd']
        newpwd = datadict['newpwd']
        user = authenticate(username = request.user.username, password = oldpwd )
        if user:
            user.set_password(newpwd)
            user.save()
            login(request, user)
            return redirect('userpanel')
        else:
            error = True

    d = {"error":error}
    return render(request, 'changepassword.html', d)

def BlogLike(request,bid):
    if not request.user.is_authenticated:
        return redirect('login')

    blogdata = BlogModel.objects.get(id = bid)
    userdata = UserDetail.objects.get(usr = request.user)
    likedata = LikeBlog.objects.filter(usr = userdata, blog = blogdata)
    if not likedata:
        LikeBlog.objects.create(usr = userdata, blog = blogdata)
    else:
        likedata.delete()

    return redirect('detail',bid)

def BlogComment(request, bid):
    blogdata = BlogModel.objects.get(id = bid)
    userdata = UserDetail.objects.get(usr = request.user)
    comment_date = date.today()
    if request.method == "POST":
        comment = request.POST['comment']
        CommentBLog.objects.create(blog = blogdata, usr = userdata,
                                    commentdate = comment_date, comment = comment)
    return redirect('detail',bid)

### email gateway ###

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

def Gateway(request):
    return render(request,'email_gateway.html')

def SendMail(request):
   
    from_mail = settings.EMAIL_HOST_USER
    to_mail = request.user.email
    sub = 'Confirmation Mail'
    msg = EmailMultiAlternatives(sub,'',from_mail,[to_mail])
    d = {"name":"jainesh"}
    html = get_template('mail_sending.html').render(d)
    msg.attach_alternative(html, 'text/html')
    msg.send()
    return HttpResponse("mail send")

