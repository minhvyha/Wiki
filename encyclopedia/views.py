from re import L
from django.shortcuts import render
from django import forms
from . import util

class AddForm(forms.Form):
    markdown = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def add(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            ...
    return render(request, "encyclopedia/add.html", {
        "form" : AddForm()
    })
