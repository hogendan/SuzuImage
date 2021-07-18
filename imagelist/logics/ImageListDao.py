from imagelist.models import ImageList, ImageListDetail

class ImageListDao:
    def register(self, fileName: str, filePath: str) -> ImageList:
        imageList = ImageList()
        imageList.file_name = fileName
        imageList.file_path = filePath
        imageList.save()
        return imageList

class ImageListDetailDao:
    def register(self, detailIds: list, parentImageListId: int):
        details = ImageListDetail.objects.filter(imageList_id=parentImageListId).order_by('-disp_order')
        parentImageList = ImageList.objects.get(pk=parentImageListId)
        max_disp_order = 0 if len(details) == 0 else details[0].disp_order
        for id in detailIds:
            detail = ImageListDetail.objects.get(pk=id)
            max_disp_order += 1
            new_detail = ImageListDetail()
            new_detail.imageList = parentImageList
            new_detail.disp_order = max_disp_order
            new_detail.file_path = detail.file_path
            new_detail.image_data = detail.image_data
            new_detail.save()
