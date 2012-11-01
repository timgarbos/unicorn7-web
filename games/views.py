# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from games.models import Game, GameForm,GamePlatform,GameCategory,GamePlatformLink,ContactForm,GameSubmitForm,GameJam,GameImage,ImageForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from djangoratings.views import AddRatingFromModel
from django.contrib.auth.models import User


def showjam(request,id):

	try:
		jam = GameJam.objects.get(id=id)
	except GameJam.DoesNotExist:
		return render_to_response('unicorn/jamdoesnotexist.html')

	game_list = Game.objects.filter(status=Game.LIVE_STATUS,jam__id=id)

	paginator = Paginator(game_list, 20)
	page = request.GET.get('page')
	try:
		games = paginator.page(page)
 	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		games = paginator.page(1)
 	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		games = paginator.page(paginator.num_pages)
	
	return render_to_response('unicorn/showjam.html', {'topnav':'showjam','games':games,'jam':jam},context_instance=RequestContext(request))
  

def profile(request,id=None):
	if id == None:
		id = request.user.id
	try:
		user = User.objects.get(id=id)
	except User.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	game_list = Game.objects.filter(status=Game.LIVE_STATUS,users=user)

	paginator = Paginator(game_list, 20)
	page = request.GET.get('page')
	try:
		games = paginator.page(page)
 	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		games = paginator.page(1)
 	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		games = paginator.page(paginator.num_pages)
	
	return render_to_response('unicorn/profile.html', {'topnav':'showjam','games':games,'user':user},context_instance=RequestContext(request))
  


def listgames(request):
	sorting = None
	category = None
	platform = None
	search = None

	game_list = Game.objects.filter(status=Game.LIVE_STATUS)

	if 'sorting' in request.GET:
		sorting=request.GET['sorting']
		if sorting == '0':
			game_list = game_list.order_by('-pub_date')
		if sorting == '1': #rating_fun
			game_list = game_list.extra(select={'rating': '((100/%s*rating_fun_score/(rating_fun_votes+%s))+100)/2' % (Game.rating_fun.range, Game.rating_fun.weight)})
			game_list = game_list.order_by('rating')
		if sorting == '2': #rating_novelty
			game_list = game_list.extra(select={'rating': '((100/%s*rating_novelty_score/(rating_novelty_votes+%s))+100)/2' % (Game.rating_novelty.range, Game.rating_novelty.weight)})
			game_list = game_list.order_by('rating')
		if sorting == '3': #rating_humour
			game_list = game_list.extra(select={'rating': '((100/%s*rating_humour_score/(rating_humour_votes+%s))+100)/2' % (Game.rating_humour.range, Game.rating_humour.weight)})
			game_list = game_list.order_by('rating')
		if sorting == '4': #rating_visuals
			game_list = game_list.extra(select={'rating': '((100/%s*rating_visuals_score/(rating_visuals_votes+%s))+100)/2' % (Game.rating_visuals.range, Game.rating_visuals.weight)})
			game_list = game_list.order_by('rating')
		if sorting == '5': #rating_audio
			game_list = game_list.extra(select={'rating': '((100/%s*rating_audio_score/(rating_audio_votes+%s))+100)/2' % (Game.rating_audio.range, Game.rating_audio.weight)})
			game_list = game_list.order_by('rating')

	if 'category' in request.GET:
		category=request.GET['category']
		game_list = game_list.filter(categories__id__exact=category)
	if 'platform' in request.GET:
		platform=request.GET['platform']
		game_list = game_list.filter(platforms__gameplatformlink__platform__id__exact=platform)
	if 'search' in request.GET:
		search=request.GET['search']
		game_list = game_list.filter(title__contains=search)

	paginator = Paginator(game_list, 20)
	page = request.GET.get('page')
	try:
		games = paginator.page(page)
 	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		games = paginator.page(1)
 	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		games = paginator.page(paginator.num_pages)
	categories = GameCategory.objects.all()
	platforms = GamePlatform.objects.all()
	return render_to_response('unicorn/games.html', {'topnav':'listgames','games':games,'categories':categories,'platforms':platforms,'cat':category,'sort':sorting,'plat':platform,'search':search},context_instance=RequestContext(request))
  
@login_required  
@csrf_protect
def submitgamebasic(request,jam=None):
	context = {'topnav':'submitgamebasic'}
	if request.method == 'POST': 
		game = Game()

		form = GameSubmitForm(request.POST,instance = game) 
		if form.is_valid():
			
			form.save()
			form.instance.users.add(request.user)
			form.instance.save()
			context['success'] = True
			return HttpResponseRedirect(reverse('games.views.submitgamemedia', kwargs={'id': game.id}))
		else:
			context['error'] = True 
	else:
		form = GameSubmitForm()

	if jam:
		try:
			jamO = GameJam.objects.get(id=jam)
			context['jam'] = jamO
		except GameJam.DoesNotExist:
			return render_to_response('unicorn/jamsdoesnotexist.html')

	context['form'] = form;
	return render_to_response('unicorn/submitgame_basic.html',context,context_instance=RequestContext(request))

