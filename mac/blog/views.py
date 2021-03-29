from django.shortcuts import render
from django.http import HttpResponse

from .models import Blogpost

# Create your views here.
def index(request):
    posts = Blogpost.objects.all()
    params = {"posts":posts}

    return render(request, "blog/index.html", params)


def blogpost(request, post_id):
    allPosts = Blogpost.objects.all()
    post = Blogpost.objects.get(post_id=post_id)
    """
    for index, item in enumerate(allPosts):
        if item.post_id == post_id:
            prev_post = allPosts[index - 1]
            next_post = allPosts[index + 1]
    """

    params = {"post":post}
    
    return render(request, "blog/blogpost.html", params)