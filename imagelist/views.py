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
from imagelist.logics import dataDelete, FileCreator, ImageOperator
from .logics.ImageImporter import ImageImporter
from .logics.ImageListDao import ImageListDao, ImageListDetailDao

from django.utils import timezone

'''
index
'''
def index(request):
    return render(request, 'imagelist/index.html')

'''
管理画面
'''
def admin(request):
    filepath_list = ImageList.objects.order_by('-id')
    context = {'filepath_list': filepath_list,}
    return render(request, 'imagelist/admin.html', context)

'''
ファイル一覧
'''
def fileList(request):
    latest_filepath_list = ImageList.objects.order_by('-id')[:30]
    context = {'latest_image_list': latest_filepath_list,}
    return render(request, 'imagelist/file_list.html', context)

'''
ファイル詳細一覧
'''
def listview(request, imagelist_id):
    try:
        fileList = ImageList.objects.order_by('-id')
        imageDatas = ImageListDetail.objects.filter(imageList_id=imagelist_id).order_by('disp_order')
        context = {'imageDatas': imageDatas, 'imageListId': imagelist_id, 'fileList': fileList,}
    except ImageList.DoesNotExist:
        raise Http404("Image does not exist")
    return render(request, 'imagelist/file_detail.html', context)

'''
画像削除
'''
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

'''
ファイル登録
'''
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

'''
全ファイル削除
'''
def deleteAllData(request):
    dataDelete.deleteAll()
    filepath_list = ImageList.objects.order_by('-id')
    context = {'filepath_list': filepath_list,}
    return HttpResponseRedirect(reverse('imagelist:admin'))

'''
個別ファイル削除
'''
def deleteAt(request, imagelist_id):
    dataDelete.deleteAt(imagelist_id)
    filepath_list = ImageList.objects.order_by('-id')
    context = {'filepath_list': filepath_list,}
    return HttpResponseRedirect(reverse('imagelist:admin'))

'''
画面に表示されている画像の保存パスをテキストファイルに出力する
    1．outputFileNameが指定されていたら、ImageListに新規登録する。そしてそのImageListを画像追加対象とする
    2．selectedImageListIdが指定されていたら、そのImageListを画像追加対象とする
    3．POSTでチェックした画像IDを取得できるようにする。
    4．その画像IDのImageDetailを、1or2のImageListIdのImageDetailに追加する
'''
def createImageListFile(request, imageListId):
    try:
        outputFileName = request.POST.get('outputFileName') # ファイル名テキストボックス入力値
        checkedList = request.POST.getlist('choice')        # 選択された画像ファイルID
        
        # ファイル名テキストが入力されていたら新規ファイルとして登録する。さらにその新規ファイルに選択画像を登録する。
        if len(str(outputFileName).strip()) > 0:
            # 選択した画像で新規ファイル作成
            imageOpe = ImageOperator.ImageOperator()
            newImageList = imageOpe.Create(outputFileName, 
                                            os.path.join('out', outputFileName), 
                                            checkedList)
            # 新規ファイルの画像一覧を表示
            imageDatas = ImageListDetail.objects.filter(imageList_id=newImageList.pk).order_by('disp_order')
            context = {'imageDatas': imageDatas, 
                        'imageListId': newImageList.pk, 
                        'fileList': ImageList.objects.order_by('-id'),}
            return HttpResponseRedirect(reverse('imagelist:listview', 
                args=(newImageList.pk, )), context)
    except ImageList.DoesNotExist:
        raise Http404("Image does not exist")
    return HttpResponseRedirect(reverse('imagelist:listview', 
        args=(imageListId, )), context)

def appendImageListFile(request, imageListId):
    try:
        selectedImageListId = request.POST.get('fileList')  # 画像リストファイルコンボ選択値
        checkedList = request.POST.getlist('choice')        # 選択された画像ファイルID

        # 選択されたファイルに画像を追加する
        detailDao = ImageListDetailDao()
        detailDao.register(checkedList, selectedImageListId)

        # 画像データを取得する
        imageDatas = ImageListDetail.objects.filter(imageList_id=imageListId)
        context = {'imageDatas': imageDatas, 'imageListId': imageListId}
    except ImageList.DoesNotExist:
        raise Http404("Image does not exist")
    return HttpResponseRedirect(reverse('imagelist:listview', 
        args=(imageListId, )), context)

'''
表示中のImageListを出力する
'''
def outputImageListFile(request, imageListId):
    # 画像データを取得する
    imageDatas = ImageListDetail.objects.filter(imageList_id=imageListId)
    fileName = ImageList.objects.get(pk=imageListId).file_name
    # 画像ファイルパスを取得する
    pathList = []
    for imageData in imageDatas:
        pathList = pathList + [imageData.file_path]
    # ファイル作成
    outputFilePath = os.path.join('out', fileName)
    fc = FileCreator.FileCreator()
    fc.createImageListFile(outputFilePath, pathList)
    context = {'imageDatas': imageDatas, 'imageListId': imageListId}
    return FileResponse(open(outputFilePath, "rb"), as_attachment=True, filename=fileName)
    

# def showImageSample():
#     image = Image.open('media/images/51393749.jpeg')
#     image.show()

