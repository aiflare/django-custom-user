from django.shortcuts import render, redirect 
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views import generic 
from utils.utils import CommonUtils
from utils.password import generate as apassword
from core.user_manager import UserManager, Group
from core.models import User


from django.db.models import Q
from core.models import User, Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate 


@login_required
def index(request):
  return render(request, "dashboard.html", {})

def clear_old_sessions(request):
  try:
    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    Session.objects.filter(session_key=session).delete()
    Session.objects.all().delete()
  except Session.DoesNotExist as error:
    return None


def register(request):
  if request.method == 'GET':
    return render(request, template_name="register.html")

  if request.method == 'POST':
    try:
        common_utils = CommonUtils()
        reqdict = common_utils.to_reqdict(request)
        print("user.is_authenticated", reqdict)
        reqdict.pop('repassword')
        clear_old_sessions(request)
        user_mgr = UserManager()
        user = user_mgr.create_user(reqdict)
        messages.success(request, 'Thank you for registering. To complete your registration please check your email for further instructions.')
        return render(request, template_name="login.html")  
    except IntegrityError as e:
      messages.error(request, "User already exists. Please try singing in or resetting your password.")
      return render(request, template_name="login.html")
    except Exception as e:
      print({"error": e})
      messages.error(request, "Server error, Please contact your adminstrator!.")
    return render(request, template_name="register.html")
      



def login(request):
    print("In login", request.method)
    if request.method == 'GET':
      return render(request, template_name="login.html")
    common_utils = CommonUtils()
    reqdict = common_utils.to_reqdict(request)
    reqdict['username'] = reqdict.get('email')
    reqdict.pop('email')
    print({"message": f"User Logging in - {reqdict} "})
    if not any(reqdict.values()):
        return render(request, template_name="login.html")
        print({"message": f"User Logging in {reqdict}"})
    user_mgr = UserManager()
    user = user_mgr.authenticate(username=reqdict['username'],
    password=reqdict['password'])
    print({"message": f"Request found for {user} "})
    if (user is not None): 
      allowed_user = user.groups.filter(name__in = settings.ALLOWED_GROUPS).exists()
      
      if allowed_user:
        auth_login(request, user)
        return redirect('home')
    return JsonResponse({"message": "Authentication failed. Reset your password or contact Admin", "code":10002, "status":False}, status=403)


def get_default_password(text=None):
  import random, string
  if not text:
    text = apassword()
  if len(text) < 10: 
    text = text+ apassword()
  res = ""
  for index, i in  enumerate(text[::-1]):
    char = random.choice(list(string.printable.replace(" ", "")))
    if index %2==0:
      res+= f'{i.upper()}{char}'
    else:
      res+=i
  # res+= f'{int(random.random()*10000)}'
  return res[:9]

def forgot_password(request):
    
    if request.method == 'GET':
      return render(request, template_name="forgot_password.html")

    common_utils = CommonUtils()
    reqdict = common_utils.to_reqdict(request)
    print({"message": f"User requesting password - {reqdict} "})
    if not any(reqdict.values()):
        return render(request, template_name="login.html")
    
    email = reqdict.get('email')
    
    user_mgr = UserManager()
    user = user_mgr.get_by_email(email)
    if user not in [None, False]:
        password = get_default_password(email)
        user_mgr.set_password(user, password)
        return JsonResponse({"message": f"Password [ {password} ] has been generated and emailed you. Kindly reset the password once you login", "code":10002, "status":False}, status=200)
    else:
        return JsonResponse({"message": "User does not exist, plese sign up.", "code":10001, "status":True}, status=200)
    

def logout(request):
  auth_logout(request)
  return redirect('login')


# def contacts(request):

#   return render(request, template_name="contacts.html")