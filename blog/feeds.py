import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, obj):
        return obj.title
    
    def item_description(self, obj):
        return truncatewords_html(markdown.markdown(obj.body), 30)

    def item_published(self, obj):
        return obj.publish