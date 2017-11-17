# #-*-coding:utf-8 -*-
# import PIL.Image as image
# import PIL.ImageChops as imagechops
# import time,re,cStringIO,urllib2,random
# def get_merge_image(filename,location_list):
#     '''    根据位置对图片进行合并还原    :filename:图片    :location_list:图片位置    '''
#     pass
#     im = image.open(filename)
#     new_im = image.new('RGB', (260,116))
#     im_list_upper=[]
#     im_list_down=[]
#     for location in location_list:
#         if location['y']==-58:
#             pass
#         im_list_upper.append(im.crop((abs(location['x']),58,abs(location['x'])+10,166)))
#         if location['y']==0:
#             pass
#         im_list_down.append(im.crop((abs(location['x']),0,abs(location['x'])+10,58)))
#         new_im = image.new('RGB', (260,116))
#         x_offset = 0
#         for im in im_list_upper:
#             new_im.paste(im, (x_offset,0))
#             x_offset += im.size[0]
#             x_offset = 0
#         for im in im_list_down:
#             new_im.paste(im, (x_offset,58))
#             x_offset += im.size[0]
#         return new_im
# def get_image(driver,div):
#     '''    下载并还原图片    :driver:webdriver    :div:图片的div    '''
#     pass
#     #找到图片所在的div
#     background_images=driver.find_elements_by_xpath(div)
#     location_list=[]
#     imageurl=''
#     for background_image in background_images:
#         location={}
#         #在html里面解析出小图片的url地址，还有长高的数值
#         location['x']=int(re.findall("background-image: url/(/"(.*)/"/); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][1])
#         location['y']=int(re.findall("background-image: url/(/"(.*)/"/); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][2])
#         imageurl=re.findall("background-image: url/(/"(.*)/"/); background-position: (.*)px (.*)px;",background_image.get_attribute('style'))[0][0]
#         location_list.append(location)
#         imageurl=imageurl.replace("webp","jpg")
#         jpgfile=cStringIO.StringIO(urllib2.urlopen(imageurl).read())
#          #重新合并图片
#         image=get_merge_image(jpgfile,location_list )
#         return image