from django.shortcuts import redirect
from .models import Answer
from django.contrib import messages

def validate_answer_count(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        answer_count = Answer.objects.filter(patient=user).count()
        if answer_count >= 10:
            return view_func(request, *args, **kwargs)
        else:
            message = "You need to complete quiz."
            messages.error(request, message)
            return redirect("patient:go-to-test-page")
    return wrapper_func

def validate_user_test(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.took_test and Answer.objects.filter(patient=user).count() >=10:
            message = "Sorry, you already took a test."
            messages.error(request, message)
            return redirect("patient:dashboard")       
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func