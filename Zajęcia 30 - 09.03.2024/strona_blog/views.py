from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, 'strona_blog/post/list.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'strona_blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

@require_POST
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} polecam Ci przeczytanie {post.title}'
            message = f'Przeczytaj {post.title} pod adresem {post_url} \n Mój komentarz do artykułu: {cd["comments"]}'
            send_mail(subject, message, 'kamil.nowak.testuj@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'strona_blog/post/share.html', {'post':post, 'form':form, 'sent':sent})
