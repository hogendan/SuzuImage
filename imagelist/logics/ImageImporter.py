from ..models import ImageList, ImageListDetail
from PIL import Image
import os

class ImageImporter:
    def __init__(self):
        super().__init__()
    
    def importImage(self, targetFile):
        print('type: %s' % type(targetFile))
        imageroot = 'media\images'

        # いったんファイルを保存
        with open('temp.txt', 'wb+') as destination:
            for chunk in targetFile.chunks():
                destination.write(chunk)

        # ファイル名をDBへ登録
        print('ImageListへ書き込み中...')
        imagelistTbl = self.saveToImageListTbl(targetFile.name)
        newImageListId = imagelistTbl.pk
        print('ImageList書き込み終了 Id=[%s]' % newImageListId)

        print('画像ファイルをローカルに保存中...')
        # ファイル読み込み
        # importFile = open(importFilePath, 'r', encoding='utf_16')
        fullpath_list = []; # ファイルの中の画像ファイルパスを保存する
        # ファイルの中の画像ファイルをimage rootに保存する
        with open('temp.txt', 'r', encoding='utf_16') as file:
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
        self.saveToImageListDetailTbl(imagelistTbl, fullpath_list)
        print('ImageListDetail書き込み終了')
        
        return newImageListId

    def saveToImageListTbl(self, filePath: str):
        imagelistTbl = ImageList()
        imagelistTbl.file_path = filePath
        imagelistTbl.file_name = os.path.basename(filePath)
        imagelistTbl.save()
        return imagelistTbl

    def saveToImageListDetailTbl(self, imagelistTbl, filefullpath_list):
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
