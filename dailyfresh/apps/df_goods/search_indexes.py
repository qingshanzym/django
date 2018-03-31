from .models import GoodsSKU
from haystack import indexes

class GoodsSkUIndex(indexes.SearchIndex, indexes.Indexable):
    # 上面意思——建立索引时被使用的类
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsSKU

    def index_queryset(self, using=None):
        # 返回要建立索引的数据集
        return self.get_model().objects.all()
