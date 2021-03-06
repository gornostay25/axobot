from telethon import TelegramClient,events
import time,requests,re,os,random,asyncio
axo_bot = "AXOClaimBot"
api_id= 2376043
api_hash= "e992d55690981f66c95ce87695434296"

t = time.localtime()
starttime = str(t.tm_hour)+":"+str(t.tm_min)

ocr_api = str(os.sys.argv[1]) if len(os.sys.argv) > 1 and len(os.sys.argv[1]) > 5 else "0748b1c15b88957"

isActive = True
client = TelegramClient(
    'axo_bot_'+(str(os.sys.argv[2]) if len(os.sys.argv) > 2 else "docker"),
    api_id, 
    api_hash
)
print(ocr_api)
client.start()
print("start app "+client.session.filename)

@client.on(events.NewMessage(outgoing=True, pattern='!bot_(s|a|d|save)'))
async def handler(event):
    global isActive
    if event._chat.username == axo_bot:
        if re.findall(r'_s$',event.message.message):
            m = await event.respond('Bot is '+("active" if isActive else "deactivated")+"\nStared at: "+starttime)
        elif re.findall(r'_a',event.message.message):
            m = await event.respond('Bot is activated! \nPlease whait 5 min')
            isActive = True
            print('Bot is activated! \nPlease whait 5 min')
        elif re.findall(r'_d',event.message.message):
            m = await event.respond('Bot is deactivated! \nPlease whait 5 min')
            isActive = False
            print('Bot is deactivated! \nPlease whait 5 min')
        elif re.findall(r'_save',event.message.message):
            await client.send_file("me",client.session.filename)
            await client.delete_messages(event.chat_id, [event.id])
            return
        await asyncio.sleep(5)
        await client.delete_messages(event.chat_id, [event.id, m.id])


async def get_messages(client):
    messsages = await client.get_messages(axo_bot,limit=3)
    for mess in messsages:
        if (mess.sender.username == axo_bot):
            return mess
    return
            



async def ocrible(mess,client):
    while 1:
        t = time.localtime()
        path = await mess.download_media(str(t.tm_mday)+str(t.tm_hour)+str(t.tm_min)+str(t.tm_sec)+str(api_id)+str(random.randint(0,9999))+".jpg")
        with open(path,"rb") as f:
            r = requests.post("https://api.ocr.space/parse/image",
            files={path: f},
            data={
            'apikey': ocr_api,

            "language": "eng",
            "isOverlayRequired": True,
            "IsCreateSearchablePDF": False,
            "isSearchablePdfHideTextLayer": True,
            "detectOrientation": False,
            "isTable": False,
            "scale": True,
            "OCREngine": 2,
            "detectCheckbox": False,
            "checkboxTemplate": 0
            })  
            try:
                r = r.json()['ParsedResults'][0]['TextOverlay']['Lines'][0]['LineText']
            except:
                await client.send_message("me", r.text)
                print("error ocr")
                os.remove(path)
                await asyncio.sleep(random.randint(2*60,4*60))
                continue
        code = re.findall(r'\d+',r)[0]
        await client.send_message(axo_bot, code)
        print("send code: "+str(code))
        await asyncio.sleep(20)
        mess = await get_messages(client)
        if not mess:
            print("bot whaiting 30min")
            await asyncio.sleep(random.randint(30*60,33*60))
            return None
            
        if mess.photo:
            await asyncio.sleep(random.randint(10,30))
            continue
        else:
            print("+ 1$")
            print("sleep 16-17,5min")
            os.remove(path)
            #await asyncio.sleep(16*60)
            await asyncio.sleep(random.randint(16*60,17.5*60))
            return

async def main():
    while 1:
        try:
            if not isActive:
                print("no activated send \"!bot_a\" to activate")
                await asyncio.sleep(5*60)
                continue
            mess = await get_messages(client)
            if not mess:
                print("bot whaiting 30min")
                await asyncio.sleep(30*60)
            print("- if")
            if not re.match(r'captcha',mess.message):
                print("- asq captcha")
                await client.send_message(axo_bot, '????Claim')
                await asyncio.sleep(5)
                mess = await get_messages(client)
                if not mess:
                    print("bot whaiting 30min")
                    await asyncio.sleep(30*60)
                    continue
                print("-"*30)
                print(mess.message.encode('ascii',"ignore").decode())
                print("-"*30)
                if mess.photo:
                    print("- yes captcha")
                    print("go ocr")
                    await ocrible(mess,client)
                else:
                    print("no photo!!!/sleep 3-5min")
                    await asyncio.sleep(random.randint(3*60,5*60))
                
            elif (mess.photo):
                print("- yes captcha")
                print("-"*30)
                print(mess.message.encode('ascii',"ignore").decode())
                print("-"*30)
                print("go ocr")
                await ocrible(mess,client)
            else:
                print("- wtf?")
                print("-"*30)
                print(mess.message.encode('ascii',"ignore").decode())
                print("-"*30)
        except KeyboardInterrupt:
            print("exit")
            print("-"*30)
            print("Dont forget to save a session!!!\n!bot_save ("+client.session.filename+")")
            exit()

while 1:
    try:
        client.loop.run_until_complete(main())
    except requests.exceptions.ConnectionError:
        pass
