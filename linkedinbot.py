import discord
from bot_token import linkedin_photo_bot
from discord.ext import commands
from LinkedIn_Commands import *

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def save(ctx):
    await ctx.message.attachments[0].save('LinkedInPhotoBot\Images\image.jpg')

@bot.command(help='Gets the names of the people who most recently message you on LinkedIn')
async def LinkedIn_Msg_Names(ctx):
    await ctx.send(get_Message_Contact_Names())

@bot.command(help='Sends an image to the name of the person given on LinkedIn')
async def send_Img_in(ctx, first_name, last_name):
    await ctx.message.attachments[0].save('LinkedInPhotoBot\Images\image.jpg')
    send_Image(first_name + ' ' + last_name)
    await ctx.send(f'Image has successfully been sent to {first_name} {last_name}')
    

bot.run(linkedin_photo_bot)