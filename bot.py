import os
import discord
from discord.ext import commands
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ضبط المفتاح بالطريقة الكلاسيكية المستقرة
genai.configure(api_key="AQ.Ab8RN6L6FXHdSSk-dPYda-_kkoyt_7QjUKuLrV4S1YKNB4WzUQ")
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} متصل وجاهز للرد كذكاء اصطناعي!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()
    
    if "سلام" in content or "السلام عليكم" in content:
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته يا هلا فيك يا {message.author.name} 👑")
        return

    # الرد المباشر على أي سؤال في العالم
    if len(content) > 0 and not content.startswith("!"):
        async with message.channel.typing():
            try:
                response = model.generate_content(content)
                if response and response.text:
                    answer = response.text
                    if len(answer) > 2000:
                        answer = answer[:2000]
                    await message.channel.send(answer)
                else:
                    await message.channel.send("عذراً، لم أتمكن من صياغة الإجابة.")
            except Exception as e:
                print(f"خطأ: {e}")
                await message.channel.send(f"يا هلا فيك يا {message.author.name}! أنا هنا لمساعدتك في كل ما تطلب وتطوير السيرفر معك 🚀")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
