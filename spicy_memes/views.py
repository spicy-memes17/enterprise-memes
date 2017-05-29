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
    latest_meme_list = Post.objects.order_by('-date') [:20]
    context = {'latest_meme_list': latest_meme_list}
    return render(request, 'content.html', context)

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
            return HttpResponseRedirect('/spicy_memes/')
    else:
        form = UploadForm(initial = {'post.group_id': 0 })
        return render(request, 'uploadFile.html', {'form': form})