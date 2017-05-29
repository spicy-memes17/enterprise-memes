from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .forms import SignUp

from .models import Post
from .forms import UploadFileForm
from .forms import UploadForm

def content(request):
    #upload_file(request)
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
	
def uploadFile(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/content/')
    else:
        form = UploadForm()
        return render(request, 'uploadFile.html', {'form': form})