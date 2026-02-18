import locale
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.db.models import Q

from .models import Profile, Action, Position, Subject
from .forms import ActionForm, PositionForm, UserForm, UserFormEdit, SignInForm, SubjectForm, ProfileForm
from TaskManager.models import Schedule


locale.setlocale(locale.LC_TIME, 'ukrainian')



def get_or_create_profile(user):
    """Повертає профіль користувача, створюючи його, якщо не існує"""
    profile, created = Profile.objects.get_or_create(user=user)
    return profile



def sign_up(request: HttpRequest):
    if request.method == "POST":
        sign_up_form = UserForm(request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if sign_up_form.is_valid():
            user = sign_up_form.save()
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
            else:
                Profile.objects.create(user=user)

            messages.success(request, "Вітаємо з реєстрацією 🎉")
            return redirect("sign_in")
            
        messages.error(request, sign_up_form.errors)
        return redirect("sign_up")
    
    return render(request, "sign_up.html", dict(sign_up_form=UserForm(), profile_form=ProfileForm()))



def sign_in(request: HttpRequest):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                
                get_or_create_profile(user)
                messages.success(request, "Вітаємо в нашій системі 😎. Вхід успішний")
                return redirect("index")
            else:
                messages.error(request, "Користувача з такими параметрами не знайдено 😢")
                return redirect("sign_in")
        messages.error(request, form.errors)
        return redirect("sign_in")

    return render(request, "sign_in.html", dict(form=SignInForm()))



@login_required
def update_profile(request: HttpRequest):
    profile = get_or_create_profile(request.user)  

    if request.method == "POST":
        user_form = UserFormEdit(data=request.POST, instance=request.user)
        if user_form.changed_data:
            user_form.save()

        profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if profile_form.changed_data:
            profile_form.save()

        messages.success(request, "Дані успішно оновлено 👍")
        return redirect("profile")
    
    return render(
        request,
        "profile.html",
        dict(user_form=UserForm(instance=request.user), profile_form=ProfileForm(instance=profile))
    )



@login_required
def index(request: HttpRequest):
    profile = get_or_create_profile(request.user)  

    if (User
        .objects
        .prefetch_related("Profile")
        .select_related("Position")
        .filter(username=request.user.username, profile__positions__name__in=["Учень","Вчитель"])
        .exists()):
        class_number = int(profile.class_room.name.split("-")[0])
        day = datetime.now().strftime("%A").title()

        task = Schedule.objects.filter(day=day, study=class_number)
        return render(request, "index.html", dict(task=task))

    return render(request, "index.html")



@login_required
def logout_view(request: HttpRequest):
    logout(request)
    messages.success(request, "Ви успішно вийшли із системи. До зустрічі!")
    return redirect("sign_in")


def toggle_theme(request):
    current_theme = request.session.get("theme", "light")
    request.session["theme"] = "dark" if current_theme == "light" else "light"
    return redirect(request.META.get("HTTP_REFERER", "/"))