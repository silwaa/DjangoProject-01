from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import MusicsInfo, MusicsScore
from django.template import loader
from django.urls import reverse
import datetime
import matplotlib.pyplot as plt
import numpy as np
from pyecharts.charts import Bar, Line, Page
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode  # 可视化的背景图片 ×
import re


class tempclass(object):  # 用于对模型里的数据进行处理(不修改原数据，除非涉及增删改查)，之后渲染到html上
    def __init__(self, scoreid=None, song=None, platform=None, level=None, infoid=None, singer=None, pubdate=None, score=None, lang=None, type=None, prize=None):
        self.scoreid = scoreid
        self.song = song
        self.platform = platform
        self.level = level
        self.infoid = infoid
        self.singer = singer
        self.pubdate = pubdate
        self.score = score
        self.lang = lang
        self.type = type
        self.prize = prize


# Create your views here.
def index(request):  # 展示一些最新添加的音乐(图片、歌名、歌手)
    #request.POST.get[]
    #request.
    newsongs_list = MusicsInfo.objects.order_by('-pub_date')[:5]
    nslist = [tempclass(scoreid=i.id, song=i.song, singer=i.singer, pubdate=i.pub_date, score=i.score, lang=i.lang, type=i.song_type, prize=i.prize) for i in newsongs_list]
    for t in nslist:
        t.pubdate = datetime.datetime.strftime(t.pubdate, '%Y.%m.%d')
    # newsongs = '\n'.join(str(q) for q in newsongs_list)
    #template = loader.get_template('LoveMusics/index.html')  # 加载模板，传递参数
    context = {
        'status': '游客',
        'new_songs': nslist,  # newsongs
    }
    return render(request, 'LoveMusics/index.html', context)  # 快捷方式，一步到位，
    #return HttpResponse(template.render(context, request))  # 返回经过数据字典渲染的模板封装而成的HttpResponse对象


# 以下是二级路由，需要传入获取二级路由用于匹配的参数music_id/music_name
def detail(request, music_id):  # 展示一首音乐的具体信息(MusicsInfo里的内容)
    #d = get_object_or_404(MusicsInfo, pk=music_id)  # 等同以下异常
    try:  # 增加模型和视图的耦合性
        d1 = MusicsInfo.objects.get(pk=music_id)  # 条件也可以是其他字段值来判断
        d2_qs = MusicsScore.objects.filter(song=d1.song)
    except MusicsInfo.DoesNotExist:
        raise Http404('抱歉，音乐《%s》不存在。'%str(music_id))
    #response = '您正在浏览音乐《%s》的详情页面。'
    #return HttpResponse(response % music_id)
    return render(request, 'LoveMusics/detail.html', {
        'info': d1, 'score': d2_qs, 'level_sum': len(d2_qs),
        'pubdate': datetime.datetime.strftime(d1.pub_date, '%Y.%m.%d'),  # 不影响d1
        'level_list': ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐'],
    })


def score(request, music_id):  # 设置评分动作(1-5颗⭐的数量分别对应2-10分，最后取平均值放在MusicsInfo里的score)
    #try:
        #s1 = MusicsInfo.objects.get(pk=music_id)
    #except MusicsInfo.DoesNotExist:
        #raise Http404('抱歉，音乐《%s》不存在。'%str(music_id))
    s1 = get_object_or_404(MusicsInfo, pk=music_id)
    # 1. request.POST是一个类似字典的对象，通过键名访问提交的数据，request.POST[’choice’]返回被选择选项的ID，
    #    并且值的类型永远是string字符串，也可以用类似的手段获取GET请求发送过来的数据；
    #    如果POST数据里没有提供choice键值，会返回表单页面并给出错误提示，触发一个KeyError异常；
    # 2. 在选择计数器加一后，返回的是一个HttpResponseRedirect而不是先前我们常用的HttpResponse；⭐
    #    HttpResponseRedirect需要一个参数：重定向的URL；建议处理POST数据后，应当保持始终返回一个HttpResponseRedirect；
    # 3. 在HttpResponseRedirect的构造器中使用了一个reverse()函数，用于避免在视图函数中硬编码URL；
    #    reverse(URLconf中指定的name，传递的数据)，例如'/polls/3/results/'，其中的3是某个question.id的值；
    #    重定向后将进入polls:results对应的视图，并将question.id传递给它，就是把活扔给另外一个路由对应的视图去干。
    try:
        s3 = request.POST['pingfen']  # 映射key为空会报错KeyError，dict.get(key)不会报错返回None
    except:  # KeyError
        #return render(request, 'LoveMuiscs/detail.html', {
            #'pf_info': s1, 'error_message': '您还没有选择评分。',
        #})
        return HttpResponse('您还没有选择评分。')
        #c = {'pf_info': s1, 'error_message': '您还没有选择评分。'}
        #return HttpResponseRedirect(reverse('LoveMusics:detail', args=(s1.id, )), context=c)
    else:
        if not MusicsScore.objects.filter(song=s1.song, platform='LoveMusics', level=chr(70 - s3.count('⭐'))):
            MusicsScore.objects.create(song=s1.song, platform='LoveMusics', level=chr(70 - s3.count('⭐')))
            #s2_list = MusicsScore.objects.filter(song=s1.song)
            #context = {
                #'pf_info': s1, 'pf_score': s2_list,
                #'level_list': ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐'],
            #}
            # 以上数据需要在detail里面处理来显示详情，因为这里只返回含id的url给result处理⭐
            #return render(request, 'LoveMusics/result.html', context)
            # 对音乐评分后，score()视图重定向到了评分的结果显示页面
            return HttpResponseRedirect(reverse('LoveMusics:result', args=(s1.id, )))  # 为啥传元组？
            # 定向传给名为result的二级路由让其指向视图里的result函数来显示结果⭐
        else:
            return HttpResponse("您已通过LoveMusics平台发布过一样的评分。")


