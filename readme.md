---

Project_Name	:	安卓APK特征提取集成工具

Author 			:	@xiaoZ @Romanov @cony @gyj @yz

Date   			:	2020.06.30

Desc   			: 	V2.0.0

---

## 文件说明

```
./APK						# 需要分析的APK
./APK_Extract_Result		# 反编译后的APK代码
./APK_Permission_Result		# APK权限信息
./APK_Uri_Result			# APK URI信息
./APK_Intent_Result			# APK Intent信息
./log						# 函数日志
./jadx-1					# 需要使用的jadx工具存放目录
./android-platforms         # 存放安卓平台的 android.jar文件
./APK_SUSI_JSONS            # 存放提取出的source-sink特征
./soot-infoflow-cmd         # 存放flowdroid工具

CollectionFeature.py 		# 主函数
RenameAPK					# 将APK名称中的空格转为下划线
ExtractAPK.py 				# 反编译脚本
FindURI.py 					# 提取反编译结果中的URI
FindIntent.py 				# 提取反编译结果中的Intent
ExtractPermission.py 		# 提取反编译结果中的permission
FindSUSI.py                 # 提取敏感source-sink
```

## 使用说明
1. 将需要的工具放到对应文件夹中

2. 将需要分析的APK放在APK目录下，执行下列命令，则结果会存储在上述指定目录中
    ```
    python3 CollectionFeature.py 
    ```