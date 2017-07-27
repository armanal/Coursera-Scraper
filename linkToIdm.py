import time
import pickle
import os.path
import os
from CEscrap import *
import sys

path = r"Intermet Download Manager path to save downloaded files"
name = ''
url = ''

lessonList = openObj('data.obj')
if lessonList == None:
    sys.exit(-1)

for lesson in lessonList:
    name = str(lesson.lessonNum+1) + '.' + lesson.name
    if lesson.videoURL != '':
        os.system('idman /a /n /p \"{0}\" /f \"{1}\" /d \"{2}\"'.format(path + "\\{0}".format(lesson.weekNum + 1) , name + ".mp4", lesson.videoURL))
    if lesson.subtitleURL != '':
        os.system('idman /a /n /p \"{0}\" /f \"{1}\" /d \"{2}\"'.format(path + "\\{0}".format(lesson.weekNum + 1) , name + ".srt", lesson.subtitleURL))
    if lesson.slideURL != '':
        os.system('idman /a /n /p \"{0}\" /f \"{1}\" /d \"{2}\"'.format(path + "\\{0}".format(lesson.weekNum + 1) , name + ".ppt", lesson.slideURL))
    print("{0} : {1}".format(lesson.weekNum+1, lesson.lessonNum+1))
