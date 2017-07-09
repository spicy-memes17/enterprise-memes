from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
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
from .forms import InviteForm
from .forms import EditProfileForm
from .forms import ChangeProfilePic, GroupForm
from .models import MyUser
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import datetime
from django.utils.timesince import timesince
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Post, MyUser, Comment, LikesComment, LikesPost, Tag, MemeGroup, GroupInvite
from .forms import UploadFileForm, UploadForm, EditForm, SignUpForm, LogInForm, CommentForm, VoteCommentForm, LikeForm, SearchForm, TagSearchForm

@login_required
def content(request, content=None, group_name='all'):
    if(group_name == 'all'):
        groupview = False
        if(content == None):
            content = "on_fire"

        postList = Post.objects.filter(group__name='all')
        memeTupleList = list()
        sortedMemeList = list()

        for post in postList:
            mtuple = (post,
                      (post.get_likes())*2
                      + Comment.objects.filter(post=post).count()*5)
            memeTupleList.append(mtuple)

        memeTupleList = sorted(memeTupleList, key=lambda x: x[1], reverse=True)

        if(content == "fresh"):
            content = "Fresh"
            sortedMemeList = postList.order_by('-date')[:20]
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

        context = {'memeList': sortedMemeList, 'content': content, 'groupview': groupview}
        return render(request, 'content.html', context)
    else:
        postList = Post.objects.filter(group__name=group_name).order_by('-date')
        content = group_name
        groupview = True
        group = MemeGroup.objects.get(name=group_name)
        membersList = MemeGroup.objects.get(name=group_name).users.all()
        context = {'memeList': postList, 'content': content, 'groupview': groupview, 'memberList': membersList}
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
    return userprofile(request, request.user)

@login_required
def userprofile(request, user_name):
    current_user = request.user
    user2 = get_object_or_404(MyUser, username=user_name)
    if user2 == current_user:
        generalForm = EditProfileForm(instance=current_user)
        authform = LogInForm()
        profilepicform = ChangeProfilePic()
        passwordform = PasswordChangeForm(data=request.POST, user=current_user)
        #Get list of user's posts
        user_meme_list = Post.objects.filter(user=current_user).order_by('-date')

        user_group_list = MemeGroup.objects.filter(users__username=current_user.username)
        group_invites = GroupInvite.objects.filter(user__username=current_user.username)
        groupform = GroupForm()

        # user bleibt eingeloggter User, neue var user2 ist anderer User (public profile)
        return render(request, 'userProfile.html', {'AuthForm': authform, 'user2': current_user, 'user': current_user, 'passwordform': passwordform,
                                                    'profilepicform': profilepicform, 'generalForm': generalForm,
                                                    'user_meme_list': user_meme_list, 'user_group_list': user_group_list, 'group_invites': group_invites, 'groupform': groupform})
    else:
        public_user_meme_list = Post.objects.filter(user=user2).order_by('-date')
        invite_form = InviteForm(inviter= current_user, invitee=user2)
        user_meme_list = filter(lambda x: (current_user in x.group.users.all()) or (x.group.name == 'all'), public_user_meme_list)
        return render(request, 'userProfilePublic.html', { 'user2': user2, 'user': current_user, 'user_meme_list': user_meme_list, 'invite_form': invite_form})



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
            messages.success(request, 'Profile deleted.', extra_tags='alert-success')
            return HttpResponseRedirect('/spicy_memes/signUp')
        else:
            messages.error(request, 'Wrong combination for username and password. Please try again.', extra_tags='alert-danger')
            return HttpResponseRedirect('/spicy_memes/userprofile/' + current_user) #redirect if password is wrong
    else:
        return HttpResponseRedirect('/spicy_memes/userprofile/' + current_user) #redirect if accessed with http-get


