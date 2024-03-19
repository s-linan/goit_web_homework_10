from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Quote, Author
# Create your views here.
from .utils import get_mongodb


def main(request, page=1):
    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required
def quote(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/quote.html', {"tags": tags, 'form': form})

    return render(request, 'quotes/quote.html', {"tags": tags, 'form': QuoteForm()})


@login_required
def author(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                new_author.tags.add(tag)

            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/author.html', {"tags": tags, 'form': form})

    return render(request, 'quotes/author.html', {"tags": tags, 'form': AuthorForm()})


@login_required
def quote_detail(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id, user=request.user)
    return render(request, 'quotes/quote_detail.html', {"quote": quote})


@login_required
def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id, user=request.user)
    return render(request, 'quotes/author_detail.html', {"author": author})


@login_required
def set_done_quote(request, note_id):
    Quote.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to='quotes:root')


@login_required
def delete_quote(request, note_id):
    Quote.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to='quotes:root')


@login_required
def set_done_author(request, note_id):
    Author.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to='quotes:root')


@login_required
def delete_author(request, note_id):
    Author.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to='quotes:root')
