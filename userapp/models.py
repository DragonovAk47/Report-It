from django.db import models
from django.contrib.auth.models import User #this is the builtin user--present in admin page

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    #additional
    handle = models.CharField(max_length=100,blank=True)


    # ie the uploaded images will be saved under 'profile_pics' in media folder

    def __str__(self):
        return self.user.username

class tweets(models.Model):
    tw = models.TextField()
    reciever = models.ForeignKey(User,on_delete = models.CASCADE)
    sender = models.CharField(max_length = 200)
    reported = models.BooleanField(default = 0)
    date = models.DateTimeField(auto_now = True)



class TotalClassified(models.Model):
    number = models.IntegerField(default = 0)
    total_reported = models.IntegerField(default=0)
