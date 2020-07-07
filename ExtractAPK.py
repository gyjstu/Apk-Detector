#-- coding:utf-8 --
import os
import re
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./log/extractAPK_log.log',
                    filemode='w')

# 反编译APK
def extractapk(filepath,file,savepath):
	try:
		cmd = "jadx-1/bin/jadx -d " + savepath + "/" + file + "_res " + filepath + "/" + file
		#cmd = "jadx -d "+ savepath + "/" + file + "_res " + filepath + "/" + file
		print(cmd)
		os.system(cmd)

	except Exception as e:
		print('some error occurred in ExtractAPK.extractapk: ', e)
		logging.info('some error occurred in ExtractAPK.extractapk: ', e)
		pass

# 获取APK列表
def getapks(filepath):
	return os.listdir(filepath)

def checkresult(file,savepath):
	try:
		if (os.path.exists(savepath + "/" + file+"_res")):
			print(file+"--> already done!")
			return True
		else:
			return False
	except Exception as e:
		print('some error occurred in ExtractAPK.checkresult: ', e)
		logging.info('some error occurred in ExtractAPK.checkresult: ', e)
		pass



def doextract(filepath,savepath):
	try:
		apks = getapks(filepath)
		for file in apks:
			if checkresult(file,savepath):
				continue
			else:
				extractapk(filepath,file,savepath)
				print(file+"--> done!")

	except Exception as e:
		print('some error occurred in ExtractAPK.doextract: ', e)
		logging.info('some error occurred in ExtractAPK.doextract: ', e)
		pass