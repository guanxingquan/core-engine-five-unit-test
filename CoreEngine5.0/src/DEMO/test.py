'''
Created on 2015-4-23

@author: kaisquare
'''



import os
from os.path import getsize, join




size = 0L
#         one_size = 0L
path = "/root/VCABox/kupcore/latest/scripts/linux/"
print path
for root,dirs,files in os.walk(path):
#             print files
#             for name in files:
#                 
#                 size += getsize(join(root,name))
#                 print "file name :%s , size: %s" % name,size
    size += sum([getsize(join(root, name)) for name in files])
#             size += sum([getsize(join(root, name)) for name in files])
print size