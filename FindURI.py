#-- coding:utf-8 --
import os
import re
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='./log/finduri_log.log',
                    filemode='w')

uris_all=['CalendarContract.CalendarSyncColumns', 'SyncStateContract.Columns', 'MediaStore.Files.FileColumns', 'SyncStateContract.Helpers', 'Telephony.ServiceStateTable', 'Browser', 'Telephony', 'ContactsContract.Contacts', 'Contacts.Intents.Insert', 'MediaStore.MediaColumns', 'SyncStateContract.Constants', 'Telephony.Mms.Part', 'MediaStore.Audio', 'CalendarContract.ExtendedProperties', 'CalendarContract.EventsEntity', 'ContactsContract.CommonDataKinds.SipAddress', 'MediaStore.Audio.Radio', 'ContactsContract.DisplayNameSources', 'ContactsContract.ContactNameColumns', 'CalendarContract', 'Telephony.MmsSms', 'ContactsContract.PinnedPositions', 'Contacts.Organizations', 'ContactsContract.PhoneLookupColumns', 'ContactsContract.PresenceColumns', 'BaseColumns', 'MediaStore.Audio.GenresColumns', 'FontsContract.FontInfo', 'MediaStore.Audio.Artists.Albums', 'CallLog.Calls', 'ContactsContract.FullNameStyle', 'Telephony.ThreadsColumns', 'ContactsContract.CommonDataKinds.Email', 'Settings.SettingNotFoundException', 'ContactsContract.CommonDataKinds.Organization', 'Telephony.Mms', 'ContactsContract.CommonDataKinds.Im', 'MediaStore.Audio.ArtistColumns', 'ContactsContract.StatusColumns', 'MediaStore.Audio.Genres.Members', 'ContactsContract.Intents.Insert', 'SettingsSlicesContract', 'ContactsContract.DataColumnsWithJoins', 'CalendarContract.ExtendedPropertiesColumns', 'ContactsContract.CommonDataKinds.Nickname', 'MediaStore.Audio.Albums', 'CalendarContract.Calendars', 'ContactsContract.Presence', 'Telephony.Sms.Outbox', 'CalendarContract.ColorsColumns', 'Contacts.ExtensionsColumns', 'ContactsContract.CommonDataKinds.Event', 'Contacts.Phones', 'Telephony.Mms.Addr', 'ContactsContract.CommonDataKinds.BaseTypes', 'Contacts.People.ContactMethods', 'MediaStore.Video.Media', 'Telephony.Sms.Conversations', 'ContactsContract.DisplayPhoto', 'FontsContract.FontRequestCallback', 'Contacts.Groups', 'ContactsContract.DataUsageFeedback', 'MediaStore', 'ContactsContract', 'ContactsContract.RawContacts', 'Settings.Global', 'ContactsContract.Contacts.Photo', 'SyncStateContract', 'ContactsContract.DataUsageStatColumns', 'ContactsContract.BaseSyncColumns', 'Contacts.People.Phones', 'Contacts.Intents.UI', 'Telephony.Sms', 'ContactsContract.ContactStatusColumns', 'MediaStore.Video.VideoColumns', 'MediaStore.Audio.Artists', 'VoicemailContract.Voicemails', 'Contacts', 'Telephony.Sms.Sent', 'Telephony.Mms.Inbox', 'Contacts.PresenceColumns', 'Telephony.Sms.Intents', 'BlockedNumberContract', 'FontsContract.FontFamilyResult', 'ContactsContract.ContactOptionsColumns', 'CalendarContract.Instances', 'ContactsContract.GroupsColumns', 'FontsContract.Columns', 'Contacts.People.Extensions', 'BlockedNumberContract.BlockedNumbers', 'ContactsContract.CommonDataKinds.Photo', 'ContactsContract.ProviderStatus', 'CalendarContract.SyncColumns', 'ContactsContract.Intents', 'ContactsContract.CommonDataKinds', 'ContactsContract.Contacts.AggregationSuggestions', 'MediaStore.Images.Thumbnails', 'MediaStore.Audio.PlaylistsColumns', 'ContactsContract.CommonDataKinds.Identity', 'Telephony.Mms.Intents', 'Contacts.Settings', 'CalendarContract.CalendarEntity', 'ContactsContract.SyncColumns', 'Contacts.OrganizationColumns', 'Contacts.PhotosColumns', 'Telephony.Sms.Draft', 'Contacts.Photos', 'ContactsContract.SyncState', 'ContactsContract.PhoneLookup', 'ContactsContract.PhoneticNameStyle', 'ContactsContract.RawContacts.Entity', 'Telephony.Mms.Draft', 'MediaStore.Audio.AudioColumns', 'ContactsContract.RawContactsColumns', 'SearchRecentSuggestions', 'MediaStore.Video.Thumbnails', 'Telephony.CarrierId', 'Telephony.TextBasedSmsColumns', 'LiveFolders', 'ContactsContract.RawContacts.Data', 'Contacts.SettingsColumns', 'ContactsContract.Groups', 'Telephony.MmsSms.PendingMessages', 'CalendarContract.Colors', 'Contacts.GroupMembership', 'ContactsContract.Directory', 'ContactsContract.RawContacts.DisplayPhoto', 'CalendarContract.EventsColumns', 'DocumentsContract.Path', 'FontRequest', 'MediaStore.Downloads', 'ContactsContract.ProfileSyncState', 'Settings.Panel', 'Contacts.People', 'Settings.System', 'MediaStore.DownloadColumns', 'ContactsContract.DeletedContacts', 'CallLog', 'DocumentsContract.Document', 'DocumentsContract.Root', 'UserDictionary.Words', 'OpenableColumns', 'ContactsContract.SearchSnippets', 'MediaStore.Audio.Playlists.Members', 'ContactsContract.CommonDataKinds.Callable', 'DocumentsContract', 'ContactsContract.Data', 'Telephony.Mms.Outbox', 'CalendarContract.Attendees', 'CalendarContract.Events', 'ContactsContract.Contacts.Data', 'CalendarContract.CalendarAlertsColumns', 'ContactsContract.CommonDataKinds.Note', 'MediaStore.Video', 'ContactsContract.Contacts.AggregationSuggestions.Builder', 'DocumentsProvider', 'ContactsContract.CommonDataKinds.Website', 'ContactsContract.DeletedContactsColumns', 'VoicemailContract.Status', 'Telephony.Mms.Sent', 'AlarmClock', 'ContactsContract.RawContactsEntity', 'Telephony.Mms.Rate', 'CalendarContract.CalendarCacheColumns', 'ContactsContract.CommonDataKinds.Relation', 'UserDictionary', 'MediaStore.Images.ImageColumns', 'Telephony.CanonicalAddressesColumns', 'MediaStore.Audio.Playlists', 'MediaStore.Audio.Genres', 'ContactsContract.DataColumns', 'ContactsContract.CommonDataKinds.CommonColumns', 'ContactsContract.CommonDataKinds.Contactables', 'ContactsContract.SettingsColumns', 'CalendarContract.CalendarColumns', 'ContactsContract.CommonDataKinds.StructuredPostal', 'Settings', 'Settings.Secure', 'Contacts.Extensions', 'Contacts.PhonesColumns', 'Contacts.PeopleColumns', 'Contacts.ContactMethodsColumns', 'FontsContract', 'ContactsContract.ContactsColumns', 'CalendarContract.CalendarCache', 'MediaStore.Images', 'MediaStore.Audio.Media', 'VoicemailContract', 'ContactsContract.QuickContact', 'CalendarContract.SyncState', 'ContactsContract.Settings', 'MediaStore.Audio.AlbumColumns', 'MediaStore.Files', 'CalendarContract.RemindersColumns', 'CalendarContract.Reminders', 'Telephony.Carriers', 'Telephony.Threads', 'CalendarContract.AttendeesColumns', 'ContactsContract.StatusUpdates', 'CalendarContract.EventDaysColumns', 'ContactsContract.CommonDataKinds.GroupMembership', 'ContactsContract.CommonDataKinds.Phone', 'MediaStore.Images.Media', 'CalendarContract.EventDays', 'ContactsContract.CommonDataKinds.StructuredName', 'Contacts.GroupsColumns', 'ContactsContract.Contacts.Entity', 'Contacts.Intents', 'ContactsContract.Profile', 'CalendarContract.CalendarAlerts', 'ContactsContract.AggregationExceptions', 'Telephony.BaseMmsColumns', 'Contacts.ContactMethods', 'Telephony.Sms.Inbox', 'Settings.NameValueTable']

