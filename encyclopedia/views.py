
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import util
from .util import get_entry, save_entry
import random
import markdown2


# index page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



# Render entry page
def entry_page(request, title):
    entry_content = markdown2.markdown(util.get_entry(title))

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry_content
    })



# Search page fuction
def search(request):
    query = request.GET.get('q', '').lower()
    entries = util.list_entries()

    # Filter entries that contain the search query
    search_results = [entry for entry in entries if query in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": search_results
    })







# Create new Entry page
def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # Check if an entry with this title already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/new.html", {
                "error_message": f"An encyclopedia entry with the title '{title}' already exists."
            })

        # Save the new entry
        util.save_entry(title, content)
        return redirect("entry_page", title=title)  # Redirect to the newly created entry page

    return render(request, "encyclopedia/new.html")




# Edit entry
def edit(request, title):
    if request.method == "POST":
        # If form was submitted, save the updated content
        new_content = request.POST['content']
        save_entry(title, new_content)
        # Redirect back to the updated entry page
        return redirect('entry', title=title)
    
    else:
        # Load the existing content to prepopulate the textarea
        content = get_entry(title)
        if content is None:
            return render(request, "encyclopedia/not_found.html", {"title": title})

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })



# Random page

def random_page(request):
    # Get a list of all entries
    entries = util.list_entries()
    # Choose a random entry from the list
    if entries:
        random_entry = random.choice(entries)
        # Redirect to the randomly selected entry page
        return redirect('entry', title=random_entry)
    else:
        return HttpResponse("No entries available.")