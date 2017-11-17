#-*- coding:utf-8 -*-
import zipfile
import os
#解压下载的打包文件
f = zipfile.ZipFile('C:\Users\leong\Downloads\wenshudownload\hensi.zip','r')
for file in f.namelist():
    f.extract(file,'C:\Users\leong\Downloads\wenshudownload')

#压缩文件
f1 = zipfile.ZipFile('E:\wenshuzip','w',zipfile.ZIP_DEFLATED)
f1.write('about_huishang.txt','C:E:\wenshuzip\temp')

# # 解压当前目录下的zip文件到当前目录，并删除原有的zip文件:一
# import zipfile
# import os
#
# file_list = os.listdir(r'.')
#
# for file_name in file_list:
#     if os.path.splitext(file_name)[1] == '.zip':
#         print file_name
#
#         file_zip = zipfile.ZipFile(file_name, 'r')
#         for file in file_zip.namelist():
#             file_zip.extract(file, r'.')
#         file_zip.close()
#         os.remove(file_name)

#解压缩一个文件
# def unzip_dir(zipfilename, unzipdirname):
#     fullzipfilename = os.path.abspath(zipfilename)
#     fullunzipdirname = os.path.abspath(unzipdirname)
#     print "Start to unzip file %s to folder %s ..." % (zipfilename, unzipdirname)
#     #Check input ...
#     if not os.path.exists(fullzipfilename):
#         print "Dir/File %s is not exist, Press any key to quit..." % fullzipfilename
#         inputStr = raw_input()
#         return
#     if not os.path.exists(fullunzipdirname):
#         os.mkdir(fullunzipdirname)
#     else:
#         if os.path.isfile(fullunzipdirname):
#             print "File %s is exist, are you sure to delet it first ? [Y/N]" % fullunzipdirname
#             while 1:
#                 inputStr = raw_input()
#                 if inputStr == "N" or inputStr == "n":
#                     return
#                 else:
#                     if inputStr == "Y" or inputStr == "y":
#                         os.remove(fullunzipdirname)
#                         print "Continue to unzip files ..."
#                         break
#
#     #Start extract files ...
#     srcZip = zipfile.ZipFile(fullzipfilename, "r")
#     for eachfile in srcZip.namelist():
#         print "Unzip file %s ..." % eachfile
#         eachfilename = os.path.normpath(os.path.join(fullunzipdirname, eachfile))
#         eachdirname = os.path.dirname(eachfilename)
#         if not os.path.exists(eachdirname):
#             os.makedirs(eachdirname)
#         fd=open(eachfilename, "wb")
#         fd.write(srcZip.read(eachfile))
#         fd.close()
#     srcZip.close()
#     print "Unzip file succeed!"

#压缩一个目录
def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()