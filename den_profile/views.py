# Import django and models

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from den_profile.forms import SignupForm, SigninForm
from den.forms import DenForm # Add this line

# Views

def profile(request, username): # Replace the old profile view with this one
  if request.user.is_authenticated:
    user = User.objects.get(username=username)

    if request.method == 'POST':
      form = DenForm(data=request.POST)

      if form.is_valid():
        den = form.save(commit=False)
        den.user = request.user
        den.save()

        redirecturl = request.POST.get('redirect', '/')

        return redirect(redirecturl)
    else:
      form = DenForm()

    return render(request, 'profile.html', {'form': form, 'user': user})
  else:
    return redirect('/')

def frontpage(request):
  if request.user.is_authenticated:
    return redirect('/' + request.user.username + '/') # Change this line
  else:
    if request.method == 'POST':
      if 'signupform' in request.POST:
        signupform = SignupForm(data=request.POST)
        signinform = SigninForm()

        if signupform.is_valid():
          username = signupform.cleaned_data['username']
          password = signupform.cleaned_data['password1']
          signupform.save()
          user = authenticate(username=username, password=password)
          login(request, user)
          return redirect('/')
      else:
        signinform = SigninForm(data=request.POST)
        signupform = SignupForm()

        if signupform.is_valid():
          login(request, signupform.get_user())
          return redirect('/')
    else:
      signupform = SignupForm()
      signinform = SigninForm()

    return render(request, 'frontpage.html', {'signupform': signupform, 'signinform': signinform})

def signout(request):
  logout(request)
  return redirect('/')

def follows(request, username):
  user = User.objects.get(username=username)
  den_profiles = user.den_profile.follows.select_related('user').all()
  return render(request, 'users.html', {'title': 'Follows', 'den_profiles': den_profiles})

def followers(request, username):
  user = User.objects.get(username=username)
  den_profiles = user.den_profile.followed_by.select_related('user').all()
  return render(request, 'users.html', {'title': 'Followers', 'den_profiles': den_profiles})

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def follow(request, username):
  user = User.objects.get(username=username)
  request.user.den_profile.follows.add(user.den_profile)

  return redirect('/' + user.username + '/')

@login_required
def stopfollow(request, username):
  user = User.objects.get(username=username)
  request.user.den_profile.follows.delete(user.den_profile)

  return redirect('/' + user.username + '/')
