from django.views.generic import CreateView, FormView,UpdateView
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from .models import User,Notification
from django.http import JsonResponse
from .forms import UserSignupForm, ClientSignupForm,\
    WriterSignupForm, UserUpdateProfileForm, UpdateTimezoneForm


# class UserRegistrationCreateView(FormView):
#     """
#     Create user api view
#     """
#     model = User
#     form_class = UserSignupForm
#     template_name = 'authenticate/register.html'

#     def post(self, request):
#         """
#         Overide the default post()
#         """
#         form = self.form_class(request.POST)
#         if not form.is_valid():
#             return render(request, self.template_name, {"form": form})
#         data = {
#             "first_name": form.cleaned_data['first_name'],
#             "last_name": form.cleaned_data['last_name'],
#             "username":form.cleaned_data['username'],
#             "password": form.cleaned_data['password'],
#             "email": form.cleaned_data['email'].lower(),
#         }
#         User.objects.create_user(**data)
#         signup_user=User.objects.get(email=data['email'])
#         # client_group=Group.objects.get(name='clients_group')
#         # client_group.user_set.add(signup_user)
#         return redirect(reverse('authentication:login'))

# class ClientRegistrationCreateView(FormView):
#     """
#     Create user api view
#     """
#     model = User
#     form_class =ClientSignupForm
#     template_name = 'authenticate/register.html'

#     def post(self, request):
#         """
#         Overide the default post()
#         """
#         form = self.form_class(request.POST)
#         if not form.is_valid():
#             return render(request, self.template_name, {"form": form})
#         data = {
#             "first_name": form.cleaned_data['first_name'],
#             "last_name": form.cleaned_data['last_name'],
#             "username":form.cleaned_data['username'],
#             "password": form.cleaned_data['password'],
#             "email": form.cleaned_data['email'].lower(),
#             "date_of_birth": form.cleaned_data['date_of_birth'],
#         }
#         User.objects.create_user(**data)
#         return redirect(reverse('authentication:login'))


# class UserLoginCreateView(FormView):
#     """
#     Create user api view
#     """
#     model = User
#     form_class = UserLoginForm
#     template_name = 'authenticate/login.html'
#     success_url = reverse_lazy("blog:home")

#     def post(self, request):
#         """
#         Overide the default post()
#         # """
#         form = self.form_class(request.POST)
#         email = request.POST['username'].lower()
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user and user.is_active:
#             login(request, user)
#             return super(UserLoginCreateView, self).form_valid(form)
#         messages.success(request, 'This email and password combination is invalid', extra_tags='red')
#         return render(request, self.template_name, {"form": form})


# def logout_view(request):
#     logout(request)
#     if request.user.is_superuser or request.user.is_staff:
#         redirect('/accounts/login')
#     else:
#         return redirect('/')


def show_notification(request,notification_id):
    n=Notification.objects.get(id=notification_id)
    return render(request,'notification.html',{'notification':n})


def delete_notification(request,notification_id):
    n=Notification.objects.get(id=notification_id)
    n.viewed=True
    n.save()
    return redirect('/')


def profile_view(request):
    context={}
    context['user']=User.objects.get(id=request.user.id)
    return render(request,'authenticate/profile.html',context)


class ProfileUpdateView(UpdateView):
    # specify the model you want to use
    model = User
    form_class = UserUpdateProfileForm
    template_name = 'authenticate/update_profile.html'
    success_url = "/authentication/profile/"

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['night_calls'] = self.object.night_calls
    #     print("aaaaaa:", initial['night_calls'])
    # #     initial['fielda2'] = self.object.fieldA.fieldA2
    #     return initial
    #
    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     form.instance.night_calls = form.cleaned_data['night_calls']
    #     form.instance.time_zone = form.cleaned_data['time_zone']
    #     form.instance.country = form.cleaned_data['country']
    #     form.save()
    #     # print("aaaaaa:", form.cleaned_data['country'],form.cleaned_data['time_zone'])
    #     return response
    # def get_initial(self):
    #     print("bbbb:", self.object.country)
    #     return {'template': 'authenticate/profile.html'}
    # def get_object(self):
    #     id_ =self.kwargs.get("id")
    #     return get_object_or_404(User, id=id_)
    #
    # def form_valid(self, form):
    #     print("aaaa::::",form.cleaned_data)
    #     return super().form_valid(form)


class TimezoneUpdateView(UpdateView):
    # specify the model you want to use
    model = User
    form_class = UpdateTimezoneForm
    template_name = 'authenticate/update_timezone_profile.html'
    success_url = "/authentication/profile/"