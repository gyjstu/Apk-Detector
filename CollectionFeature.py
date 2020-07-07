#-- coding:utf-8 --
"""
使用说明:本工具用于提取apk特征，目前只能用于linux或者mac os系统
依赖：
	1.jdk
	2.目录下aapt需要与对应系统匹配
	3.python3.6+
"""
import logging
import xml.sax
import os
from ExtractPermission import doextractpermission
from ExtractAPK import doextract
from FindURI import dofinduri
from FindIntent import dofindintent
from FindSUSI import dofindSUSI
from RenameAPK import APK_rename
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./log/CollectionFeature_log.log',
                    filemode='w')


filepath = './APK'
#filepath = './malware'
#filepath = './benign'

savepath_SUSI_xmls = './APK_SUSI_XMLS'
savepath_SUSI_jsons = './APK_SUSI_JSONS'
savepath_extract = './APK_Extract_Result'
savepath_permission = './APK_Permission_Result'
savepath_uri = './APK_Uri_Result'
savepath_intent = './APK_Intent_Result'



def doCollection_Feature():
	try:
		APK_rename() 	# 将apk名称中的空格替换为下划线
		dofindSUSI(filepath,savepath_SUSI_xmls,savepath_SUSI_jsons) # 批量获取SUSI
		doextract(filepath,savepath_extract)       					# 批量反编译apk，会将结果存储在 savepath_extract 中
		dofinduri(savepath_extract,savepath_uri)   					# 批量获取apk中的uri
		dofindintent(savepath_extract,savepath_intent)				# 批量获取apk中的intent
		doextractpermission(savepath_extract,savepath_permission)	# 批量获取apk中的权限信息

	except Exception as e:
		print('some error occurred in main.doCollection_Feature: ', e)
		logging.info('some error occurred in main.doCollection_Feature: ', e)
		pass




if __name__ == '__main__':
    doCollection_Feature()