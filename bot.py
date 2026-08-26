import os
import discord
from discord.ext import commands
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ضبط مفتاح الاتصال
genai.configure(api_key="AQ.Ab8RN6JUxb7SXQvppw971NTXe6Jlpd9Xe4HoPYUaXHzKLhprzA")
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} شغال وجاهز!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()
    
    # ردود سريعة للسلام
    if "سلام" in content or "السلام عليكم" in content:
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته يا هلا فيك يا {message.author.name} 👑")
        return

    # للأسئلة والدردشة العامة
    if len(content) > 0 and not content.startswith("!"):
        try:
            # إرسال الطلب لجوجل بشكل آمن وسريع
            response = model.generate_content(content)
            if response and hasattr(response, 'text') and response.text:
                answer = response.text
                if len(answer) > 2000:
                    answer = answer[:2000]
                await message.channel.send(answer)
            else:
                await message.channel.send("أهلاً بك! استلمت رسالتك لكن لم أتمكن من صياغة إجابة.")
        except Exception as e:
            print(f"خطأ: {e}")
            await message.channel.send("علي معليش، حصل ضغط بسيط. جرب تسألني مرة ثانية!")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