def result(request, music_id):  # 展示一首音乐的评分结果，可做可视化
    # (1-5颗⭐的数量分别对应2-10分，最后取平均值放在MusicsInfo里的score)
    r1 = get_object_or_404(MusicsInfo, pk=music_id)
    try:
        r2_list = MusicsScore.objects.filter(song=r1.song).order_by('-id')
    except MusicsScore.DoesNotExist:
        raise Http404('抱歉，音乐《%s》还未有评分。'%str(r1.song))
    else:
        rsum = sum(70 - ord(r.level) for r in r2_list)
        r1.score = round(rsum * 2 / len(r2_list), 1)  # 可以加一个判断，有改动或不相等才修改并保存
        r1.save()
        r3_list = [tempclass(scoreid=i.id, song=i.song, platform=i.platform, level=i.level) for i in r2_list]
        for i in r3_list:  # 用于展示“⭐”
            i.level = '⭐' * (70 - ord(i.level))  # 不会修改系统和类/模型的数据，只修改类tempclass的数据
        template = loader.get_template('LoveMusics/result.html')
        return HttpResponse(template.render({'info': r1, 'score': r3_list}, request))  # context和request的顺序不能变


def visual(request):
    v_qs = MusicsInfo.objects.all().order_by('pub_date')  # 时间升序
    vx_list = ['（%s）%s'%(str(i.id), i.song) for i in v_qs]
    vy1_list = [i.score for i in v_qs]
    vy2_list = [len(MusicsScore.objects.filter(song=i.song)) for i in v_qs]
    vl = (
        Bar(init_opts=opts.InitOpts(width='1200px', height='500px', is_horizontal_center=True))  #, bg_color='#fff3c7', is_fill_bg_color=True
        .add_xaxis(vx_list)
        .add_yaxis("评分", vy1_list, color='orange', itemstyle_opts=opts.ItemStyleOpts(opacity=0.68))  # 透明度
        .add_yaxis("在听人数", vy2_list, color='darkgray', itemstyle_opts=opts.ItemStyleOpts(opacity=0.68))
        .set_global_opts(title_opts=opts.TitleOpts(title="LoveMusics乐库", subtitle="*按时间排序".center(43), pos_left='center',
                                                   title_textstyle_opts=opts.TextStyleOpts(font_size=28, color='orange')),
                         legend_opts=opts.LegendOpts(pos_bottom="bottom"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))  # x轴索引旋转30°
    )
    #pagelayout = Page(layout=Page.SimplePageLayout)  # 页面布局
    #pagelayout.add(vl)
    #pagelayout.add_image("./static/LoveMusics/images/橙色背景.jpg")

    # HttpResponse(str)，返回只有这个str的http响应，也就是一个只有str的空白页面，render_embed不会生成本地html文件⭐
    # render_embed应该无法再编辑html语句，用render会每次生成新的html，编辑之后会被覆盖⭐
    # render()返回str类型的生成的render.html的默认路径，更改后会覆盖原html
    # render(r':\...\test.html')返回str类型的生成的test.html的路径
    # 用render需要先生成html文件，之后再：①直接返回render(request, 'html')；
    # ②HttpResponse(loader.get_template('html').render({}, request))。
#①√ #return HttpResponse(vl.render_embed())  # 返回的是str类型的html语句
#②√ #return render(request, vl.render(r'F:\study\before_work_projects\A02_FavoriteMusics\LoveMusics\templates\LoveMusics\visual.html'))
#③√ #vl.render(r'F:\study\before_work_projects\A02_FavoriteMusics\LoveMusics\templates\LoveMusics\visual.html')
#   #t = loader.get_template('LoveMusics/visual.html')
#   #return HttpResponse(t.render({}, request))  # context must be a dict rather than WSGIRequest.
    # 在图表html里插入自定义语句⭐
# √ #html_str1 = vl.render_embed()
#   #i = re.search('<body[^>]*>', html_str1).span()[1]
#   #html_str2 = html_str1[:i] + '<h1>测试</h1>' + html_str1[i:]
#   #return HttpResponse(html_str2)
    # ×以下在新建的html中写入图表的html语句，不能执行，只是一个类型为str的值，
    # 最好直接复制图表的代码到html文件中，或者直接自己用JavaScript在html文件中编写图表
    #html_str = vl.render_embed()
    #i = re.search('<div(.*)</script>', html_str, re.S).span()
    #context = {'htmlstr': html_str[i[0]:i[1]]}

    #return HttpResponse(vl.render_embed())  # 先执行这句，把图表的html生成语句复制过来放visual.html中，之后执行下面
    return render(request, 'LoveMusics/visual.html')

    # bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}
# add_js_funcs(
#         """
#         var img = new Image();
#         img.src = 'LoveMusics/static/LoveMusics/images/橙色背景.jpg';
#         """
#     )