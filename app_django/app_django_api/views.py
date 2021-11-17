from more_itertools import take 
from django.http.response import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Posts
from collections import Counter
from .serializers import PostsSerialiser
import json



@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Lists':'/list/',
        'Authors':'/authors/',
        'Stats':'/stats/'
    }
    return Response(api_urls)

@api_view(['GET'])
def postsList(request):
    posts = Posts.objects.all()
    serializer = PostsSerialiser(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def postsStats(request):
    posts = Posts.objects.values('content')

    word_list=[]
    w_list=[]
    new_word_list=[]
    counted={}
    for w in posts:
        i = w.values()
        list_values=list(i)
        w_list.append(list_values)

        for i in list_values:
            i = str(i)
            word_list.append(i.split())

    for word in word_list:
        word = str(word)
        word = word.replace(',','')
        word = word[1:-1]
        new_word_list=word.split()
        counts = Counter(new_word_list)
        counted.update(counts)

    print(len(counted))
    #print(counted)

    counted = dict(sorted(counted.items(),key=lambda i: i[1], reverse=True))
    counted = dict(take(10, counted.items()))

    return HttpResponse(json.dumps(counted),content_type = 'application/json; charset=UTF-8')

@api_view(['GET'])
def postsStatsAuthors(request,author):
    posts = Posts.objects.filter(authors__contains=author)
    posts = posts.values('content')

    word_list=[]
    w_list=[]
    new_word_list=[]
    counted={}
    for w in posts:
        i = w.values()
        list_values=list(i)
        w_list.append(list_values)

        for i in list_values:
            i = str(i)
            word_list.append(i.split())
            
    for word in word_list:
        word = str(word)
        word = word.replace(',','')
        word = word[1:-1]
        new_word_list=word.split()
        counts = Counter(new_word_list)
        counted.update(counts)
        
    print(len(counted))

    counted = dict(sorted(counted.items(),key=lambda i: i[1], reverse=True))
    counted = dict(take(10, counted.items()))
    return HttpResponse(json.dumps(counted),content_type = 'application/json; charset=UTF-8')

@api_view(['GET'])
def postsAuthorsAuthor(request):
    posts = Posts.objects.values('authors')

    list_combined = {}
    authors_list = []
    lowercase_authors_list = []
    for i in posts:
        i = dict(i)
        i = i.values()
        for x in i:
            print(x)
            authors_list.append(x)
        for x in i:
            x = str(x)
            x = x.replace(' ','')
            x = x.lower()
            lowercase_authors_list.append(x)
            print(x)
       
    list_combined= dict(zip(authors_list,lowercase_authors_list))
    # serializer = PostsSerialiser(posts, many=True)
    # return Response(serializer.data)

    return HttpResponse(json.dumps(list_combined),content_type = 'application/json; charset=UTF-8')