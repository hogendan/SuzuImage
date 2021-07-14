from imagelist.models import ImageList, ImageListDetail

class ImageListDao:
    def register(self, fileName: str, filePath: str) -> ImageList:
        imageList = ImageList()
        imageList.file_name = fileName
        imageList.file_path = filePath
        imageList.save()
        return imageList

class ImageListDetailDao:
    def register(self, detailIds: list, parentImageList: ImageList):
            disp_order = 0
            for id in detailIds:
                detail = ImageListDetail.objects.get(pk=id)
                disp_order += 1
                new_detail = ImageListDetail()
                new_detail.imageList = parentImageList
                new_detail.disp_order = disp_order
                new_detail.file_path = detail.file_path
                new_detail.image_data = detail.image_data
                new_detail.save()