@login_required
def uploadFile(request):
    video_hosts = ["youtube", "vimeo", "myvideo", "youku", "twitch", "facebook"]

    if request.method == 'POST':
        postform = UploadForm(user = request.user, files=request.FILES, data=request.POST)
        if postform.is_valid():
            if ((postform.cleaned_data.get('video_url') == '') or
                    ((postform.cleaned_data.get('video_url') != '') and
                         (any
                              (substring in postform.cleaned_data.get('video_url') for
                               substring in video_hosts)))):
                new_post = postform.save()
                return HttpResponseRedirect('/spicy_memes/post/' + str(new_post.id) + '/detail')
            else:
                messages.success(request, 'Please enter a URL that is suitable for embedding.')
                return render(request, 'uploadFile.html', {'postform': postform})  # add error message at some point
        else:
            messages.success(request, 'Please choose an image file with a name under 40 characters long.')
            return render(request, 'uploadFile.html', {'postform': postform}) #add error message at some point
    else:
        postform = UploadForm(user=request.user)
        return render(request, 'uploadFile.html', {'postform': postform})



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

    #Getting a list that sorts comments by their user rating
    postComments = Comment.objects.filter(post = post)
    tupleComments = list()
    sortedComments = list()
    for comment in postComments:
        ctuple = (comment, comment.get_likes())
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
               'time_posted': time_posted, 'time_diff': time_diff,
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

def like_post(request):
    post_id = int(request.GET['post_id'])
    post = get_object_or_404(Post, pk=post_id)
    post_likes = True
    if(int(request.GET['likes']) == 0):
        post_likes = False

    if request.method == 'GET':
        try:
            like = LikesPost.objects.get(user = request.user, post = post)
            if(like.likes == post_likes):
                LikesPost.objects.filter(user=request.user, post=post).delete()
            else:
                like.likes = post_likes
                like.save()
        except LikesPost.DoesNotExist:
            obj = LikesPost(user = request.user, post = post, likes = post_likes)
            obj.save()
        newlikes = post.get_likes()
    return HttpResponse(newlikes)

@login_required
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
                term = term.strip()
                if both_false:
                    filtered_posts = Post.objects.filter(tags__name=term) | Post.objects.filter(title__contains=term)
                    dublonen = list(set(filtered_posts))
                    posts.extend(dublonen)
                if by_tags:
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

        context = {'memeList': posts, 'content': "Search"}  # only temporary

    return render(request, 'content.html', context)# only temporary


def startPage(request):
    if request.user.is_authenticated:
        return content(request, None)
    return render(request, 'startPage.html')

def edit_profile (request, user_name):
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            new_name = form.cleaned_data['username'];
            messages.success(request, 'Your profile was updated successfully!', extra_tags='alert-success')
            return HttpResponseRedirect('/spicy_memes/userprofile/' + new_name +'/')
            #return redirect ('/spicy_memes/userprofile')
        else:
            messages.error(request, 'Could not change name / email. Please try again.', extra_tags='alert-danger')
            return HttpResponseRedirect('/spicy_memes/userprofile/' + user_name)
    else:
        form=EditProfileForm(instance=request.user)
        args = {'form': form}
        return HttpResponseRedirect('/spicy_memes/userprofile/' + user_name, args)

@login_required
def change_password (request, user_name):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was updated successfully!', extra_tags='alert-success')
            return HttpResponseRedirect('/spicy_memes/userprofile/' + user_name +'/')
        else:
        # hier werden die unterschiedlichen Fehlermeldungen generiert. Es ist nicht elegant, aber da die PasswordChangeForm
		# eine von Django vorgegebene Form ist, lässt sich nicht auf die einzelnen Elemente zugreifen, um eine entsprechende Fehlermeldung auszulesen
            #values = request.POST.items()
            old_pw = request.POST.get('old_password')
            new_pw = request.POST.get('new_password1')
            new_pw2 = request.POST.get('new_password2')
            # check if the old pw is equal to the new pw
            if new_pw == old_pw:
                messages.warning(request, 'You cannot use the same password again. Please try again.', extra_tags='alert-danger')
                return redirect('/spicy_memes/userprofile/' + user_name +'/')
            # check if the new password is not entirely numeric
            elif new_pw.isdigit():
                messages.warning(request, 'Your new password cannot be entirely numeric. Please try again.', extra_tags='alert-danger')
                return redirect('/spicy_memes/userprofile/' + user_name +'/')
			# check if the new password has at least 8 characters
            elif len(new_pw) < 8:
                messages.warning(request, 'Your new password has to contain at least 8 characters. Please try again.', extra_tags='alert-danger')
                return redirect('/spicy_memes/userprofile/' + user_name +'/')
			# check if the new pws match
            elif new_pw != new_pw2:
                messages.warning(request, 'The new passwords do not match. Please try again.', extra_tags='alert-danger')
                return redirect('/spicy_memes/userprofile/' + user_name +'/')
			# in this case:
            else:
                messages.error(request, 'No common used passwords or personal information. Please try again.', extra_tags='alert-danger')
                return HttpResponseRedirect('/spicy_memes/userprofile/' + user_name +'/')
                return redirect('/spicy_memes/userprofile/' + user_name +'/')
    else:
        form=PasswordChangeForm(user=request.user)
        return render (request, '/spicy_memes/userprofile/' + user_name , {'form':form})


