# coding=utf-8
'''
解析manifest.xml文件，将其中调用的权限读取出来
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
'''
import logging
import xml.sax
import os

permission_all=['ACCEPT_HANDOVER','ACCESS_BACKGROUND_LOCATION','ACCESS_CALL_AUDIO','ACCESS_CHECKIN_PROPERTIES','ACCESS_COARSE_LOCATION','ACCESS_FINE_LOCATION','ACCESS_LOCATION_EXTRA_COMMANDS','ACCESS_MEDIA_LOCATION','ACCESS_NETWORK_STATE','ACCESS_NOTIFICATION_POLICY','ACCESS_WIFI_STATE','ACCOUNT_MANAGER','ACTIVITY_RECOGNITION','ADD_VOICEMAIL','ANSWER_PHONE_CALLS','BATTERY_STATS','BIND_ACCESSIBILITY_SERVICE','BIND_APPWIDGET','BIND_AUTOFILL_SERVICE','BIND_CALL_REDIRECTION_SERVICE','BIND_CARRIER_MESSAGING_CLIENT_SERVICE','BIND_CARRIER_MESSAGING_SERVICE','BIND_CARRIER_SERVICES','BIND_CHOOSER_TARGET_SERVICE','BIND_CONDITION_PROVIDER_SERVICE','BIND_CONTROLS','BIND_DEVICE_ADMIN','BIND_DREAM_SERVICE','BIND_INCALL_SERVICE','BIND_INPUT_METHOD','BIND_MIDI_DEVICE_SERVICE','BIND_NFC_SERVICE','BIND_NOTIFICATION_LISTENER_SERVICE','BIND_PRINT_SERVICE','BIND_QUICK_ACCESS_WALLET_SERVICE','BIND_QUICK_SETTINGS_TILE','BIND_REMOTEVIEWS','BIND_SCREENING_SERVICE','BIND_TELECOM_CONNECTION_SERVICE','BIND_TEXT_SERVICE','BIND_TV_INPUT','BIND_VISUAL_VOICEMAIL_SERVICE','BIND_VOICE_INTERACTION','BIND_VPN_SERVICE','BIND_VR_LISTENER_SERVICE','BIND_WALLPAPER','BLUETOOTH','BLUETOOTH_ADMIN','BLUETOOTH_PRIVILEGED','BODY_SENSORS','BROADCAST_PACKAGE_REMOVED','BROADCAST_SMS','BROADCAST_STICKY','BROADCAST_WAP_PUSH','CALL_COMPANION_APP','CALL_PHONE','CALL_PRIVILEGED','CAMERA','CAPTURE_AUDIO_OUTPUT','CHANGE_COMPONENT_ENABLED_STATE','CHANGE_CONFIGURATION','CHANGE_NETWORK_STATE','CHANGE_WIFI_MULTICAST_STATE','CHANGE_WIFI_STATE','CLEAR_APP_CACHE','CONTROL_LOCATION_UPDATES','DELETE_CACHE_FILES','DELETE_PACKAGES','DIAGNOSTIC','DISABLE_KEYGUARD','DUMP','EXPAND_STATUS_BAR','FACTORY_TEST','FOREGROUND_SERVICE','GET_ACCOUNTS','GET_ACCOUNTS_PRIVILEGED','GET_PACKAGE_SIZE','GET_TASKS','GLOBAL_SEARCH','INSTALL_LOCATION_PROVIDER','INSTALL_PACKAGES','INSTALL_SHORTCUT','INSTANT_APP_FOREGROUND_SERVICE','INTERACT_ACROSS_PROFILES','INTERNET','KILL_BACKGROUND_PROCESSES','LOADER_USAGE_STATS','LOCATION_HARDWARE','MANAGE_DOCUMENTS','MANAGE_EXTERNAL_STORAGE','MANAGE_OWN_CALLS','MASTER_CLEAR','MEDIA_CONTENT_CONTROL','MODIFY_AUDIO_SETTINGS','MODIFY_PHONE_STATE','MOUNT_FORMAT_FILESYSTEMS','MOUNT_UNMOUNT_FILESYSTEMS','NFC','NFC_PREFERRED_PAYMENT_INFO','NFC_TRANSACTION_EVENT','PACKAGE_USAGE_STATS','PERSISTENT_ACTIVITY','PROCESS_OUTGOING_CALLS','QUERY_ALL_PACKAGES','READ_CALENDAR','READ_CALL_LOG','READ_CONTACTS','READ_EXTERNAL_STORAGE','READ_INPUT_STATE','READ_LOGS','READ_PHONE_NUMBERS','READ_PHONE_STATE','READ_PRECISE_PHONE_STATE','READ_SMS','READ_SYNC_SETTINGS','READ_SYNC_STATS','READ_VOICEMAIL','REBOOT','RECEIVE_BOOT_COMPLETED','RECEIVE_MMS','RECEIVE_SMS','RECEIVE_WAP_PUSH','RECORD_AUDIO','REORDER_TASKS','REQUEST_COMPANION_RUN_IN_BACKGROUND','REQUEST_COMPANION_USE_DATA_IN_BACKGROUND','REQUEST_DELETE_PACKAGES','REQUEST_IGNORE_BATTERY_OPTIMIZATIONS','REQUEST_INSTALL_PACKAGES','REQUEST_PASSWORD_COMPLEXITY','RESTART_PACKAGES','SEND_RESPOND_VIA_MESSAGE','SEND_SMS','SET_ALARM','SET_ALWAYS_FINISH','SET_ANIMATION_SCALE','SET_DEBUG_APP','SET_PREFERRED_APPLICATIONS','SET_PROCESS_LIMIT','SET_TIME','SET_TIME_ZONE','SET_WALLPAPER','SET_WALLPAPER_HINTS','SIGNAL_PERSISTENT_PROCESSES','SMS_FINANCIAL_TRANSACTIONS','START_VIEW_PERMISSION_USAGE','STATUS_BAR','SYSTEM_ALERT_WINDOW','TRANSMIT_IR','UNINSTALL_SHORTCUT','UPDATE_DEVICE_STATS','USE_BIOMETRIC','USE_FINGERPRINT','USE_FULL_SCREEN_INTENT','USE_SIP','VIBRATE','WAKE_LOCK','WRITE_APN_SETTINGS','WRITE_CALENDAR','WRITE_CALL_LOG','WRITE_CONTACTS','WRITE_EXTERNAL_STORAGE','WRITE_GSERVICES','WRITE_SECURE_SETTINGS','WRITE_SETTINGS','WRITE_SYNC_SETTINGS','WRITE_VOICEMAIL']

