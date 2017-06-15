from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Post
from .forms import UploadFileForm
from .forms import UploadForm
from .forms import EditForm
from .forms import SignUpForm
from .forms import LogInForm
from .forms import EditProfileForm
from .forms import ChangeProfilePic
from .models import MyUser
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import datetime
from django.utils.timesince import timesince
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Post, MyUser, Comment, LikesComment, LikesPost
from .forms import UploadFileForm, UploadForm, EditForm, SignUpForm, LogInForm, CommentForm, VoteCommentForm, LikeForm

@login_required
def content(request, content=None):
    if(content == None):
        content = "on_fire"

    memeList = Post.objects.all()
    memeTupleList = list()
    sortedMemeList = list()

    for post in memeList:
        mtuple = (post,
                  (LikesPost.objects.filter(post=post).filter(likes=True).count()
                   - LikesPost.objects.filter(post=post).filter(likes=False).count())*2
                  + Comment.objects.filter(post=post).count()*5)
        memeTupleList.append(mtuple)

    memeTupleList = sorted(memeTupleList, key=lambda x: x[1], reverse=True)
    
    if(content == "fresh"):
        content = "Fresh"
        sortedMemeList = Post.objects.order_by('-date') [:20]
    elif(content == "spicy"):
        content = "Spicy"
        for tup in memeTupleList:
            if(tup[1] >= 5 and tup[1] < 15):
                sortedMemeList.append(tup[0])
    elif(content == "on_fire"):
        content = "On Fire"
        for tup in memeTupleList:
            if(tup[1] >= 15):
                sortedMemeList.append(tup[0])
                
    context = {'memeList': sortedMemeList, 'content': content}
    return render(request, 'content.html', context)    


def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.set_password(request.POST['password'])
            user.save()
            user_auth = authenticate(username=user.username, password=user.password)
            login(request, user_auth)
            return HttpResponseRedirect('/spicy_memes')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'signUpForm': form})


@login_required
def userprofile(request):
    current_user = request.user
    generalForm = EditProfileForm(instance=request.user);
    authform = LogInForm()
    profilepicform = ChangeProfilePic()
    passwordform = PasswordChangeForm(data=request.POST, user=request.user)
    return render(request, 'userProfile.html', {'AuthForm': authform, 'user' : current_user, 'passwordform': passwordform, 'profilepicform': profilepicform, 'generalForm': generalForm})



def loginPage(request):
    current_user = request.user
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                # Links change and this is hardcoded, how to replace this?
                return HttpResponseRedirect('/spicy_memes') #succes redirect to the startpage
    else:
        form = LogInForm()
    return render(request, 'login.html', {'LogInForm': form, 'user' : current_user})


@login_required
def logOut(request):
    logout(request)
    return HttpResponseRedirect('/spicy_memes/')


@login_required
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


