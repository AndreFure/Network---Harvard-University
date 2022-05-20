from django.contrib.auth import authenticate, login, logout
import json
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from network.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User


def index(request):
    posts_list = Post.objects.all().order_by("-created")
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": posts,
        "header": "All posts"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
###############################################################################


@login_required(redirect_field_name='index')
def create_post(request):
    if request.method == "POST":
        post = request.POST["post"]
        new_post = Post(
            user_id=request.user.id,
            post=post)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")


@login_required(redirect_field_name='index')
def user_profile(request, username):
    dataUser = User.objects.get(username=username)
    postsUser = Post.objects.filter(user_id=dataUser.id).order_by("-created")
    paginator = Paginator(postsUser, 10)
    numPage = request.GET.get('page')
    posts = paginator.get_page(numPage)
    return render(request, "network/profile.html", {
        "curent_user_id": dataUser.id,
        "username": username,
        "followers": dataUser.followers.count(),
        "follow": dataUser.follow.count(),
        "posts": posts,
        "header": "ALL POSTS FROM " + username
    })


@csrf_exempt
@login_required
def post_likes(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like"):
            post.unlikes.remove(data["like"])
            post.likes.add(data["like"])
        elif data.get("unlike"):
            post.likes.remove(data["unlike"])
            post.unlikes.add(data["unlike"])
        return JsonResponse({"likes_counter": post.likes_counter(), "message": "YOU VOTED"}, status=201)
    return JsonResponse({"message": "PUT REQUEST REQUIRED"}, status=201)


@csrf_exempt
@login_required(redirect_field_name='index')
def follow(request, user_id):
    if request.method == "PUT":
        srp = User.objects.get(id=user_id)
        data = json.loads(request.body)
        if data.get("follow"):
            srp.followers.add(request.user.id)
        elif data.get("unfollow"):
            srp.followers.remove(request.user.id)
        return JsonResponse({"followers_counter": srp.followers.count(), "message": "YOU ARE FOLLOWING THIS USER NOW"}, status=201)
    return JsonResponse({"message": "PUT REQUEST REQUIRED"}, status=201)


@csrf_exempt
@login_required(redirect_field_name='index')
def following(request):
    uru = Post.objects.filter(
        user__followers__id=request.user.id).order_by("-created")
    paginator = Paginator(uru, 10)
    numPage = request.GET.get('page')
    posts = paginator.get_page(numPage)
    return render(request, "network/index.html", {
        "posts": posts,
        "header": "POSTS FROM USERS I FOLLOW"
    })


@csrf_exempt
@login_required(redirect_field_name='index')
def edit_post(request, post_id):
    if request.method == "PUT":
        post = Post.objects.get(id=post_id)
        data = json.loads(request.body)
        post.post = data["post"]
        post.save()
        return JsonResponse({"message": "OK"}, status=201)
