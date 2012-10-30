from games.models import Game,GameImage,GamePlatform,GameCategory,GamePlatformLink,GameJam
from django.contrib import admin

admin.site.register(Game)

admin.site.register(GameImage)
admin.site.register(GameJam)
admin.site.register(GamePlatform)
admin.site.register(GameCategory)
admin.site.register(GamePlatformLink)