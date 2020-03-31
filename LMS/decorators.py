from django.http import HttpResponse
from django.shortcuts import redirect

#Checks if current user is authenticated and if so,
# returns them to the home screen,
#else allows them to view the page
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args, **kwargs)

    return wrapper_func

#Checks if user is in one or more ofthe allowed
# groups for this view, if so allows them to view,
# else returns an error page
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group =  None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised to view this page.')
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator