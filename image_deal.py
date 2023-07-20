#pip install baidu-aip;pip install chardet
from aip import AipOcr
import re

APP_ID = '30239728'
API_KEY = 'bpVTIYhhREwOSLPwxwgyemEz'
SECRET_KEY = '7HkLiChYIyGUWXDE33i2WTu0RVnAZ3gX'

class read_image():
    def __init__(self):
        self.app_id=APP_ID
        self.api_key=API_KEY
        self.secret_key=SECRET_KEY
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        # self.filePath=filePath

    """ 读取图片 """
    def get_file_content(self,filepath):
        with open(filepath, 'rb') as fp:
            return fp.read()

    def do_ai(self,image):
        # image = self.get_file_content(filepath)
        """ 调用通用文字识别, 图片参数为本地图片 """
        data=str(self.client.basicGeneral(image)).replace(' ','')
        # print(data)
        pat=re.compile(r"{'words':'(.*?)'}")
        result=pat.findall(data)
        return result

if __name__=='__main__':
    T=read_image()
    image = T.get_file_content(r'C:\Users\1\Desktop\image/dd.jpg')
    result=T.do_ai(image)
    for i in result:
        print(i)