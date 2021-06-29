import array
import os

class FileCreator:
    def createImageListFile(self, savePath:str, filePathList: array):
        root, ext = os.path.splitext(savePath)        
        if (ext == ''):
            savePath = savePath + '.txt'
        os.makedirs(os.path.dirname(savePath), exist_ok=True)
        with open(savePath, 'w', encoding='utf_16') as file:
            file.writelines('\n'.join(filePathList) + '\n')
