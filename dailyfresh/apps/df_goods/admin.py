from django.contrib import admin
from .models import GoodsCategory, Goods, GoodsSKU, GoodsImage, IndexCategoryGoodsBanner, IndexGoodsBanner, \
    IndexPromotionBanner
from django.conf import settings



# Register your models here.
class BaseAdmin(admin.ModelAdmin):
#     当对象被添加、修改时，会调用保存的方法
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
#         在这里生成静态首页————这里首页内容发生了改变，是最合适的点。
        from celery_tasks.tasks import generate_index
        generate_index.delay()
#         这个时候应该让缓存立即失效，因为页面发生了改变

#     当对象被删除时，会调用删除的方法
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        from celery_tasks.tasks import generate_index
        generate_index.delay()

class IndexGoodsBannerAdmin(BaseAdmin):
    pass

class IndexCategoryGoodsBannerAdmin(BaseAdmin):
    pass

class IndexPromotionBannerAdmin(BaseAdmin):
    pass

class GoodsCategoryAdmin(BaseAdmin):
    pass
admin.site.register(GoodsCategory,GoodsCategoryAdmin)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexCategoryGoodsBanner,IndexCategoryGoodsBannerAdmin)
admin.site.register(IndexGoodsBanner,IndexGoodsBannerAdmin)
admin.site.register(IndexPromotionBanner,IndexPromotionBannerAdmin)

