from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView
from groups.models import Group, GroupMember
from django.shortcuts import get_object_or_404 
from django.db import IntegrityError
from django.contrib import messages #using to check user belong to a group before join group
from . import models
# Create your views here.
class CreateGroup(LoginRequiredMixin, CreateView):
    fields = ('name','description')
    model = Group
    template_name = 'groups/group_form.html'
      

class SingleGroup(DetailView):
    model = Group
    template_name = 'groups/group_detail.html'
    context_object_name = 'group'
class ListGroups(ListView):
    model = Group
    template_name = 'groups/group_list.html'
    context_object_name = 'group_list'

class JoinGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request,*args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request,('Warning already a member'))
            messageDict = {'warningMessage':'You are already a member of the group'}
        else:
            messages.success(self.request,'You are now a member')
            messageDict = {'warningMessage':'You are now a member of the group'}
        #myRender = render(request,'groups/group_detail.html',context=messageDict)
        #context = super().get(request,*args,**kwargs)
        #context['warningMessage'] = 'You are now a member of the group'
        return super().get(request,*args,**kwargs)

    
class LeaveGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')                
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you leave this group be cause you are not in the group')
        else:
            membership.delete()
            messages.success(self.request,'You have leaved this group successfully')

        return super().get(request,*args,**kwargs)