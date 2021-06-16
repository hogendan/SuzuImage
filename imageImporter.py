from django.db import models
import os
import sys
import django
from django.utils import timezone
from PIL import Image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PinkSuzu.settings")  # コマンドラインからpython実行するために必須
django.setup()                                                      # コマンドラインからpython実行するために必須

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagelist.models import ImageList, ImageListDetail

def importImage():
    if len(sys.argv) < 2:
        print('パラメータに読み込むファイルパスを指定してください')
        input()
        exit()

    imageroot = 'media\images'
    importFilePath = sys.argv[1]    # file path
    if not os.path.exists(importFilePath):
        print('ファイルが存在しません [%s]' %(importFilePath))
        input()
        exit()

    # ファイル名をDBへ登録
    print('ImageListへ書き込み中...')
    imagelistTbl = saveToImageListTbl(importFilePath)
    print('ImageList書き込み終了 Id=[%s]' % imagelistTbl.pk)

    print('画像ファイルをローカルに保存中...')
    # ファイル読み込み
    # importFile = open(importFilePath, 'r', encoding='utf_16')
    fullpath_list = []; # ファイルの中の画像ファイルパスを保存する
    # ファイルの中の画像ファイルをimage rootに保存する
    with open(importFilePath, 'r', encoding='utf_16') as file:
        for line in file.readlines():
            line = line.replace('\n', '')
            filename = os.path.basename(line)
            # 画像ファイルパスではない場合はスキップ
            if filename == '' or os.path.dirname(line) == '':
                continue
            fullpath_list.append(line)

            savePath = os.path.join(imageroot, os.path.splitdrive(line)[1].strip("\\")) # Driveレターを除いたパスとimagerootを付ける
            if (not os.path.exists(os.path.dirname(savePath))):
                os.makedirs(os.path.dirname(savePath))
            print('画像ファイルをローカルへ保存 [%s]' % savePath)
            # 画像ファイル読み込み
            image = Image.open(line)
            # 画像ファイル保存
            image.save(savePath)
    print('画像ファイル保存終了')

    print('ImageListDetailへ書き込み中...')
    # 保存した画像ファイルをDBへ登録
    saveToImageListDetailTbl(imagelistTbl, fullpath_list)
    print('ImageListDetail書き込み終了')

def showImageSample():
    image = Image.open('media/images/51393749.jpeg')
    image.show()

def saveToImageListTbl(filePath: str):
    imagelistTbl = ImageList()
    imagelistTbl.file_path = filePath
    imagelistTbl.file_name = os.path.basename(filePath)
    imagelistTbl.save()
    return imagelistTbl


def saveToImageListDetailTbl(imagelistTbl, filefullpath_list):
    disp_order = 0    
    for fullpath in filefullpath_list:
        print('画像ファイルをDBへ保存 [%s]' % fullpath)
        disp_order+=1
        detail = ImageListDetail()
        detail.imageList = imagelistTbl
        detail.file_path = fullpath
        detail.image_data = 'images/' + os.path.splitdrive(fullpath)[1]     # Driveレターを除いたパス
        detail.disp_order = disp_order

        detail.save()

    contents = ImageList.objects.all()
    print(contents)

importImage()
# saveToDb()