uris = []
def finduri(file):
    global uris
    for root, dirs, files in os.walk(str(file + "/sources/")):  # 遍历apk下的所有.java文件
        if files:
            for file_now in files:
                # print(file_now)
                if file_now[-5:] == ".java":
                    # print(root+"/"+file_now)
                    fr = open(root + "/" + file_now, encoding='utf-8')
                    try:
                        for line in fr.readlines():
                            if ".CONTENT_URI" in line or "_CONTENT_URI" in line :
                                # 正则表达式部分
                                #a = re.findall(r'\("content://.*?"\)', line)
                                b = re.findall(r'[A-Z][0-9a-zA-Z.]*[_|.]CONTENT_URI', line)
                                # url = re.findall(r'".*[http|ftp|https]://.*"',line)
                                # if url:
                                #     print(url[0])
                                # for i in range(len(a)):
                                #     if a[i] not in uris:
                                #         uris.append(a[i])
                                #         #print(a[i])
                                for i in range(len(b)):
                                    b[i]=b[i].strip('.CONTENT_URI')
                                    b[i] = b[i].strip('.EXTERNAL_CONTENT_URI')
                                    b[i] = b[i].strip('.INTERNAL_CONTENT_URI')
                                    if b[i] in uris_all:
                                        uris.append(b[i])
                    except Exception as e:
                        print('some error occurred in FindURI.finduri: ', e)
                        logging.info('some error occurred in FindURI.finduri: ', e)
                        pass

def printURI(file,savepath):
    try:
        res_name = savepath + "/" + file[0:-4] + "_uri.txt"
        fw = open(res_name, 'w')  # 创建相应apk对应的结果文件
        global uris
        uris = list(set(uris))
        for j in range(len(uris)):
            fw.write(uris[j])
            fw.write("\n")
    except Exception as e:
        print('some error occurred in FindURI.printURI: ', e)
        logging.info('some error occurred in FindURI.printURI: ', e)
        pass

def dofinduri(filepath,savepath):
    try:
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        apks = os.listdir(filepath)
        for file in apks:
            global uris
            uris = []
            # print(filepath + "/" + file)
            finduri(filepath + "/" + file)
            printURI(file,savepath)
            print(file,'--> finduri done')

    except Exception as e:
        print('some error occurred in FindURI.dofinduri: ', e)
        logging.info('some error occurred in FindURI.dofinduri: ', e)
        pass
