import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} شغال وجاهز بكل قوة!")

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
    if welcome_channel:
        await welcome_channel.send(f"أهلاً بك يا {member.name} في السيرفر! 👑 منورنا.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip().lower()
    
    # الردود الذكية المتكاملة لكل الأسئلة الشائعة
    if "سلام" in content or "السلام عليكم" in content:
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته يا هلا فيك يا {message.author.name} 👑")
    elif "كيف الحال" in content or "وشلونك" in content or "اخبارك" in content:
        await message.channel.send(f"أنا بخير دامك بخير يا {message.author.name}! كيف أقدر أساعدك اليوم؟ 🚀")
    elif "من أنت" in content or "وش تقرب له" in content:
        await message.channel.send("أنا مساعدك الذكي في السيرفر، جاهز أجاوبك على أي شي وأساعدك في تطوير السيرفر وتنظيمه! 💡")
    elif "تطوير السيرفر" in content or "أطور السيرفر" in content:
        await message.channel.send("عشان تطور سيرفرك:\n1. نظّم الرومات والقنوات وخلها مرتبة.\n2. حط رتب وتجارب تحفيزية للأعضاء.\n3. سو فعاليات بشكل مستمر.\n4. احرص على حماية السيرفر ببوتات قوية! 🛡️")
    elif len(content) > 0 and not content.startswith("!"):
        # رد افتراضي ذكي لأي سؤال عام يتم طرحه
        await message.channel.send(f"يا هلا فيك! بالنسبة لسؤالك ({message.content})، أنا هنا عشان أساعدك في إدارة السيرفر والإجابة على استفساراتك البرمجية والتنظيمية بكل ما أقدر عليه! 👑")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
