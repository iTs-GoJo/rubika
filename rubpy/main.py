from rubpy import Client, handlers,methods, Message, models 
from asyncio import run
import json
import os
import time
import datetime
import requests
import random
import aiofiles

# """
# rubpy==6.4.6
# requests
# rubpy
# colorama
# aiofile
# """

def CheckType(message,m):
    if m == 0:
        #text
        if 'text' in message['message']:
            return [True,'متن']
    elif m == 1:
        if 'file_inline' in message['message']:
            if (message['message']['file_inline']['type'] == 'Gif'):
                return [True,'گیف']
    elif m == 2:
        if 'file_inline' in message['message']:
            if (message['message']['file_inline']['type'] == 'Voice'):
                return [True,'ویس']
    elif m == 3:
        if 'file_inline' in message['message']:
            if (message['message']['file_inline']['type'] == 'Music'):
                return [True,'اهنگ']
    elif m == 4:
        if 'file_inline' in message['message']:
            if (message['message']['file_inline']['type'] == 'Image'):
                return [True,'عکس']
    elif m == 5:
        if 'file_inline' in message['message']:
            if (message['message']['file_inline']['type'] == 'Video'):
                return [True,'ویدیو']
    elif m == 6:
        if 'file_inline' in message['message']:
            if (message['message']['file_inline']['type'] == 'File'):
                return [True,'فایل']
    elif m == 7:
        if 'text' in message['message']:
            text = message['message']['text']
            strs = ["@"]
            for str in strs:
                if str in text:
                    return [True,'ایدی']
    elif m == 8:
        if 'text' in message['message']:
            text = message['message']['text']
            strs = ["https://","http://",".com",".ir"]
            for str in strs:
                if str in text:
                    return [True,'لینک']
    elif m == 9:
        if 'forwarded_from' in message['message']:
            return [True,'فوروارد']
        
    return [False]

def FormDate(result):
    
    result = result['result']
    date_jalali = result['date']['jalali']
    date_miladi = result['date']['miladi']
    date_ghamari = result['date']['ghamari']

    season_number = result['season']['number']
    season_name = result['season']['name']

    time_hour = result['time']['hour']
    time_minute = result['time']['minute']
    time_second = result['time']['second']

    day_number = result['day']['number']
    day_name_week = result['day']['name_week']
    day_name_month = result['day']['name_month']

    month_number = result['month']['number']
    month_name_past = result['month']['name_past']
    month_name = result['month']['name']

    year_number = result['year']['number']
    year_name = result['year']['name']
    year_name_past = result['year']['name_past']
    year_remaining = result['year']['remaining']

    occasion_miladi = result['occasion']['miladi']
    occasion_jalali = result['occasion']['jalali']
    occasion_ghamari = result['occasion']['ghamari']

    TEXT = "| #ᗪᗩTᗴ\n\n"
    TEXT += "𝗬𝗲𝗮𝗿 𝗷𝗮𝗹𝗮𝗹𝗶 » "+date_jalali+" [ "+year_name_past+" ]\n"
    TEXT += "𝗬𝗲𝗮𝗿 𝗺𝗶𝗹𝗮𝗱𝗶 » "+date_miladi+"\n"
    TEXT += "𝗬𝗲𝗮𝗿 𝗴𝗵𝗮𝗺𝗮𝗿𝗶 » "+date_ghamari+"\n"
    TEXT += "𝗿𝗲𝗺𝗮𝗶𝗻𝗶𝗻𝗴 » [ "+year_remaining+" روز باقی مانده "+" ]\n"
    TEXT += "𝗦𝗲𝗮𝘀𝗼𝗻 » "+season_name+"\n"
    TEXT += "𝗠𝗼𝗻𝘁𝗵 » "+month_name+" [ "+month_name_past+" ] \n"
    TEXT += "𝗗𝗮𝘆 » "+day_name_week+" [ "+day_number+" ] \n"
    TEXT += "𝗧𝗶𝗺𝗲 » "+time_hour+" : "+time_minute+" : "+time_second+"\n"
    TEXT += "𝗢𝗰𝗰𝗮𝘀𝗶𝗼𝗻 » \n\n"+occasion_jalali+"\n"+occasion_miladi+"\n"+occasion_ghamari
    
    return TEXT
    
def UPFILES(json,file_name,FILE):
    with open(file_name, "w") as outfile:
        json.dump(FILE, outfile)

def Title(step1,step2 = ''):
    step1 = str(step1)
    step2 = str(step2)
    ok =  "◄"+" "+step1+' '+step2+"\n\n"
    return ok

def Mini(step,method = True):
    step = str(step)
    if method:
        ok = "•"+" "+step+"\n"
    else:
        ok = "❖"+" "+step+"\n"
    return ok
async def Set_group_default_access(cient,object_guid,access,action = bool):
    DefaultAccess = await cient.get_group_default_access(object_guid)
    DefaultAccess = DefaultAccess['access_list']
    if action:
        DefaultAccess.append(access)
    else:
        DefaultAccess.remove(access)
    await cient.set_group_default_access(object_guid,DefaultAccess)
async def ExtraInfo(client,INFOS,object_guid,message_id,method,ltSet,TimeMessages):
    
    step = PorotectMSS(TimeMessages,object_guid)
    if not step:
        return False
    
    key = 1
    if method == 'bye':
        num = 'خدافظی'
    elif method == 'welcome':
        num = 'خوشامدگویی'
    else:
        num = method
    if num in ltSet:
        key = ltSet[num]
    keys = list(INFOS[object_guid]['setting'])
    step1 = int(keys[0])
    step2 = int(keys[key])
    if step1 == 1 and step2 == 1:
        mess = INFOS[object_guid][method]
        return await client.send_message(object_guid,mess,message_id)
def CheckSetting(lSet,INFOS,object_guid,method):
    key = lSet[method]
    keys = list(INFOS[object_guid]['setting'])
    step1 = int(keys[0])
    step2 = int(keys[key])
    if step1 == 1 and step2 == 1:
        return True
    return False
async def GetInfoByMessageId(client,object_guid,reply_message_id):
    try:
        messages_info = await client.get_messages_by_ID(object_guid,reply_message_id)
        return messages_info['messages'][0]
    except:
        return False
def GetReplyGuid(reply_message):
    reply_message_guid = False
    if 'author_object_guid' in reply_message:
        reply_message_guid = reply_message['author_object_guid']
    elif 'event_data' in reply_message:
        if 'peer_objects' in reply_message['event_data']:
            reply_message_guid = reply_message['event_data']['peer_objects'][0]['object_guid']
        else:
            reply_message_guid= reply_message['event_data']['performer_object']['object_guid']
    return reply_message_guid
def Font_shec(text):
    NewText = ''
    TXTP = "ض-ص-ث-ق-ف-غ-ع-ه-خ-ح-ج-چ-ش-س-ی-ب-ل-ا-ت-ن-م-ک-گ-ظ-ط-ژ-ز-ر-ذ-د-پ-و"+"ـچ_ـو_ـپ_ـد_ـذ_ـر_ـز_ـژ_ـط_ـظ_ـگ_ـک_ـم_ـن_ـت_ـا_ـل_ـب_ـی_ـس_ـش_ـج_ـح_ـخ_ـه_ـع_ـغ_ـف_ـق_ث_ـص_ـض_چـ_پـ_طـ_ظـ_گـ_کـ_مـ_نـ_تـ_لـ_بـ_یـ_سـ_شـ_جـ_حـ_خـ_هـ_عـ_غـ_فـ_قـ_ثـ_صـ_ضـ_"
    for x in text:
        if TXTP.find(x) >= 0:
            NewText += x+"‍‌"
        else:
            NewText += x
    return NewText
def Font_kesh(text):
    NewText = ''
    TXTP = "ض-ص-ث-ق-ف-غ-ع-ه-خ-ح-ج-چ-ش-س-ی-ب-ل-ا-ت-ن-م-ک-گ-ظ-ط-ژ-ز-ر-ذ-د-پ-و"+"ـچ_ـو_ـپ_ـد_ـذ_ـر_ـز_ـژ_ـط_ـظ_ـگ_ـک_ـم_ـن_ـت_ـا_ـل_ـب_ـی_ـس_ـش_ـج_ـح_ـخ_ـه_ـع_ـغ_ـف_ـق_ث_ـص_ـض_چـ_پـ_طـ_ظـ_گـ_کـ_مـ_نـ_تـ_لـ_بـ_یـ_سـ_شـ_جـ_حـ_خـ_هـ_عـ_غـ_فـ_قـ_ثـ_صـ_ضـ_"
    for x in text:
        if TXTP.find(x) >= 0:
            if x == 'ا' or x == 'ا' or x == 'و' or x == 'د' or x == 'ذ' or x == 'ر' or x == 'ز' or x == 'ژ':
                NewText += x
                continue
            m = "ـ"
            c = ''
            rand = random.randint(0,4)
            if rand == 1:
                c = m
            elif rand == 2:
                c = m+m
            elif rand == 3:
                c = m+m+m
            elif rand == 4:
                c = m+m+m+m
            NewText += x+c
        else:
            NewText += x
    return NewText
def Font_lash(text):
    NewText = ''
    TXTP = "ض-ص-ث-ق-ف-غ-ع-ه-خ-ح-ج-چ-ش-س-ی-ب-ل-ا-ت-ن-م-ک-گ-ظ-ط-ژ-ز-ر-ذ-د-پ-و"+"ـچ_ـو_ـپ_ـد_ـذ_ـر_ـز_ـژ_ـط_ـظ_ـگ_ـک_ـم_ـن_ـت_ـا_ـل_ـب_ـی_ـس_ـش_ـج_ـح_ـخ_ـه_ـع_ـغ_ـف_ـق_ث_ـص_ـض_چـ_پـ_طـ_ظـ_گـ_کـ_مـ_نـ_تـ_لـ_بـ_یـ_سـ_شـ_جـ_حـ_خـ_هـ_عـ_غـ_فـ_قـ_ثـ_صـ_ضـ_"
    for x in text:
        if TXTP.find(x) >= 0:
            Lash = ['َ','ٕ','ً','ّ','ٌ','ٍ','ٔ','ٰ','ٓ','َ','َ','َ','ٍ','ٖ','ِ','ِ','ِ','ُ']
            mx = len(Lash)-1
            r1 = random.randint(0,mx)
            r2 = random.randint(0,mx)
            r3 = random.randint(0,mx)
            fn1 = Lash[r1]
            fn2 = Lash[r2]
            fn2 = Lash[r3]
            NewText += x+fn1+fn2+fn2
        else:
            NewText += x
    return NewText
def PorotectMSS(TimeMessages,object_guid):
    result = True
    if len(TimeMessages[object_guid]) >= 20:
        now = datetime.datetime.now()
        timestamp = int(time.mktime(now.timetuple())) 
        if timestamp-TimeMessages[object_guid][15] <= 5 or timestamp-TimeMessages[object_guid][10] <= 20 or timestamp-TimeMessages[object_guid][5] <= 30 or timestamp-TimeMessages[object_guid][0] <= 50:
            result = False

    return result

# GUID MALEK
# 09392226837
Coder = 'u0FhGhF089ace325a44718dd5123b7af'

IsUpdated = True

Listlocks = {'متن':0,'گیف':1,'ویس':2,'اهنگ':3,'عکس':4,'فیلم':5,'فایل':6,'ایدی':7,'لینک':8,'فوروارد':9}
Listset = {'ربات':0,'سخنگو':1,'سخنگو پیشفرض':2,'سخنگو شخصی':3,'ضد تبچی':4,'بن':5,'اخطار':6,'خوشامدگویی':7,'خدافظی':8,'اعلان':9}
# Listkeys = {'ربات':0,'جوک':1,'بیو':2,'فال':3,'تاریخ':4,'داستان':5,'فکت':6,'اعتراف':7,'تکست':8,'دانستنی':9,'اینفو':10,'تاس':11,'لینک':12,'ورژن':13,'اینفو':14,'لیست ویژه':15,'لیست ادمین':16,'لیست قفل':17,'عدد شانسی':18,'قوانین':19,'سکه':20,'داشبورد':21,'لیست دستورات':22,'ساعت':23}
# Listkeys = {'ربات':0,'تاریخ':1,'اینفو':2,'تاس':3,'لینک':4,'ورژن':5,'اینفو':6,'لیست ویژه':7,'لیست ادمین':8,'لیست قفل':9,'عدد شانسی':10,'قوانین':11,'سکه':12,'داشبورد':13,'ساعت':14,'لیست دستورات':15,'جوک':16,'چالش':17,'بیو':18,'فکت':19,'اعتراف':20,'دانستنی':21,'داستان':22,'تکست':23,'فال':24,'کرونا':25}
# Listkeys = {'تاریخ':1,'اینفو':2,'تاس':3,'لینک':4,'ورژن':5,'اینفو':6,'لیست ویژه':7,'لیست ادمین':8,'لیست قفل':9,'عدد شانسی':10,'قوانین':11,'سکه':12,'داشبورد':13,'ساعت':14,'لیست دستورات':15,'جوک':16,'چالش':17,'بیو':18,'فکت':19,'اعتراف':20,'دانستنی':21,'داستان':22,'تکست':23,'فال':24,'لیست':26,'کشیده':27,'لش':28,'شکسته':29}
Listkeys = {'تاریخ':1,'اینفو':2,'تاس':3,'لینک':4,'ورژن':5,'اینفو':6,'لیست ویژه':7,'لیست ادمین':8,'لیست قفل':9,'عدد شانسی':10,'قوانین':11,'سکه':12,'داشبورد':13,'ساعت':14,'لیست دستورات':15,'جوک':16,'چالش':17,'بیو':18,'فکت':19,'اعتراف':20,'دانستنی':21,'داستان':22,'تکست':23,'فال':24,'لیست':26,'کشیده':27,'لش':28,'شکسته':29,'گوید':30,'مقام':31,'اصل':32,'لقب':33,'تعداد اخطار':34,'تعداد پیام':35,'بنر':36,'خدافظی':37,'خوشامدگویی':38}

NEWVR = '3.3.4'

LSMessage = {}
ARMessages = {}
TimeMessages = {}

OLDVR = {'version':NEWVR}
File_version = 'version.json'
File_version_is = (os.path.isfile(File_version))
if not(File_version_is):
    with open(File_version, "w") as outfile:
        json.dump(OLDVR, outfile)
else:
    with open(File_version, 'r') as openfile:
        # Reading from json file
        OLDVR = json.load(openfile)
        
INFOS = {}
File_infos = 'Infos.json'
File_infos_is = (os.path.isfile(File_infos))
if not(File_infos_is):
    with open(File_infos, "w") as outfile:
        json.dump(INFOS, outfile)
        # exit()
