from django.urls import path
from . import views

app_name = 'LoveMusics'  # 使用URLconf的命名空间，指定该应用的命名空间，使项目的一级url与该应用下的二级url和相关html正确对应
urlpatterns = [  # 二级路由以int类型匹配music_id并用<>将url捕获(不能有空格)，调用views里对应的函数
    path('', views.index, name = 'index'),  # 把一级路由匹配'.../LoveMusics/'后的剩下部分str用于二级路由匹配，
    path('<int:music_id>/', views.detail, name = 'detail'),  # 并将这条url传给views视图下的对应函数，
    path('<int:music_id>/result/', views.result, name = 'result'),  # 将对应的url取全局变量进行命名，
    path('<int:music_id>/score/', views.score, name = 'score'),  # 避免出现硬编码
    path('visual/', views.visual, name = 'visual'),
]  # <str:music_name>