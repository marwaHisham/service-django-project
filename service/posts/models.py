from __future__ import unicode_literals
from django.db.models import Count    

from django.conf import settings

from django.db import models
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from comments.models import Comment
from category.models import Category
from django.contrib.contenttypes.models import ContentType


# Create your models here.

class PostManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(PostManager ,self)

# Create your models here.
def upload_location(instance ,filename):
    #filebase ,extension=filename.split('.')
    return "%s/%s" %(instance.id,filename)



class Post (models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,default=1)
    category= models.ForeignKey(Category, on_delete=models.PROTECT,default=1)
    title = models.CharField(max_length=255)
    #slug= models.SlugField(unique=True)
    #image = models.FileField(null = True , blank=True)
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    image = models.ImageField(upload_to=upload_location,
        null = True , blank=True, 
        width_field="width_field",height_field="height_field")
    content= models.TextField(default='this is content')
    qoute= models.TextField(default='this is content' ,null= True)
    #draft=models.BooleanField(default= False)
    publish = models.DateField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True ,auto_now_add=False)
    timestamp=models.DateTimeField(auto_now=False ,auto_now_add=True)
    uniquewords = models.CharField(max_length=255,default="project")
    is_favorite = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    #objects=PostManager()
    
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("postDetails",kwargs={"id":self.id})
        #return "/posts/detail/%s/" %(self.id)

    class Meta:
        ordering = ['timestamp']
    
    def upload_location(instance ,filename):
    #filebase ,extension=filename.split('.')
        return "%s/%s" %(instance.id,filename)

    @property
    def comments(self):
        instance=self
        qs=Comment.objects.filter_by_instace(instance)
        return qs

    @property
    def get_content_type(self):
        instance=self
        content_type=ContentType.objects.get_for_model(instance.__class__)
        return content_type
    


class Post_user_fav(models.Model):
     user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,default=1)
     post= models.ForeignKey(Post, on_delete=models.PROTECT,default=1)
     timestamp=models.DateTimeField(auto_now=False ,auto_now_add=True)
 
     def __unicode__(self):
        return self.user

     def __str__(self):
        return self.post.title