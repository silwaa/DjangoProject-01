from django.db import models

class MusicsInfo(models.Model):
    song = models.CharField(max_length=100)
    singer = models.CharField(max_length=50)
    pub_date = models.DateField()
    score = models.FloatField()  # 改：属性名 →
    lang = models.CharField(max_length=30)
    song_type = models.CharField(max_length=30)
    prize = models.CharField(max_length=30)  # 改：类型和可空
    #def __str__(self):
        #return '{:d} 🎵 {:s} - {:s}'.format(self.id, self.song, self.singer)


class MusicsScore(models.Model):
    song = models.CharField(max_length=100)
    platform = models.CharField(max_length=30)
    level = models.CharField(max_length=10)  # A~E
    #def __str__(self):  # 不会显示在html上
        # self.level = '⭐' * (70 - ord(self.level))  # 只能做str的处理
        #if self.level == 'A':
            #self.level = '⭐⭐⭐⭐⭐'
        #elif self.level == 'B':
            #self.level = '⭐⭐⭐⭐'
        #elif self.level == 'C':
            #self.level = '⭐⭐⭐'
        #elif self.level == 'D':
            #self.level = '⭐⭐'
        #else:
            #self.level = '⭐'
        #return '{:d} {:s} ：{:s} —— form {:s}'.format(self.id, self.song, self.level, self.platform)

#class KindsList(models.Model):
#    lang_kinds = models.CharField(max_length=30)
#    type_kinds = models.CharField(max_length=30)
#    prize_kinds = models.CharField(max_length=30)  # 改：类型
#    song_sum = models.IntegerField()  # 改：新增
#    platform_kinds = models.CharField(max_length=30)

#👇shell插入随机评分
#j = 0  # 无重复数据的次数
#for i in range(28):  # i是生成的总次数
#    a = MusicsScore(song=l1[random.randrange(len(l1))], platform=l2[random.randrange(len(l2))], level=l3[random.randrange(len(l3))])
#    if not MusicsScore.objects.filter(song=a.song, platform=a.platform, level=a.level):
#        j = j + 1
#        a.id = j + len(MusicsScore.objects.all())  # 开始是j + 0
#        a.save()
#👇更改id，之后增加新数据id仍会在之前的旧id上自增
#j = 0
#for i in MusicsScore.objects.all():
#    j = j + 1
#    i.id = j
#    i.save()