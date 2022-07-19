from re import L
from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
class AddForm(forms.Form):
    title = forms.CharField(label='Title')
    content = forms.CharField(widget=forms.Textarea, label="Content")


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
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "{% url 'add' %}")
    return render(request, "encyclopedia/add.html", {
        "form" : AddForm()
    })
