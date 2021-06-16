import sys, os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PinkSuzu.settings")  # コマンドラインからpython実行するために必須
django.setup()                                                      # コマンドラインからpython実行するために必須

from imagelist.models import ImageList, ImageListDetail

if len(sys.argv) < 2:
    print('パラメータに削除タイプを指定してください。[all or id]')

def deleteAll():
    ImageListDetail.objects.all().delete()
    ImageList.objects.all().delete()
    print('テーブルを全件削除しました。')
    input()

def deleteTarget(imageListId):
    ImageListDetail.objects.filter(imageList_id=imageListId).delete()
    ImageList.objects.filter(id=imageListId).delete()
    print('ID[%s]のデータをテーブルから削除しました。' % imageListId)

deleteParam = sys.argv[1]
if deleteParam.lower() == 'all':
    deleteAll()
else:
    deleteTarget(deleteParam)

