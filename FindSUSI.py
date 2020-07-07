#! /usr/bin/python3
import xml.etree.ElementTree as ET
import subprocess
import os
import json
import re
import logging
# 批量处理apk文件生成对应的.json

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./log/Find_SUSI.log',
                    filemode='w')

def check_sdk(filepath):
    # Variables
    location_list = {}
    apk_with_sdk = 0
    apk_without_sdk = 0
    # Retrieve all APK files into my_list
    apk_dir = filepath + '/'
    try:
        my_list = os.listdir(apk_dir)

        for apk in my_list:
            apk_path = apk_dir + apk


            aapt_cmd = "aapt dump badging " + apk_path
            proc = subprocess.Popen(aapt_cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()

            sdk_byte = None
            if b'targetSdkVersion:' in out:
                index = out.find('targetSdkVersion:'.encode())
                sdk_byte = out[index + 17:index + 20]
                target = True
            elif b'sdkVersion:' in out:
                index = out.find('sdkVersion:'.encode())
                sdk_byte = out[index + 11:index + 14]
            if sdk_byte:
                sdk = str(sdk_byte, "utf-8")
                result = sdk.replace("'", "")
                apk_with_sdk = apk_with_sdk + 1

                location_list[apk_path] = result
            else:
                apk_without_sdk = apk_without_sdk + 1
    except Exception as e:
        logging.info('some error occurred in FindSUSI.check_sdk:', e)
        pass

    return location_list, apk_with_sdk, apk_without_sdk


def madeXML(filepath,savepath_SUSI_xmls):
    location_list, apk_with_sdk, apk_without_sdk = check_sdk(filepath)
    taint_directory = savepath_SUSI_xmls + '/'
    try:
        for k, v in location_list.items():
            sdk_version = v
            apk_file = k
            apk_filename = apk_file[len(filepath)+1:]
            sdk_file = "android-platforms/android-" + sdk_version + "/android.jar"
            filename = taint_directory + "/" + apk_filename + ".xml"

            if os.path.exists(filename):
                print("xml for "+filename+" already exists")
            else:
                print("[Flowdroid] Start make .xml file for", apk_filename)
                if os.path.isfile(sdk_file):  # Continue if sdk exists
                    os.system("java -jar soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar -a " + apk_file + " -p " + "android-platforms -s SourcesAndSinks.txt -o " + filename)
                    print("[Flowdroid] made xml for", apk_filename, ". Results saved into", filename)

                else:
                    print("[Flowdroid]", "Android SDK platform not found for", apk_filename, ". Required SDK Version",sdk_version)
    except Exception as e:
        logging.info('some error occurred in FindSUSI.madeXML:', e)
        pass

def XML2JSON(path,dir_name,jsonsdir):
    try:
        tree = ET.parse(path+dir_name)
        # 这里有一部分被移动到get_SUSI中去了
        root = tree.getroot()
        Results = root.find("Results")
        # print(Results.tag)
        try:
            results = Results.findall("Result")
        except Exception as e:
            print(path+dir_name+" has no sources and sinks")
            return
        # print(len(results))
        json_name = jsonsdir + '/' + str(dir_name) + ".json"
        f= open(json_name, 'w')
        res_dict = {}
        for result in results:
            Sources = result.find("Sources")
            Sink = result.find("Sink")
            statement_Sink = Sink.find("Statement")
            try:
                sin = str(statement_Sink.text)
            except:
                sin = Sink.attrib["Statement"]
            sin=re.findall(r'[<].*[>]',sin)[0]
            sources = Sources.findall("Source")
            source_list = []
            for source in sources:
                statement_Source = source.find("Statement")
                try:
                    sou = str(statement_Source.text)
                except:
                    sou = source.attrib["Statement"]

                if sou not in source_list:
                    source_list.append(sou)

            for i in range(0, len(source_list)):
                source_list[i]=re.findall(r'[<].*[>]',source_list[i])[0]
                res_dict.update(source=source_list[i], sink=sin)
                json_str = json.dumps(res_dict)
                f.write(json_str)
                f.write('\n')
        f.close()
    except Exception as e:
        logging.info('some error occurred in FindSUSI.XML2JSOn:', e)


def dofindSUSI(filepath,savepath_SUSI_xmls,savepath_SUSI_jsons):
    # 创建文件目录
    print('kaishi')
    if not os.path.exists(savepath_SUSI_xmls):
        os.makedirs(savepath_SUSI_xmls)

    if os.path.exists(savepath_SUSI_jsons):
        pass
    else:
        os.system("mkdir " + savepath_SUSI_jsons)

    xmls_path = savepath_SUSI_xmls + '/'  # 对path下的所有xml文件进行处理并生成相应的json文件
    madeXML(filepath,savepath_SUSI_xmls)
    print('jieshu')
    try:
        xmls = os.listdir(xmls_path)
        for xml in xmls:
            print('susi')
            if xml[-4:] == '.xml':
                XML2JSON(xmls_path,xml,savepath_SUSI_jsons)
    except Exception as e:
        print('some error occurred in FindSUSI.dofindSUSI:')
        logging.info('some error occurred in FindSUSI.dofindSUSI:', e)
        pass