@login_required  
@csrf_protect
def submitgameplatforms(request,id="-1"):
	context = {'topnav':'submitgameplatforms'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))

	if request.method == 'POST': 
		
		for platform in GamePlatform.objects.all():
			if (str(platform.id) in request.POST) or 'file_'+str(platform.id) in request.FILES:
				try:
					old = GamePlatformLink.objects.get(game=game,platform=platform)
				except GamePlatformLink.DoesNotExist:
					old = None

				url = request.POST[str(platform.id)]
		
				if 'file_'+str(platform.id) in request.FILES:
					link = GamePlatformLink(platform=platform,game=game,archive=request.FILES['file_'+str(platform.id)])
					if link.archive.size>40*1024*1024:
						context['error'] = True
						context['errorMsg'] = "The file was too large. Keep it under 40MB or host it yourself.";
					else:
						link.save()
					if old:
						old.delete()
				elif url != '':
					link = GamePlatformLink(platform=platform,game=game,url=url)
					link.save()
					if old:
						old.delete()
		game.save()
		context['success'] = True 
		return HttpResponseRedirect(reverse('games.views.submitgamecategories', kwargs={'id': game.id}))
	
	links = []
	for platform in GamePlatform.objects.all():
		link = GamePlatformLink(platform=platform,game=game)
		for l in GamePlatformLink.objects.filter(game=game):
			if(l.platform == platform):
				link = l
				hasLink = True
		links.append({'platform':link.platform,'url':link.url,'file':link.archive})

	context['game'] = game;
	context['links'] = links;
	return render_to_response('unicorn/submitgame_links.html', context,context_instance=RequestContext(request))

@login_required  
@csrf_protect
def submitgamecategories(request,id="-1"):
	context = {'topnav':'submitgamecategories'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))
	
	if request.method == 'POST': 
		game.categories.clear()
		for category in GameCategory.objects.all():
			if (str(category.id) in request.POST):
				game.categories.add(category)
		game.save()
		context['success'] = True 
		return HttpResponseRedirect(reverse('games.views.submitgamecontact', kwargs={'id': game.id}))
	cats = []
	for category in GameCategory.objects.all():
		has = False
		for c in game.categories.all():
			if(c.id == category.id):
				has = True
		cats.append({'category':category,'has':has})

	context['game'] = game;
	context['categories'] = cats;
	return render_to_response('unicorn/submitgame_categories.html', context,context_instance=RequestContext(request))

@login_required  
@csrf_protect
def submitgamecontact(request,id="-1"):
	context = {'topnav':'submitgamecontact'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))

	if request.method == 'POST': 
		form = ContactForm(request.POST,instance = game) 
		if form.is_valid():
			form.save()
			context['success'] = True 
			return HttpResponseRedirect(reverse('games.views.submitgamepublish', kwargs={'id': game.id}))
		else:
			context['error'] = True 
	else:
		form = ContactForm(instance=game)
	context['form'] = form;
	context['game'] = game;
	return render_to_response('unicorn/submitgame_contact.html', context,context_instance=RequestContext(request))

@login_required  
@csrf_protect
def submitgamepublish(request,id="-1"):
	context = {'topnav':'submitgamepublish'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))

	if request.method == 'POST': 
			context['success'] = True 
			game.status = Game.LIVE_STATUS
			game.save()
			return HttpResponseRedirect(reverse('games.views.submitgamepublished', kwargs={'id': game.id}))
	context['game'] = game;
	return render_to_response('unicorn/submitgame_publish.html', context,context_instance=RequestContext(request))

@login_required  
@csrf_protect
def submitgamemedia(request,id="-1"):
	context = {'topnav':'submitgamemedia'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))

	if request.method == 'POST': 
		
	else:
		#for all images
		imgs = GameImage.objects.all().filter(game=game)
		forms = []
		for img in imgs:
			forms.append(ImageForm(instance=img))
		while len(forms)<=5:
			forms.append(ImageForm())

	context['forms'] = forms;
	context['game'] = game;
	return render_to_response('unicorn/submitgame_media.html', context,context_instance=RequestContext(request))

@login_required  
def submitgamepublished(request,id="-1"):
	context = {'topnav':'submitgamepublished'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))

	context['game'] = game;
	return render_to_response('unicorn/submitgame_published.html', context,context_instance=RequestContext(request))

    
