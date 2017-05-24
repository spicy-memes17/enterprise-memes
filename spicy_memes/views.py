from django.shortcuts import render

def content(request):
    return render(request, 'content.html')

def userprofile(request):
    return render(request, 'userProfile.html')
