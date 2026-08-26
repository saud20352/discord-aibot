import os
import discord
from discord.ext import commands
from google import genai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# استخدام المفتاح الجديد مع العميل الحديث
client = genai.Client(api_key="AQ.Ab8RN6JUxb7SXQvppw971NTXe6Jlpd9Xe4HoPYUaXHzKLhprzA")

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} متصل وجاهز للرد على كل شي بالنموذج المطلوب!")

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

    # الرد على أي سؤال باستخدام نموذج gemini-3.6-flash
    if len(content) > 0 and not content.startswith("!"):
        async with message.channel.typing():
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=content,
                )
                if response and response.text:
                    answer = response.text
                    if len(answer) > 2000:
                        answer = answer[:2000]
                    await message.channel.send(answer)
                else:
                    await message.channel.send("أهلاً بك! استلمت سؤالك، لكن لم أتمكن من صياغة إجابة.")
            except Exception as e:
                print(f"خطأ في الاتصال: {e}")
                await message.channel.send("عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي. جرب مرة أخرى!")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
