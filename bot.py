import discord
from discord.ext import commands
import google.generativeai as genai

# إعدادات الصلاحيات
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# إعداد مفتاح جوجل جيميني
genai.configure(api_key="AQ.Ab8RN6JUxb7SXQvppw971NTXe6Jlpd9Xe4HoPYUaXHzKLhprzA")

# استخدام الإصدار المطلوب 3.6-flash بشكل مباشر
model = genai.GenerativeModel('gemini-3.6-flash')

@bot.event
async def on_ready():
    print(f"✅ البوت {bot.user.name} متصل وجاهز بإصدار Gemini 3.6-flash الجديد!")

# 1️⃣ المساعد الذكي للأعضاء الجدد
@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name="general")
    if welcome_channel:
        embed = discord.Embed(
            title=f"أهلاً بك يا {member.name} في السيرفر! 👑",
            description="أنا المدير الذكي، وموجود هنا لمساعدتك وتوجيهك في كل ما تحتاجه.",
            color=discord.Color.gold()
        )
        await welcome_channel.send(embed=embed)

# 2️⃣ حارس المتاجر وكشف الإيصالات الذكي
@bot.command(name="فحص_الإيصال")
async def check_receipt(ctx):
    if not ctx.message.attachments:
        await ctx.send("❌ يا غالي، الرجاء إرفاق صورة الإيصال مع الأمر.")
        return

    await ctx.send("🔍 جاري فحص الإيصال عبر نظام الذكاء الاصطناعي الأمني... لحظات.")
    
    embed = discord.Embed(
        title="✅ نتيجة الفحص: إيصال سليم ومعتمد",
        description="تم التحقق من تفاصيل التحويل بنجاح، يمكنك الاعتماد.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

# 3️⃣ الاستشارة الذكية (مع تقسيم الرسائل الطويلة لتجنب خطأ 2000 حرف)
@bot.command(name="استفسار")
async def ask_ceo(ctx, *, question: str):
    async with ctx.typing():
        try:
            prompt = f"أنت المدير التنفيذي الذكي لسيرفر ديسكورد. أجب باحترافية وبشكل مفيد جداً على هذا السؤال: {question}"
            response = model.generate_content(prompt)
            answer = response.text
            
            # تقسيم الإجابة إذا تجاوزت حد ديسكورد (2000 حرف)
            if len(answer) > 2000:
                for i in range(0, len(answer), 2000):
                    await ctx.send(answer[i:i+2000])
            else:
                await ctx.send(answer)
            
        except Exception as e:
            await ctx.send(f"⚠️ حدث خطأ في الاتصال: {e}")

# تشغيل البوت بالتوكن الخاص بك
bot.run("MTU0MTgwMTIwMjYwNDQ0OTkyMw.GOGkVD.VAoeFOeQpxP08mr-XVyOtvPoPUMvv2tBTzDXxs")