def showgame(request,id="-1"):
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	showEdit = False
	platforms = GamePlatformLink.objects.filter(game=game)
	if request.user.is_authenticated():
		if ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			showEdit = True;
	return render_to_response('unicorn/showgame.html', {'topnav':'showgame','game':game,'platforms':platforms,'showEditOptions':showEdit},context_instance=RequestContext(request))


@login_required  
@csrf_protect
def editgamebasic(request,id="-1"):
	context = {'topnav':'editgamebasic'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')

	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))

	if request.method == 'POST': 
		form = GameForm(request.POST,instance = game) 
		if form.is_valid():
			form.save()
			context['success'] = True 
		else:
			context['error'] = True 
	else:
		form = GameForm(instance=game)

	context['form'] = form;
	context['game'] = game;

	return render_to_response('unicorn/editgame_basic.html', context,context_instance=RequestContext(request))

@login_required  
@csrf_protect
def editgamecontact(request,id="-1"):
	context = {'topnav':'editgamecontact'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html',)
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))

	if request.method == 'POST': 
		form = ContactForm(request.POST,instance = game) 
		if form.is_valid():
			form.save()
			context['success'] = True 
		else:
			context['error'] = True 
	else:
		form = ContactForm(instance=game)
	context['form'] = form;
	context['game'] = game;
	return render_to_response('unicorn/editgame_contact.html', context,context_instance=RequestContext(request))

@login_required  
@csrf_protect
def editgameplatforms(request,id="-1"):
	context = {'topnav':'editgameplatforms'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))

	if request.method == 'POST': 
		
		for platform in GamePlatform.objects.all():
			if (str(platform.id) in request.POST) or 'file_'+str(platform.id) in request.FILES:
				try:
					old = GamePlatformLink.objects.get(game=game,platform=platform)
				except GamePlatformLink.DoesNotExist:
					old = None

				url = request.POST[str(platform.id)]
		
				if 'file_'+str(platform.id) in request.FILES:
					link = GamePlatformLink(platform=platform,game=game,archive=request.FILES['file_'+str(platform.id)])
					if link.archive.size>40*1024*1024:
						context['error'] = True
						context['errorMsg'] = "The file was too large. Keep it under 40MB or host it yourself.";
					else:
						link.save()
					if old:
						old.delete()
				elif url != '':
					link = GamePlatformLink(platform=platform,game=game,url=url)
					link.save()
					if old:
						old.delete()
		game.save()
		context['success'] = True 
	
	links = []
	for platform in GamePlatform.objects.all():
		link = GamePlatformLink(platform=platform,game=game)
		for l in GamePlatformLink.objects.filter(game=game):
			if(l.platform == platform):
				link = l
				hasLink = True
		links.append({'platform':link.platform,'url':link.url,'file':link.archive})

	context['game'] = game;
	context['links'] = links;
	return render_to_response('unicorn/editgame_links.html', context,context_instance=RequestContext(request))

@login_required  
@csrf_protect
def editgamecategories(request,id="-1"):
	context = {'topnav':'editgamecategories'}
	try:
		game = Game.objects.get(id=id)
	except Game.DoesNotExist:
		return render_to_response('unicorn/gamesdoesnotexist.html')
	if request.user.is_authenticated():
		if not ((game.users.filter(id = request.user.id)[:1]) or (request.user.is_staff)):
			return HttpResponseRedirect(reverse('account_login'))
	
	if request.method == 'POST': 
		game.categories.clear()
		for category in GameCategory.objects.all():
			if (str(category.id) in request.POST):
				game.categories.add(category)
		game.save()
		context['success'] = True 
	
	cats = []
	for category in GameCategory.objects.all():
		has = False
		for c in game.categories.all():
			if(c.id == category.id):
				has = True
		cats.append({'category':category,'has':has})

	context['game'] = game;
	context['categories'] = cats;
	return render_to_response('unicorn/editgame_categories.html', context,context_instance=RequestContext(request))

@login_required  
def editgamemedia(request,id="-1"):
	

def rategame(request,id="-1",type="-1"):


	if request.method == 'GET': 
		rate = request.GET['rate']
		field = ''
		if type=='0':
			field = 'rating_fun'
		if type=='1':
			field = 'rating_novelty'
		if type=='2':
			field = 'rating_humour'
		if type=='3':
			field = 'rating_visuals'
		if type=='4':
			field = 'rating_audio'

		params = {
		    'model': 'game',
		    'object_id': id,
		    'app_label': 'games',
		    'field_name': field, # this should match the field name defined in your model
		    'score': rate, # the score value they're sending
		}
		response = AddRatingFromModel()(request, **params)
		
		return HttpResponse(content=response.content)
	return HttpResponse(content='')