from django.shortcuts import render
from django.http import Http404
from df_goods.models import GoodsSKU
from django.http import JsonResponse
from django_redis import get_redis_connection
import json


def add(request):
    # 当前对购物数据进行添加，只支持post请求方式。
    if request.method != 'POST':
        return Http404
    dict = request.POST
    # 接收请求的商品编号和数量
    sku_id = dict.get('sku_id', '0')
    count = int(dict.get('count', 0))
    # 不要完整相信js的验证，因为非法的请求者会直接请求地址，不会通过界面操作。
    # 判断sku_id对应的商品是否存在
    if GoodsSKU.objects.filter(id=sku_id).count() <= 0:
        print(sku_id)
        return JsonResponse({'status': 2})

    # 判断数量是否合法
    if count <= 0:
        return JsonResponse({'status': 3})

    # 判断用户是否登陆
    if request.user.is_authenticated():
        # 如果已经登陆，则购物车数据存放在redis当中。
        redis_client = get_redis_connection()
        # 创建键
        key = 'cart%d' % request.user.id
        # 判断redis的hash数据中某个属性是否存在，命令为——hexists（键，属性）
        if redis_client.hexists(key, sku_id):
            # 如果此商品已存在，则购买数量相加再赋值
            # 此处要特别注意，要把从hash数据中取出的值进行转换。
            # hash的值为string类型。
            count1 = int(redis_client.hget(key, sku_id))
            count0 = count1 + count
            if count0 > 5:
                count0 = 5
            redis_client.hset(key, sku_id, count0)
        else:
            # 如果此商品不存在
            # redis中hash格式数据的操作命令
            # 写入：hset（键，属性，值）
            # 读取：hget（键，属性，值）
            redis_client.hset(key, sku_id, count)
        # 计算总数量
        total_count = 0
        # 获取hash中所有属性的值，用hvals（键）命令，返回一个列表。
        for c in redis_client.hvals(key):
            # 此处要特别注意，要将c的值的类型进行转换。
            total_count += int(c)
        return JsonResponse({'status': 1, 'total_count': total_count})
    else:
        # 如果未登陆，则数据存储在cookies中。
        # 先读取原来的购物车数据
        cart_str = request.COOKIES.get('cart')
        if cart_str:
            # 将字符串转换成字典格式
            cart_dict = json.loads(cart_str)
        else:
            cart_dict = {}

            # 接下来将购物车的数据进行更新
        # 如果购物车中此商品已存在，则更新数量
        if sku_id in cart_dict:
            count = cart_dict[sku_id] + count
            if count > 5:
                count = 5
            cart_dict[sku_id] = count
        else:
            cart_dict[sku_id] = count
        # 计算商品数量并返回
        total_count = 0
        for k, v in cart_dict.items():
            total_count += v
        # 将字典转换成字符串格式，因为COOKIES中存储的是字符串类型
        cart_str = json.dumps(cart_dict)
        # 创建响应对象，写入cookies。
        response = JsonResponse({'status': 1, 'total_count': total_count})
        response.set_cookie('cart', cart_str, 60 * 60 * 24 * 7)
        return response


def index(request):
    # 构建一个空列表
    sku_list = []
    # 判断用户是否登陆
    if request.user.is_authenticated():
    #     如果登陆，从redis中读取数据
        redis_client = get_redis_connection()
        # hash数据中取某个对象(唯一的)的所有属性的命令————
        id_list = redis_client.hkeys('cart%d' % request.user.id)
        for id1 in id_list:
            sku = GoodsSKU.objects.get(pk=id1)
            sku.cart_count = redis_client.hget('cart%d' % request.user.id, id1)
            sku_list.append(sku)
    # 如果未登陆,则从cookies中读取数据
    else:
        cart_str = request.COOKIES.get('cart')
        if cart_str:
            cart_dict = json.loads(cart_str)
            for k, v in cart_dict.items():
                sku = GoodsSKU.objects.get(pk = k)
                sku.cart_count = v
                sku_list.append(sku)
    context = {
        'title': '购物小车车',
        'sku_list':sku_list
    }
    return render(request, 'cart.html', context)
