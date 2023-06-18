from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url='/login/')
def medicines(request):
    if request.method=="POST":
        data=request.POST
        medicine_name=data.get('medicine_name')
        medicine_desc=data.get("medicine_desc")
        medicine_img=request.FILES.get('medicine_img')
        Medicine.objects.create(medicine_name=medicine_name,
        medicine_desc=medicine_desc,
        medicine_img=medicine_img)
        print(medicine_img)
        return redirect('/medicines/')
    qs=Medicine.objects.all()
    if request.GET.get('search'):
        print(request.GET.get('search'))
        qs=qs.filter(medicine_name__icontains=request.GET.get('search'))
    context={'medicines':qs}
    print(qs)
    return render(request,'medicine.html',context)

def viewall(request):
    qs=Medicine.objects.all()
    if request.GET.get('search'):
        print(request.GET.get('search'))
        qs=qs.filter(medicine_name__icontains=request.GET.get('search'))
    paginator = Paginator(qs, 5)  # Show 25 contacts per page.

    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)
    context={'medicines':page_obj}
    print(qs)
    return render(request,'display.html',context)



def medicine(request):
    if request.method=="POST":
        data=request.POST
        medicine_name=data.get('medicine_name')
        medicine_desc=data.get("medicine_desc")
        medicine_img=request.FILES.get('medicine_img')
        Medicine.objects.create(medicine_name=medicine_name,
        medicine_desc=medicine_desc,
        medicine_img=medicine_img)
        print(medicine_img)
        return redirect('/medicines/')
    qs=Medicine.objects.all()
    #context={'medicines':qs}
    print(qs)
    return render(request,'front.html')

@login_required(login_url='/login/')
def del_medicine(request,id):
    print("insisde delete")
    query=Medicine.objects.get(id=id)
    print(query)
    query.delete()
    #query.delete()
    return redirect('/medicines/')

@login_required(login_url='/login/')
def update_med(request,id):
    qs=Medicine.objects.get(id=id)
    

    if request.method=="POST":
        data=request.POST
        medicine_name=data.get('medicine_name')
        medicine_desc=data.get('medicine_desc')
        medicine_img=request.FILES.get('medicine_img')
        qs.medicine_name=medicine_name
        qs.medicine_desc=medicine_desc
        if medicine_img:
            qs.medicine_img=request.FILES.get('medicine_img')
        qs.save()
        return redirect('/medicines/')
    context={'medicine':qs}
    return render(request,'update_medicine.html',context)

def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid user')
            return redirect('/login/')

        user=authenticate(username=username,password=password)

        if user is None:
            messages.error(request,'Invalid Password')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/medicines/')
    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')




def register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'User already taken')
            return redirect('/register/')

        user=User.objects.create(first_name=first_name,last_name=last_name,username=username)
        user.set_password(password)
        user.save()
        messages.info(request,"Account created successfully")

        return redirect('/register/')
    return render(request,'register.html')



    