else:
    with open(File_infos, 'r') as openfile:
        # Reading from json file
        INFOS = json.load(openfile)

SPEAK = {}
file_speak = 'Speak.json'
file_speak_is = (os.path.isfile(file_speak))
if not(file_speak_is):
    with open(file_speak, "w") as outfile:
        json.dump(SPEAK, outfile)
else:
    with open(file_speak, 'r') as openfile:
        # Reading from json file
        SPEAK = json.load(openfile)
try:
    dataSpeak = requests.get(url="https://l8pstudio.ir/SpeakD.json")
    SPEAKD = dataSpeak.json()
except:
    SPEAKD = {}
file_speakd = 'SpeakD.json'
file_speakd_is = (os.path.isfile(file_speakd))
if not(file_speakd_is):
    with open(file_speakd, "w") as outfile:
        json.dump(SPEAKD, outfile)
else:
    UPFILES(json,file_speakd,SPEAKD)

USERS = {}
File_users = 'Users.json'
File_users_is = (os.path.isfile(File_users))
if not(File_users_is):
    with open(File_users, "w") as outfile:
        json.dump(USERS, outfile)
else:
    with open(File_users, 'r') as openfile:
        # Reading from json file
        USERS = json.load(openfile)

deleting = []
for object_guid in USERS:
    for user_guid in USERS[object_guid]:
        user = USERS[object_guid][user_guid]
        mes = user[0]
        war = user[1]
        state = mes-war
        if (state <= 0):
            deleting.append(user_guid)

    for user in deleting:
        USERS[object_guid].pop(user)
    deleting = []
    
with open(File_users, "w") as outfile:
    json.dump(USERS, outfile)

OWNER = {}
File_owner = 'owner.json'
File_owner_is = (os.path.isfile(File_owner))
if File_owner_is:
    with open(File_owner, 'r') as openfile:
        # Reading from json file
        OWNER = json.load(openfile)

for group in INFOS:
    LSMessage[group] = [0,1]
    ARMessages[group] = []
    TimeMessages[group] = []

