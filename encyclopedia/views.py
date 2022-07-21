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


class IndexForm(forms.Form):
    search = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        'default': IndexForm(),
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
                    'default': IndexForm(),
                    'form' : AddForm(),
                    'errors': 'Title is required'
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "{% url 'add' %}", {
                'default': IndexForm(),
                "form" : AddForm(),
                'errors': None
            })

    return render(request, "encyclopedia/add.html", {
        'default': IndexForm(),
        "form" : AddForm(),
        'errors': None
    })


def wiki(request, title):
    entries = util.list_entries()
    for i in entries:
        if title.lower() == i.lower():
            html =  markdown2.markdown(util.get_entry(i))
            return render(request, "encyclopedia/view.html", {
                'default': IndexForm(),
                'title':title,
                'html':html
            })
    return render(request, "encyclopedia/error.html", {
        'default': IndexForm(),
        'top':'Sorry',
        'bottom':'Page Not Fount 404'
    })

def random(request):
    return wiki(request, choice(util.list_entries()))

def edit(request, title):
    content = util.get_entry(title)
    form = EditForm(initial={'content':content, 'title':title})
    return render(request, "encyclopedia/edit.html", {
        'default': IndexForm(),
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
            'default': IndexForm(),
            'title':'CSS',
            'html':html
        })

def search(request):
    form = IndexForm(request.POST)

    if form.is_valid():
        search = form.cleaned_data['search']
        entries = util.list_entries()
        if not search:
            return render(request, "encyclopedia/error.html", {
                'default': IndexForm(),
                'top':'Sorry',
                'bottom':'No Search'
            })
        new = []
        for name in entries:
            if name.lower() == search.lower():
                return wiki(request, new[0])
            if search.lower() in name.lower():
                new.append(name)
            
        return render(request, "encyclopedia/index.html", {
            'default': IndexForm(),
            "entries": new
        })