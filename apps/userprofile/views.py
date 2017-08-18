import datetime
import os
import json

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_decode

from apps.userprofile.models import User
from apps.userprofile.forms import SendAppForm


class SedAppForm(FormView):
    email_template_name = 'userprofile/send_app_email.html'
    device = 'android'
    form_class = SendAppForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'userprofile/send_app_subject.txt'
    template_name = 'userprofile/send_app_form.html'
    title = 'Send android app'
    app_name = 'Sonat'
    token_generator = default_token_generator

    def get(self, request, email, device, *args, **kwargs):
        form = SendAppForm()
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'device': device,
            'email': email,
            'app_name': self.app_name,
        }
        form.save(**opts)
        return redirect(self.request.META['HTTP_REFERER'])


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


class DownloadAppView(View):
    token_generator = default_token_generator

    def get(self, request, uidb64, time, token, device):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        time_diff = None
        try:
            time = urlsafe_base64_decode(time).decode()
            time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')

            if time > datetime.datetime.now():
                time_diff = True

        except (TypeError, ValueError):
            time_diff = False
        
        if user is not None and self.token_generator.check_token(user, token) and request.user == user and time_diff:
            if device == 'android':
                file_name = 'maxime.ogg'
            else:
                file_name = 'leonid.mp3'

            file_path = os.path.join(settings.MEDIA_ROOT, 'apps', file_name)

            if not os.path.exists(file_path):
                raise Http404('There is no file on the server.')

            serverfile = open(file_path, 'rb') 
            response = HttpResponse(serverfile)
            response['X-Sendfile'] = file_path
            response['Content-Type'] = 'audio/mpeg3;audio/x-mpeg-3;video/mpeg;video/x-mpeg;text/xml'
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 
            return response
        else:
            raise Http404('Link was valid only for {} for 30 minutes.'.format(user))
