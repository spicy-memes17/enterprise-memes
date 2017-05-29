from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .forms import SignUp

from .models import Post
from .forms import UploadFileForm

def content(request):
    upload_file(request)
    return render(request, 'content.html')

def signUp(request):
    if request.method == 'POST':
        signUpForm = SignUp(request.POST)
        if signUpForm.isVaild():
            # use data
            return HttpResponseRedirect('/content/')

    else:
        signUpForm = SignUp()

    return render(request, 'signup.html', {'signUpForm': signUpForm})

def userprofile(request):
    return render(request, 'userProfile.html')

def trendingPage(request):
    return render(request, 'trending.html')

def freshPage(request):
    return render(request, 'fresh.html')

def loginPage(request):
    return render(request, 'login.html')
	
def upload_file(request):
    print("bla")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newPost = Post()
            newPost.title = form.cleaned_data['title']
            newPost.description = form.cleaned_data['description']
            newPost.date = "1/1/17"
            newPost.image_field = request.FILES['image_field']
            newPost.save()
            return HttpResponseRedirect('/content/')
    else:
        form = UploadFileForm()
        return render(request, 'content.html', {'form': form})

    
