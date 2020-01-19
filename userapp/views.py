from django.shortcuts import render,redirect
from .forms import UserForm, UserProfileInfoForm,SearchForm
from django.contrib.auth.models import User
import tweepy
import threading ,time
import re
import pandas as pd
import nltk
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import requests
from .models import tweets,TotalClassified
# for login..
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views import View
import tweepy
import threading ,time
import re
import pandas as pd
import nltk
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import requests
from django.shortcuts import get_object_or_404


# Create your views here.
def withlogin(request):
     posts = tweets.objects.filter(reciever = request.user).order_by('date')
     print(posts)
     number = get_object_or_404(TotalClassified,id=2)
     reported = get_object_or_404(TotalClassified,id=2)
     
     users =  User.objects.all().count()
     miss = 5
     print(number)
     print(reported)
     context = {
'posts':posts,
'number':number,
'total_reported':reported,
'users':users,
'miss':miss,
     }
     return render(request, 'userapp/withlogin.html' ,{})


def model_proc(query):
    if not query:
        query = "@realDonaldTrump"
    badwords = []
    bow = pickle.load(open("C:/Users/Grindelwald/Desktop/tweeter/App1/tfidf.pickle",'rb'))
    dct = pickle.load(open("C:/Users/Grindelwald/Desktop/tweeter/App1/finalized_model1.sav",'rb'))
    for line in open("C:/Users/Grindelwald/Desktop/tweeter/App1/badwords.txt"):
            for word in line.split( ):
                badwords.append(word)
    consumer_secret = 'Y7xcl4yvOzHCbUG1lQo6KcuX9CocVFwaO8pEp2QCI70Yh1jxuS'
    consumer_key = 'FtdxPkwxNycQsoff0YyBT6mhr'
    access_token = '808233723481100288-DreiznXUXvFUJ25CUkbe3pcmixsa4ia'
    access_token_secret = 'rD9qXxwt51rdUqgX8FbSCHgGJCMAt3THevNxYpKJd6j9G'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    twe = []
    results = []
    for tweet in tweepy.Cursor(api.search, q=query,tweet_mode='extended').items(10):
         
        
        if hasattr(tweet, 'retweeted_status'):
         
            tw = tweet.retweeted_status.full_text
            msg = model_process(tweet.retweeted_status.full_text,badwords)
            if(msg==1):
                result = 1
            
            else:
                bow_matrix = bow.transform([msg])
                df_bow = pd.DataFrame(bow_matrix.todense())
                result  =dct.predict(df_bow)
            print(result)

        else:
            tw = tweet.full_text

            msg = model_process(tweet.full_text,badwords)
            if(msg==1):
                result = 1
            
            else:
                bow_matrix = bow.transform([msg])
                df_bow = pd.DataFrame(bow_matrix.todense())
                result  =dct.predict(df_bow)
        twe.append(tw)
        results.append(result)
        
        if result=='[1]' or result == 1:
              user = User.objects.get(username= "Donald_Trump")
              tweets.objects.create(reciever = user,tw= tw,sender ="@nickson" )

    
    return twe,results






    

def model_process(text,badwords):
    pattern = "@[\w]*"
    
    r=  re.findall(pattern,text)
    
    for i in r:
        text = re.sub(i,"",text)
    text = ' '.join([w for w in text.split() if w.lower() not in stopwords.words('english')])
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    x = text.split()
    for word in x:
        if word in badwords:
            return 1
    
    
    return text

@csrf_exempt
def register(request):
    registered= False
    if request.method=='POST':
        
        user_form= UserForm(data=request.POST)
        profile_form =UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)    #pws saved via hashing
            user.save()

            profile = profile_form.save(commit=False)   #commit=False since we've to check if the pic is there or not before saving it
            profile.user=user   #this is setting the OneToOne relationship in views as it was in models

            # now checking if they provided a profile picture or not

    else:
        
        user_form =  UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'userapp/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered})


@csrf_exempt
def user_login(request):


    if request.method == 'POST':
        username = request.POST.get('username') #since we've given user name as -->name="username" in login.html
        password = request.POST.get('password')


        user= authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                
                return render(request,'userapp/withlogin.html')
                # return HttpResponseRedirect(reverse('index'))

            else:
                # return HttpResponse("Account Not active")
                return HttpResponseRedirect(reverse('user_login'))
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password{}".format(username,password))
            return HttpResponse('invalid login details supplied!')
    else:
        return HttpResponseRedirect(reverse('withlogin'))

@login_required
def special(request):
    return HttpResponse("You are logged in..;-)")



@login_required
def user_logout(request):
    logout(request)
    return render(request,'userapp/index.html',{})




def index(request):
    
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        q =  request.POST['search']
        print(q)
        print("-----------------------------------------")
        result,tweet = model_proc(q)
        posts = tweets.objects.all().order_by('date')
        classify = get_object_or_404(TotalClassified,id=2)
        
     
        users =  User.objects.all().count()
        miss = 5
        
        context = {'data': zip(result, tweet),'posts':posts, 'classify':classify,'users':users,'miss':miss,}
        return render(request,"userapp/withoutlogin.html",context)
   

    posts = tweets.objects.all().order_by('date')
    classify = get_object_or_404(TotalClassified,id=2)
    users =  User.objects.all().count()
    miss = 5
   
    context = {'classify':classify,'users':users,'miss':miss,'form':form,'posts':posts, }
    return render(request,"userapp/index.html",context)

