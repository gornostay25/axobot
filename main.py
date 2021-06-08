from telethon import TelegramClient,events
import time,requests,re,os,random,asyncio
axo_bot = "AXOClaimBot"
api_id= 2376043
api_hash= "e992d55690981f66c95ce87695434296"

ocr_api = str(os.sys.argv[1]) if len(os.sys.argv) > 2 else "0748b1c15b88957"

isActive = False
client = TelegramClient(
    'axo_bot_'+(str(os.sys.argv[2]) if len(os.sys.argv) > 3 else "docker"),
    api_id, 
    api_hash
)
print(ocr_api)
client.start()
print("start app")

@client.on(events.NewMessage(outgoing=True, pattern='!bot_(s|a|d)'))
async def handler(event):
    global isActive
    if event._chat.username == axo_bot:
        if re.findall(r'_s',event.message.message):
            m = await event.respond('Bot is '+("active" if isActive else "deactivated"))
        elif re.findall(r'_a',event.message.message):
            m = await event.respond('Bot is activated! \nPlease whait 5 min')
            isActive = True
        elif re.findall(r'_d',event.message.message):
            m = await event.respond('Bot is deactivated! \nPlease whait 5 min')
            isActive = False
        await asyncio.sleep(5)
        await client.delete_messages(event.chat_id, [event.id, m.id])


async def get_messages(client):
    messages = await client.get_messages(axo_bot,limit=3)
    for mess in messages:
        if (mess.sender.username == axo_bot):
            return mess
        else:
            print("recive own mess(((")
    return None



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
                await client.send_message(axo_bot, r.text)
                print("error ocr")
                os.remove(path)
                await asyncio.sleep(2*60)
                continue
        await client.send_message(axo_bot, re.findall(r'\d+',r)[0])
        await asyncio.sleep(2)
        mess = await get_messages(client)
        if not mess:
            print("bot whaiting 30min")
            await asyncio.sleep(30*60)
            return None
            
        if mess.photo:
            continue
        else:
            print("+ 1$")
            print("sleep 16min")
            os.remove(path)
            await asyncio.sleep(16*60)
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
                await client.send_message(axo_bot, '💵Claim')
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
                    print("no photo!!!/sleep 3min")
                    await asyncio.sleep(3*60)
                
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
            exit()

client.loop.run_until_complete(main())
