from imagelist.models import ImageList
from imagelist.logics.ImageListDao import ImageListDao, ImageListDetailDao

class ImageOperator:
    def Create(self, fileName: str, filePath: str, detailIds: list) -> ImageList:
        # ImageList登録
        imageListDao = ImageListDao()
        newImageList = imageListDao.register(fileName, filePath)
        # ImageListDetail登録
        detailDao = ImageListDetailDao()
        detailDao.register(detailIds, newImageList)
        return newImageList
