from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(topnav, pattern):
	import re
	if re.search(pattern, topnav):
		return 'active'
	return ''


@register.inclusion_tag('unicorn/game_thumbnail.html', takes_context=False)
def showgamethumbnail(game):

	return {'game': game,'url':reverse('games.views.showgame', kwargs={'id': game.id})}