permissionlist=[]

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./log/extractpermisson_log.log',
                    filemode='w')


class manifestHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.currentdata=''
        self.permission=''

    def startElement(self, name, attrs):
        self.currentdata=name
        if self.currentdata=='uses-permission':
            permission=attrs['android:name']
            # print(permission)
            self.permission=permission

    def endElement(self, name):
        if self.currentdata=='uses-permission':
            self.permission=self.permission.strip('android.permission.')
            if self.permission in permission_all:
                permissionlist.append(self.permission)


def getxml(file):
    try:
        fs=os.listdir(file)
        for f in fs:
            if f=='AndroidManifest.xml':
                return os.path.join(file,f)
        return None

    except Exception as e:
        print('some error occurred in extractPermission.getxml: ', e)
        logging.info('some error occurred in extractPermission.getxml: ', e)
        pass
    


# path 为存储xml文件路径，savepath为保存文件的路径
def doextractpermission(filepath,savepath):
        apks = os.listdir(filepath)
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        for path in apks:
            try:
                file_name = path
                path = filepath + "/" + path
                parser=xml.sax.make_parser()
                parser.setFeature(xml.sax.handler.feature_namespaces, 0)
                Handler = manifestHandler()
                parser.setContentHandler(Handler)
                # print(parser)
                files=os.listdir(path)
                for file in files:
                    # print('正在处理%s'%file)
                    savefile=os.path.join(savepath,file_name)+'_permission.txt'
                    file=os.path.join(path,file)
                    xmlfile=getxml(file)
                    if xmlfile==None:
                        #logging.info('%s下无 AndroidManifest.xml'%file)
                        continue
                    # print(xmlfile)
                    parser.parse(xmlfile)
                    # print(parser)
                    with open(savefile,'w') as f:
                        global permissionlist
                        permissionlist=list(set(permissionlist))
                        for permission in permissionlist:
                            f.write(permission+'_permission'+'\n')
                print(file_name,'--> extractPermission done')
    
            except Exception as e:
                print('some error occurred in extractPermission.doextractPermission: '+ str(e))
                logging.info('some error occurred in extractPermission.doextractPermission: '+str(e))
                pass
