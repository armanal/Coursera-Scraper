import time
import pickle
import os.path
import os
from CEscrap import *
import sys

path = r"course path in file system"
name = ''
url = ''

lessonList = openObj('data.obj')
if lessonList == None:
    sys.exit(-1)


for lesson in lessonList:
    name = lesson.name.replace('?', '')
    print(os.getcwd())
    try:
        if lesson.videoURL != '':
            os.chdir(path + "\\{0}".format(lesson.weekNum + 1))
            os.rename( name + ".mp4", str(lesson.lessonNum+1) + '.' + name + ".mp4")
        if lesson.subtitleURL != '':
            os.chdir(path + "\\{0}".format(lesson.weekNum + 1))
            os.rename( name + ".srt", str(lesson.lessonNum+1) + '.' + name + ".srt")
        if lesson.slideURL != '':
            os.chdir(path + "\\{0}".format(lesson.weekNum + 1))
            os.rename( name + ".ppt", str(lesson.lessonNum+1) + '.' + name + ".ppt")
    except:
        print('?')
    print("{0} : {1}".format(lesson.weekNum+1, lesson.lessonNum+1))
    #break