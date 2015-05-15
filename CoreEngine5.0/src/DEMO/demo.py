# import commands
# 
# (status, output) = commands.getstatusoutput("(ffmpeg -i rtsp://127.0.0.1:12021/rtsp/2/0 -vcodec copy -acodec copy -f mp4 -y test.mp4 > out.log 2>&1 &);sleep 3;ls -l test.mp4 | awk '{print $5}'")
# 
# print output


# def get():
#     return (1,2)
# 
# (a,b) = get()
# print a,b
# print b

for i in range(5):
    print i
