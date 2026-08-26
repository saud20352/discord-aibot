import os
import discord
from discord.ext import commands
import requests
import json

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

API_KEY = "AQ.Ab8RN6L6FXHdSSk-dPYda-_kkoyt_7QjUKuLrV4S1YKNB4WzUQ"

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} شغال وجاهز!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()
    
    if "سلام" in content or "السلام عليكم" in content:
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته يا هلا فيك يا {message.author.name} 👑")
        return

    if len(content) > 0 and not content.startswith("!"):
        async with message.channel.typing():
            try:
                # استخدام نموذج gemini-1.5-flash مع الـ API الصحيح
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [{"text": content}]
                    }]
                }
                
                response = requests.post(url, headers=headers, data=json.dumps(data))
                result = response.json()
                
                # طباعة الرد الفعلي من جوجل
                if "candidates" in result:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    if len(answer) > 2000:
                        answer = answer[:2000]
                    await message.channel.send(answer)
                else:
                    # في حال رجع خطأ من جوجل نفسه، نطبع الخطأ عشان نعرفه
                    print(f"رد جوجل: {result}")
                    await message.channel.send(f"عذراً يا {message.author.name}، استلمت سؤالك ولكن مفتاح الـ API يطلب صلاحيات إضافية أو نموذج مختلف.")
                
            except Exception as e:
                print(f"خطأ برمجي: {e}")
                await message.channel.send(f"عذراً يا {message.author.name}، حدث خطأ في الاتصال.")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
