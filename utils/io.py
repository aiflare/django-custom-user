import os
import datetime 
from django.conf import settings


def create_temp_name(name='temp', ext=None):
    return f'{name}_{datetime.datetime.now().strftime("%Y%b%d%H%M%S")}{ext}'


def create_dir(path):
  try:
    os.mkdir(path)
  except OSError as e:
    print({'error': e})

def join_paths(name, *args):
  return os.path.join(name, *args)

def get_or_create_dir(name=None):
  try:
    if not name:
      name = create_temp_name()
    if not os.path.exists(name):
      os.makedirs(settings.MEDIA_ROOT, name)
    return name
  except Exception as e:
    print(e)


def get_profile_path(_id, ext):
    profile_path = join_paths('staff',_id,'profile')
    profile_path = get_or_create_dir(profile_path)
    filename = create_temp_name(_id, ext=ext)
    return join_paths(profile_path, filename)