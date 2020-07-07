#-- coding:utf-8 --
import os
import re
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./log/findintent_log.log',
                    filemode='w')

intents = []

action_pre=['VIEW', 'INSTALL_PACKAGE', 'CONNECTION_CHANGE', 'ACTION_SHUTDOWN', 'NETWORK_IDS_CHANGED', 'DOCK_EVENT', 'ANSWER', 'CONNECTION_STATE_CHANGED', 'NEW_VIDEO', 'SET_WALLPAPER', 'SENDTO', 'DISCOVERY_FINISHED', 'BOND_STATE_CHANGED', 'MEDIA_BAD_REMOVAL', 'APPLICATION_PREFERENCES', 'BATTERY_OKAY', 'PACKAGE_REPLACED', 'ACL_DISCONNECTED', 'STATE_CHANGE', 'TIME_TICK', 'ASSIST', 'MEDIA_UNMOUNTED', 'MEDIA_SHARED', 'APP_ERROR', 'SCAN_RESULTS', 'INPUT_METHOD_SETTINGS', 'SCREEN_ON', 'SHOW_ALARMS', 'SEARCH', 'INPUT_METHOD_CHANGED', 'AIRPLANE_MODE', 'PEERS_CHANGED', 'LOCATION_SOURCE_SETTINGS', 'MEDIA_REMOVED', 'MANAGED_PROFILE_ADDED', 'WALLPAPER_CHANGED', 'MAIN', 'QUERY_KEYBOARD_LAYOUTS', 'VENDOR_SPECIFIC_HEADSET_EVENT', 'UID_REMOVED', 'MY_PACKAGE_UNSUSPENDED', 'CONNECTION_STATE_CHANGE', 'MANAGED_PROFILE_AVAILABLE', 'DEVICE_ADMIN_ENABLED', 'RSSI_CHANGED', 'GTALK_DISCONNECTED', 'DEVICE_SELECTED', 'PROVIDER_CHANGED', 'PACKAGE_REMOVED', 'FACTORY_TEST', 'TIMEZONE_CHANGED', 'VIBRATE_SETTING_CHANGED', 'PROXY_CHANGE', 'SYSTEM_TUTORIAL', 'WIFI_SETTINGS', 'INSERT', 'ACTION_POWER_DISCONNECTED', 'BLUETOOTH_SETTINGS', 'DEFAULT', 'NEW_VOICEMAIL', 'DISPLAY_SETTINGS', 'MANAGE_PACKAGE_STORAGE', 'PACKAGE_CHANGED', 'MEDIA_SCANNER_STARTED', 'OPEN_AUDIO_EFFECT_CONTROL_SESSION', 'MEDIA_SCANNER_SCAN_FILE', 'USER_INITIALIZE', 'INTERNAL_STORAGE_SETTINGS', 'DOCUMENTS_PROVIDER', 'VOICE_COMMAND', 'QUICK_CLOCK', 'CHOOSER', 'CREATE_REMINDER', 'INSTALL_FAILURE', 'GTALK_SERVICE_CONNECTED', 'DEVICE_STORAGE_OK', 'CREATE_NOTE', 'SHOW_APP_INFO', 'BATTERY_LOW', 'PACKAGES_UNSUSPENDED', 'AIRPLANE_MODE_CHANGED', 'VIEW_PERMISSION_USAGE', 'POWER_CONNECTED', 'PLAYING_STATE_CHANGED', 'UNINSTALL_PACKAGE', 'APN_SETTINGS', 'WIFI_STATE_CHANGED', 'UMS_CONNECTED', 'THIS_DEVICE_CHANGED', 'DISCOVERY_STARTED', 'CARRIER_SETUP', 'VIEW_LOCUS', 'DISCOVERY_STATE_CHANGE', 'SET_TIMER', 'DATE_SETTINGS', 'POWER_USAGE_SUMMARY', 'MEDIA_UNMOUNTABLE', 'GTALK_CONNECTED', 'DEVICE_ADMIN_DISABLED', 'STILL_IMAGE_CAMERA', 'STATE_CHANGED', 'APPLICATION_RESTRICTIONS_CHANGED', 'MEDIA_NOFS', 'DATE_CHANGED', 'EXTERNAL_APPLICATIONS_AVAILABLE', 'EDIT', 'ACTION_PASSWORD_CHANGED', 'UUID', 'PACKAGES_SUSPENDED', 'CREATE_DOCUMENT', 'BUG_REPORT', 'SEARCH_LONG_PRESS', 'SHUTDOWN', 'ALL_APPS', 'CALL', 'BATTERY_CHANGED', 'RUN', 'MY_PACKAGE_REPLACED', 'PACKAGE_NEEDS_VERIFICATION', 'DEVICE_STORAGE_LOW', 'RESERVE_TAXI_RESERVATION', 'CLOSE_SYSTEM_DIALOGS', 'FOUND', 'MEDIA_PLAY_FROM_SEARCH', 'HEADSET_PLUG', 'WEB_SEARCH', 'CAMERA_BUTTON', 'CONFIGURATION_CHANGED', 'AIRPLANE_MODE_SETTINGS', 'MANAGED_PROFILE_UNAVAILABLE', 'PACKAGE_RESTARTED', 'ACTION_POWER_CONNECTED', 'USER_FOREGROUND', 'OPEN_DOCUMENT', 'SET_ALARM', 'QUICK_VIEW', 'ACTION_PASSWORD_FAILED', 'PACKAGE_DATA_CLEARED', 'MANAGED_PROFILE_REMOVED', 'CONNECTIVITY_CHANGE', 'PASTE', 'USER_BACKGROUND', 'CALL_BUTTON', 'MEMORY_CARD_SETTINGS', 'DEVICE_ADMIN_DISABLE_REQUESTED', 'PROCESS_TEXT', 'TIME_SET', 'WIRELESS_SETTINGS', 'SYNC', 'IMAGE_CAPTURE', 'LOCKED_BOOT_COMPLETED', 'DREAMING_STOPPED', 'VIDEO_CAMERA', 'PICK_ACTIVITY', 'MY_PACKAGE_SUSPENDED', 'ATTACH_DATA', 'USER_PRESENT', 'CREATE_SHORTCUT', 'ACL_DISCONNECT_REQUESTED', 'SEND_MULTIPLE', 'NEW_OUTGOING_CALL', 'PICK', 'DREAMING_STARTED', 'GET_CONTENT', 'PACKAGE_FIRST_LAUNCH', 'DIAL', 'MANAGE_NETWORK_USAGE', 'REBOOT', 'MEDIA_EJECT', 'TIME_CHANGED', 'MANAGED_PROFILE_UNLOCKED', 'PACKAGE_INSTALL', 'LOCALE_SETTINGS', 'MEDIA_BUTTON', 'GET_RESTRICTION_ENTRIES', 'USER_UNLOCKED', 'CLOSE_AUDIO_EFFECT_CONTROL_SESSION', 'LOCALE_CHANGED', 'BACKGROUND_DATA_SETTING_CHANGED', 'PACKAGE_FULLY_REMOVED', 'ACTION_PASSWORD_EXPIRING', 'ACL_CONNECTED', 'AUDIO_STATE_CHANGED', 'MEDIA_SCANNER_FINISHED', 'MEDIA_CHECKING', 'ACTION_PASSWORD_SUCCEEDED', 'SEND', 'INSERT_OR_EDIT', 'PHONE_STATE', 'VIDEO_CAPTURE', 'FETCH_VOICEMAIL', 'LAUNCH', 'TTS_QUEUE_PROCESSING_COMPLETED', 'GTALK_SERVICE_DISCONNECTED', 'SETTINGS', 'EXTERNAL_APPLICATIONS_UNAVAILABLE', 'PACKAGE_ADDED', 'ACTION_SCO_AUDIO_STATE_UPDATED', 'NEW_PICTURE', 'UMS_DISCONNECTED', 'SCAN_MODE_CHANGED', 'TRANSLATE', 'OPEN_DOCUMENT_TREE', 'PACKAGE_VERIFIED', 'CLASS_CHANGED', 'DEFINE', 'DELETE', 'SCREEN_OFF', 'SECURITY_SETTINGS', 'BOOT_COMPLETED', 'MEDIA_MOUNTED', 'LOCAL_NAME_CHANGED', 'POWER_DISCONNECTED', 'NAME_CHANGED', 'TTS_DATA_INSTALLED']

