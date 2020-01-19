from django.contrib import admin
from userapp.models import UserProfileInfo,tweets,TotalClassified

# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(tweets)
admin.site.register(TotalClassified)
