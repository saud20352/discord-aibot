import os
import discord
from discord.ext import commands
from google import genai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# استخدام العميل الحديث المتوافق مع مفاتيح AQ
client = genai.Client(api_key="AQ.Ab8RN6L6FXHdSSk-dPYda-_kkoyt_7QjUKuLrV4S1YKNB4WzUQ")

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} متصل ويعمل كذكاء اصطناعي بنجاح تام!")

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
    
    # ردود سريعة للسلام
    if "سلام" in content or "السلام عليكم" in content:
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته يا هلا فيك يا {message.author.name} 👑")
        return

    # الرد على أي سؤال في العالم كذكاء اصطناعي متكامل
    if len(content) > 0 and not content.startswith("!"):
        async with message.channel.typing():
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=content,
                )
                if response and response.text:
                    answer = response.text
                    if len(answer) > 2000:
                        for i in range(0, len(answer), 2000):
                            await message.channel.send(answer[i:i+2000])
                    else:
                        await message.channel.send(answer)
                else:
                    await message.channel.send("أهلاً بك! استلمت سؤالك، لكن لم أتمكن من صياغة إجابة.")
            except Exception as e:
                print(f"خطأ في الاتصال: {e}")
                await message.channel.send(f"يا هلا فيك يا {message.author.name}! أنا جاهز لمساعدتك في كل ما تطلب وتطوير السيرفر معك 🚀")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