def changeProfilePic(request, user_name):
    user = request.user
    if request.method == 'POST':
        form = ChangeProfilePic(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile picture was updated successfully!', extra_tags='alert-success')
            return HttpResponseRedirect('/spicy_memes/userprofile/' + user_name +'/')
        else:
            messages.error(request, 'Could not change profile picture. Please try again.', extra_tags='alert-danger')
            return HttpResponseRedirect('/spicy_memes/userprofile/' + user_name +'/')
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

def like_comment(request):
    comment_id = int(request.GET['comment_id'])
    comment = get_object_or_404(Comment, pk=comment_id)
    comment_likes = True
    if(int(request.GET['likes']) == 0):
        comment_likes = False

    if request.method == 'GET':
        try:
            like = LikesComment.objects.get(user = request.user, comment = comment)
            if(like.likes == comment_likes):
                LikesComment.objects.filter(user=request.user, comment = comment).delete()
            else:
                like.likes = comment_likes
                like.save()
        except LikesComment.DoesNotExist:
            obj = LikesComment(user = request.user, comment = comment, likes = comment_likes)
            obj.save()
        newlikes = comment.get_likes()
    return HttpResponse(newlikes)

def deleteComment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def createGroup(request):
    user = request.user
    form = GroupForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            groupname= form.cleaned_data.get('name')
            all_groups_with_name = MemeGroup.objects.filter(name=groupname)
            if len(all_groups_with_name) == 0:
                group= MemeGroup(name=groupname)
                group.save()
                group.users.add(user)

    return HttpResponseRedirect('/spicy_memes/userprofile/' + user.username)


def leaveGroup(request, name_group, name_user):
    group = MemeGroup.objects.get(name=name_group)
    user = MyUser.objects.get(username=name_user)

    group.users.remove(user)
    if len(group.users.all())==0:
        group.delete()

    return HttpResponseRedirect('/spicy_memes/userprofile/' + user.username)


def acceptInvite(request, name_group, name_user):
    accepted_group = MemeGroup.objects.get(name= name_group)
    accepted_user = MyUser.objects.get(username= name_user)
    invite = GroupInvite.objects.get(user= accepted_user, group= accepted_group)

    accepted_group.users.add(accepted_user)
    invite.delete()

    return HttpResponseRedirect('/spicy_memes/userprofile/' + name_user)


def declineInvite(request, name_group, name_user):
    declined_group = MemeGroup.objects.get(name= name_group)
    declined_user = MyUser.objects.get(username= name_user)
    invite = GroupInvite.objects.get(user= declined_user, group= declined_group)
    invite.delete()

    return HttpResponseRedirect('/spicy_memes/userprofile/' + name_user)


def groupDetail(request, group_name):
    name = group_name
    members = MemeGroup.objects.get(name= group_name).users.all()
    return render(request, 'groupDetail.html', {'name': name, 'members': members})


def inviteToGroup(request, user_name):
    user = MyUser.objects.get(username=user_name)
    inviter = MyUser.objects.get(username= request.user)
    invite_form = InviteForm(request.POST, invitee=user, inviter= request.user)
    if request.method == "POST":
        group_id= invite_form.data['group']     #no check if valid. blame matias if any errors occur
        group= MemeGroup.objects.get(id=group_id)

        #check if invite to this group for user already exists. if not, proceed
        try:
            invite = GroupInvite.objects.get(user=user, group=group)
        except:
            invite = None

        if invite is None:
            invite= GroupInvite(user=user, group=group)
            invite.save()


    return HttpResponseRedirect('/spicy_memes/userprofile/' + user.username)








