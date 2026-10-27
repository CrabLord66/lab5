from django.shortcuts import render, redirect
from django.http import Http404
from .models import Article

def archive(request):

    posts = Article.objects.all()

    context = {
        'posts': posts
    }

    return render(
        request,
        'archive.html',
        context
    )

def get_article(request, article_id):

    try:
        post = Article.objects.get(id=article_id)

        context = {
            'post': post
        }

        return render(
            request,
            'article.html',
            context
        )

    except Article.DoesNotExist:
        raise Http404("Статья не найдена")

def create_post(request):

    if not request.user.is_authenticated:
        raise Http404("Для создания статьи требуется авторизация")

    form = {
        'title': '',
        'text': '',
        'errors': ''
    }

    if request.method == "POST":

        form['title'] = request.POST.get(
            'title', ''
        ).strip()

        form['text'] = request.POST.get(
            'text', ''
        ).strip()

        title = form['title']
        text = form['text']

        if not title or not text:
            form['errors'] = "Не все поля заполнены"

        elif len(title) > 200:
            form['errors'] = (
                "Название статьи не должно "
                "превышать 200 символов"
            )

        elif Article.objects.filter(
            title__iexact=title
        ).exists():
            form['errors'] = (
                "Статья с таким названием уже существует"
            )

        else:
            article = Article.objects.create(
                title=title,
                text=text,
                author=request.user
            )

            return redirect(
                'get_article',
                article_id=article.id
            )

    return render(
        request,
        'create_post.html',
        {'form': form}
    )
