from django.db import models

# 歌手模型
class Artist(models.Model):
    name = models.CharField(max_length=100, verbose_name='歌手姓名')  # 歌手姓名
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='国籍')  # 可选字段
    biography = models.TextField(blank=True, null=True, verbose_name='简介')  # 歌手简介

    def __str__(self):
        return self.name

# 歌曲模型
class Song(models.Model):
    title = models.CharField(max_length=200, verbose_name='歌名')  # 歌曲名称
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs', verbose_name='歌手')  # 所属歌手
    album = models.CharField(max_length=200, blank=True, null=True, verbose_name='专辑')  # 专辑名
    release_date = models.DateField(blank=True, null=True, verbose_name='发行日期')  # 可选
    genre = models.CharField(max_length=100, blank=True, null=True, verbose_name='风格')  # 歌曲风格

    def __str__(self):
        return self.title

# 歌词模型
class Lyric(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='lyric', verbose_name='所属歌曲')  # 每首歌一个歌词
    content = models.TextField(verbose_name='歌词内容')  # 歌词正文

    def __str__(self):
        return f"{self.song.title} 的歌词"
