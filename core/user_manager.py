from django.db.models import Q
from core.models import User, Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate 

# from django.contrib.auth.models import Group


# Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))


class UserManager:

  def all(self):
    return User.objects.all()

  def get_professors(self):
    return User.objects.all().exclude(groups__name__in=['student', 'parent'])


  def get_staff(self):
    return User.objects.all().exclude(groups__name__in=['student', 'parent'])

  def groups(self):
    return Group.objects.all()

  def create_user(self, reqdict):
    if not self.get_user(reqdict.get('username')):
      # reqdict['username'] = reqdict.get('email')
      is_admin = True if reqdict.pop('is_admin', None) == 'true' else False
      user = User.objects.create_user(**reqdict) 
      grp , created= Group.objects.get_or_create(name='other')
      if is_admin:
        grp, created = Group.objects.get_or_create(name='admin')
      user.groups.add(grp)
      user.save()
    return user

  def get_by_email(self, email):
    try:
      return User.objects.get(
        email=email
      )
    except User.DoesNotExist as err:
      return False
    except ValueError as err:
      return False

  def get_user(self, user_field):
    """ login_field could be email or mobile or id""" 
    try:
      return User.objects.get(
        Q(email=user_field)|Q(id=user_field)|Q(mobile=user_field) 
      )
    except User.DoesNotExist as err:
      return False
    except ValueError as err:
      return False


  def authenticate(self, username=None, password=None):
    user = self.get_user(username)
    print(user, user.check_password(password), "Check") 
    if user and user.check_password(password):
      return user
    return None
      
  def set_password(self, user, password):
      user.set_password(password)
      user.save()

  def update_user(self, user_id, reqdict):
      pass