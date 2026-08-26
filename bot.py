import os
import discord
from discord.ext import commands
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# إعداد مفتاح جيميني بالنموذج السريع والمضمون
genai.configure(api_key="AQ.Ab8RN6JUxb7SXQvppw971NTXe6Jlpd9Xe4HoPYUaXHzKLhprzA")
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} شغال وجاهز بكامل طاقته!")

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
    if welcome_channel:
        await welcome_channel.send(f"أهلاً بك يا {member.name} في السيرفر! 👑 اسألني أي شيء وسأجيبك فوراً.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()
    
    # 1. ردود سريعة للسلام والتحيات
    if "سلام" in content or "السلام عليكم" in content:
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته يا هلا فيك يا {message.author.name} 👑")
        return
    
    if "هلا" in content or "اهلن" in content:
        await message.channel.send(f"أهلين وسهلين! منور السيرفر 🚀")
        return

    # 2. أي رسالة ثانية يرسلها للذكاء الاصطناعي ويرد عليها فوراً
    if len(content) > 0 and not content.startswith("!"):
        try:
            response = model.generate_content(content)
            if response and response.text:
                answer = response.text
                if len(answer) > 2000:
                    answer = answer[:2000]
                await message.channel.send(answer)
        except Exception as e:
            print(f"خطأ في الرد: {e}")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
