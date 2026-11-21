"""线上初始化数据脚本：python seed.py"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.merchants.models import Merchant
from apps.shops.models import Shop
from apps.products.models import Product

PWD = 'hyc12345'

merchants = [
    {'name': '山野茶事', 'phone': '13900000002', 'shop': '山野茶事旗舰店', 'addr': '杭州市西湖区龙井路88号', 'desc': '精选各地好茶，传递东方茶文化',
     'products': [
        ('明前龙井 2026新茶', '雨前采摘，豆香浓郁，鲜爽回甘', 298, '食品'),
        ('武夷岩茶 大红袍', '岩骨花香，汤色橙黄明亮，回甘持久', 398, '食品'),
        ('茉莉花茶 飘雪', '茉莉窨制，花香茶香交融，清雅怡人', 128, '食品'),
     ]},
    {'name': '素心手作', 'phone': '13900000003', 'shop': '素心手作工坊', 'addr': '景德镇市珠山区陶艺街12号', 'desc': '手工匠心，每一件都独一无二',
     'products': [
        ('手工陶瓷马克杯', '手拉坯成型，釉色温润，握感舒适', 88, '家居用品'),
        ('竹编收纳篮', '天然竹材，手工编织，环保耐用', 68, '家居用品'),
        ('手工香薰蜡烛', '大豆蜡配天然精油，香气舒缓', 58, '家居用品'),
     ]},
    {'name': '暖居生活馆', 'phone': '13900000004', 'shop': '暖居生活馆', 'addr': '上海市徐汇区衡山路66号', 'desc': '让家更有温度的生活好物',
     'products': [
        ('原木实木茶几', '北美黑胡桃木，简约设计，稳固耐用', 1299, '家居用品'),
        ('棉麻抱枕套', '天然棉麻，亲肤透气，四季皆宜', 49, '家居用品'),
        ('暖光香薰台灯', '暖光氛围，助眠好物，三档调光', 199, '家居用品'),
        ('亚麻桌布', '垂感自然，易清洗，提升餐桌格调', 79, '家居用品'),
     ]},
]

seq = 0
for m in merchants:
    merchant, _ = Merchant.objects.get_or_create(phone_number=m['phone'], defaults={'name': m['name']})
    merchant.name = m['name']
    merchant.set_password(PWD)
    merchant.save()

    shop, _ = Shop.objects.get_or_create(name=m['shop'], defaults={'merchant': merchant})
    shop.merchant = merchant
    shop.merchant_name = merchant.name
    shop.merchant_phone = merchant.phone_number
    shop.address = m['addr']
    shop.phone_number = m['phone']
    shop.description = m['desc']
    shop.status = 'approved'
    shop.save()

    for name, desc, price, cat in m['products']:
        seq += 1
        Product.objects.get_or_create(
            shop=shop, name=name,
            defaults={
                'description': desc,
                'price': price,
                'category': cat,
                'is_active': True,
                'image': ['https://picsum.photos/seed/hyc%d/400/300' % seq],
                'shop_name': shop.name,
                'merchant_name': merchant.name,
            },
        )

print('数据初始化完成：商家 %d 个，商品 %d 个' % (Merchant.objects.count(), Product.objects.count()))
