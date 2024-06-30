from django.contrib import admin
from .models import MusicsInfo, MusicsScore

# Register your models here.
class InfoManage(admin.ModelAdmin):  # 继承模型管理类
    search_fields = ['song']  # 按字段“song”搜索
    list_filter = ['pub_date']  # 按字段“pub_date”自动筛选合适范围
    list_display = ('id', 'song', 'singer', 'score', 'pub_date')  # 展示的字段
class ScoreManage(admin.ModelAdmin):
    search_fields = ['song']
    list_display = ('id', 'song', 'level', 'platform')
admin.site.register(MusicsInfo, InfoManage)   # 在admin中注册，将模型加入站点管理
admin.site.register(MusicsScore, ScoreManage)