from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from estoreapp.models import product,Cart
from django.db.models import Q

# Create your views here.
def index(request):
    context={}
    p=product.objects.filter(is_active=True)
    context['products']=p
    return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col="-price"
    p=product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 &q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def pdetails(request,pid):
    p=product.objects.filter(id=pid)
    print(p)
    context={}
    context['products']=p
    return render(request,'productdetails.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        p=product.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        context={}
        context['products']=p
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        if n==1:
            context['errmsg']="Product already exists in cart"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['successmsg']="Product added successfully"
        return render(request,'productdetails.html',context)
    else:
        return redirect("/ulogin")

def viewcart(request):
    u=User.objects.filter(id=request.user.id)
    c=Cart.objects.filter(uid=request.user.id)
    context={}
    context['data']=c
    context['name']=u[0]
    context['email']=u[0].email
    return render(request,'viewcart.html',context)

def register(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        #print(uname,upass,ucpass)
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields cannot be empty!"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="Password and Confirm Password not matching!"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['successmsg']="User Registered Successfully!"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User already exits, use another emailID!"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    
def ulogin(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(uname,upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="fields cannot be empty!!"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/index')
            else:
                context['errmsg']="Incorrect Username or Password!!"
                return render(request,'login.html',context)
    else:
        return render(request,"login.html")
    

def ulogout(request):
    logout(request)
    return redirect('/index')