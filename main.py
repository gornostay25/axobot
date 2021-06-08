from telethon import TelegramClient
import time,requests,re,os,random
axo_bot = "AXOClaimBot"
api_id= 2376043
api_hash= "e992d55690981f66c95ce87695434296"

ocr_api = "0748b1c15b88957"


client = TelegramClient('axo_bot_'+str(os.sys.argv[1]), api_id, api_hash)
client.start()
print("start app")

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
                continue
        await client.send_message(axo_bot, re.findall(r'\d+',r)[0])
        time.sleep(2)
        mess = await client.get_messages(axo_bot)
        mess=mess[0]
        if mess.photo:
            continue
        else:
            print("+ 1$")
            print("sleep 16min")
            os.remove(path)
            time.sleep(16*60)
            return

async def main():
    while 1:
        try:
            mess = await client.get_messages(axo_bot)
            mess= mess[0]
            print("- if")
            if not re.match(r'captcha',mess.message):
                print("- not captcha")
                await client.send_message(axo_bot, '💵Claim')
                time.sleep(2)
                mess = await client.get_messages(axo_bot)
                mess=mess[0]
                print("-"*30)
                print(mess.message)
                print("-"*30)
                if mess.photo:
                    print("go ocr")
                    await ocrible(mess,client)
                else:
                    print("no photo/sleep 3min")
                    time.sleep(3*60)
                
            elif (mess.photo):
                print("- yes captcha")
                print("-"*30)
                print(mess.message)
                print("-"*30)
                print("go ocr")
                await ocrible(mess,client)
            else:
                print("- wtf?")
                print("-"*30)
                print(mess.message)
                print("-"*30)
        except KeyboardInterrupt:
            print("exit")
            exit()

client.loop.run_until_complete(main())
