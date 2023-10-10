# -*- coding: utf-8 -*-

import discord 
import discord.ext
import requests
    
async def Save_replay(ctx, attachment: discord.Attachment):
   attach = attachment.url
   await ctx.channel.send('processing file...')
   
   if not(attachment):
       await ctx.channel.send('please attach a file')
       
   elif attach.endswith('html'):
           if attach.find('/'):
               Filename = attach.rsplit('/',1)[1]
               grab = requests.get(attach, allow_redirects = True)
               open(Filename, 'wb').write(grab.content)
               await ctx.channel.send(str(Filename)) 
               
       
       