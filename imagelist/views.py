'''
・DBのイメージファイル（media\images）を読み込みList表示する
・Index.html
    ・画像リストファイルをリンクで表示する。
    ・リンクをクリックすると画像リスト表示画面へ遷移する。
・画像リスト.html
    ・画像リストファイルの中の画像がリスト表示される
'''
import os
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import ImageList, ImageListDetail
import dataDelete

from django.utils import timezone
from PIL import Image

def index(request):
    return render(request, 'imagelist/index.html')

def admin(request):
    return render(request, 'imagelist/admin.html')

def fileList(request):
    latest_filepath_list = ImageList.objects.order_by('file_path')[:30]
    context = {'latest_image_list': latest_filepath_list,}
    return render(request, 'imagelist/file_list.html', context)

def listview(request, imagelist_id):
    try:
        imageDatas = ImageListDetail.objects.filter(imageList_id=imagelist_id)
        context = {'imageDatas': imageDatas, 'imageListId': imagelist_id}
    except ImageList.DoesNotExist:
        raise Http404("Image does not exist")
    return render(request, 'imagelist/file_detail.html', context)

def deleteImage(request, imageList_id):
    try:
        # 削除処理
        checkedList = request.POST.getlist('choice')
        for detailId in checkedList:
            ImageListDetail.objects.get(pk=detailId).delete()
        # 削除後データ取得
        imageDatas = ImageListDetail.objects.filter(imageList_id=imageList_id)
        context = {'imageDatas': imageDatas, 'imageListId': imageList_id}
    except ImageList.DoesNotExist:
        raise Http404("Image does not exist")
    return HttpResponseRedirect(reverse('imagelist:listview', 
        args=(imageList_id, )), context)

def registerImageListFile(request):
    if request.method != 'POST':
        return render(request, 'imagelist:index')

    # Get filelist from request.
    files = request.FILES.getlist('imagefilelist')
    # Import image to DB
    lastImportId = 0
    for file in files:
        lastImportId = importImage(file)

    imageList_id = lastImportId
    latest_filepath_list = ImageList.objects.order_by('-file_path')[:30]
    context = {'latest_image_list': latest_filepath_list,}
    
    return HttpResponseRedirect(reverse('imagelist:listview',
        args=(imageList_id, )), context)

def deleteAllData(request):
    dataDelete.deleteAll()
    return HttpResponseRedirect(reverse('imagelist:admin'))

def importImage(targetFile):
    print('type: %s' % type(targetFile))
    imageroot = 'media\images'

    # いったんファイルを保存
    with open('temp.txt', 'wb+') as destination:
        for chunk in targetFile.chunks():
            destination.write(chunk)

    # ファイル名をDBへ登録
    print('ImageListへ書き込み中...')
    imagelistTbl = saveToImageListTbl(targetFile.name)
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
    saveToImageListDetailTbl(imagelistTbl, fullpath_list)
    print('ImageListDetail書き込み終了')
    
    return newImageListId

# def showImageSample():
#     image = Image.open('media/images/51393749.jpeg')
#     image.show()

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
