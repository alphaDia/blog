from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, \
                                           SearchQuery, \
                                           SearchRank
from taggit.models import Tag
from django.core.paginator import Paginator, \
                                  EmptyPage, \
                                  PageNotAnInteger 
from .models import Post
from .forms import EmailFormPost,\
                   CommentForm,\
                   SearchForm


def post_list(request, tag_slug=None):
    """
        Return list of posts by tag
    """
    post_list = Post.published.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # paginnation with 3 post per page 
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request,
                'blog/post/list.html',
                {
                   'posts': posts,
                   'tag': tag 
                })

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        # Create a comment object without saving it to the database
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    
    
    return render(request, 
                    'blog/post/comment.html', 
                    {'comment': comment,
                     'form': form,
                     'post': post})                 
                                                                    
def post_share(request, post_id):
    post = get_object_or_404(Post, pk=post_id, status=Post.Status.PUBLISHED)
    sent = False


    if request.method == 'POST':
        form = EmailFormPost(request.POST)
        if form.is_valid():
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            cd = form.cleaned_data
            subject = f"{cd.get('name')} recommends you read" \
                     f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{cd.get('name')}\'s comments: {cd.get('comments')}"
            
            send_mail(subject, message, 
                      settings.EMAIL_HOST_USER, 
                      [f"{cd.get('to')}"])
            
            sent = True

    else:
        form = EmailFormPost()

    return render(request, 
                  'blog/post/share.html', 
                  {'post': post, 
                   'form': form,
                   'sent': sent})


    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, 
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             slug=slug,
                             status=Post.Status.PUBLISHED)
    
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # List of similar posts
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Get similar posts and exclude the current post 
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.pk)
    # Count the number of tags simillar post share with the current post
    similar_posts = similar_posts.annotate(same_tags=Count('*'))\
                                 .order_by('-same_tags', '-publish')[:4]

    return render(request,
                'blog/post/detail.html', 
                {'post': post,
                 'comments': comments,
                 'form': form,
                 'similar_posts': similar_posts,
                })

def post_search(request):
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    

    return render(request,
                  'blog/post/search.html',
                  {
                    'query': query,
                    'results': results,})