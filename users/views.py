from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile, Skill, Message
from .utils import searchProfiles, paginateProfiles


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
        else:
            messages.error(request, "Password is incorrect")

    return render(request, 'users/login-register.html')


def logoutUser(request):
    logout(request)
    messages.error(request, "User are logged out successefully !")
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(
                request, 'User account has created successfully ! ')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(
                request, 'An error has occured in registration. Try again with correct information. ')

    context = {
        'page': page,
        'form': form
    }
    return render(request, 'users/login-register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)
    profiles, custom_range, paginator = paginateProfiles(request, profiles, 3)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator
    }
    return render(request, 'users/profiles.html', context)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")

    context = {
        'profile': profile,
        'topskills': topskills,
        'otherskills': otherskills
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()

    context = {
        'profile': profile,
        'skills': skills,
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid:
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'A new skill added successfully !')

            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid:
            form.save()
            messages.success(request, 'Your skill has updated successfully !')
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill has deleted successfully !')
        return redirect('account')

    context = {
        'object': skill
    }
    return render(request, 'delete-template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context = {
        'messageRequests': messageRequests,
        'unreadCount': unreadCount
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {
        'message': message
    }
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message has successfully sent !')
            return redirect('profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form
    }
    return render(request, 'users/message-form.html', context)
