from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required


class Login(View):
  def post(self, request):
    if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      user = authenticate(email=email,
                          password=password)
      if user:
        if user.active:
          login(request, user)
    return HttpResponse(json.dumps(response))


@login_required
def Logout(request):
  logout(request)
  response = {'status': 'success',
              'message': 'logged out'}
  return HttpResponse(json.dumps(response))
