import datetime
from haystack import indexes

from users.models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user_name = indexes.CharField(model_attr='user_name')
    user_account = indexes.NgramField(model_attr='user_account')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter()


