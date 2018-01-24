from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from . import models
from django.urls import reverse_lazy


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'


class SchoolListView(ListView):
    #define my own object name of class SchoolListView
    context_object_name = 'schools'
    model = models.School
    

class SchoolDetailView(DetailView):
    context_object_name = 'school_detail'
    model = models.School
    template_name = 'basicApp/school_detail.html'

class SchoolCreateView(CreateView):
    fields = ('name', 'principal', 'location')
    model = models.School

class SchoolUpdateView(UpdateView):
    fields = ('name', 'principal')  #select which fields you'd like to update
    model = models.School

class SchoolDeleteView(DeleteView):
    model = models.School
    success_url = reverse_lazy('basicApp:list')
