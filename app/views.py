from django.shortcuts import render,redirect
from .models import User,Contact,Product,Wishlist,Cart
from django.conf import settings
from django.core.mail import send_mail
import random
# Create your views here.

def index(request):
    products=Product.objects.all()
    return render(request,'index.html',{'products':products})

def shop(request):
    return render(request,'shop.html')
def detail(request):
    return render(request,'detail.html')

def contact(request):
    if request.method=="POST":
        Contact.objects.create(
            fname=request.POST['fname'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        msg="Message Send Successfully"
        return render(request,'contact.html',{'msg':msg})
    else:
        return render(request,'contact.html')

def checkout(request):
    return render(request,'checkout.html')

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Exists"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    zipcode=request.POST['zipcode'],
                    password=request.POST['password'],
                    profile=request.FILES['profile'],
                    usertype=request.POST['usertype'],
                )
                msg="Email Register Successfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Not Match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')
    

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                if user.usertype=="buyer":
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    request.session['profile']=user.profile.url

                    return render(request,'index.html')
                else:
                    request.session['email']=user.email
                    request.session['fname']=user.fname
                    request.session['profile']=user.profile.url
                    return render(request,'seller-index.html')
            else:
                msg="Incorrect Password"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email Not Register"
            return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'login.html')

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return redirect('logout')
    except:
        return render(request,'login.html')

def change_password(request):
    user=User.objects.get(email=request.session['email'])  
    if request.method=="POST":
        if user.password==request.POST['oldpassword']:
            if request.POST['newpassword']==request.POST['cnewpassword']:
                user.password=request.POST['newpassword']
                user.save()
                return redirect('logout')
            else:
                if user.usertype=="buyer":                    
                    msg="New Password & Confirm Password Does Not Matched"
                    return render(request,'change-password.html',{'msg':msg})
                else:
                    msg="New Password & Confirm Password Does Not Matched"
                    return render(request,'seller-change-password.html',{'msg':msg})
        else:
            if user.usertype=="buyer":
                msg="Incorrect Old Password"
                return render(request,'change-password.html',{'msg':msg})
            else:
                msg="Incorrect Old Password"
                return render(request,'seller-change-password.html',{'msg':msg})
                
    else:
        if user.usertype=="buyer":
            return render(request,'change-password.html')
        else:
            return render(request,'seller-change-password.html')
    
def forgot_password(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            subject = 'OTP For Forgot Password'
            message = "Hello "+user.fname+ " Your OTP Is "+ str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'otp.html',{'email':user.email,'otp':otp})
        except Exception as e:
            print(e)
            msg="Email Not Register"
            return render(request,'forgot-password.html',{'msg':msg})
    else:
        return render(request,'forgot-password.html')

def verify_otp(request):
    email=request.POST['email']
    otp=request.POST['otp']
    uotp=request.POST['uotp']

    if otp==uotp:        
        return render(request,'new-password.html')
    else:
        msg="Incorrect OTP"
        return render(request,'otp.html',{'msg':msg})
    
def new_password(request):
    email=request.POST['email']
    np=request.POST['newpassword']
    cnp=request.POST['cnewpassword']

    if np==cnp:
        user=User.objects.get(email=email)
        user.password=np
        user.save()
        return redirect('login')
    else:
        msg="New Password & Confirm New Password Does Not Matched"
        return render(request,'new-password.html',{'email':email,'msg':msg})

def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.email=request.POST['email']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        try:
            user.profile=request.FILES['profile']
        except:
            pass
        user.save()
        request.session['profile']=user.profile.url   # for header image
        msg="Profile Update Successfully"
        if user.usertype=="buyer":
            return render(request,'profile.html',{'msg':msg,'user':user})
        else:
            return render(request,'seller-profile.html',{'msg':msg,'user':user})
    else:
        if user.usertype=="buyer":
            return render(request,'profile.html',{'user':user})
        else:
            return render(request,'seller-profile.html',{'user':user})


def seller_index(request):
    return render(request,'seller-index.html')

def seller_add_product(request):
    seller=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        Product.objects.create(
            seller=seller,
            product_category=request.POST['product_category'],
            product_name=request.POST['product_name'],
            product_price=request.POST['product_price'],
            product_desc=request.POST['product_desc'],
            product_image=request.FILES['product_image'],
        )
        msg="Product Added Successfully"
        return render(request,'seller-add-product.html',{'msg':msg})
    else:
        return render(request,'seller-add-product.html')

def seller_view_product(request):
    seller=User.objects.get(email=request.session['email'])
    products=Product.objects.filter(seller=seller)
    return render(request,'seller-view-product.html',{'products':products})

def seller_order_product(request):
    return render(request,'seller-order-product.html')\
    

def seller_view_detail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'seller-view-detail.html',{'product':product})

def seller_edit_product(request,pk):
    seller=User.objects.get(email=request.session['email'])
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.product_category=request.POST['product_category']
        product.product_name=request.POST['product_name']
        product.product_price=request.POST['product_price']
        product.product_desc=request.POST['product_desc']
        try:
            product.product_image=request.FILES['product_image']
        except:
            pass
        product.save()
        msg="Product Update Successfully"
        return render(request,'seller-edit-detail.html',{'product':product,'msg':msg})
    else:
        return render(request,'seller-edit-detail.html',{'product':product})
    
def seller_delete_product(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect('seller-view-product')

def view_detail(request,pk):
    wishlist_flag=False
    cart_flag=False
    product=Product.objects.get(pk=pk)
    try:
        user=User.objects.get(email=request.session['email'])
        try:
            Cart.objects.get(user=user,product=product)
            cart_flag=True
        except:
            pass
        
        try:
            Wishlist.objects.get(user=user,product=product)
            wishlist_flag=True
        except:
            pass
        return render(request,'view-detail.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag})
    except:
        return render(request,'view-detail.html',{'product':product})

   
def add_to_wishlist(request, pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(
        user=user,
        product=product
    )
    return redirect('wishlist')

def wishlist(request):
    try:
        user=User.objects.get(email=request.session['email'])
        wishlist=Wishlist.objects.filter(user=user)
        return render(request,"wishlist.html",{'wishlist':wishlist})

    except:
    
        return render(request,'login.html')

def remove_from_wishlist(request, pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.filter(user=user,product=product)
    wishlist.delete()
    return redirect('wishlist')

def add_to_cart(request, pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(
        user=user,
        product=product,
        product_price=product.product_price,
        product_qty=1,
        total_price=product.product_price,
    )
    return redirect('cart')

def cart(request):
    try:
        user=User.objects.get(email=request.session['email'])
        cart=Cart.objects.filter(user=user)
        return render(request,"cart.html",{'cart':cart})
    except:
        return render(request,'login.html')


def remove_from_cart(request, pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.filter(user=user,product=product)
    cart.delete()
    return redirect('cart')
