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
from imagelist.logics import dataDelete, FileCreator
from .logics.ImageImporter import ImageImporter

from django.utils import timezone

def index(request):
    return render(request, 'imagelist/index.html')

def admin(request):
    filepath_list = ImageList.objects.order_by('-id')
    context = {'filepath_list': filepath_list,}
    return render(request, 'imagelist/admin.html', context)

def fileList(request):
    latest_filepath_list = ImageList.objects.order_by('-id')[:30]
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
    imageImporter = ImageImporter()
    for file in files:
        lastImportId = imageImporter.importImage(file)

    imageList_id = lastImportId
    latest_filepath_list = ImageList.objects.order_by('-file_path')[:30]
    context = {'latest_image_list': latest_filepath_list,}
    
    return HttpResponseRedirect(reverse('imagelist:listview',
        args=(imageList_id, )), context)

def deleteAllData(request):
    dataDelete.deleteAll()
    filepath_list = ImageList.objects.order_by('-id')
    context = {'filepath_list': filepath_list,}
    return HttpResponseRedirect(reverse('imagelist:admin'))

def deleteAt(request, imagelist_id):
    dataDelete.deleteAt(imagelist_id)
    filepath_list = ImageList.objects.order_by('-id')
    context = {'filepath_list': filepath_list,}
    return HttpResponseRedirect(reverse('imagelist:admin'))

def createImageListFile(request, imageListId):
    try:
        outputFileName = request.POST.get('outputFileName')
        imageDatas = ImageListDetail.objects.filter(imageList_id=imageListId)
        pathList = []
        for imageData in imageDatas:
            pathList = pathList + [imageData.file_path]
        # ファイル作成
        fc = FileCreator.FileCreator()
        fc.createImageListFile(os.path.join('out', outputFileName), pathList)
        context = {'imageDatas': imageDatas, 'imageListId': imageListId}
    except ImageList.DoesNotExist:
        raise Http404("Image does not exist")
    return render(request, 'imagelist/file_detail.html', context)

# def showImageSample():
#     image = Image.open('media/images/51393749.jpeg')
#     image.show()

