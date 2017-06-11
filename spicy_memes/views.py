from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from .models import Post
from .forms import UploadFileForm
from .forms import UploadForm
from .forms import EditForm
from .forms import SignUpForm
from .forms import LogInForm
from .forms import EditProfileForm
from .models import MyUser
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
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
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/spicy_memes/hotPage') #succes redirect to the startpage
    else:
        form = LogInForm()
    return render(request, 'login.html', {'LogInForm': form, 'user' : current_user})

def logOut(request):
    logout(request)
    return HttpResponseRedirect('/spicy_memes')

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


def startPage(request):
    return render(request, 'startPage.html')

def edit_profile (request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/spicy_memes/userprofile')
            #return redirect ('/spicy_memes/userprofile')
    else:
        form=EditProfileForm(instance=request.user)
        args = {'form':form}
        return render (request, 'edit_profile.html' , args)

def change_password (request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user = request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/spicy_memes/userprofile')
            #return redirect ('/spicy_memes/userprofile')
    else:
        form=PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render (request, 'change_password.html' , args)
