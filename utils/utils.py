import operator
from itertools import chain
from django.contrib import messages

class CommonUtils:

  def to_reqdict(self, request):
    reqdict = {}
    if request.method == 'POST':
      reqdict = dict(zip(request.POST.keys(), request.POST.values()))
    else:
      reqdict = dict(zip(request.GET.keys(), request.GET.values()))
    reqdict.pop('csrfmiddlewaretoken', None)
    password = reqdict.pop('password', None)
    print({'Request:': reqdict})
    reqdict['password'] = password
    return reqdict

  def extract_only(self, keys, dictobj):
    try:
      return dict(zip(keys, [dictobj.get(k, None) for k in keys]))
    except Exception as err:
      print({"error in extract_only": err})
      return {}

  def setattr(self, instance, info):
    for attr in info.keys():
      try:
        if hasattr(instance, attr):
          setattr(instance, attr, info.get(attr))
        if hasattr(instance, 'save'):
          instance.save()
      except Exception as err:
        print ('error in `setattr` saving to database ', err)
        return None, err
    return instance, 'success'

  def valid_text(self, text, *args):
    print(text, dict(zip([text, *args], [isinstance(i, str) for i in chain((text,), args)])))
    return all([isinstance(i, str) for i in chain((text,), args)])

