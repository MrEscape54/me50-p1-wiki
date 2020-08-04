import random
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
import markdown2
from . import util
from encyclopedia.forms import NewEntryForm

def index(request):
    query = request.GET.get('q')
    if query:
        if util.get_entry(query):
            return redirect('encyclopedia:entry', query)

        # Using lower to avoid case sensitive search    
        entries = [e for e in util.list_entries() if query.lower() in e.lower()] 
        return render(request, "encyclopedia/index.html", {"entries": entries, "query": query})

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    if util.get_entry(title) is None:
        raise Http404
    return render(request, 'encyclopedia/entry.html', {'entry': markdown2.markdown(util.get_entry(title)), 'title': title})


def new_entry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if util.get_entry(cd['title']):
                message = "Error: There already exists an Entry with this title"
                return render(request, 'encyclopedia/new_entry.html', {'message': message, 'form': form})
            util.save_entry(cd['title'], cd['content'])
            return redirect('encyclopedia:entry', cd['title'])
    else:
        form = NewEntryForm()
    return render(request, 'encyclopedia/new_entry.html', {"form": form})


def edit_entry(request, title):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            util.save_entry(cd['title'], cd['content'])
            return redirect('encyclopedia:entry', cd['title'])
    
    content = util.get_entry(title)
    # Just to display an error if typing a wrong URL 
    if content is None:
        message = 'Error: There is not entries with this title'
        return render(request, 'encyclopedia/edit_entry.html', {"message": message})
    data = {'title': title, 'content': content}
    form = NewEntryForm(initial=data)
    return render(request, 'encyclopedia/edit_entry.html', {"form": form, 'title': title})

def random_page(request):
    entries = util.list_entries()
    random_page = random.choice(entries)
    return redirect('encyclopedia:entry', random_page)