@login_required
def uploadFile(request):
    if request.method == 'POST':
        form = UploadForm(user = request.user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/spicy_memes/')
        else:
            messages.success(request, 'Please choose an image file with a name under 40 characters long.')
            return render(request, 'uploadFile.html', {'form': form})
    else:
        form = UploadForm()
        return render(request, 'uploadFile.html', {'form': form})


@login_required
def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    #Initialize forms
    editform = EditForm(initial={'title': post.title,'description': post.description})
    commentform = CommentForm()
    commentform.user = request.user
    voteform = VoteCommentForm()

    #Get difference between time posted and now
    tdelta = datetime.datetime.now() - post.date.replace(tzinfo=None)
    time_posted = (tdelta.seconds/60) - 120
    if((datetime.datetime.today().strftime('%d-%m-%Y')) != (post.date.strftime('%d-%m-%Y'))):
        time_posted = 16

    time_diff = round(15 - time_posted)

    #Probably very complicated way of getting a list that sorts comments by
    #their user rating, but it's according to the model where there is no
    #reference to LikesPost from Comment. Improvements welcome
    postComments = Comment.objects.filter(post = post)
    tupleComments = list()
    sortedComments = list()
    for comment in postComments:
        ctuple = (comment, LikesComment.objects.filter(comment=comment).filter(likes=True).count() - LikesComment.objects.filter(comment=comment).filter(likes=False).count())
        tupleComments.append(ctuple)
    tupleComments = sorted(tupleComments, key=lambda x: x[1], reverse=True)
    for tup in tupleComments:
        sortedComments.append(tup[0])

    #Identify post owner for editing purposes.
    if (post.user == request.user):
        postOwner = True
    else:
        postOwner = False
    context = {'post': post, 'user': user, 'owner': postOwner, 'editform': editform,'commentform': commentform,
               'time_posted': time_posted, 'time_diff': time_diff, 'postComments': postComments,
               'voteform': voteform, 'sortedComments': sortedComments}
    return render(request, 'postDetail.html', context)


@login_required
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


def likePost(request, pk, likes):
        post = get_object_or_404(Post, pk=pk)
        likeform = LikeForm(request.POST or None)
        like = LikesPost()
        if request.method == "POST":
            # Find out if this user has already voted on the specific comment,
            # if yes, remove whatever his vote was.
            votes = LikesPost.objects.filter(post=post).filter(user=request.user)
            if votes:
                LikesPost.objects.filter(post=post).filter(user=request.user).delete()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if likeform.is_valid():
                like = likeform.save(commit=False)
                like.post = post
                like.user = request.user

                # Upvote: likes == "1"; Downvote: likes=="0" - I don't know how to
                # adjust the matching RegEx in urls.py to accept Booleans instead of
                # Integers
                if (likes == "0"):
                    like.likes = False
                else:
                    like.likes = True
                like.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            likeform = LikeForm()
        return render(request, 'postDetail.html', {'likeform': likeform, 'totalLikes': totalLikes, 'user': request.user})

@login_required
def deleteFile(request, pk):
    po = get_object_or_404(Post, pk=pk)
    po.delete()
    return HttpResponseRedirect('/spicy_memes/')


def startPage(request):
    print(request.user)
    if request.user.is_authenticated:
        return HttpResponseRedirect('/spicy_memes/hotPage')
    return render(request, 'startPage.html')

def edit_profile (request):
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST, instance=request.user)
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
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/spicy_memes/userprofile')
        else:
            print('not valid')
            return HttpResponseRedirect('/spicy_memes/userprofile')
    else:
        form=PasswordChangeForm(user=request.user)
        return render (request, '/spicy_memes/userprofile' , {'form':form})


def changeProfilePic(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeProfilePic(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/spicy_memes/userprofile')
        else:
            return HttpResponseRedirect('/spicy_memes/userprofile')
    else:
        form = ChangeProfilePic()
        return render(request, 'test.html', {'form': form})


def addComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    commentform = CommentForm(request.POST or None)
    if request.method == "POST":
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        commentform = CommentForm()
    return render(request, 'postDetail.html', {'commentform': commentform})

def voteComment(request, pk, likes):
    comment = get_object_or_404(Comment, pk=pk)
    voteform = VoteCommentForm(request.POST or None)
    vote = LikesComment()
    if request.method == "POST":

        #Find out if this user has already voted on the specific comment,
        #if yes, remove whatever his vote was.
        votes = LikesComment.objects.filter(comment = comment).filter(user = request.user).filter(comment = comment)
        if votes:
            LikesComment.objects.filter(comment = comment).filter(user = request.user).delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if voteform.is_valid():
            vote = voteform.save(commit=False)
            vote.user = request.user
            vote.comment = comment

            #Upvote: likes == "1"; Downvote: likes=="0" - I don't know how to
            #adjust the matching RegEx in urls.py to accept Booleans instead of
            #Integers
            if (likes == "0"):
                vote.likes = False
            else:
                vote.likes = True
            vote.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        voteform = VoteCommentForm()
    return render(request, 'postDetail.html', {'voteform': voteform, 'totalLikes': totalLikes, 'user': request.user})

def deleteComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
