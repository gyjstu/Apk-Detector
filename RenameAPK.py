#! /usr/bin/python
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./log/RenameAPK.log',
                    filemode='w')

# 批量处理apk文件生成对应的.json


def APK_rename():

    try:
        apk_dir = "APK/"
        my_list = os.listdir(apk_dir)

        # Rename the APKs in fodler named './APK'
        for apk in my_list:
            if ' ' in apk:
                print("Ori_Name --> ",apk)
                apk_newname=apk.replace(' ','_')
                print("Rename_To --> ",apk_newname)
                os.rename(apk_dir + apk,apk_dir + apk_newname)

    except Exception as e:
        print('some error occurred in RenameAPK.APK_rename: ', e)
        logging.info('some error occurred in RenameAPK.APK_rename: ', e)
        pass
