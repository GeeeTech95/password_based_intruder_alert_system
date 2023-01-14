from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .forms import LoginForm
from .models import AccessControl
# Create your views here.


class Index(TemplateView):
    template_name = "index.html"


class Resource(LoginRequiredMixin, TemplateView):
    template_name = "resource.html"


class Login(View):
    template = 'login.html'
    model = get_user_model()
    form_class = LoginForm
    error = None
    max_trials = 3
    access_model = AccessControl

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template, locals())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # clear access trial record if any
                access_record = self.access_model.objects.filter(
                    username=username)
                if access_record.exists():
                    access_record.delete()

                # redirect to resource
                return HttpResponseRedirect(reverse("resource"))
            else:
                self.error = "authentication failed, please enter a correct username and password."
                # create access trial record
                access_record, created = self.access_model.objects.get_or_create(
                    username=username)
                if not created:
                    # increament
                    access_record.trials = access_record.trials + 1
                    access_record.save()

                if access_record.trials >= self.max_trials:
                    self.error = "You have exhausted Your maximum password trials, if you have forgotten your access credentials, please contact admin. An intruder alert notification has been sent !!."
                    #send mail

                else:
                    self.error += "You have only {} remaining attempts ".format(
                        self.max_trials - access_record.trials)
        return render(request, self.template, {"form": form, "error": self.error})


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))
