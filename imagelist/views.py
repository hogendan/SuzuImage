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
from django.http import Http404, HttpResponseRedirect, FileResponse
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
        fileList = ImageList.objects.order_by('-id')
        imageDatas = ImageListDetail.objects.filter(imageList_id=imagelist_id).order_by('disp_order')
        context = {'imageDatas': imageDatas, 'imageListId': imagelist_id, 'fileList': fileList,}
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

'''
画面に表示されている画像の保存パスをテキストファイルに出力する
'''
def createImageListFile(request, imageListId):
    try:
        outputFileName = request.POST.get('outputFileName') # ファイル名テキストボックス入力値
        selectedImageListId = request.POST.get('fileList')  # 画像リストファイルコンボ選択値
        checkedList = request.POST.getlist('choice')        # 選択された画像ファイルID

        targetImageList = ImageList.objects.get(pk=selectedImageListId)
        max_disp_order = ImageListDetail.objects.filter(imageList_id=selectedImageListId).order_by('-disp_order')[0].disp_order
        for id in checkedList:
            max_disp_order += 1
            detail = ImageListDetail.objects.get(pk=id)
            new_detail = ImageListDetail()
            new_detail.imageList = targetImageList
            new_detail.file_path = detail.file_path
            new_detail.image_data = detail.image_data
            new_detail.disp_order = max_disp_order
            new_detail.save()

        ''' 
        1．outputFileNameが指定されていたら、ImageListに新規登録する。そしてそのImageListを画像追加対象とする
        2．selectedImageListIdが指定されていたら、そのImageListを画像追加対象とする
        3．POSTでチェックした画像IDを取得できるようにする。
        4．その画像IDのImageDetailを、1or2のImageListIdのImageDetailに追加する
        '''

        '''
        以下の処理は別のファイル出力処理を作ったら移動する
        '''
        # 画像データを取得する
        imageDatas = ImageListDetail.objects.filter(imageList_id=imageListId)
        # 画像ファイルパスを取得する
        pathList = []
        for imageData in imageDatas:
            pathList = pathList + [imageData.file_path]
        # ファイル作成
        outputFilePath = os.path.join('out', outputFileName)
        fc = FileCreator.FileCreator()
        fc.createImageListFile(outputFilePath, pathList)
        context = {'imageDatas': imageDatas, 'imageListId': imageListId}
    except ImageList.DoesNotExist:
        raise Http404("Image does not exist")
    # return render(request, 'imagelist/file_detail.html', context)
    return FileResponse(open(outputFilePath, "rb"), as_attachment=True, filename=outputFileName)

# def showImageSample():
#     image = Image.open('media/images/51393749.jpeg')
#     image.show()

