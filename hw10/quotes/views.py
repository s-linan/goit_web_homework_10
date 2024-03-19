from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .forms import TagForm, AuthorForm
from .models import Tag, Quote, Author


# Create your views here.


def main(request, page=1):
    quotes = Quote.objects.all().order_by('id')
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
            tag.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required
def quote(request):
    if request.method == 'POST':
        quote = request.POST.get('quote')
        author_id = request.POST.get('author')
        tag_ids = request.POST.getlist('tags')

        author = get_object_or_404(Author, id=author_id)

        quote = Quote.objects.create(
            quote=quote,
            author=author,
        )

        tags = Tag.objects.filter(id__in=tag_ids)
        quote.tags.set(tags)

        return redirect('quotes:root')

    authors = Author.objects.all()
    tags = Tag.objects.all()
    return render(request, 'quotes/quote.html', {'authors': authors, "tags": tags})


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.save()

            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/author.html', {'form': form})

    return render(request, 'quotes/author.html', {'form': AuthorForm()})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {"author": author})