def FindIntent(file):
    global intents,action_pre
    for root, dirs, files in os.walk(str(file + "/sources/")):  # 遍历apk下的所有.java文件
        if files:
            uris=[]
            uris_get=[]
            uris_set=[]
            uris_add=[]
            for file_now in files:
                # print(file_now)
                if file_now[-5:] == ".java":
                    # print(root+"/"+file_now)
                    fr = open(root + "/" + file_now, encoding='utf-8')
                    try:
                        for line in fr.readlines():
                            # print(line)
                            intent_action=re.findall(r'((I|i)ntent[(](.*(action|ACTION).*)[)])',line)
                            intent_add=re.findall(r'addAction[(]"(.*)"[)]',line)
                            intent_get=re.findall(r'getAction[(]"(.*)"[)]',line)
                            intent_set=re.findall(r'setAction[(]"(.*)"[)]',line)

                            if len(intent_action)!=0:
                                if 'R.id' not in intent_action[0][2] and 'setComponent'not in intent_action[0][2] and 'activity' not in intent_action[0][2] \
                                                and 'getParcelableExtra'not in intent_action[0][2] and 'new Intent'not in intent_action[0][2]\
                                                and 'addAction' not in intent_action[0][2] and 'setAction' not in intent_action[0][2] \
                                                and 'getAction' not in intent_action[0][2]:
                                            if ','  in intent_action[0][2]:
                                                # print(c[0][2].split(',')[0].strip('"'))
                                                uris.append(intent_action[0][2].split(',')[0].strip('"').split('.')[-1])
                                            else:
                                                uris.append(intent_action[0][2].strip('"').split('.')[-1])
                                                # print(c[0][2].strip('"'))
                            if len(intent_add)!=0:
                                uris_add.append(intent_add[0].split('.')[-1])
                            if len(intent_get)!=0:
                                uris_get.append(intent_get[0].split('.')[-1])
                            if len(intent_set)!=0:
                                uris_set.append(intent_set[0].split('.')[-1])

                    except Exception as e:
                        print('some error occurred in FindIntent.FindIntent: ', e)
                        pass
            total_list=[]
            # print('tracing')
            for x in uris:
                if x in action_pre:
                    total_list.append(x)
            for x in uris_add:
                if x in action_pre:
                    total_list.append(x)
            for x in uris_set:
                if x in action_pre:
                    total_list.append(x)
            for x in uris_get:
                if x in action_pre:
                    total_list.append(x)
            total_set=set(total_list)
            intents=list(total_set)
            # print(total_set)
            # for x in total_set:
            #     fw.write(x)
            #     fw.write("\n")
            # fw.close()



def printINTENT(file,savepath):
    try:
        res_name = savepath + "/" + file[0:-4] + "_intent.txt"
        fw = open(res_name, 'w')  # 创建相应apk对应的结果文件
        for j in range(len(intents)):
            fw.write(intents[j]+"_action")
            fw.write("\n")
    except Exception as e:
        print('some error occurred in FindIntent.printINTENT: ', e)
        pass

def dofindintent(filepath,savepath):
    try:
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        apks = os.listdir(filepath)
        for file in apks:
            # print(filepath + "/" + file)
            FindIntent(filepath + "/" + file)
            printINTENT(file,savepath)
            print(file,'--> findintent done')

    except Exception as e:
        print('some error occurred in FindIntent.dofindintent: ', e)
        pass
