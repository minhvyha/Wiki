from re import L
from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2

class AddForm(forms.Form):
    title = forms.CharField(label='Title', required=False)
    content = forms.CharField(widget=forms.Textarea, required=False, label="Content")


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
    ...