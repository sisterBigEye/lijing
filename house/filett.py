import os ,sys
print os.path.split(os.path.abspath(sys.argv[0]))
dirname,filename = os.path.split(os.path.abspath(sys.argv[0]))
print os.path.abspath(sys.argv[0])
print "runing from",dirname
print "file is",filename


print "this is __file__",__file__