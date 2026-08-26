import os
import discord
from discord.ext import commands
import google.generativeai as genai

# إعدادات الصلاحيات الأساسية
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# إعداد مفتاح جوجل جيميني
genai.configure(api_key="AQ.Ab8RN6JUxb7SXQvppw971NTXe6Jlpd9Xe4HoPYUaXHzKLhprzA")
model = genai.GenerativeModel('gemini-3.6-flash')

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} متصل وجاهز للعمل!")

# 1️⃣ الرد التلقائي على الرسائل العادية (مثل: سلام، هلا، إلخ)
@bot.event
async def on_message(message):
    # عشان البوت ما يرد على نفسه ويدخل في لوب (حلقة مفرغة)
    if message.author == bot.user:
        return

    content = message.content.lower()

    # لو الشخص كتب سلام أو هلا
    if "سلام" in content or "السلام عليكم" in content:
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته يا هلا فيك يا {message.author.name} 👑")
        return
    
    if "هلا" in content or "اهلن" in content:
        await message.channel.send(f"أهلين وسهلين! منور السيرفر 🚀")
        return

    # 2️⃣ أمر الذكاء الاصطناعي لو تبي تسأله أي شيء باستخدام كلمة !سؤال
    if content.startswith("!سؤال"):
        question = message.content[5:].strip()
        if question:
            async with message.channel.typing():
                try:
                    response = model.generate_content(question)
                    answer = response.text
                    
                    if len(answer) > 2000:
                        for i in range(0, len(answer), 2000):
                            await message.channel.send(answer[i:i+2000])
                    else:
                        await message.channel.send(answer)
                except Exception as e:
                    await message.channel.send(f"⚠️ حدث خطأ: {e}")
        else:
            await message.channel.send("اكتب بعد كلمة !سؤال الشيء اللي تبي تسأل عنه.")
        return

    # السماح بباقي الأوامر لو وجدت
    await bot.process_commands(message)

# تشغيل البوت بأمان
bot.run(os.getenv("DISCORD_TOKEN"))
