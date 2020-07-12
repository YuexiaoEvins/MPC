from haystack import indexes

from article.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    title = indexes.CharField(model_attr='title')
    simple_content = indexes.CharField(model_attr='simple_content')
    content = indexes.CharField(model_attr='content')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        
        return self.get_model().objects.filter(flag=1)
