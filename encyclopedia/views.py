from re import L
from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from random import choice

class AddForm(forms.Form):
    title = forms.CharField(label='Title', required=False)
    content = forms.CharField(widget=forms.Textarea, required=False, label="Content")

class EditForm(forms.Form):
    title = forms.CharField(label="Title",disabled = False,required = False, widget= forms.HiddenInput(attrs={'class':'col-sm-12','style':'bottom:1rem'}))
   
    content = forms.CharField(label="Content", widget= forms.Textarea(attrs={"rows":20, "cols":80,'class':'col-sm-11','style':'top:2rem'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            
            if not title:
                return render(request, "{% url 'add' %}",{
                    'form' : AddForm(),
                    'errors': 'Title is required'
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "{% url 'add' %}", {
                "form" : AddForm(),
                'errors': None
            })

    return render(request, "encyclopedia/add.html", {
        "form" : AddForm(),
        'errors': None
    })


def wiki(request, title):

    html =  markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/view.html", {
        'title':title,
        'html':html
    })

def random(request):
    return wiki(request, choice(util.list_entries()))

def edit(request, title):
    content = util.get_entry(title)
    form = EditForm(initial={'content':content, 'title':title})
    return render(request, "encyclopedia/edit.html", {
        "form" : form,
        'title': title,
    })

def save(request):
    form = EditForm(request.POST)
    
    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        util.save_entry(title, content)
        html =  markdown2.markdown(util.get_entry('CSS'))
        return render(request, "encyclopedia/view.html", {
            'title':'CSS',
            'html':html
        })

def search(request, search):
    l = util.list_entries()
    new_list = []
    for i in l:
        if search.lower() == i.lower():
            return wiki(request, i)
        new_list += [i]
    return render(request, "encyclopedia/index.html", {
        "entries": new_list
    })
