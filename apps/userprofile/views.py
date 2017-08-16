import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from apps.userprofile.models import User


class SendAndroidView(View):
    def get(self, request, email):
        print(email)
        return redirect(request.META['HTTP_REFERER'])


class SendIOSView(View):
    def get(self, request, email):
        print(email)
        return redirect(request.META['HTTP_REFERER'])


class BlockUserView(View):
    def get(self, request, email):
        user = User.objects.get(email=email)

        if not user.is_admin:
            if user.is_blocked:
                user.is_blocked = False
            else:
                user.is_blocked = True
            user.save()

        return redirect(request.META['HTTP_REFERER'])
