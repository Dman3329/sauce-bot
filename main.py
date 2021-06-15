import urllib.request
from datetime import date
import time
import discord
import asyncio


def get_image():
    today = 'Day ' + str(date.today()).split('-')[2]
    webUrl = urllib.request.urlopen('https://www.youtube.com/c/Kamitsurugi/community')
    data = webUrl.read()
    try:
        code = str(data).split(today)[1].split("url\"")[6].split("\"")[1].split("/")[2]
        imageUrl = urllib.request.urlopen('https://www.youtube.com/channel/UCUErrriX4EM3BXXZNPKW4Sw/community?lb=' + code)
        image_data = imageUrl.read()
        image = str(image_data).split(today)[1].split("url\"")[5].split("\"")[1]
    except IndexError:
        image = None
    if image is None:
        return image
    else:
        count = 0
        with open("sauce", "r+") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                if stripped_line.split(' ')[1] == str(date.today()).split('-')[2]:
                    count = count + 1
            if count == 0:
                a_file.write("\nDay " + str(date.today()).split('-')[2] + " " + image)
        return image


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(status=discord.Status.online, activity=discord.Game('You want the sauce? We got the sauce, do ./sauce for the sauce'))

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        user_input = message.content.split(' ')

        if (user_input[0] == './sauce') and len(user_input) < 2:
            try:
                image = get_image()
            except:
                print()
            if image is None:
                try:
                    await message.channel.send("No image available for that day")
                except:
                    None
            else:
                try:
                    await message.channel.send('Day ' + str(date.today()).split('-')[2] + ': \n')
                    await message.channel.send(image)
                except:
                    None

        if (user_input[0] == './sauce') and len(user_input) == 2:
            count = 0
            with open("sauce", "r+") as a_file:
                for line in a_file:
                    stripped_line = line.strip()
                    if stripped_line.split(' ')[1] == user_input[1]:
                        try:
                            await message.channel.send('Day ' + stripped_line.split(' ')[1] + ': \n')
                            await message.channel.send(stripped_line.split(' ')[2])
                            count = count + 1
                        except:
                            None

            if count == 0:
                await message.channel.send("No image available for that day, try doing ./sauce to update the list")


client = MyClient()
client.run('ODUzNzU0ODUxNDAwNjEzOTE5.YMZ_Kg.cIGWhrVCxzQfR1kQU9EHXwzIRGw')
