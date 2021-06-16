from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class ImageList(models.Model):
    def __str__(self):
        return self.file_name

    file_path = models.CharField(
        verbose_name='ファイルパス',
        max_length=1000,
        blank=False,
        null=False,
    )

    file_name = models.CharField(
        verbose_name='ファイル名',
        max_length=100,        
    )


class ImageListDetail(models.Model):
    imageList = models.ForeignKey(ImageList, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_path
    # ファイルパス(オリジナルの画像ファイルパス)
    file_path = models.CharField(
        verbose_name='ファイルパス',
        max_length=500,
        blank=False,
        null=False,
    )
    # 画像データ
    image_data = models.ImageField(
        verbose_name='画像データ',
        upload_to='images/',
    )
    # サムネイル
    thumbnail = ImageSpecField(source="image_data",
        processors=[ResizeToFill(150,150)],
        format='JPEG',
        options={'quality': 60}
    )

    # 表示順
    disp_order = models.IntegerField(
        verbose_name='表示順',
        blank=False,
        null=False,
    )