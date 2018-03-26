from django.shortcuts import render
from .models import GoodsCategory, IndexGoodsBanner, IndexPromotionBanner, IndexCategoryGoodsBanner


# Create your views here.
def test(request):
    category = GoodsCategory.objects.get(pk=1)
    context = {'category': category}
    return render(request, 'fdfs_test.html', context)


def index(request):
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
    return render(request, 'index.html', context)
