from django.shortcuts import render

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