import json
import re
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .forms import *


from .models import User, Category, Product, Comment, Bid, Contactus


class ProductCreate(CreateView):
    model = Product
    fields = ['category', 'created_by', 'title', 'image', 'description', 'starting_bid', 'is_active', 'slug']
    #

class ContactCreate(CreateView):
    model = Contactus
    fields = ['name', 'email', 'mobile', 'subject']



def index(request):
    actives = Product.objects.filter(is_active=True)
    context = {
        "actives": actives
    }
    return render(request, "auctions/index.html", context)

def about(request):
    return render(request, "auctions/about.html")

def categories(request):

    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return context 

def product_detail(request, slug):

    product = get_object_or_404(Product, slug=slug, is_active=True)

    #similar_products = Product.objects.filter(category=category)


    comments_per_product = product.commented_product.filter(active=True)

    form = CommentForm()
    bid_form = BidForm()
        

    context = {
        'active': product,
        #'all_comments': all_comments,
        'all_comments': comments_per_product,
        'form': form,
        'bid_form': bid_form,
        #'similar_products': similar_products
    }

    return render(request, 'auctions/products/detail.html', context)


def category_list(request, category_slug):

    category = get_object_or_404(Category, slug=category_slug)
    products_in_this_category = Product.objects.filter(category=category, is_active=True)

    context = {
        'category': category,
        'products_in_this_category': products_in_this_category
    }

    return render(request, 'auctions/products/category.html', context)


def make_bid(request, slug):
    #pass
    #
    product = get_object_or_404(Product, slug=slug)
    update_product = Product.objects.get(slug=slug)
    update_product.starting_bid 
    print(update_product.starting_bid)
    

    if request.method == 'POST':
        str_val = float(str(request.POST.get('the_bid')))
        bid_input = str_val
        response_data = {}

        if bid_input > update_product.starting_bid:
            print(f'{bid_input} is greater than {update_product.starting_bid}')
            update_product.starting_bid = bid_input
            print(f'starting_bid new val is {update_product.starting_bid}')
            update_product.save()
        else:
            return HttpResponse(
            json.dumps({"Not Acceptable": "Bid higher!"}),
            content_type="application/json"
            )

        new_bid = Bid(user=request.user, product=product, bid_amount=bid_input, )
        new_bid.save()
        

        response_data['result'] = 'Your bid was recorded successfully!'
        response_data['bid_id'] = new_bid.pk
        response_data['bid_amount'] = new_bid.bid_amount
        response_data['bid_time'] = new_bid.bid_time.strftime('%B %d, %Y %I:%M %p')
        response_data['user'] = new_bid.user.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening because of the bid error"}),
            content_type="application/json"
        )


        


def give_comment(request, slug):
    #pass
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        comment_text = request.POST.get('the_post')
        response_data = {}

        comment = Comment(product=product, user=request.user, body=comment_text, )
        comment.save()

        response_data['result'] = 'Comment made successfully!'
        response_data['commentpk'] = comment.pk
        response_data['body'] = comment.body
        response_data['created_on'] = comment.created_on.strftime('%B %d, %Y %I:%M %p')
        response_data['user'] = comment.user.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def add_to_watchlist(request, p_id):
    the_product = get_object_or_404(Product, pk=p_id)

    # check the presence of the item in the watchlist
    if Watchlist.objects.filter(user=request.user, product=product_id).exists():
        messages.add_message(request, messages.ERROR, "You already have it available in your watchlist.")
        return HttpResponseRedirect(reverse("auctions:index"))

    # Get the user watchlist or create it if it doesn't exists
    #use_list, created = Watchlist.obect



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
