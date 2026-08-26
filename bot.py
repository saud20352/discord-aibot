import os
import discord
from discord.ext import commands
import google.generativeai as genai

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# استخدام مفتاح جيميني القياسي الفعّال
genai.configure(api_key="AQ.Ab8RN6JUxb7SXQvppw971NTXe6Jlpd9Xe4HoPYUaXHzKLhprzA")
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} متصل ويعمل كذكاء اصطناعي كامل!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()
    
    # إذا كتب أي شيء (وليس أمراً يبدأ بـ !)، يرسله لعقل جيميني مباشرة
    if len(content) > 0 and not content.startswith("!"):
        async with message.channel.typing():
            try:
                # طلب الإجابة من الذكاء الاصطناعي الحقيقي
                response = model.generate_content(content)
                if response and response.text:
                    answer = response.text
                    # تقسيم النص لو كان طويلاً جداً على ديسكورد
                    if len(answer) > 2000:
                        for i in range(0, len(answer), 2000):
                            await message.channel.send(answer[i:i+2000])
                    else:
                        await message.channel.send(answer)
                else:
                    await message.channel.send("عذراً، لم أستطع توليد إجابة لهذا السؤال.")
            except Exception as e:
                print(f"خطأ: {e}")
                await message.channel.send("عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي.")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
