# from django.shortcuts import render
#
# # Create your views here.
from django.shortcuts import render

from .models import Den

def feed(request):
  userids = []
  for id in request.user.den_profile.follows.all():
    userids.append(id)

  userids.append(request.user.id)
  dens = Den.objects.filter(user_id__in=userids)[0:25]

  return render(request, 'feed.html', {'dens': dens})

# def follows(request, username):
#   user = User.objects.get(username=username)
#   den_profiles = user.den_profile.follows
#
#   return render(request, 'users.html', {'title': 'Follows', 'den_profiles': den_profiles})
#
# def followers(request, username):
#   user = User.objects.get(username=username)
#   den_profiles = user.den_profile.followed_by
#
#   return render(request, 'users.html', {'title': 'Followers', 'den_profiles': den_profiles})
#
#
#
# def follows(request, username):
#   den_profiles = user.den_profile.follows.select_related('user').all()
#
# def followers(request, username):
#   den_profiles = user.den_profile.followed_by.select_related('user').all()
