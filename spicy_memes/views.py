from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from .models import Post, Tag
from .forms import UploadFileForm
from .forms import UploadForm
from .forms import EditForm
from .forms import SignUpForm
from .forms import LogInForm, SearchForm, TagSearchForm
from .models import MyUser
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta
import datetime
from django.utils.timesince import timesince

def hotPage(request):
    latest_meme_list = Post.objects.order_by('-date') [:20]
    context = {'latest_meme_list': latest_meme_list}
    return render(request, 'hotPage.html', context)

def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.set_password(request.POST['password'])
            user.save()
            user_auth = authenticate(request, username=user.username, password=user.password)
            login(request, user_auth)
            return HttpResponseRedirect('/spicy_memes')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'signUpForm': form})

def userprofile(request):
    current_user = request.user
    authform = LogInForm()
    return render(request, 'userProfile.html', {'AuthForm': authform, 'user' : current_user})

def trendingPage(request):
    return render(request, 'trending.html')

def freshPage(request):
    latest_meme_list = Post.objects.order_by('-date') [:20]
    context = {'latest_meme_list': latest_meme_list}
    return render(request, 'hotPage.html', context)

def loginPage(request):
    current_user = request.user
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/spicy_memes') #succes redirect to the startpage
    else:
        form = LogInForm()
    return render(request, 'login.html', {'LogInForm': form, 'user' : current_user})

def logOut(request):
    logout(request)
    return HttpResponseRedirect('/spicy_memes/loginPage')

def deleteUser(request):
    current_user = request.user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if current_user == user:
            logout(request)
            current_user.delete()
            return HttpResponseRedirect('/spicy_memes/signUp')
        else:
            return HttpResponseRedirect('/spicy_memes/userprofile') #redirect if password is wrong
    else:
        return HttpResponseRedirect('/spicy_memes/userprofile') #redirect if accessed with http-get

def uploadFile(request):
    if request.method == 'POST':
        form = UploadForm(user = request.user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/spicy_memes/')
        else:
            return render(request, 'uploadFile.html', {'form': form}) #add error message at some point
    else:
        form = UploadForm()
        return render(request, 'uploadFile.html', {'form': form})

def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    editform = EditForm(initial={'title': post.title,'description': post.description})
    tdelta = datetime.datetime.now() - post.date.replace(tzinfo=None)
    time_posted = (tdelta.seconds/60) - 120
    time_diff = round(15 - time_posted)
#    if (time_posted <= 15):
#        editable = True
#    else :
#        editable = False
    if (post.user == request.user):
        postOwner = True
    else:
        postOwner = False
    context = {'post': post, 'user': user, 'owner': postOwner, 'editform': editform, 'time_posted': time_posted, 'time_diff': time_diff}
    return render(request, 'postDetail.html', context)

def editPost(request, pk):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, pk=pk)
            post.title = form.cleaned_data['title']
            post.description = form.cleaned_data['description']
            post.save()
            #messages.success(request, 'Post \"%s\" was edited successfully' % post_text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        form = EditForm()
        return render(request, '/spicy_memes/', {'form': form})   

def deleteFile(request, pk):
        po = get_object_or_404(Post, pk=pk)
        po.delete()
        return HttpResponseRedirect('/spicy_memes/')


def search(request):
    if request.method == 'GET':
        searchform= SearchForm(request.GET)
        tagsearchform= TagSearchForm(request.GET)
        posts = []
        if searchform.is_valid():
            search_terms = searchform.cleaned_data.get('search_term').split(',')
            by_tags = searchform.cleaned_data.get('by_tag')
            by_name = searchform.cleaned_data.get('by_name')
            both_false = not (by_tags or by_name)
            for term in search_terms:   #we sort by tags if the tag selection is true or neither is set (default)
                if both_false or by_tags:
                    try:
                        tag= Tag.objects.get(name=term).name
                        if tag is not "":#here or one step up?
                            filtered_posts = Post.objects.filter(tags__name=tag)
                            posts.extend(filtered_posts)
                    except:
                        pass
                if by_name:
                    filtered_posts = Post.objects.filter(title__contains=term)
                    posts.extend(filtered_posts)

        #TODO: clean this code up a bit. maybe add a new function. is shit now
        if tagsearchform.is_valid():
            term= tagsearchform.cleaned_data.get('tag')
            try:
                tag= Tag.objects.get(name=term).name
                if tag is not "":
                    filtered_posts = Post.objects.filter(tags__name=tag)
                    posts.extend(filtered_posts)
            except:
                pass
                        
        context = {'latest_meme_list': posts}  # only temporary
                
    return render(request, 'hotPage.html', context)# only temporary
    
    





















    
