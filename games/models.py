from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.forms import ModelForm
from djangoratings.fields import RatingField


# Create your models here.

class GameCategory(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(null=True,blank=True,max_length=255,help_text='internal note: Why do we have this category? ')

    def __unicode__(self):
        return self.title

class GamePlatform(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title


class GameJam(models.Model):
    title = models.CharField(max_length=130)
    long_description = models.TextField('description',help_text='Example: The coziest game jam in the world.')
    
    def __unicode__(self):
        return self.title


class Game(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS)

    title = models.CharField(max_length=130)
    pub_date = models.DateTimeField('date created',auto_now=False, auto_now_add=True)
    modified_date = models.DateTimeField('date created',auto_now=True, auto_now_add=False)
    short_description = models.CharField('Short teaser',max_length=255,help_text='Example: This is an erotic rythm game. Do not miss this')
    long_description = models.TextField('description',help_text='Example: it is a game about ... and it is great because of ... you should try it out. (if you would want to write the story of your life then this is the place)')
    short_credits = models.TextField('credits',blank=True,null=True,help_text='Example: It was made by Tim Garbos and Julie Heyde. Thanks to Patrick for the moaning sound effects')
    video = models.URLField(help_text='Optional video (youtube, vimeo, etc) link',null=True,blank=True)
    twitter = models.CharField('twitter id',max_length=100,blank=True)
    developer_url = models.URLField(null=True,blank=True)
    facebook_page = models.URLField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)


    users = models.ManyToManyField(User,null=True,blank=True)
    tags = TaggableManager(blank=True)

    categories = models.ManyToManyField(GameCategory,null=True,blank=True)
    platforms = models.ManyToManyField(GamePlatform, through='GamePlatformLink',null=True,blank=True)


    rating_fun = RatingField(range=5,allow_anonymous=True)
    rating_novelty = RatingField(range=5,allow_anonymous=True)
    rating_humour = RatingField(range=5,allow_anonymous=True)
    rating_visuals = RatingField(range=5,allow_anonymous=True)
    rating_audio = RatingField(range=5,allow_anonymous=True)


    jam = models.ForeignKey(GameJam,null=True,blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "games"

    @classmethod
    def create(cls, title):
        game = cls(title=title)
        # add default links

        return game



class GamePlatformLink(models.Model):
    game = models.ForeignKey(Game)
    platform = models.ForeignKey(GamePlatform)
    url = models.URLField(blank=True)
    archive = models.FileField(upload_to='games/',null=True)



class FrontpagePeriod(models.Model):
    game = models.ForeignKey(Game)
    start_date = models.DateTimeField('start of period')
    end_date = models.DateTimeField('end of period')


class GameImage(models.Model):
    game = models.ForeignKey(Game)
    caption = models.CharField(max_length=200,blank=True)
    image = models.ImageField(upload_to='images')

    def __unicode__(self):
        return self.caption


class GameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ('pub_date','users','categories','platforms','video','twitter','developer_url','facebook_page','email','jam','tags')

class GameSubmitForm(ModelForm):
    class Meta:
        model = Game
        exclude = ('pub_date','users','categories','platforms','video','twitter','developer_url','status','facebook_page','email','jam','tags')

class ContactForm(ModelForm):
    class Meta:
        model = Game
        fields = ('email','twitter','developer_url','facebook_page')

class ImageForm(ModelForm):
    class Meta:
        model = GameImage
        exclude = ('caption')
