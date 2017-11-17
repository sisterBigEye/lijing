from PIL import Image
import pytesseract

image=Image.open("capt.png")    #打开验证码图片
image.load()        #加载一下图片，防止报错，此处可省略
image.show() #调用show来展示图片，调试用，可省略

vcode=pytesseract.image_to_string(image)
print (vcode)