async def main():
    async with Client(session='BotMe') as client:     
        print('Robot is running')
        @client.on(handlers.MessageUpdates)
        async def updates(message: Message):
            global OWNER
            global INFOS
            global USERS
            global SPEAK
            global SPEAKD
            global NEWVR
            global OLDVR
            global File_owner_is
            global IsUpdated
            global LSMessage
            global ARMessages
            global TimeMessages

            if not IsUpdated:
                UPFILES(json,File_infos,INFOS)
                UPFILES(json,File_users,USERS)

            # # make valuables
            object_guid = message.object_guid
            command = ''
            if 'text' in message['message']:
                command = message['message']['text']
                # command = xcommand.lower()
            guid_sender = object_guid
            if 'author_object_guid' in message['message']:
                guid_sender = message['message']['author_object_guid']
            elif 'event_data' in message['message']:
                guid_sender = message['message']['event_data']['performer_object']['object_guid']

            wordCount = command.count(" ")
            message_id = message.message_id
            is_reply_message = False
            if 'reply_to_message_id' in message['message']:
                is_reply_message = message['message']['reply_to_message_id']
            command = command.replace('آ','ا')
            ERRORTIME = ''
            CanSend = True
            if not File_owner_is and message.type == 'User':
                with open(File_owner, "w") as outfile:
                    now = datetime.datetime.now()
                    timestamp = int(time.mktime(now.timetuple()))
                    OWNER = {guid_sender:{'spire':9999999999999999,'date':timestamp}}
                    json.dump(OWNER, outfile)
                NOTIC = 'you are my owner'
                await client.send_message(guid_sender,NOTIC,message_id)
                File_owner_is = True
                CanSend = False

            # VALIDATE THE GAPS
            if object_guid in INFOS and message.type == 'Group' and CanSend:
                ResultME = False
                IsUpdated = False

                #GET GAP INFO
                HOWNER = INFOS[object_guid]['owner']
                full_admins = INFOS[object_guid]['full_admins']
                admins = INFOS[object_guid]['admins']

                # validate the user
                TIP0 = False
                TIP1 = False
                TIP2 = False
                TIP3 = False
                if guid_sender == Coder:
                    TIP0 = True
                    TIP1 = True
                    TIP2 = True
                    TIP3 = True
                if guid_sender == HOWNER:
                    TIP1 = True
                    TIP2 = True
                    TIP3 = True
                elif guid_sender in full_admins:
                    TIP2 = True
                    TIP3 = True
                elif guid_sender in admins:
                    TIP3 = True

                # is active or not
                if TIP1:
                    if command == 'غیر فعال' or command == 'غیرفعال':
                        if INFOS[object_guid]['state']:
                            ResultME = await client.send_message(object_guid,'ربات غیرفعال شد.',message_id)
                            INFOS[object_guid]['state'] = False
                            UPFILES(json,File_infos,INFOS)
                            return True
                        else:
                            ResultME = await client.send_message(object_guid,'ربات از قبل غیرفعال بود.',message_id)
                            return True
                    elif command == 'فعال':
                        if not INFOS[object_guid]['state']:
                            ResultME = await client.send_message(object_guid,'ربات فعال شد.',message_id)
                            INFOS[object_guid]['state'] = True
                            UPFILES(json,File_infos,INFOS)
                            return True
                        elif INFOS[object_guid]['state']:
                            ResultME = await client.send_message(object_guid,'ربات از قبل فعال بود.',message_id)
                            return True
                
                if not INFOS[object_guid]['state']:
                    return True     
                
                
                # DELETE MESSAGE
                if not TIP2 and CanSend:
                    # check message
                    keys = list(INFOS[object_guid]['locks'])
                    m = 0
                    for x in keys:
                        if (x == '0'):
                            Check = CheckType(message,m)
                            if Check[0]:
                                try:
                                    await client.delete_messages(object_guid,message_id)
                                except:pass
                                key = Listset['بن']
                                keys = list(INFOS[object_guid]['setting'])
                                step = int(keys[key])
                                if step == 1:
                                    count = INFOS[object_guid]['warnning']
                                    if guid_sender not in USERS[object_guid]:
                                        USERS[object_guid][guid_sender] = [0,0,'','']
                                    pscount = USERS[object_guid][guid_sender][1]
                                    pscount += 1
                                    USERS[object_guid][guid_sender][1] = pscount
                                    if pscount >= count:
                                            INFOS[object_guid]['ban'] += 1
                                            try:
                                                result = await client.ban_group_member(object_guid,guid_sender)
                                                key = Listset['خدافظی']
                                                keys = list(INFOS[object_guid]['setting'])
                                                step = int(keys[key])
                                                if step == 1:
                                                    mess = INFOS[object_guid]['bye']
                                                    reply_message_banded_id = result['data']['chat_update']['chat']['last_message']['message_id']
                                                    ResultME = await client.send_message(object_guid,mess,reply_message_banded_id)
                                            except:pass
                                            if pscount == count:
                                                try:
                                                    key = Listset['اخطار']
                                                    keys = list(INFOS[object_guid]['setting'])
                                                    step = int(keys[key])
                                                    if step == 1:
                                                            mess = Check[1]+" ممنوع است."+" 🚫"+'[ اخراج شد ]'+"\n"
                                                            mess += "اخطار"+' [ '+str(pscount)+' ] '+"از"+' [ '+str(count)+' ] '
                                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                                except:pass
                                    else:
                                        try:
                                            key = Listset['اخطار']
                                            keys = list(INFOS[object_guid]['setting'])
                                            step = int(keys[key])
                                            if step == 1:
                                                mess = Check[1]+" ممنوع است."+" ⚠️"+"\n"
                                                mess += "اخطار"+' [ '+str(pscount)+' ] '+"از"+' [ '+str(count)+' ] '
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                        except:pass
                                CanSend = False
                                return True
                            
                        m = m+1    
                
                # EVENT DATA
                if 'event_data' in message['message']:
                    CanSend = False
                    evendata = message['message']['event_data']
                    if evendata['type'] == 'LeaveGroup':
                        INFOS[object_guid]['left'] += 1
                        ResultME = await ExtraInfo(client,INFOS,object_guid,message_id,"bye",Listset,TimeMessages)
                    elif evendata['type'] == 'JoinedGroupByLink':
                        INFOS[object_guid]['join'] += 1
                        ResultME = await ExtraInfo(client,INFOS,object_guid,message_id,"welcome",Listset,TimeMessages)
                    elif evendata['type'] == 'AddedGroupMembers':
                        INFOS[object_guid]['add'] += 1
                        ResultME = await ExtraInfo(client,INFOS,object_guid,message_id,"welcome",Listset,TimeMessages)
                    elif evendata['type'] == 'RemoveGroupMembers':
                        INFOS[object_guid]['ban'] += 1
                        ResultME = await ExtraInfo(client,INFOS,object_guid,message_id,"bye",Listset,TimeMessages)
                    elif evendata['type'] == 'CreateGroupVoiceChat':
                        result = CheckSetting(Listset,INFOS,object_guid,'اعلان')
                        if result:
                            ResultME = await client.send_message(object_guid,'[ '+'#ویس_کال_ایجاد'+' ]',message_id)
                    elif evendata['type'] == 'StopGroupVoiceChat':
                        result = CheckSetting(Listset,INFOS,object_guid,'اعلان')
                        if result:
                            ResultME = await client.send_message(object_guid,'[ '+'#ویس_کال_قطع'+' ]',message_id)
                    elif evendata['type'] == 'TitleUpdate':
                        INFOS[object_guid]['name'] = evendata['title']
                        result = CheckSetting(Listset,INFOS,object_guid,'اعلان')
                        if result:
                            ResultME = await client.send_message(object_guid,'[ '+'#اسم_گروه_اپدیت'+' ]',message_id)
                    elif evendata['type'] == 'PhotoUpdate':
                        result = CheckSetting(Listset,INFOS,object_guid,'اعلان')
                        if result:
                            ResultME = await client.send_message(object_guid,'[ '+'#عکس_گروه_اپدیت'+' ]',message_id)
                    return True
        
                # COMMANDS 
                if CanSend and wordCount < 4:
                    # FOR CODER
                    if TIP0 and CanSend:
                        if command == 'Check':
                            context_message = message
                            if is_reply_message:
                                context_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                            context = str(context_message)
                            ResultME = await client.send_message(Coder,context)
                            ResultME = await client.send_message(object_guid,'پی وی ارسال شد.',message_id)
                            CanSend = False          
                    # FOR OWNER
                    if TIP1 and CanSend:
                        # reply and no reply
                        if is_reply_message:
                            if wordCount == 0:
                                if command == 'ویژه':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid == HOWNER:
                                            mess = '» شما مالک من هستید.'
                                        elif reply_message_guid in full_admins:
                                            mess = '» ایشون ادمین ویژه است.'
                                        elif reply_message_guid:
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            mess = '» کاربر '+first_name+' ادمین ویژه شد. ✅'
                                            result = await client.get_user_info(reply_message_guid)
                                            INFOS[object_guid]['full_admins'][reply_message_guid] = first_name
                                            try:
                                                await client.set_group_admin(object_guid,reply_message_guid,["DeleteGlobalAllMessages"],'SetAdmin')  
                                            except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id) 
                                    CanSend = False
                                elif command == 'برکناری':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid == HOWNER:
                                            mess = '» شما مالک من هستید.'
                                        elif reply_message_guid not in full_admins and reply_message_guid not in admins:
                                            mess = '» مقامی ندارد.'
                                        elif reply_message_guid:
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            mess = '» کاربر '+first_name+' برکنار شد. ✅'
                                            if reply_message_guid in full_admins:
                                                INFOS[object_guid]['full_admins'].pop(reply_message_guid)
                                            if reply_message_guid in admins:
                                                INFOS[object_guid]['admins'].pop(reply_message_guid)
                                            try:
                                                await client.set_group_admin(object_guid,reply_message_guid,[],'UnsetAdmin')
                                            except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                        else:
                            if wordCount == 0:
                                if command == 'لفت':
                                    mess = '» لفت دادم. ✅'
                                    await client.leave_group(object_guid)
                                    ResultME = await client.send_message(guid_sender,mess,message_id)
                                    CanSend = False
                                elif command == 'RESETINFO':
                                    INFOS.pop(object_guid)
                                    USERS.pop(object_guid)
                                    LSMessage.pop(object_guid)
                                    ARMessages.pop(object_guid)
                                    TimeMessages.pop(object_guid)
                                    UPFILES(json,File_infos,INFOS)
                                    UPFILES(json,File_users,USERS)
                                    ResultME = await client.send_message(object_guid,'» تمام اطلاعات ربات پاک شد. ✅',message_id)
                                    return True
                                elif command == 'RESETWORDS':
                                    SPEAK = {}
                                    UPFILES(json,file_speak,SPEAK)
                                    mess = Mini('کلمات سخنگوی شخصی حذف شد. ✅',False)
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    return True
                            elif wordCount == 1:
                                if command == 'ریست ربات':
                                    noti = "🛑 » درصورت ریست کردن ربات تمام اطلاعات ربات +امار گپ و اطلاعات گپ + پاک خواهد شد!\n\nاگر مطمئن هستید لطفاً کلمه RESETINFO رو ارسال کن."
                                    ResultME = await client.send_message(object_guid,noti,message_id)
                                elif command == 'ریست کلمات':
                                    noti = "🛑 » درصورت ریست کردن کلمات تمام کلمات سخنگو شخصی پاک خواهد شد!\n\nاگر مطمئن هستید لطفاً کلمه RESETWORDS رو ارسال کن."
                                    ResultME = await client.send_message(object_guid,noti,message_id)
                                elif command == 'لیست کلمات':
                                    txt = Title('لیست کلمات')
                                    nkeys = 0
                                    nans = 0
                                    for word in SPEAK:
                                        nkeys +=1
                                        txt += Mini(word,False)
                                        txt += '\n'
                                        for answer in SPEAK[word]:
                                            nans +=1
                                            txt += Mini(answer)
                                        txt += '\n'
                                    caption = Title('لیست کلمات')
                                    caption += Mini('کلیدواژه : '+' [ '+str(nkeys)+' ]')
                                    caption += Mini('جواب : '+' [ '+str(nans)+' ]')
                                    lword = 'listWords.txt'
                                    with open(lword, "w" ,encoding="utf-8") as file:
                                        file.write(txt)
                                        file.close()
                                    async with aiopen(r""+lword, 'rb') as file:
                                        try:
                                            result = await client.send_file(object_guid, await file.read(),file_name=lword,caption=caption)
                                        except:
                                            ResultME = await client.send_message(object_guid,'ظاهرا همچین فایلی وجود ندارد',message_id)
                                        await file.close()
                                    CanSend = False
                                elif command.startswith('برکناری'):
                                    command = command.replace('برکناری','')
                                    command = command.strip()
                                    reply_message_guid = False
                                    if command.find('@') >= 0:
                                        command = command.replace('@','')
                                        try:
                                            objectInfo = await client.get_object_by_username(command)
                                            reply_message_guid = objectInfo['user']['user_guid']
                                        except:
                                            mess = 'کاربر یافت نشد.'
                                    else:
                                        command = command.replace("https://web.rubika.ir/#c=","")
                                        command = command.replace("https://rubika.ir/#c=","")
                                        try:
                                            objectInfo = await client.get_user_info(command)
                                            reply_message_guid = objectInfo['user']['user_guid']
                                        except:
                                            mess = 'کاربر یافت نشد.'

                                    if reply_message_guid:
                                        if reply_message_guid == HOWNER:
                                            mess = '» شما مالک من هستید.'
                                        elif reply_message_guid not in full_admins and reply_message_guid not in admins:
                                            mess = '» مقامی ندارد.'
                                        else:
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            mess = '» کاربر '+first_name+' برکنار شد. ✅'
                                            if reply_message_guid in full_admins:
                                                INFOS[object_guid]['full_admins'].pop(reply_message_guid)
                                            if reply_message_guid in admins:
                                                INFOS[object_guid]['admins'].pop(reply_message_guid)
                                            try:
                                                await client.set_group_admin(object_guid,reply_message_guid,[],'UnsetAdmin')
                                            except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command.startswith('ویژه'):
                                    command = command.replace('ویژه','')
                                    command = command.strip()
                                    reply_message_guid = False
                                    if command.find('@') >= 0:
                                        command = command.replace('@','')
                                        try:
                                            objectInfo = await client.get_object_by_username(command)
                                            reply_message_guid = objectInfo['user']['user_guid']
                                        except:
                                            mess = 'کاربر یافت نشد.'
                                    else:
                                        command = command.replace("https://web.rubika.ir/#c=","")
                                        command = command.replace("https://rubika.ir/#c=","")
                                        try:
                                            objectInfo = await client.get_user_info(command)
                                            reply_message_guid = objectInfo['user']['user_guid']
                                        except:
                                            mess = 'کاربر یافت نشد.'

                                    if reply_message_guid:
                                        if reply_message_guid == HOWNER:
                                            mess = '» شما مالک من هستید.'
                                        elif reply_message_guid in full_admins:
                                            mess = '» ایشون ادمین ویژه است.'
                                        else:
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            INFOS[object_guid]['full_admins'][reply_message_guid] = first_name
                                            mess = '» کاربر '+first_name+' ادمین ویژه شد. ✅'
                                            try:
                                                await client.set_group_admin(object_guid,reply_message_guid,["DeleteGlobalAllMessages"],'SetAdmin')  
                                            except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id) 
                                    CanSend = False
                            elif wordCount == 2:
                                if command == 'پاکسازی لیست ویژه':
                                    INFOS[object_guid]['full_admins'] = {}
                                    ResultME = await client.send_message(object_guid,'لیست ویژه پاکسازی شد. ✅',message_id)
                                    CanSend = False
                                elif command == 'پاکسازی لیست ادمین':
                                    INFOS[object_guid]['admins'] = {}
                                    ResultME = await client.send_message(object_guid,'لیست ادمین پاکسازی شد. ✅',message_id)
                                    CanSend = False
                            if command.startswith('برو') and CanSend:
                                command = command.replace('برو','')
                                command = command.strip()
                                if command.startswith("https://rubika.ir/joing/"):
                                    link = command.replace("https://rubika.ir/joing/","")
                                    link = link.strip()
                                    link = link.upper()
                                    result = await client.join_group(link)
                                    mess = '» لینک گروه نامعتبر است. 🚫'
                                    try:
                                        if result['is_valid']:
                                            mess = '» عضو گروه شدم. ✅'
                                    except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command.startswith("https://rubika.ir/joinc/"):
                                    link = command.replace("https://rubika.ir/joinc/","")
                                    link = link.strip()
                                    link = link.upper()
                                    result = await client.join_channel_by_link(link)
                                    mess = '» لینک کانال نامعتبر است. 🚫'
                                    try:
                                        if result['is_valid']:
                                            mess = '» عضو کانال شدم. ✅'
                                    except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command.startswith("@"):
                                    username = command.replace("@","")
                                    username = username.strip()
                                    username = username.upper()
                                    result = await client.get_object_by_username(username)
                                    if 'Channel' in result:
                                        direction_guid = result['chat']['object_guid']
                                        result = await client.join_channel(direction_guid)
                                        mess = '» ایدی کانال نامعتبر است. 🚫'
                                        try:
                                            if result['is_valid']:
                                                mess = '» عضو کانال شدم. ✅'
                                        except:pass
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                        CanSend = False
                    # FOR FULLADMINS
                    if TIP2 and CanSend:
                        # reply and no reply
                        if is_reply_message:
                            if wordCount == 0:
                                if command == 'پین':
                                    try:
                                        mess = '» پین شد. ✅'
                                        await client.set_pin_message(object_guid,is_reply_message,'Pin')
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                    except:pass
                                    CanSend = False
                                elif command == 'ارتقا':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid == HOWNER:
                                            mess = '» ایشون مالک من هستند.'
                                        elif reply_message_guid in full_admins:
                                            mess = '» ایشون ادمین ویژه است.'
                                        elif reply_message_guid  in admins:
                                            mess = '» ایشون ادمین است.'
                                        elif reply_message_guid:
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            mess = '» کاربر '+first_name+' ادمین شد. ✅'
                                            INFOS[object_guid]['admins'][reply_message_guid] = first_name
                                            try:
                                                await client.set_group_admin(object_guid,reply_message_guid,["DeleteGlobalAllMessages"],'SetAdmin')
                                            except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'برکناری':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid == HOWNER:
                                            mess = '» ایشون مالک من هستند.'
                                        elif reply_message_guid in full_admins:
                                            mess = '» ایشون ادمین ویژه است.'
                                        elif reply_message_guid  not in admins:
                                            mess = '» ایشون ادمین نیست.'
                                        elif reply_message_guid:
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            mess = '» کاربر '+first_name+' برکنار شد. ✅'
                                            INFOS[object_guid]['admin'].pop(reply_message_guid)
                                            try:
                                                await client.set_group_admin(object_guid,reply_message_guid,[],'UnsetAdmin')
                                            except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'بن':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid == HOWNER:
                                            mess = '» ایشون مالک من هستند.'
                                        elif reply_message_guid in full_admins:
                                            mess = '» ایشون ادمین ویژه است.'
                                        elif reply_message_guid  in admins:
                                            mess = '» ایشون ادمین است.'
                                        elif reply_message_guid:
                                            INFOS[object_guid]['ban'] += 1
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            mess = '» کاربر '+first_name+' بن شد. ✅'
                                            try:
                                                await client.ban_group_member(object_guid,reply_message_guid)
                                            except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'اخطار':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid == HOWNER:
                                            mess = '» ایشون مالک من هستند.'
                                        elif reply_message_guid in full_admins:
                                            mess = '» ایشون ادمین ویژه است.'
                                        elif reply_message_guid:
                                            count = INFOS[object_guid]['warnning']
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            pscount = USERS[object_guid][reply_message_guid][1]
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            pscount += 1
                                            USERS[object_guid][reply_message_guid][1] = pscount
                                            mess = "کاربر "+first_name+'\n'+"اخطار"+' [ '+str(pscount)+' ] '+"از"+' [ '+str(count)+' ] '
                                    ResultME = await client.send_message(object_guid,mess,is_reply_message)
                                    CanSend = False
                                elif command == 'امار':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid:
                                            rank = 'کاربر عادی 👤'
                                            if reply_message_guid == HOWNER:
                                                rank = 'مالک ‍👑‍'
                                            elif reply_message_guid in full_admins:
                                                rank = 'ادمین ویژه ⭐'
                                            elif reply_message_guid  in admins:
                                                rank = 'ادمین ✨'

                                            mess = Title('مقام','[ '+rank+' ]')

                                            result = await client.get_user_info(reply_message_guid)
                                            user = result['user']
                                            if 'first_name' in user:
                                                first_name = user['first_name']
                                                mess += Mini('اسم : '+first_name)
                                            if 'last_name' in user:
                                                last_name = user['last_name']
                                                mess += Mini('فامیلی : '+last_name)
                                            if 'username' in user:
                                                username = user['username']
                                                mess += Mini('آیدی : '+'@'+username)
                                            if 'last_online' in user:
                                                last_online = datetime.datetime.fromtimestamp(user['last_online'])
                                                mess += Mini('آخرین بازدید : '+str(last_online))

                                            if reply_message_guid not in USERS[object_guid]:
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']

                                            countms = USERS[object_guid][reply_message_guid][0]
                                            countwr = USERS[object_guid][reply_message_guid][1]
                                            nickname = USERS[object_guid][reply_message_guid][2]
                                            infouser = USERS[object_guid][reply_message_guid][3]
                                            
                                            mess += Mini('لقب : '+nickname)
                                            mess += Mini('اصل : '+infouser)
                                            mess += Mini('تعداد پیام : '+str(countms))
                                            mess += Mini('تعداد اخطار : '+str(countwr))

                                            mess += '\n'
                                            mess += Mini("[ "+str(reply_message_guid)+" ]")
                                            mess += '\n'+'─┅━━━━━━━┅─'
                                            if 'bio' in user:
                                                bio = user['bio']
                                                mess += "\n\n"+bio
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                            
                            elif wordCount == 1:
                                if command == 'رفع محدودیت':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid:
                                            mess = '» رفع محدودیت شد. ✅'
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            else:
                                                USERS[object_guid][reply_message_guid][1] = 0
                                            try:
                                                await client.unban_group_member(object_guid,reply_message_guid)
                                            except:pass
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'حذف اخطار':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)                                        
                                        if reply_message_guid:
                                            mess = '» اخطار حدف شد. ✅'
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            else:
                                                USERS[object_guid][reply_message_guid][1] = 0

                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'ثبت لقب':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid:
                                            mess = '» لقب ثبت شد. ✅'
                                            reply_message_text = reply_message['text']
                                            if reply_message_guid not in USERS[object_guid]:
                                                USERS[object_guid][reply_message_guid] = [0,0,reply_message_text,'']
                                            else:
                                                USERS[object_guid][reply_message_guid][2] = reply_message_text
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'ثبت اصل':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid:
                                            mess = '» اصل ثبت شد. ✅'
                                            reply_message_text = reply_message['text']
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,reply_message_text]
                                            else:
                                                USERS[object_guid][reply_message_guid][3] = reply_message_text
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                        else:
                            if wordCount == 0:
                                if command == 'کال':
                                    mess = '» کال ایجاد شد. ✅'
                                    try:
                                        result = await client.create_voice_call(object_guid)
                                        if result['status'] == 'VoiceChatExist':
                                            countMember = result['exist_group_voice_chat']['participant_count']
                                            title = result['exist_group_voice_chat']['title']
                                            mess = Title('ویسکال ایجاد شده است. ✅')
                                            mess += Mini('عنوان : '+title)
                                            mess += Mini('تعداد افراد : '+str(countMember))
                                    except:
                                        mess = '» کال ایجاد نشد.'
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'امارم':
                                    reply_message = message['message']
                                    mess = '» روی پیام پاک شده ریپلای زدی.'
                                    if reply_message:
                                        reply_message_guid = reply_message['author_object_guid']
                                        rank = 'کاربر عادی 👤'
                                        if reply_message_guid == HOWNER:
                                            rank = 'مالک ‍👑‍'
                                        elif reply_message_guid in full_admins:
                                            rank = 'ادمین ویژه ⭐'
                                        elif reply_message_guid  in admins:
                                            rank = 'ادمین ✨'

                                        mess = Title('مقام','[ '+rank+' ]')

                                        result = await client.get_user_info(reply_message_guid)
                                        user = result['user']
                                        if 'first_name' in user:
                                            first_name = user['first_name']
                                            mess += Mini('اسم : '+first_name)
                                        if 'last_name' in user:
                                            last_name = user['last_name']
                                            mess += Mini('فامیلی : '+last_name)
                                        if 'username' in user:
                                            username = user['username']
                                            mess += Mini('آیدی : '+'@'+username)
                                        if 'last_online' in user:
                                            last_online = datetime.datetime.fromtimestamp(user['last_online'])
                                            mess += Mini('آخرین بازدید : '+str(last_online))

                                        if reply_message_guid not in USERS[object_guid]:
                                            USERS[object_guid][reply_message_guid] = [0,0,first_name,'']

                                        countms = USERS[object_guid][reply_message_guid][0]
                                        countwr = USERS[object_guid][reply_message_guid][1]
                                        nickname = USERS[object_guid][reply_message_guid][2]
                                        infouser = USERS[object_guid][reply_message_guid][3]
                                        
                                        mess += Mini('لقب : '+nickname)
                                        mess += Mini('اصل : '+infouser)
                                        mess += Mini('تعداد پیام : '+str(countms))
                                        mess += Mini('تعداد اخطار : '+str(countwr))

                                        mess += '\n'
                                        mess += Mini("[ "+str(reply_message_guid)+" ]")
                                        mess += '\n'+'─┅━━━━━━━┅─'
                                        if 'bio' in user:
                                            bio = user['bio']
                                            mess += "\n\n"+bio
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                            elif wordCount == 1:
                                if command.startswith('ریست'):
                                    xxcomand = command.replace('ریست','')
                                    xxcomand = xxcomand.strip()
                                    isreset = False
                                    if xxcomand == 'قفل':
                                        INFOS[object_guid]['locks'] = "11111110001111111111111"
                                        isreset = True
                                    elif xxcomand == 'دستورات':
                                        INFOS[object_guid]['keys'] = "11111111111111111111111"
                                        isreset = True
                                    elif xxcomand == 'داشبورد':
                                        INFOS[object_guid]['setting'] = "11111111111111111111111111111111"
                                        isreset = True
                                    elif xxcomand == 'قوانین':
                                        result = await client.get_group_info(object_guid)
                                        group_title = result['group']['group_title']
                                        INFOS[object_guid]['rols'] = '📜 قوانین گپ [ '+group_title+' ] به شرح زیر میباشد.\n\n» احترام به کاربران\n» احترام به عقاید و فرهنگ ها\n» ارسال نکردن تبلیغات [آیدی.لینک.فوروارد]\n» ممبر دزدی نکنید.\n» اسپم و محتوای نامناسب ارسال نکنید.'
                                        isreset = True
                                    elif xxcomand == 'خدافظی':
                                        INFOS[object_guid]['bye'] = '🤲'
                                        isreset = True
                                    elif xxcomand == 'خوشامدگویی':
                                        result = await client.get_group_info(object_guid)
                                        group_title = result['group']['group_title']
                                        INFOS[object_guid]['welcome'] = '+ به گپ [ '+group_title+' ] خوش آمدی عزیزم 💎✨\n- بمونی برامون +×)'
                                        isreset = True
                                    elif xxcomand == 'تنظیمات':
                                        result = await client.get_group_info(object_guid)
                                        group_title = result['group']['group_title']
                                        INFOS[object_guid]['welcome'] = '+ به گپ [ '+group_title+' ] خوش آمدی عزیزم 💎✨\n- بمونی برامون +×)'
                                        INFOS[object_guid]['bye'] = '🤲'
                                        INFOS[object_guid]['rols'] = '📜 قوانین گپ [ '+group_title+' ] به شرح زیر میباشد.\n\n» احترام به کاربران\n» احترام به عقاید و فرهنگ ها\n» ارسال نکردن تبلیغات [آیدی.لینک.فوروارد]\n» ممبر دزدی نکنید.\n» اسپم و محتوای نامناسب ارسال نکنید.'
                                        INFOS[object_guid]['setting'] = "11111111111111111111111"
                                        INFOS[object_guid]['keys'] = "11111111111111111111111"
                                        INFOS[object_guid]['locks'] = "11111110001111111111111"
                                        isreset = True
                                    if isreset:
                                        mess = xxcomand+' ریست شد. ✅'
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                        CanSend = False
                                elif command == 'امار گپ':
                                    mess = Title('امار گپ','[ '+str(INFOS[object_guid]['name'])+' ]')

                                    def myFunc(e):
                                        return e['mes']
                                    listMems = []
                                    allMes = 0
                                    for mems in USERS[object_guid]:
                                        allMes += int(USERS[object_guid][mems][0])
                                        listMems.append({'mes':int(USERS[object_guid][mems][0]),'name':str(USERS[object_guid][mems][2]),'guid':str(mems)})

                                    now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                                    time_oj = datetime.datetime.fromtimestamp(int(INFOS[object_guid]['date']))
                                    mess += Mini('شروع فعایت : '+str(time_oj))
                                    mess += Mini('زمان : '+str(now))
                                    mess += '\n'
                                    mess += Mini('تعداد کل پیام ثبت شده : '+str(INFOS[object_guid]['messages']))
                                    mess += Mini('تعداد کل پیام مجاز : '+str(allMes))
                                    mess += Mini('تعداد جوین شده : '+str(INFOS[object_guid]['join']))
                                    mess += Mini('تعداد افزوده شده : '+str(INFOS[object_guid]['add']))
                                    mess += Mini('تعداد لفت داده : '+str(INFOS[object_guid]['left']))
                                    mess += Mini('تعداد حذف شده : '+str(INFOS[object_guid]['ban']))
                                    mess += '\n'
                                    mess += 'تعداد پیام ها '+' '+'━━━━━━━━┅─'
                                    mess += '\n\n'
                                    listMems.sort(reverse=True,key=myFunc)
                                    limit = 1
                                    for member in listMems:
                                        if limit > 20:
                                            break
                                        memberGuid = member['guid']
                                        # rank = 'کاربر عادی 👤'
                                        rank = ''
                                        if memberGuid == HOWNER:
                                            rank = " | "+'مالک ‍👑‍'
                                        elif memberGuid in full_admins:
                                            rank = " | "+'ادمین ویژه ⭐'
                                        elif memberGuid  in admins:
                                            rank = " | "+'ادمین ✨'

                                        countms = member['mes']
                                        nickname = member['name']
                                        
                                        mess += str(limit)+'.'+'کاربر '+nickname+' با '+str(countms)+rank+'\n'
                                        limit += 1
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'مرتب سازی':
                                    listManage = []
                                    for key in SPEAK:
                                        listManage.append(key)
                                    def myFunc(e):
                                        return len(e)
                                    listManage.sort(reverse=True,key=myFunc)
                                    NSPEAK = {}
                                    for newkey in listManage:
                                        NSPEAK[newkey] = SPEAK[newkey]
                                    SPEAK = NSPEAK
                                    NSPEAK = {}
                                    UPFILES(json,file_speak,SPEAK)
                                    mess = Mini('جملات ربات مرتب سازی شد. ✅',False)
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                                elif command == 'فایل کلمات':
                                    async with aiopen(r""+file_speak, 'rb') as file:
                                        try:
                                            result = await client.send_file(object_guid, await file.read(),file_name=file_speak,caption='فایل کلمات شخصی')
                                        except:
                                            ResultME = await client.send_message(object_guid,'ظاهرا همچین فایلی وجود ندارد',message_id)
                                        await file.close()
                                    CanSend = False
                                elif command == 'حذف بنر':
                                    mess = INFOS[object_guid]['baner']
                                    if len(mess) == 0:
                                        mess = 'بنری ثبت نشده است.'
                                    else:
                                        mess = '» بنر حذف شد. ✅'
                                        INFOS[object_guid]['baner'] = ''
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                    CanSend = False
                            if command.startswith('کرونا') and CanSend:
                                locat = command.replace('کرونا','')
                                locat = locat.strip()
                                date = requests.get(url ="https://one-api.ir/corona/?token=833942:64919956105c3")
                                date = date.json()
                                if date['status'] == 200:
                                    mess = 'کشور مورد نظر یافت نشد.'
                                    entries = date['result']['entries']
                                    countris = [["United States","ایالات متحده","امریکا","USA"],["India","هند"],["Brazil","برزیل"],["United Kingdom","انگلستان"],["France","فرانسه"],["Russia","روسیه"],["Turkey","بوقلمون"],["Colombia","کلمبیا"],["Spain","اسپانیا"],["Italy","ایتالیا"],["Iran","ایران"],["Germany","المان"],["Mexico","مکزیک"],["South Africa","افریقای جنوبی"],["Peru","پرو"],["Chile","شیلی"],["Canada","کانادا"],["Afghanistan","افغانستان"],["Albania","البانی"],["Algeria","الجزایر"],["Andorra","اندورا"],["Angola","انگولا"],["Antigua and Barbuda","انتیگوا و باربودا"],["Argentina","ارژانتین"],["Armenia","ارمنستان"],["Aruba","اروبا"],["Australia","استرالیا"],["Austria","اتریش"],["Azerbaijan","اذربایجان"],["Bahamas","باهاما"],["Bahrain","بحرین"],["Bangladesh","بنگلادش"],["Barbados","باربادوس"],["Belarus","بلاروس"],["Belgium","بلژیک"],["Belize","بلیز"],["Benin","بنین"],["Bermuda","بنین"],["Bermuda","برمودا"],["Bhutan","بوتان"],["Bolivia","بولیوی"],["Bosnia and Herzegovina","بوسنی و هرزگوین"],["Bonaire, Sint Eustatius and Saba","بونیر، سینت اوستاتیوس و صبا"],["Botswana","بوتسوانا"],["British Virgin Islands","جزایر ویرجین بریتانیا"],["Brunei","برونئی"],["Bulgaria","بلغارستان"],["Burkina Faso","بورکینافاسو"],["Burundi","بوروندی"],["Cape Verde","کیپ ورد"],["Cambodia","کامبوج"],["Cameroon","کامرون"],["Cayman Islands","جزایر کیمن"],["Central African Republic","جمهوری افریقای مرکزی"],["Chad","چاد"],["Pakistan","پاکستان"],["Republic of Congo","جمهوری کنگو"],["Costa Rica","کاستاریکا"],["Cote d'Ivoire","ساحل عاج"],["Croatia","کرواسی"],["Cuba","کوبا"],["Curaçao","کوراسائو"],["Cyprus","قبرس"],["Czech Republic","جمهوری چک"],["Democratic Republic of Congo","جمهوری دموکراتیک کنگو"],["Denmark","دانمارک"],["Djibouti","جیبوتی"],["Dominica","دومینیکا"],["Dominican Republic","جمهوری دومینیکن"],["Ecuador","اکوادور"],["Egypt","مصر"],["El Salvador","السالوادور"],["Equatorial Guinea","گینه استوایی"],["Estonia","استونی"],["Eswatini","اسواتینی"],["Ethiopia","اتیوپی"],["Eritrea","اریتره"],["Faroe Islands","جزایر فارو"],["Fiji","فیجی"],["Finland","فنلاند"],["French Guiana","گویان فرانسه"],["French Polynesia","پلینزی فرانسه"],["Gabon","گابن"],["Gambia","گامبیا"],["Georgia","گرجستان"],["Ghana","غنا"],["Gibraltar","جبل الطارق"],["Grand Princess","پرنسس بزرگ"],["Greece","یونان"],["Greenland","گرینلند"],["Grenada","گرانادا"],["Guadeloupe","گوادلوپ"],["Guatemala","گواتمالا"],["Guernsey","گرنزی"],["Guinea","گینه"],["Guinea-Bissau","گینه بیسائو"],["Guyana","گویان"],["Haiti","هائیتی"],["Holy See","مقرّس"],["Honduras","هندوراس"],["Hungary","مجارستان"],["Iceland","ایسلند"],["Iraq","عراق"],["Ireland","ایرلند"],["Isle of Man","جزیره من"],["Israel","اسرائيل"],["Japan","ژاپن"],["Diamond Princess","پرنسس الماس"],["Jamaica","جامائیکا"],["Jersey","پیراهن ورزشی"],["Jordan","اردن"],["Kenya","کنیا"],["Kazakhstan","قزاقستان"],["Kosovo","کوزوو"],["Kuwait","کویت"],["Kyrgyzstan","قرقیزستان"],["Laos","لائوس"],["Latvia","لتونی"],["Lebanon","لبنان"],["Liberia","لیبریا"],["Libya","لیبی"],["Liechtenstein","لیختن اشتاین"],["Lithuania","لیتوانی"],["Luxembourg","لوکزامبورگ"],["Madagascar","ماداگاسکار"],["Maldives","مالدیو"],["Mali","مالی"],["Malta","مالت"],["Malawi","مالاوی"],["Martinique","مارتینیک"],["Mauritania","موریتانی"],["Mauritius","موریس"],["Mayotte","مایوت"],["Moldova","مولداوی"],["Monaco","موناکو"],["Mongolia","مغولستان"],["Montenegro","مونته نگرو"],["Montserrat","مونتسرات"],["Morocco","مراکش"],["Mozambique","موزامبیک"],["MS Zaandam","ام اس زندم"],["Myanmar","میانمار"],["Namibia","نامیبیا"],["Nepal","نپال"],["Netherlands","هلند"],["New Caledonia","کالدونیای جدید"],["New Zealand","نیوزلند"],["Nicaragua","نیکاراگوئه"],["Niger","نیجر"],["Nigeria","نیجریه"],["North Macedonia","مقدونیه شمالی"],["Norway","نروژ"],["Occupied Palestinian territory","سرزمین فلسطین اشغالی"],["Oman","عمان"],["Panama","پاناما"],["Paraguay","پاراگوئه"],["Philippines","فیلیپین"],["Papua New Guinea","پاپوا گینه نو"],["Poland","لهستان"],["Portugal","کشور پرتغال"],["Qatar","قطر"],["Reunion","تجدید دیدار"],["Romania","رومانی"],["Singapore","سنگاپور"],["Rwanda","رواندا"],["San Marino","سن مارینو"],["Saint Kitts and Nevis","سنت کیتس و نویس"],["Saint Lucia","سنت لوسیا"],["Sint Maarten","سینت مارتن"],["Saint Pierre and Miquelon","سنت پیر و میکلون"],["Saint Vincent and the Grenadines","سنت وینسنت و گرنادین"],["Sao Tome and Principe","سائوتومه و پرنسیپ"],["Saudi Arabia","عربستان سعودی"],["Seychelles","سیشل"],["Senegal","سنگال"],["Serbia","صربستان"],["Sierra Leone","سیرا لئون"],["Indonesia","اندونزی"],["Slovakia","اسلواکی"],["Slovenia","اسلوونی"],["Somalia","سومالی"],["South Korea","کره جنوبی"],["South Sudan","سودان جنوبی"],["Malaysia","مالزی"],["Sri Lanka","سری لانکا"],["Sudan","سودان"],["Suriname","سورینام"],["Sweden","سوئد"],["Switzerland","سوئیس"],["Syria","سوریه"],["Tanzania","تانزانیا"],["Thailand","تایلند"],["Timor-Leste","تیمور شرقی"],["Togo","رفتن"],["Trinidad and Tobago","ترینیداد و توباگو"],["Tunisia","تونس"],["Turks and Caicos Islands","جزایر تورکس و کایکوس"],["Uganda","اوگاندا"],["Ukraine","اوکراین"],["United Arab Emirates","امارات متحده عربی"],["Taiwan","تایوان"],["United States Virgin Islands","جزایر ویرجین ایالات متحده"],["Uruguay","اروگوئه"],["Uzbekistan","ازبکستان"],["Venezuela","ونزوئلا"],["Vietnam","ویتنام"],["Western Sahara","صحرای غربی"],["Yemen","یمن"],["Zambia","زامبیا"],["Zimbabwe","زیمبابوه"]]
                                    
                                    isok = False
                                    for mins in countris:
                                        for min in mins:
                                            if locat == min:
                                                isok = True
                                                break
                                        if isok:
                                            pname = mins[0]
                                            ename = mins[1]
                                            # print(entries)
                                            for num in entries:
                                                if 'country' in num:
                                                    name = num['country']
                                                    if name == pname:
                                                        country = num
                                                        Name_continent = country['continent']
                                                        Name_country = country['country']
                                                        cases = country['cases']
                                                        deaths = country['deaths']
                                                        recovered = country['recovered']

                                                        Name_continentF = ''
                                                        if Name_continent == 'Asia':
                                                            Name_continentF = 'اسیا'
                                                        elif Name_continent == 'Africa':
                                                            Name_continentF = 'افریقا'
                                                        elif Name_continent == 'Europe':
                                                            Name_continentF = 'اروپا'
                                                        elif Name_continent == 'North America':
                                                            Name_continentF = 'امریکای شمالی'
                                                        elif Name_continent == 'South America':
                                                            Name_continentF = 'امریکای جنوبی'
                                                        elif Name_continent == 'Australia':
                                                            Name_continentF = 'استرالیا'
                                                        elif Name_continent == 'Antarctica':
                                                            Name_continentF = 'جنوبگان'
                                                        elif Name_continent == 'Oceania':
                                                            Name_continentF = 'اقیانوسیه'

                                                        mess = "| #ᑕOᖇOᑎᗩ\n\n"
                                                        mess += "𝗖𝗼𝗻𝘁𝗶𝗻𝗲𝗻𝘁 » "+Name_continent+" | "+Name_continentF+"\n"
                                                        mess += "𝗖𝗼𝘂𝗻𝘁𝗿𝘆 » "+Name_country+" | "+ename+"\n\n"
                                                        mess += "𝗖𝗮𝘀𝗲𝘀 » "+cases+" "+"مورد"+"\n"
                                                        mess += "𝗗𝗲𝗮𝘁𝗵𝘀 » "+deaths+" "+"فوت شده"+"\n"
                                                        mess += "𝗥𝗲𝗰𝗼𝘃𝗲𝗿𝗱 » "+recovered+" "+"بهبود یافته"+"\n"
                                                        break
                                            break
                                    ResultME = await client.send_message(object_guid,mess,message_id)
                                CanSend = False
                            elif command.startswith('وضعیت'):
                                locat = command.replace('وضعیت','')
                                locat = locat.strip()
                                cities = [['Tehran','تهران'],['Tabriz','تبریز','اذربایجان شرقی','اذربایجان شرقی'],['Urmia','ارومیه','اذربایجان غربی','اذربایجان غربی'],['Ardabil','اردبیل'],['Isfahan','اصفهان'],['Karaj','کرج','البرز'],['Ilam','ایلام'],['Bushehr','بوشهر'],['Shahre-Kord','شهرکرد','چهارمحال و بختیاری','چهارمحال'],['Birjand','بیرجند','خراسان جنوبی'],['Mashhad','مشهد','خراسان رضوی'],['Bojnord','بجنورد','خراسان شمالی'],['Ahvaz','اهواز','خوزستان'],['Zanjan','زنجان'],['Semnan','سمنان'],['Zahedan','زاهدان','سیستان و بلوچستان','سیستان'],['Shiraz','شیراز','فارس'],['Qazvin','قزوین'],['Qom','قم'],['Sanandaj','کردستان','سنندج'],['Kerman','کرمان'],['Kermanshah','کرمانشاه'],['Yasuj','یاسوج','کهگیلویه و بویراحمد','کهگیلویه'],['Gorgan','گلستان','گرگان'],['Rasht','گیلان','رشت'],['Khorramabad','لرستان','خرم‌اباد','خرم‌اباد'],['Sari','مازندران','ساری'],['Arak','اراک','مرکزی'],['Bandar-Abbas','هرمزگان','بندرعباس'],['Hamadan','همدان'],['Yazd','یزد']]
                                
                                elocat = False
                                mess = 'شهر مورد نظر یافت نشد.'
                                for city in cities:
                                    for step in city:
                                        if step == locat:
                                            elocat = city[0]
                                            plocat = city[1]
                                            break
                                    if elocat:
                                        date = requests.get(url ="http://dorweb.ir/api/weather/"+elocat)
                                        date = date.json()
                                        if not date['IsOK']:break
                                        
                                        result = date['Result']
                                        location = result['location']
                                        province = location['province']['caption']
                                        city = location['city']['caption']
                                        
                                        weather = result['weather']
                                        date = weather['persian_dt']
                                        descriptionF = weather['description']
                                        descriptionE = str(weather['main'])
                                        temp_min = str(weather['temp_min'])
                                        temp_max = str(weather['temp_max'])
                                        humidity = str(weather['humidity'])
                                        windSpeed = str(weather['wind']['speed'])

                                        temp_max = temp_max+"°C"
                                        temp_min = temp_min+"°C"
                                        humidity = humidity+" %"
                                        windSpeed = windSpeed+" km/h"

                                        mess = "| #ᗯᗴᗩTᕼᗴᖇ\n\n"
                                        mess += "𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻 » "+province+" / "+city+"\n"
                                        mess += "𝗗𝗮𝘁𝗲 » "+date+"\n\n"
                                        mess += descriptionE+" | "+descriptionF+"\n"
                                        mess += "𝗧𝗲𝗺𝗽 » "+temp_max+" / "+temp_min+"\n"
                                        mess += "𝗛𝘂𝗺𝗶𝗱𝗶𝘁𝘆 » "+humidity+"\n"
                                        mess += "𝗪𝗶𝗻𝗱 𝗦𝗽𝗲𝗲𝗱 » "+windSpeed+"\n"
                                        break
                                ResultME = await client.send_message(object_guid,mess,message_id)
                                CanSend = False
                            elif command.startswith('بهینه سازی') and wordCount <= 3:
                                lims = command.replace('بهینه سازی','')
                                try:
                                    lims = int(lims.strip())
                                    if lims < 0:lims = 10
                                except:lims = 10
                                deleting = []
                                Alls = 0
                                for child in USERS[object_guid]:
                                    user = USERS[object_guid][child]
                                    mes = user[0]
                                    war = user[1]
                                    state = mes-war
                                    if (state <= lims):
                                        Alls += mes
                                        deleting.append(child)

                                for child in deleting:
                                    USERS[object_guid].pop(child)
                                with open(File_users, "w") as outfile:
                                    json.dump(USERS, outfile)   
                                mess = Mini('کاربران با تعداد پیام کمتر از'+" "+str(lims)+" "+'از حافظه پاک شد. ✅'+'\n'+'در مجموع '+str(Alls)+' پیام پاک شده است.',False)
                                ResultME = await client.send_message(object_guid,mess,message_id)
                                Alls = 0
                                deleting = []
                                CanSend = False

                            # managing tools
                            if CanSend and wordCount <= 2:
                                specific = False
                                method = True
                                reply_message_guid = False
                                xcom = command
                                if not command.startswith('@') and command.find('@') >= 0 and  len(command) > 8:
                                    specific = True
                                    xcom = xcom.replace('@','')
                                elif len(command) > 20:
                                    specific = True
                                    method = False
                                    xcom = xcom.replace("https://web.rubika.ir/#c=","")
                                    xcom = xcom.replace("https://rubika.ir/#c=","")
                                if specific:
                                    xcom = xcom.replace('بن','')
                                    xcom = xcom.replace('ارتقا','')
                                    xcom = xcom.replace('برکناری','')
                                    xcom = xcom.replace('رفع محدودیت','')
                                    xcom = xcom.replace('حذف اخطار','')
                                    xcom = xcom.replace('اخطار','')
                                    xcom = xcom.replace('امار','')
                                    xcom = xcom.strip()
                                    if method:
                                        try:
                                            objectInfo = await client.get_object_by_username(xcom)
                                            reply_message_guid = objectInfo['user']['user_guid']
                                        except:
                                            mess = 'کاربر یافت نشد.'
                                    else:
                                        try:
                                            objectInfo = await client.get_user_info(xcom)
                                            reply_message_guid = objectInfo['user']['user_guid']
                                        except:
                                            mess = 'کاربر یافت نشد.'
                                    if command.startswith('بن'):
                                        if reply_message_guid:
                                            if reply_message_guid == HOWNER:
                                                mess = '» ایشون مالک من هستند.'
                                            elif reply_message_guid in full_admins:
                                                mess = '» ایشون ادمین ویژه است.'
                                            elif reply_message_guid  in admins:
                                                mess = '» ایشون ادمین است.'
                                            else:
                                                INFOS[object_guid]['ban'] += 1
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                first_name = USERS[object_guid][reply_message_guid][2]
                                                mess = '» کاربر '+first_name+' بن شد. ✅'
                                                try:
                                                    await client.ban_group_member(object_guid,reply_message_guid)
                                                except:pass
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                        CanSend = False
                                    elif command.startswith('برکناری'):
                                        if reply_message_guid:
                                            if reply_message_guid == HOWNER:
                                                mess = '» ایشون مالک من هستند.'
                                            elif reply_message_guid in full_admins:
                                                mess = '» ایشون ادمین ویژه است.'
                                            elif reply_message_guid  not in admins:
                                                mess = '» ایشون ادمین نیست.'
                                            else:
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                first_name = USERS[object_guid][reply_message_guid][2]
                                                INFOS[object_guid]['admin'].pop(reply_message_guid)
                                                mess = '» کاربر '+first_name+' برکنار شد. ✅'
                                                try:
                                                    await client.set_group_admin(object_guid,reply_message_guid,[],'UnsetAdmin')
                                                except:pass
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                        CanSend = False
                                    elif command.startswith('ارتقا'):
                                        if reply_message_guid:
                                            if reply_message_guid == HOWNER:
                                                mess = '» ایشون مالک من هستند.'
                                            elif reply_message_guid in full_admins:
                                                mess = '» ایشون ادمین ویژه است.'
                                            elif reply_message_guid  in admins:
                                                mess = '» ایشون ادمین است.'
                                            else:
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                first_name = USERS[object_guid][reply_message_guid][2]
                                                INFOS[object_guid]['admins'][reply_message_guid] = first_name
                                                mess = '» کاربر '+first_name+' ادمین شد. ✅'
                                                try:
                                                    await client.set_group_admin(object_guid,reply_message_guid,["DeleteGlobalAllMessages"],'SetAdmin')
                                                except:pass
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                        CanSend = False
                                    elif command.startswith('رفع محدودیت'):
                                        if reply_message_guid:
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            else:
                                                USERS[object_guid][reply_message_guid][1] = 0
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            mess = '» کاربر '+first_name+' رفع محدودیت شد. ✅'
                                            try:
                                                await client.unban_group_member(object_guid,reply_message_guid)
                                            except:pass
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                        CanSend = False
                                    elif command.startswith('اخطار'):
                                        if reply_message_guid:
                                            if reply_message_guid == HOWNER:
                                                mess = '» ایشون مالک من هستند.'
                                            elif reply_message_guid in full_admins:
                                                mess = '» ایشون ادمین ویژه است.'
                                            else:
                                                count = INFOS[object_guid]['warnning']
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                pscount = USERS[object_guid][reply_message_guid][1]
                                                first_name = USERS[object_guid][reply_message_guid][2]
                                                pscount += 1
                                                USERS[object_guid][reply_message_guid][1] = pscount
                                                mess = "کاربر "+first_name+'\n'+"اخطار"+' [ '+str(pscount)+' ] '+"از"+' [ '+str(count)+' ] '
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                        CanSend = False
                                    elif command.startswith('حذف اخطار'):
                                        if reply_message_guid:
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                            else:
                                                USERS[object_guid][reply_message_guid][1] = 0
                                                
                                            first_name = USERS[object_guid][reply_message_guid][2]
                                            mess = '» اخطار '+first_name+' حدف شد. ✅'
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                                        CanSend = False
                                    elif command.startswith('امار'):
                                        if reply_message_guid:
                                            rank = 'کاربر عادی 👤'
                                            if reply_message_guid == HOWNER:
                                                rank = 'مالک ‍👑‍'
                                            elif reply_message_guid in full_admins:
                                                rank = 'ادمین ویژه ⭐'
                                            elif reply_message_guid  in admins:
                                                rank = 'ادمین ✨'

                                            mess = Title('مقام','[ '+rank+' ]')

                                            result = await client.get_user_info(reply_message_guid)
                                            user = result['user']
                                            if 'first_name' in user:
                                                first_name = user['first_name']
                                                mess += Mini('اسم : '+first_name)
                                            if 'last_name' in user:
                                                last_name = user['last_name']
                                                mess += Mini('فامیلی :',last_name)
                                            if 'username' in user:
                                                username = user['username']
                                                mess += Mini('آیدی : '+'@'+username)
                                            if 'last_online' in user:
                                                last_online = datetime.datetime.fromtimestamp(user['last_online'])
                                                mess += Mini('آخرین بازدید : '+str(last_online))

                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,'']

                                            countms = USERS[object_guid][reply_message_guid][0]
                                            countwr = USERS[object_guid][reply_message_guid][1]
                                            nickname = USERS[object_guid][reply_message_guid][2]
                                            infouser = USERS[object_guid][reply_message_guid][3]
                                            
                                            mess += Mini('لقب : '+nickname)
                                            mess += Mini('اصل : '+infouser)
                                            mess += Mini('تعداد پیام : '+str(countms))
                                            mess += Mini('تعداد اخطار : '+str(countwr))

                                            mess += '\n'
                                            mess += Mini("[ "+str(reply_message_guid)+" ]")
                                            mess += '\n'+'─┅━━━━━━━┅─'
                                            if 'bio' in user:
                                                bio = user['bio']
                                                mess += "\n\n"+bio
                                        ResultME = await client.send_message(object_guid,mess,message_id)
                            # locks settings keys
                            if CanSend:
                                cmd = False
                                mess = False
                                cmd1 = 'بسته'
                                cmd2 = 'خاموش'
                                cmd3 = 'قفل'
                                cmd4 = 'باز'
                                cmd5 = 'روشن'
                                cmd6 = 'ازاد'
                                if command.find(cmd1) >= 0:
                                    cmd = command.replace(cmd1,'')
                                    mess = cmd1
                                    Vb = False
                                elif command.find(cmd2) >= 0:
                                    cmd = command.replace(cmd2,'')
                                    mess = cmd2
                                    Vb = False
                                elif command.find(cmd3) >= 0:
                                    cmd = command.replace(cmd3,'')
                                    mess = cmd3
                                    Vb = False
                                elif command.find(cmd4) >= 0:
                                    cmd = command.replace(cmd4,'')
                                    mess = cmd4
                                    Vb = True
                                elif command.find(cmd5) >= 0:
                                    cmd = command.replace(cmd5,'')
                                    mess = cmd5
                                    Vb = True
                                elif command.find(cmd6) >= 0:
                                    cmd = command.replace(cmd6,'')
                                    mess = cmd6
                                    Vb = True
                                order = False
                                if cmd and cmd.startswith('دستور'):
                                    cmd = cmd.replace('دستور'+' ','')
                                    order = True
                                if cmd:
                                    cmd = cmd.strip()
                                    if cmd in Listkeys and order:
                                        key = int(Listkeys[cmd])
                                        keys = list(INFOS[object_guid]['keys'])
                                        keys[key] = str(int(Vb))
                                        INFOS[object_guid]['keys'] = ''.join(keys)
                                        ResultME = await client.send_message(object_guid,'دستور '+cmd+' '+mess+' است. ✅',message_id)
                                        CanSend = False
                                    elif not order:
                                        if cmd == "افزودن عضو":
                                            await Set_group_default_access(client,object_guid,"AddMember",Vb)
                                            ResultME = await client.send_message(object_guid,'افزودن عضو '+mess+' است. ✅',message_id)
                                            CanSend = False
                                        elif cmd == "مشاهده مدیر" or cmd == "مشاهده مدیران":
                                            await Set_group_default_access(client,object_guid,"ViewAdmins",Vb)
                                            ResultME = await client.send_message(object_guid,'مشاهده مدیران '+mess+' است. ✅',message_id)
                                            CanSend = False
                                        elif cmd == "مشاهده اعضا":
                                            await Set_group_default_access(client,object_guid,"ViewMembers",Vb)
                                            ResultME = await client.send_message(object_guid,'مشاهده اعضا '+mess+' است. ✅',message_id)
                                            CanSend = False
                                        elif cmd == 'گپ' or cmd == 'گروه':
                                            await Set_group_default_access(client,object_guid,"SendMessages",Vb)
                                            ResultME = await client.send_message(object_guid,'گپ '+mess+' است. ✅',message_id)
                                            CanSend = False
                                        elif cmd in Listlocks:
                                            key = int(Listlocks[cmd])
                                            locks = list(INFOS[object_guid]['locks'])
                                            locks[key] = str(int(Vb))
                                            INFOS[object_guid]['locks'] = ''.join(locks)
                                            ResultME = await client.send_message(object_guid,cmd+' '+mess+' است. ✅',message_id)
                                            CanSend = False
                                        elif cmd in Listset:
                                            key = int(Listset[cmd])
                                            setting = list(INFOS[object_guid]['setting'])
                                            setting[key] = str(int(Vb))
                                            INFOS[object_guid]['setting'] = ''.join(setting)
                                            ResultME = await client.send_message(object_guid,cmd+' '+mess+' است. ✅',message_id)
                                            CanSend = False
                        
                        # set seting
                        if CanSend and command.startswith('تنظیم') and wordCount <= 2:
                            xxcomand = command.replace('تنظیم','')
                            xxcomand = xxcomand.strip()
                            isok = False
                            mess = False
                            if is_reply_message:
                                if xxcomand == 'خوشامدگویی':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    if reply_message:
                                        reply_message_text = reply_message['text']
                                        INFOS[object_guid]['welcome'] = reply_message_text
                                        isok = True
                                elif xxcomand == 'خدافظی':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    if reply_message:
                                        reply_message_text = reply_message['text']
                                        INFOS[object_guid]['bye'] = reply_message_text
                                        isok = True
                                elif xxcomand == 'قوانین':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    if reply_message:
                                        reply_message_text = reply_message['text']
                                        INFOS[object_guid]['rols'] = reply_message_text
                                        isok = True
                                elif xxcomand == 'لقب':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid:
                                            reply_message_text = reply_message['text']
                                            if reply_message_guid not in USERS[object_guid]:
                                                USERS[object_guid][reply_message_guid] = [0,0,reply_message_text,'']
                                            else:
                                                USERS[object_guid][reply_message_guid][2] = reply_message_text
                                            isok = True
                                elif xxcomand == 'اصل':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    if reply_message:
                                        mess = 'کاربر شناسایی نشد.'
                                        reply_message_guid = GetReplyGuid(reply_message)
                                        if reply_message_guid:
                                            reply_message_text = reply_message['text']
                                            if reply_message_guid not in USERS[object_guid]:
                                                result = await client.get_user_info(reply_message_guid)
                                                user = result['user']
                                                first_name = ''
                                                if 'first_name' in user:
                                                    first_name = user['first_name']
                                                USERS[object_guid][reply_message_guid] = [0,0,first_name,reply_message_text]
                                            else:
                                                USERS[object_guid][reply_message_guid][3] = reply_message_text
                                            isok = True
                                elif xxcomand == 'بنر':
                                    reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                    if reply_message:
                                        reply_message_text = reply_message['text']
                                        INFOS[object_guid]['baner'] = reply_message_text
                                        isok = True
                            else:
                                if xxcomand.startswith('اخطار'):
                                    zzcomand = xxcomand.replace('اخطار','')
                                    zzcomand = zzcomand.strip()
                                    zzcomand = int(zzcomand)
                                    if zzcomand > 100:
                                        zzcomand = 100
                                    elif zzcomand <= 0:
                                        zzcomand = 0
                                    INFOS[object_guid]['warnning'] = zzcomand
                                    isok = True
                            
                            if isok:
                                mess = xxcomand+' تنظیم شد. ✅'
                                ResultME = await client.send_message(object_guid,mess,message_id)
                                CanSend = False
                            elif mess:
                                ResultME = await client.send_message(object_guid,mess,message_id)
                                CanSend = False
                    # FOR ADMINS AND MEMBERS
                    key = 0
                    search = command
                    if CanSend and search in Listkeys:
                        if TIP2:
                            step1 = 1
                            step2 = 1
                            step3 = True
                        else:
                            step3 = PorotectMSS(TimeMessages,object_guid)
                            key = Listkeys[search]
                            keys = list(INFOS[object_guid]['keys'])
                            step1 = int(keys[0])
                            step2 = int(keys[key])
                        if step1 == 1 and step2 == 1 and step3:
                            # FOR ADMINS
                            if TIP3 and CanSend:
                                # reply and no reply
                                if is_reply_message:
                                    if wordCount == 0:
                                        if command == 'اینفو' or command == 'امار':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = 'کاربر شناسایی نشد.'
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid:
                                                    rank = 'کاربر عادی 👤'
                                                    if reply_message_guid == HOWNER:
                                                        rank = 'مالک ‍👑‍'
                                                    elif reply_message_guid in full_admins:
                                                        rank = 'ادمین ویژه ⭐'
                                                    elif reply_message_guid  in admins:
                                                        rank = 'ادمین ✨'

                                                    mess = Title('مقام','[ '+rank+' ]')
                                                    if reply_message_guid not in USERS[object_guid]:
                                                        result = await client.get_user_info(reply_message_guid)
                                                        user = result['user']
                                                        first_name = ''
                                                        if 'first_name' in user:    
                                                            first_name = user['first_name']
                                                        USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                    countms = USERS[object_guid][reply_message_guid][0]
                                                    countwr = USERS[object_guid][reply_message_guid][1]
                                                    nickname = USERS[object_guid][reply_message_guid][2]
                                                    infouser = USERS[object_guid][reply_message_guid][3]
                                                    mess += Mini('لقب : '+nickname)
                                                    mess += Mini('اصل : '+infouser)
                                                    mess += Mini('تعداد پیام : '+str(countms))
                                                    mess += Mini('تعداد اخطار : '+str(countwr))
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                else:
                                    if wordCount == 0:
                                        if command == 'داشبورد':
                                            now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                                            mess = Title('داشبورد')
                                            mess += Mini('زمان : '+str(now))
                                            mess += '\n'
                                            setting = list(INFOS[object_guid]['setting'])
                                            for lock in Listset:
                                                res = ''
                                                if int(setting[Listset[lock]]) == 0:
                                                    res = '[ خاموش ]'
                                                mess += Mini(lock+' '+res)
                                                
                                            mess += '\n'
                                            mess += Mini('تعداد اخطار : '+str(INFOS[object_guid]['warnning']))
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'لیست':
                                            mess = Title('لیست ها'+' 💎 ')
                                            mess += Mini('لیست دستورات',False)
                                            mess += Mini('لیست قفل',False)
                                            mess += Mini('لیست ویژه',False)
                                            mess += Mini('لیست ادمین',False)
                                            mess += Mini('لیست کلمات',False)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                        elif command == 'اینفو' or command == 'امار' or command == 'امارم':
                                            mess = 'کاربر شناسایی نشد.'
                                            reply_message_guid = message_id
                                            if reply_message_guid:
                                                rank = 'کاربر عادی 👤'
                                                if reply_message_guid == HOWNER:
                                                    rank = 'مالک ‍👑‍'
                                                elif reply_message_guid in full_admins:
                                                    rank = 'ادمین ویژه ⭐'
                                                elif reply_message_guid  in admins:
                                                    rank = 'ادمین ✨'

                                                mess = Title('مقام','[ '+rank+' ]')
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:    
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                countms = USERS[object_guid][reply_message_guid][0]
                                                countwr = USERS[object_guid][reply_message_guid][1]
                                                nickname = USERS[object_guid][reply_message_guid][2]
                                                infouser = USERS[object_guid][reply_message_guid][3]
                                                mess += Mini('لقب : '+nickname)
                                                mess += Mini('اصل : '+infouser)
                                                mess += Mini('تعداد پیام : '+str(countms))
                                                mess += Mini('تعداد اخطار : '+str(countwr))
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                    # two word command
                                    elif wordCount == 1:                                                                               
                                        if command == 'لیست ویژه':
                                            mess = Title('لیست ویژه','⭐')
                                            empty = True
                                            for prs in INFOS[object_guid]['full_admins']:
                                                mess += Mini('کاربر '+INFOS[object_guid]['full_admins'][prs])
                                                empty = False
                                            if empty:
                                                mess += Mini('لیست مدیران ویژه خالی میباشد.')
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'لیست ادمین':
                                            mess = Title('لیست ادمین','✨')
                                            empty = True
                                            for prs in INFOS[object_guid]['admins']:
                                                mess += Mini('کاربر '+INFOS[object_guid]['admins'][prs])
                                                empty = False
                                            if empty:
                                                mess += Mini('لیست ادمین ها خالی میباشد.')
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'لیست قفل':
                                            mess = Title('لیست قفل','🔓‍')
                                            locks = list(INFOS[object_guid]['locks'])
                                            for lock in Listlocks:
                                                res = ''
                                                if int(locks[Listlocks[lock]]) == 0:
                                                    res = ' | قفل 🚫'
                                                mess += Mini(lock+' '+res)
                                                
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'لیست دستورات':
                                            mess = Title('لیست دستورات','⚙')
                                            orders = list(INFOS[object_guid]['keys'])
                                            for lock in Listkeys:
                                                res = ''
                                                num = Listkeys[lock]
                                                if orders[num] == '0':
                                                    res = ' | خاموش 💤'
                                                mess += Mini(lock+' '+res)
                                                
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False


                            # FOR MEMBERS
                            if CanSend:
                            # reply and no reply
                                if is_reply_message:
                                    if wordCount == 0:
                                        if command == 'کشیده':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = reply_message['text']
                                                mess = Font_kesh(mess)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'لش':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = reply_message['text']
                                                mess = Font_lash(mess)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'شکسته':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = reply_message['text']
                                                mess = Font_shec(mess)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'لقب':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = 'کاربر شناسایی نشد.'
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid:
                                                    if reply_message_guid not in USERS[object_guid]:
                                                        result = await client.get_user_info(reply_message_guid)
                                                        user = result['user']
                                                        first_name = ''
                                                        if 'first_name' in user:    
                                                            first_name = user['first_name']
                                                        USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                    nickname = USERS[object_guid][reply_message_guid][2]
                                                    mess = Mini('لقبش : '+nickname)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'اصل':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = 'کاربر شناسایی نشد.'
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid:
                                                    if reply_message_guid not in USERS[object_guid]:
                                                        result = await client.get_user_info(reply_message_guid)
                                                        user = result['user']
                                                        first_name = ''
                                                        if 'first_name' in user:    
                                                            first_name = user['first_name']
                                                        USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                    infouser = USERS[object_guid][reply_message_guid][3]
                                                    mess = Mini('اصلش : '+infouser)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'مقام':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = 'کاربر شناسایی نشد.'
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid:
                                                    rank = 'کاربر عادی 👤'
                                                    if reply_message_guid == HOWNER:
                                                        rank = 'مالک ‍👑‍'
                                                    elif reply_message_guid in full_admins:
                                                        rank = 'ادمین ویژه ⭐'
                                                    elif reply_message_guid  in admins:
                                                        rank = 'ادمین ✨'

                                                    mess = Mini('مقامش : '+rank)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'گوید':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = 'کاربر شناسایی نشد.'
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid:
                                                    mess = Mini('گویدش : '+reply_message_guid)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                    if wordCount == 2:
                                        if command == 'تعداد پیام':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = 'کاربر شناسایی نشد.'
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid:
                                                    if reply_message_guid not in USERS[object_guid]:
                                                        result = await client.get_user_info(reply_message_guid)
                                                        user = result['user']
                                                        first_name = ''
                                                        if 'first_name' in user:    
                                                            first_name = user['first_name']
                                                        USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                    countms = USERS[object_guid][reply_message_guid][0]
                                                    mess = Mini('تعداد پیامش : '+str(countms))
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'تعداد اخطار':
                                            reply_message = await GetInfoByMessageId(client,object_guid,is_reply_message)
                                            mess = '» روی پیام پاک شده ریپلای زدی.'
                                            if reply_message:
                                                mess = 'کاربر شناسایی نشد.'
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid:
                                                    if reply_message_guid not in USERS[object_guid]:
                                                        result = await client.get_user_info(reply_message_guid)
                                                        user = result['user']
                                                        first_name = ''
                                                        if 'first_name' in user:    
                                                            first_name = user['first_name']
                                                        USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                    countwr = USERS[object_guid][reply_message_guid][1]
                                                    mess = Mini('تعداد اخطارش : '+str(countwr))
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        
                                else:
                                    if wordCount == 0:
                                        if command == 'ورژن':
                                            ResultME = await client.send_message(object_guid,'v'+NEWVR,message_id)
                                            CanSend = False
                                        elif command == 'لینک':
                                            try:
                                                result = await client.get_group_link(object_guid)
                                                group_title = INFOS[object_guid]['name']
                                                mess = '» لینک دعوت گپ [ '+group_title+' ] : \n'+result['join_link']
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            except:pass
                                            CanSend = False
                                        elif command == 'تاریخ':
                                            now = datetime.datetime.now()
                                            timestamp = str(time.mktime(now.timetuple()))
                                            date = requests.get(url = "https://one-api.ir/time/?token=833942:64919956105c3&action=timestamp&timestamp="+timestamp+"&timezone='Asia/Tehran'")
                                            date = date.json()
                                            mess = FormDate(date)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'ساعت':
                                            days = {'Saturday':'شنبه','Sunday':'یکشنبه','Monday':'دوشنبه','Tuesday':'سه شنبه','Wednesday':'چهارشنبه','Thursday':'پنج شنبه','Friday':'جمعه'}
                                            week = datetime.datetime.now().strftime("%A")
                                            if week in days:
                                                nowweek = days[week]
                                            now = datetime.datetime.now().strftime("%H:%M:%S")
                                            mess = '» '+now+' | '+nowweek
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'تاس':
                                            rand = random.randint(1,6)
                                            if rand == 1:
                                                mess = "⬤"
                                            elif rand == 2:
                                                mess = "⬤ ⬤"
                                            elif rand == 3:
                                                mess = "⬤ ⬤\n  ⬤"
                                            elif rand == 4:
                                                mess = "⬤ ⬤\n⬤ ⬤"
                                            elif rand == 5:
                                                mess = "⬤ ⬤\n  ⬤\n⬤ ⬤"
                                            elif rand == 6:
                                                mess = "⬤ ⬤\n⬤ ⬤\n⬤ ⬤"
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'سکه':
                                            rand = random.randint(1,2)
                                            if rand == 1:
                                                mess = '⦿ #شیر ⦿'
                                            else:
                                                mess = '⊝ #خط ⊝'
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'جوک':
                                            date = requests.get(url = "https://l8p.ir/jock/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                result = date['result']
                                                mess = "| #"+"ᒍOᑕK"+"\n\n"+result
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'چالش':
                                            date = requests.get(url = "https://l8p.ir/chalesh/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                mess = date['result']
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'بیو':
                                            date = requests.get(url = "https://l8p.ir/bio/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                result = date['result']
                                                mess = "| #"+"ᗷIO"+"\n\n"+result
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'فکت':
                                            date = requests.get(url = "https://l8p.ir/fact/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                result = date['result']
                                                mess = "| #"+"ᖴᗩᑕT"+"\n\n"+result
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'اعتراف':
                                            date = requests.get(url = "https://l8p.ir/etraf/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                result = date['result']
                                                mess = "| #"+"ᗴTᖇᗩᖴ"+"\n\n"+result
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'دانستنی':
                                            date = requests.get(url = "https://l8p.ir/dnstni/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                result = date['result']
                                                mess = "| #"+"ᗪᑎՏTᑎI"+"\n\n"+result
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'داستان':
                                            date = requests.get(url = "https://l8p.ir/story/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                result = date['result']
                                                mess = "| #"+"ՏTOᖇY"+"\n\n"+result
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'تکست':
                                            date = requests.get(url = "https://l8p.ir/text/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                result = date['result']
                                                mess = "| #"+"TᗴXT"+"\n\n"+result
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'فال':
                                            date = requests.get(url = "https://l8p.ir/fal/?key=Ab@4317247&chat_id="+object_guid+"&user_id="+guid_sender)
                                            date = date.json()
                                            if date['status'] == 200:
                                                result = date['result']
                                                title = result['title']
                                                rhyme = result['rhyme']
                                                meaning = result['meaning']
                                                title = Font_shec(title)
                                                title = "◄"+" "+title

                                                mess = "| #ᖴᗩᒪ\n\n"
                                                mess += "𝗧𝗜𝗧𝗟𝗘 »\n"+title+"\n\n"
                                                mess += "𝗥𝗛𝗬𝗠𝗘 »\n"
                                                lines = rhyme.split('\n')
                                                for line in lines:
                                                    mess += Mini(line)
                                                mess += "\n\n"
                                                mess += "𝗠𝗘𝗔𝗡𝗜𝗡𝗚 »\n\n"+meaning

                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'لقب':
                                            reply_message = await GetInfoByMessageId(client,object_guid,message_id)
                                            if reply_message:
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:    
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                nickname = USERS[object_guid][reply_message_guid][2]
                                                mess = Mini('لقبت : '+nickname)
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                                CanSend = False
                                        elif command == 'اصل':
                                            reply_message = await GetInfoByMessageId(client,object_guid,message_id)
                                            if reply_message:
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:    
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                infouser = USERS[object_guid][reply_message_guid][3]
                                                mess = Mini('اصلت : '+infouser)
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                                CanSend = False
                                        elif command == 'مقام':
                                            reply_message = await GetInfoByMessageId(client,object_guid,message_id)
                                            if reply_message:
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid:
                                                    rank = 'کاربر عادی 👤'
                                                    if reply_message_guid == HOWNER:
                                                        rank = 'مالک ‍👑‍'
                                                    elif reply_message_guid in full_admins:
                                                        rank = 'ادمین ویژه ⭐'
                                                    elif reply_message_guid  in admins:
                                                        rank = 'ادمین ✨'
                                                    mess = Mini('مقامت : '+rank)
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                                CanSend = False
                                        elif command == 'گوید':
                                            reply_message = await GetInfoByMessageId(client,object_guid,message_id)
                                            if reply_message:
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                mess = Mini('گویدت : '+reply_message_guid)
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                                CanSend = False
                                        elif command == 'خوشامدگویی':
                                            mess = INFOS[object_guid]['welcome']
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'خدافظی':
                                            mess = INFOS[object_guid]['bye']
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'بنر':
                                            mess = INFOS[object_guid]['baner']
                                            if len(mess) == 0:
                                                mess = 'بنری ثبت نشده است.'
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'قوانین':
                                            mess = INFOS[object_guid]['rols']
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'محدودیت':
                                            warnning = INFOS[object_guid]['warnning']
                                            mess = Title('محدودیت')
                                            mess += Mini('ارسال موارد زیر ممنوع است.'+' [ قفل 🚫 ]')
                                            locks = list(INFOS[object_guid]['locks'])
                                            for lock in Listlocks:
                                                if int(locks[Listlocks[lock]]) == 0:
                                                    mess += Mini(lock+' '+res)
                                            mess += '\n'
                                            mess += Mini('تعداد اخطار : '+str(INFOS[object_guid]['warnning']),False)
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                    elif wordCount == 1:
                                        if command == 'عدد شانسی':
                                            mess = str(random.randint(1,1000))
                                            mess = '°•'+mess
                                            ResultME = await client.send_message(object_guid,mess,message_id)
                                            CanSend = False
                                        elif command == 'تعداد پیام':
                                            reply_message = await GetInfoByMessageId(client,object_guid,message_id)
                                            if reply_message:
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:    
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                countms = USERS[object_guid][reply_message_guid][0]
                                                mess = Mini('تعداد پیامت : '+str(countms))
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                                CanSend = False
                                        elif command == 'تعداد اخطار':
                                            reply_message = await GetInfoByMessageId(client,object_guid,message_id)
                                            if reply_message:
                                                reply_message_guid = GetReplyGuid(reply_message)
                                                if reply_message_guid not in USERS[object_guid]:
                                                    result = await client.get_user_info(reply_message_guid)
                                                    user = result['user']
                                                    first_name = ''
                                                    if 'first_name' in user:    
                                                        first_name = user['first_name']
                                                    USERS[object_guid][reply_message_guid] = [0,0,first_name,'']
                                                countwr = USERS[object_guid][reply_message_guid][1]
                                                mess = Mini('تعداد اخطارت : '+str(countwr))
                                                ResultME = await client.send_message(object_guid,mess,message_id)
                                                CanSend = False
                                        

                if command == 'دستورات' or command == 'راهنما':
                    step = PorotectMSS(TimeMessages,object_guid)
                    if step:
                        NOTIC = '@l8pstudio_commands'
                        ResultME = await client.send_message(object_guid,NOTIC,message_id)
                
                if TIP2 and CanSend and ((is_reply_message and is_reply_message in ARMessages[object_guid]) or (not is_reply_message)):                    
                    if command.find(' !!') >= 0:
                        sended = False
                        steps = command.split(' !!')
                        ans = []
                        key = False
                        for step in steps:
                            step = step.strip()
                            if len(step) > 0:
                                if not key:
                                    key = step
                                else:
                                    ans.append(step)
                        if len(ans) <= 0:
                            if key in SPEAK:
                                cnt = str(len(SPEAK[key]))
                                SPEAK.pop(key)
                                mess = str(cnt)+' کلمه و کلیدواژه '+' [ '+key+' ] حذف شد. '
                                sended = True
                        else:
                            if key in SPEAK:
                                cnt = 0
                                for de in ans:
                                    try:
                                        SPEAK[key].remove(de)
                                        cnt +=1
                                    except:continue
                                if not cnt == 0:
                                    mess = str(cnt)+' کلمه از کلیدواژه '+' [ '+key+' ] حذف شد. '
                                    sended = True
                        if sended:
                            UPFILES(json,file_speak,SPEAK)
                            ResultME = await client.send_message(object_guid,mess,message_id)
                            CanSend = False
                    elif command.startswith('! '):
                        mess = Title('جملات مورد نظر')
                        searchs = command[1::]
                        empty = True
                        for word in SPEAK:
                            if searchs.find(word) >= 0:
                                empty = False
                                mess += Mini(word,False)
                                mess += '\n'
                                for answer in SPEAK[word]:
                                    mess += Mini(answer)
                                mess += '\n'
                        if empty:
                            mess = 'لغتی پیدا نشد.'
                        ResultME = await client.send_message(object_guid,mess,message_id)
                        CanSend = False
                    elif command.find(' ! ') >= 0:
                        steps = command.split(' ! ')
                        iskey = False
                        isadded = False
                        for step in steps:
                            if len(step) <= 0:
                                continue
                            if not iskey:
                                key = step.strip()
                                iskey = True
                            else:
                                step = step.strip()
                                if not key in SPEAK:
                                    SPEAK[key] = []
                                SPEAK[key].append(step)
                                isadded = True
                        if isadded:
                            UPFILES(json,file_speak,SPEAK)
                            mess = Mini('یاد گرفتم. ✅',False)
                            ResultME = await client.send_message(object_guid,mess,message_id)
                            CanSend = False         
                    elif command.startswith('/'):
                        try:
                            mess = ''
                            baner = INFOS[object_guid]['baner']
                            if len(baner) > 1 :
                                mess = baner
                            ResultME = await client.send_message(object_guid,"لطفا صبر کنید..."+'\n'+mess,message_id)
                            QUS = command.replace('/','')
                            QUS = QUS.strip()
                            if len(QUS) > 0:
                                result = requests.get("https://pyrubi.b80.xyz/chat.php/?text="+QUS)
                                date = result.json()
                                ResultME = await client.send_message(object_guid,date[0]['text'],message_id)
                                CanSend = False
                        except:pass
                    elif command.startswith('ویس زن'):
                        try:
                            mess = ''
                            baner = INFOS[object_guid]['baner']
                            if len(baner) > 1 :
                                mess = baner
                            ResultME = await client.send_message(object_guid,"لطفا صبر کنید..."+'\n'+mess,message_id)
                            QUS = command.replace('ویس زن','')
                            QUS = QUS.strip()
                            if len(QUS) > 0:
                                result = requests.get("https://pyrubi.b80.xyz/voice.php?mod=women&text="+QUS)
                                data = result.json()
                                url = data['result']['url']
                                response = requests.get(url)
                                name = datetime.datetime.now().strftime("%H_%M_%S")
                                name = str(name)
                                name_file = name+'.'+'mpeg'
                                with open(name_file, "wb") as file:
                                    file.write(response.content)
                                    file.close()
                                async with aiopen(r""+name_file, 'rb') as file:
                                    try:
                                        ResultME = await client.send_voice(object_guid, await file.read(),file_name=name_file,time='20',reply_to_message_id=message_id)
                                        CanSend = False
                                    except:pass
                                os.remove(name_file)
                        except:pass
                    elif command.startswith('ویس مرد'):
                        try:
                            mess = ''
                            baner = INFOS[object_guid]['baner']
                            if len(baner) > 1 :
                                mess = baner
                            ResultME = await client.send_message(object_guid,"لطفا صبر کنید..."+'\n'+mess,message_id)
                            QUS = command.replace('ویس مرد','')
                            QUS = QUS.strip()
                            if len(QUS) > 0:
                                result = requests.get("https://pyrubi.b80.xyz/voice.php?mod=man&text="+QUS)
                                data = result.json()
                                url = data['result']['url']
                                response = requests.get(url)
                                name = datetime.datetime.now().strftime("%H_%M_%S")
                                name = str(name)
                                name_file = name+'.'+'mpeg'
                                with open(name_file, "wb") as file:
                                    file.write(response.content)
                                    file.close()
                                async with aiopen(r""+name_file, 'rb') as file:
                                    try:
                                        ResultME = await client.send_voice(object_guid, await file.read(),file_name=name_file,time='20',reply_to_message_id=message_id)
                                        CanSend = False
                                    except:pass
                                os.remove(name_file)   
                        except:pass                        
                    elif command.startswith('لوگو2'):
                        try:
                            mess = ''
                            baner = INFOS[object_guid]['baner']
                            if len(baner) > 1 :
                                mess = baner
                            ResultME = await client.send_message(object_guid,"لطفا صبر کنید..."+'\n'+mess,message_id)
                            QUS = command.replace('لوگو2','')
                            QUS = QUS.strip()
                            if len(QUS) > 0:
                                result = requests.get("https://pyrubi.b80.xyz/Logo-top.php?page=90&text="+QUS)
                                data = result.json()
                                urls = data['result']
                                rand = random.randint(0,len(urls)-1)
                                url = urls[rand].replace(';','&')
                                response = requests.get(url)
                                name_file = QUS+'.'+'png'
                                with open(name_file, "wb") as file:
                                    file.write(response.content)
                                    file.close()
                                async with aiopen(r""+name_file, 'rb') as file:
                                    try:
                                        ResultME = await client.send_file(object_guid, await file.read(),file_name=name_file,reply_to_message_id=message_id)
                                        CanSend = False
                                    except:pass
                                os.remove(name_file)   
                        except:pass
                    elif command.startswith('لوگو'):
                        try:
                            mess = ''
                            baner = INFOS[object_guid]['baner']
                            if len(baner) > 1 :
                                mess = baner
                            ResultME = await client.send_message(object_guid,"لطفا صبر کنید..."+'\n'+mess,message_id)
                            QUS = command.replace('لوگو','')
                            QUS = QUS.strip()
                            if len(QUS) > 0:
                                rand = str(random.randint(1,100))
                                result = requests.get("https://pyrubi.b80.xyz/Logo.php?style="+rand+"&text="+QUS)
                                data = result.json()
                                urls = data['result']
                                rand = random.randint(0,len(urls)-1)
                                url = urls[rand]
                                response = requests.get(url)
                                name_file = QUS+'.'+'png'
                                with open(name_file, "wb") as file:
                                    file.write(response.content)
                                    file.close()
                                async with aiopen(r""+name_file, 'rb') as file:
                                    try:
                                        ResultME = await client.send_file(object_guid, await file.read(),file_name=name_file,reply_to_message_id=message_id)
                                        CanSend = False
                                    except:pass
                                os.remove(name_file)
                        except:pass
                    elif command.startswith('عکس'):
                        try:
                            mess = ''
                            baner = INFOS[object_guid]['baner']
                            if len(baner) > 1 :
                                mess = baner
                            ResultME = await client.send_message(object_guid,"لطفا صبر کنید..."+'\n'+mess,message_id)
                            QUS = command.replace('عکس','')
                            QUS = QUS.strip()
                            if len(QUS) > 0:
                                QUS = requests.get("https://pyrubi.b80.xyz/Trans.php/?text="+QUS)
                                QUS = QUS.json()
                                QUS = QUS[1::]
                                result = requests.get("https://pyrubi.b80.xyz/img.php/?text="+QUS)
                                data = result.json()
                                url = data['output']
                                prompt = data['prompt']
                                # prompt = requests.get("https://one-api.ir/translate/?token=833942:64919956105c3&action=google&lang=fa&q="+prompt)
                                # prompt = prompt.json()
                                # prompt = prompt['result']
                                response = requests.get(url)
                                name_file = QUS+'.'+'png'
                                with open(name_file, "wb") as file:
                                    file.write(response.content)
                                    file.close()
                                async with aiopen(r""+name_file, 'rb') as file:
                                    try:
                                        ResultME = await client.send_file(object_guid, await file.read(),file_name=name_file,reply_to_message_id=message_id)
                                        CanSend = False
                                    except:pass
                                os.remove(name_file)   
                        except:pass
                            
                step1 = 1
                step2 = True
                step3 = True
                if not TIP2:
                    step2 = PorotectMSS(TimeMessages,object_guid)
                    key = Listset['سخنگو']
                    keys = list(INFOS[object_guid]['setting'])
                    step1 = int(keys[key])
                    nums = random.randint(1,10)
                    step3 = False
                    if not nums == 5 and not nums == 8 and not nums == 2:
                        step3 = True
                if step1 == 1 and step2 and CanSend and step3:
                    start = False
                    if LSMessage[object_guid][0] == LSMessage[object_guid][1] and not is_reply_message:
                        start = True
                    if is_reply_message and is_reply_message in ARMessages[object_guid]:
                        start = True
                    elif not is_reply_message:
                        klids = ['ربات','سلام','صلام','بای','خدافظ','فعلا','خوش','خش','های','خدانگهدار','خدافز','ثلام','سالام','شلام','hi','hello']
                        for klid in klids:
                            if command.find(klid) >= 0:
                                start = True
                                break
                    if start:
                        key = Listset['سخنگو شخصی']
                        keys = list(INFOS[object_guid]['setting'])
                        step = int(keys[key])
                        if step == 1 and CanSend:
                            keies = []
                            for word in SPEAK:
                                if command.find(word) >= 0:
                                    if len(SPEAK[word]) > 0:
                                        rand = random.randint(0,len(SPEAK[word])-1)
                                        if rand >= 0:
                                            answer = SPEAK[word][rand]
                                            ResultME = await client.send_message(object_guid,answer,message_id)
                                            CanSend = False
                                            break
                        if CanSend:
                            key = Listset['سخنگو پیشفرض']
                            keys = list(INFOS[object_guid]['setting'])
                            step = int(keys[key])
                            if step == 1:
                                keies = []
                                for word in SPEAKD:
                                    if command.find(word) >= 0:
                                        if len(SPEAKD[word]) > 0:
                                            rand = random.randint(0,len(SPEAKD[word])-1)
                                            if rand >= 0:
                                                answer = SPEAKD[word][rand]
                                                ResultME = await client.send_message(object_guid,answer,message_id)
                                                CanSend = False
                                                break
                
                try:
                    if ResultME:
                        now = datetime.datetime.now()
                        timestamp = int(time.mktime(now.timetuple()))
                        message_sended_id = ResultME['message_update']['message_id']
                        LSMessage[object_guid][0] = message_sended_id
                        LSMessage[object_guid][1] = message_sended_id
                        if len(ARMessages[object_guid]) >= 25:
                            ARMessages[object_guid].pop(0)
                            ARMessages[object_guid].append(message_sended_id)
                        else:
                            ARMessages[object_guid].append(message_sended_id)
                        if len(TimeMessages[object_guid]) >= 20:
                            TimeMessages[object_guid].pop(0)
                            TimeMessages[object_guid].append(timestamp)
                        else:
                            TimeMessages[object_guid].append(timestamp)
                    else:
                        LSMessage[object_guid][0] = message_id
                except:pass

                # insert info users
                if object_guid not in USERS:
                    USERS[object_guid] = {}
                if guid_sender not in USERS[object_guid]:
                    result = await client.get_user_info(guid_sender)
                    user = result['user']
                    first_name = ''
                    if 'first_name' in user:
                        first_name = user['first_name']
                    USERS[object_guid][guid_sender] = [0,0,first_name,'']
                # UPDATE INFORMATIONS
                INFOS[object_guid]['messages'] += 1
                UPFILES(json,File_infos,INFOS)

                USERS[object_guid][guid_sender][0] += 1
                UPFILES(json,File_users,USERS)
                
                IsUpdated = True
                CanSend = False

            # OWNER IN ANOTHER GROUPS
            elif message.type == 'Group' and guid_sender in OWNER and CanSend:
                # reply and no reply
                if is_reply_message:pass
                else:
                    # one word command
                    if wordCount == 0 and CanSend:
                        if command == 'فعال':
                            now = datetime.datetime.now()
                            timestamp = int(time.mktime(now.timetuple()))
                            if object_guid not in INFOS:
                                admins = {}
                                try:
                                    result = await client.get_group_admin_members(object_guid)
                                    if result:
                                            for admin in result['in_chat_members']:
                                                if 'first_name' in admin:
                                                    admins[admin['member_guid']] = admin['first_name']
                                                else:
                                                    admins[admin['member_guid']] = 'بدون نام'
                                except:pass
                                result = await client.get_group_info(object_guid)
                                group_title = result['group']['group_title']
                                INFOS[object_guid] = {}
                                INFOS[object_guid]['state'] = True
                                INFOS[object_guid]['date'] = timestamp
                                INFOS[object_guid]['name'] = group_title
                                INFOS[object_guid]['locks'] = "111111100011111111111111111111111111"
                                INFOS[object_guid]['keys'] =  "11111111111111111111111111111111"
                                INFOS[object_guid]['setting'] = "11111111111111111111111111111111"
                                INFOS[object_guid]['welcome'] =  '+ به گپ [ '+group_title+' ] خوش آمدی عزیزم 💎✨\n- بمونی برامون +×)'
                                INFOS[object_guid]['bye'] =  '🤲'
                                INFOS[object_guid]['rols'] =  '📜 قوانین گپ [ '+group_title+' ] به شرح زیر میباشد.\n\n» احترام به کاربران\n» احترام به عقاید و فرهنگ ها\n» ارسال نکردن تبلیغات [آیدی.لینک.فوروارد]\n» ممبر دزدی نکنید.\n» اسپم و محتوای نامناسب ارسال نکنید.'
                                INFOS[object_guid]['baner'] = ''
                                INFOS[object_guid]['warnning'] = 3
                                INFOS[object_guid]['admins'] = admins
                                INFOS[object_guid]['full_admins'] = {}
                                INFOS[object_guid]['left'] = 0
                                INFOS[object_guid]['join'] = 0
                                INFOS[object_guid]['ban'] = 0
                                INFOS[object_guid]['add'] = 0
                                INFOS[object_guid]['messages'] = 0
                                # INFOS[object_guid]['type_messages'] = []
                                INFOS[object_guid]['owner'] = guid_sender
                                UPFILES(json,File_infos,INFOS)
                                
                                LSMessage[object_guid] = [0,1]
                                ARMessages[object_guid] = []
                                TimeMessages[object_guid] = []

                                NOTIC = 'this is a free bot in rubika form @l8pstudio'
                                await client.send_message(object_guid,NOTIC)
                                File_owner_is = True
                                CanSend = False
                            if object_guid not in USERS:
                                USERS[object_guid] = {}
                                # mss , warning , name
                                result = await client.get_user_info(guid_sender)
                                user = result['user']
                                first_name = ''
                                if 'first_name' in user:
                                    first_name = user['first_name']
                                USERS[object_guid][guid_sender] = [0,0,first_name,'']
                                UPFILES(json,File_users,USERS)
                            await client.send_message(object_guid,'» ربات فعال است. ✅',message_id)
                            CanSend = False
                        elif command == 'لفت':
                            mess = '» لفت دادم. ✅'
                            await client.leave_group(object_guid)
                            await client.send_message(guid_sender,mess,message_id)
                            CanSend = False
                        
                    if command.startswith('برو') and CanSend:
                        command = command.replace('برو','')
                        command = command.strip()
                        if command.startswith("https://rubika.ir/joing/"):
                            link = command.replace("https://rubika.ir/joing/","")
                            link = link.strip()
                            link = link.upper()
                            result = await client.join_group(link)
                            mess = '» لینک گروه نامعتبر است. 🚫'
                            try:
                                if result['is_valid']:
                                    mess = '» عضو گروه شدم. ✅'
                            except:pass
                            await client.send_message(object_guid,mess,message_id)
                            CanSend = False
                        elif command.startswith("https://rubika.ir/joinc/"):
                            link = command.replace("https://rubika.ir/joinc/","")
                            link = link.strip()
                            link = link.upper()
                            result = await client.join_channel_by_link(link)
                            mess = '» لینک کانال نامعتبر است. 🚫'
                            try:
                                if result['is_valid']:
                                    mess = '» عضو کانال شدم. ✅'
                            except:pass
                            await client.send_message(object_guid,mess,message_id)
                            CanSend = False
                        elif command.startswith("@"):
                            username = command.replace("@","")
                            username = username.strip()
                            username = username.upper()
                            result = await client.get_object_by_username(username)
                            if 'Channel' in result:
                                direction_guid = result['chat']['object_guid']
                                result = await client.join_channel(direction_guid)
                                mess = '» ایدی کانال نامعتبر است. 🚫'
                                try:
                                    if result['is_valid']:
                                        mess = '» عضو کانال شدم. ✅'
                                except:pass
                                await client.send_message(object_guid,mess,message_id)
                                CanSend = False
        
            # FOR OWNERS IN PRIVATE
            elif message.type == 'User' and guid_sender in OWNER and CanSend:
                if command.startswith("https://rubika.ir/joing/"):
                    link = command.replace("https://rubika.ir/joing/","")
                    link = link.strip()
                    link = link.upper()
                    result = await client.join_group(link)
                    mess = '» لینک گروه نامعتبر است. 🚫'
                    try:
                        if result['is_valid']:
                            mess = '» عضو گروه شدم. ✅'
                    except:pass
                    await client.send_message(object_guid,mess,message_id)
                    CanSend = False
                elif command.startswith("https://rubika.ir/joinc/"):
                    link = command.replace("https://rubika.ir/joinc/","")
                    link = link.strip()
                    link = link.upper()
                    result = await client.join_channel_by_link(link)
                    mess = '» لینک کانال نامعتبر است. 🚫'
                    try:
                        if result['is_valid']:
                            mess = '» عضو کانال شدم. ✅'
                    except:pass
                    await client.send_message(object_guid,mess,message_id)
                    CanSend = False
                elif command.startswith("@"):
                    username = command.replace("@","")
                    username = username.strip()
                    username = username.upper()
                    result = await client.get_object_by_username(username)
                    if 'Channel' in result:
                        direction_guid = result['chat']['object_guid']
                        result = await client.join_channel(direction_guid)
                        mess = '» ایدی کانال نامعتبر است. 🚫'
                        try:
                            if result['is_valid']:
                                mess = '» عضو کانال شدم. ✅'
                        except:pass
                        await client.send_message(object_guid,mess,message_id)
                        CanSend = False
                elif command.startswith('لفت'):
                        link = command.replace('لفت',"")
                        link = link.replace("https://web.rubika.ir/#c=","")
                        link = link.replace("https://rubika.ir/#c=","")
                        gap_guid = link.strip()
                        mess = '» لفت دادم. ✅'
                        try:
                            await client.leave_group(gap_guid)
                        except:
                            mess = '» گوید نامعتبر است. 🚫'
                        await client.send_message(object_guid,mess,message_id)
                        CanSend = False
        

            # FOR MEMBERS 
            elif message.type == 'User' and CanSend:
                for guid_gap in INFOS:
                    key = Listset['ضد تبچی']
                    keys = list(INFOS[guid_gap]['setting'])
                    step1 = int(keys[0])
                    step2 = int(keys[key])
                    if step2 == 1:
                        #GET GAP INFO
                        HOWNER = INFOS[guid_gap]['owner']
                        full_admins = INFOS[guid_gap]['full_admins']
                        admins = INFOS[guid_gap]['admins']

                        # validate the user
                        TIP0 = False
                        TIP1 = False
                        TIP2 = False
                        TIP3 = False
                        if guid_sender == Coder:
                            TIP0 = True
                            TIP1 = True
                            TIP2 = True
                            TIP3 = True
                        if guid_sender == HOWNER:
                            TIP1 = True
                            TIP2 = True
                            TIP3 = True
                        elif guid_sender in full_admins:
                            TIP2 = True
                            TIP3 = True
                        elif guid_sender in admins:
                            TIP3 = True

                        if not TIP3:
                            try:
                                await client.set_group_admin(guid_gap,guid_sender,["DeleteGlobalAllMessages"],'SetAdmin')
                                if guid_gap not in USERS:
                                    USERS[guid_gap] = {}
                                if guid_sender not in USERS[guid_gap]:
                                    first_name = ''
                                    result = await client.get_user_info(guid_sender)
                                    user = result['user']
                                    if 'first_name' in user:
                                        first_name = user['first_name']
                                    USERS[guid_gap][guid_sender] = [0,0,first_name,'']
                                INFOS[guid_gap]['admins'][guid_sender] = USERS[guid_gap][guid_sender][2]
                                # await ExtraInfo(client,INFOS,guid_gap,None,"welcome",Listset,TimeMessages)
                                UPFILES(json,File_infos,INFOS)
                                UPFILES(json,File_users,USERS)
                                if step1 == 1:
                                    mess = 'اد شدی. ✅'
                                    baner = INFOS[guid_gap]['baner']
                                    if len(baner) > 1 :
                                        mess = baner
                                    await client.send_message(guid_sender,mess,message_id)
                            except:pass
                        
                        

            # FOR CODER IN PRIVATE
            if(message.type == 'User' and object_guid == Coder  and guid_sender == Coder and CanSend):
                if command == 'لینک':pass
                elif command == 'پاک':
                    await client.delete_user_chat(Coder,message_id)
                elif not is_reply_message:
                    context = str(message)
                    await client.send_message(Coder,context)
                CanSend = False


        await client.run_until_disconnected()

run(main())