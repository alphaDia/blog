from django.template import Library
from django.utils.safestring import mark_safe
from django.db.models import Count
import markdown
from ..models import Post
from ..forms import SearchForm

register = Library()

@register.simple_tag
def total_post():
    return Post.published.count()

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).filter(total_comments__gte=1)\
    .order_by('-total_comments')[:count]

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.all()[:count]
    return {'latest_posts': latest_posts}

@register.inclusion_tag('blog/post/includes/search_form.html')
def post_search():
    form = SearchForm()
    return {'form': form}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))