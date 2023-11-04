# -*- coding: utf-8 -*-

import discord
import discord.ext
import requests
import os

from debug.rnd_pkm_picker import get_20_rnd_ints
from process import summary_data


async def Save_replay(ctx, attachment: discord.Attachment):
    attach = attachment.url
    #await ctx.channel.send('processing file...')

    # if not attachment:
    #     await ctx.channel.send('please attach a file')
    #
    if 'html' in attach:
        grab = requests.get(attach, allow_redirects=True)
        filename = get_20_rnd_ints()
        file = open(filename, 'wb')
        file.write(grab.content)
        file.close()
        file = open(filename, 'r+')
        await ctx.respond(str(summary_data(file)))
        file.close()
        os.remove(filename)
    # if attach.endswith('html'):
    #     print(attach)
    #     if attach.find('/'):
    #         filename = attach.rsplit('/', 1)[1]
    #         grab = requests.get(attach, allow_redirects=True)
    #         open(filename, 'wb').write(grab.content)
    #         await ctx.channel.send(str(filename))
