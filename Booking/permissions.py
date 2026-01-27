from functools import wraps
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpRequest



def has_permission(action_name:str):
    def decorator(func):
        @wraps(func)
        def wrap_func(request:HttpRequest,args,**kwargs):
            if request.user.profile.positions.filter(action__name=action_name).exists():
                return func(request,*args,**kwargs,)
            else:
                messages.error(request,"У вас недостатньо прав")
                return redirect("index")
        return wrap_func
    return decorator    