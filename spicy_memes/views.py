from django.shortcuts import render

def content(request):
    return render(request, 'content.html')