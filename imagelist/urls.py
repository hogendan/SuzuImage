from django.urls import path

from . import views

app_name = 'imagelist'  # アプリの名前空間を設定。
urlpatterns = [
    # ex: /imagelist/
    path('', views.index, name='index'),
    path('admin/', views.admin, name='admin'),
    path('filelist/', views.fileList, name='filelist'),
    # ex: /imagelist/c:\image\list.txt
    # path('<str:filepath>/', views.listview, name='listview')
    path('<int:imagelist_id>/', views.listview, name='listview'),
    path('<int:imageList_id>/deleteimage/', views.deleteImage, name='deleteimage'),
    path('register/', views.registerImageListFile, name='registerimagelistfile'),
    path('deleteall/', views.deleteAllData, name='deletealldata'),
    path('<int:imagelist_id>/deleteat/', views.deleteAt, name='deleteat'),
    path('<int:imageListId>/createimagelistfile/', views.createImageListFile, name='createimagelistfile'),
    path('<int:imageListId>/appendimagelistfile/', views.appendImageListFile, name='appendimagelistfile'),
    path('<int:imageListId>/outputimagelistfile/', views.outputImageListFile, name='outputimagelistfile'),
]
