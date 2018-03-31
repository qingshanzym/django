from django.shortcuts import render
from .models import GoodsCategory, IndexGoodsBanner, IndexPromotionBanner, IndexCategoryGoodsBanner,GoodsSKU,Goods
from django.http import Http404,HttpResponse
from django_redis import get_redis_connection
from haystack.generic_views import SearchView


# Create your views here.
def test(request):
    category = GoodsCategory.objects.get(pk=1)
    context = {'category': category}
    return render(request, 'fdfs_test.html', context)


def index_test(request):
    # 查询分类信息
    category_list = GoodsCategory.objects.all()

    # 查询首页轮播图片数据
    banner_list = IndexGoodsBanner.objects.all().order_by('index')

    # 查询首页广告位数据
    adv_list = IndexPromotionBanner.objects.all().order_by('index')

    # 查询分类的推荐商品信息
    for category in category_list:
        # 查询当前分类的推荐文本商品
        category.title_list = IndexCategoryGoodsBanner.objects.filter(category=category, display_type=0).order_by(
            'index')[0:3]

        # 查询当前分类的推荐图片商品
        category.img_list = IndexCategoryGoodsBanner.objects.filter(category=category, display_type=1).order_by(
            'index')[0:4]

    context = {
        'title': '首页',
        'category_list': category_list,
        'banner_list': banner_list,
        'adv_list': adv_list,
    }
    return render(request, 'index_test.html', context)

def index(request):
    # return HttpResponse('主页')
    category_list = GoodsCategory.objects.all()

    # 查询首页轮播图片数据
    banner_list = IndexGoodsBanner.objects.all().order_by('index')

    # 查询首页广告位数据
    adv_list = IndexPromotionBanner.objects.all().order_by('index')

    # 查询分类的推荐商品信息
    for category in category_list:
        # 查询当前分类的推荐文本商品
        category.title_list = IndexCategoryGoodsBanner.objects.filter(category=category, display_type=0).order_by(
            'index')[0:3]

        # 查询当前分类的推荐图片商品
        category.img_list = IndexCategoryGoodsBanner.objects.filter(category=category, display_type=1).order_by(
            'index')[0:4]

    context = {
        'title': '首页',
        'category_list': category_list,
        'banner_list': banner_list,
        'adv_list': adv_list,
    }
    return render(request, 'index.html', context)
def detail(request, sku_id):
#     根据编号查询商品
    try:
        sku =GoodsSKU.objects.get(pk = sku_id)
    except:
        raise Http404

#     查询所有分类
    category_list = GoodsCategory.objects.all()
#     根据商品找分类，属于多找一。用外键属性。
#     根据分类找商品，属于一找多。用隐含属性。
    new_list = sku.category.goodssku_set.all().order_by('-id')[0:2]
    # 查询其他商品的陈列（SKU）
    other_list = sku.goods.goodssku_set.all()

    context = {
        'title':'商品详情',
        'sku':sku,
        'category_list':category_list,
        'new_list':new_list,
        'other_list':other_list,
    }
#   保存用户最近浏览的商品信息
    if request.user.is_authenticated():
        key = 'history%d' % request.user.id
        redis_client = get_redis_connection()
        # 如果这个商品已经存在，如何处理？
        redis_client.lrem(key, 0, sku_id)
        redis_client.lpush(key, sku_id)
        # 如果列表元素个数超过5个，怎么处理？
        if redis_client.llen(key) > 5:
            redis_client.rpop(key)

    return render(request, 'detail.html', context)

class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = '全文搜索如下'
        return context