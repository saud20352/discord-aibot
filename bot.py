import os
import discord
from discord.ext import commands
import google.generativeai as genai

# إعدادات الصلاحيات الأساسية
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# إعداد مفتاح جوجل جيميني بالنموذج المطلوب
genai.configure(api_key="AQ.Ab8RN6JUxb7SXQvppw971NTXe6Jlpd9Xe4HoPYUaXHzKLhprzA")
model = genai.GenerativeModel('gemini-3.6-flash')

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} متصل وجاهز للعمل بكامل طاقته!")

# ترحيب بالعضو الجديد
@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
    if welcome_channel:
        await welcome_channel.send(f"أهلاً بك يا {member.name} في السيرفر! 👑 اسألني أي شيء وسأجيبك فوراً.")

# تشغيل الذكاء الاصطناعي على أي رسالة تنكتب في الشات
@bot.event
async def on_message(message):
    # عشان البوت ما يرد على نفسه ويدخل في لوب
    if message.author == bot.user:
        return

    # تجاهل الأوامر لو حبيت، أو خل البوت يرد مباشرة على كلامك
    async with message.channel.typing():
        try:
            # إرسال رسالتك مباشرة لجوجل جيميني واستقبال الرد
            response = model.generate_content(message.content)
            answer = response.text
            
            # تقسيم الإجابة لو كانت طويلة عشان ما تعطيني خطأ في ديسكورد
            if len(answer) > 2000:
                for i in range(0, len(answer), 2000):
                    await message.channel.send(answer[i:i+2000])
            else:
                await message.channel.send(answer)
                
        except Exception as e:
            print(f"خطأ: {e}")

    await bot.process_commands(message)

# تشغيل البوت
bot.run(os.getenv("DISCORD_TOKEN"))
