# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from games.models import Game

def index(request):
	games = Game.objects.all()[:6]
	return render_to_response('unicorn/index.html', {'topnav':'index','games':games})

def about(request):
    return render_to_response('unicorn/about.html', {'topnav':'about'})


def blog(request):
    return render_to_response('unicorn/blog.html', {'topnav':'blog'})