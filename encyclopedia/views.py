from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def entry_page(request, title):
    entry_content = util.get_entry(title)
     
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry_content
    })



def search(request):
    query = request.GET.get('q', '').lower()
    entries = util.list_entries()

    # Filter entries that contain the search query
    search_results = [entry for entry in entries if query in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": search_results
    })




# Creating html form using django
class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title")
    body = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'rows':3, 'cols':5}), label="Enter page content")


def newpage(request):
    form = NewPageForm(request.POST)
    return render(request, "encyclopedia/new.html",{
        "form": form
    })



