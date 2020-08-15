import threading, requests, json, websockets, asyncio, discord, re, logging
from flask import Flask, render_template, request

ip = '0.0.0.0'
port = 5000
bot_token = 'token_here'
channel_command = '채팅채널 지정'

client = discord.Client()
web = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

chat_data = None
chat_stat = False
chatting_channel = None

@client.event
async def on_ready():
    print('======================')
    print(client.user.name)
    print(client.user.id)
    print('======================')
    await client.change_presence(status=discord.Status.online)

@client.event
async def on_message(message):
    global chat_data
    global chat_stat
    global chatting_channel

    if message.content.startswith(channel_command):
        if chatting_channel != message.channel:
            await message.channel.send(f'<#{message.channel.id}> 채널의 채팅을 연결합니다.')
            chatting_channel = message.channel
            return None

    if chatting_channel == message.channel:
        content = message.content

        if message.attachments != []:
            content = f'<img src="{message.attachments[0].url}?size=256" Height="128" style="vertical-align:middle"></img>'

        emoji = re.findall(r'<:[\w]*:[\d]*>', content)
        if emoji != []:
            for i, item in enumerate(emoji):
                item = re.findall(r':[\d]*>', item)[0][1:-1]
                for emti in message.guild.emojis:
                    if int(item) == emti.id:
                        content = content.replace(emoji[i], f'<img src="https://cdn.discordapp.com/emojis/{item}.jpg?size=32" style="vertical-align:middle"></img>')

        author = message.author

        chat_data = {}
        chat_data['name'] = f"<name style='color: rgba({author.colour.r}, {author.colour.g}, {author.colour.b})'>{author.display_name}</name>"
        chat_data['content'] = re.sub(r"<(?!img)[\w].*[>$]", '', content)
        chat_data = json.dumps(chat_data)
        chat_stat = True

@web.route("/", methods=['GET'])
def index():
    return render_template("index.html", port=port, channel=chatting_channel.name, ip=ip)

@web.errorhandler(500)
def error(e):
    return render_template("error.html")

async def accept(websocket, path):
    global chat_data
    global chat_stat
    while True:
        if chat_data != None and chat_stat:
            await websocket.send(chat_data)
            chat_stat = False

def Ws():
    asyncio.set_event_loop(asyncio.new_event_loop())
    server = websockets.serve(accept, ip, port+1)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

def Webapp():
    web.run(host=ip, port=port, debug=False)

if __name__ == '__main__':
    threading.Thread(target=Ws).start()
    threading.Thread(target=Webapp).start()
    client.run(bot_token)