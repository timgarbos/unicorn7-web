# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from games.models import Game
from django.template import RequestContext


def index(request):
	games = Game.objects.all().filter(status=Game.Game.LIVE_STATUS)[:6]
	return render_to_response('unicorn/index.html', {'topnav':'index','games':games},context_instance=RequestContext(request))

def about(request):
    return render_to_response('unicorn/about.html', {'topnav':'about'},context_instance=RequestContext(request))


def blog(request):
    return render_to_response('unicorn/blog.html', {'topnav':'blog'},context_instance=RequestContext(request))