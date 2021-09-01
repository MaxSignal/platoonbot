# インストールした discord.py を読み込む
from collections import deque
from sys import version
from discord import channel
import discord

TOKEN = ''
client = discord.Client()

CHANNEL_ID_PARTY_1 = 000000000000000000 #小隊チャンネル１
CHANNEL_ID_PARTY_2 = 000000000000000000 #小隊チャンネル２
CHANNEL_ID_PARTY_3 = 000000000000000000 #小隊チャンネル３
CHANNEL_ID_PARTY_LOBBY = 000000000000000000 #小隊情報表示用チャンネル
MSG_ID_1= 000000000000000000 #小隊情報表示用メッセージ1
MSG_ID_2= 000000000000000000 #小隊情報表示用メッセージ2
MSG_ID_3= 000000000000000000 #小隊情報表示用メッセージ3

party_status = True
party_status2 = True
party_status3 = True
party_member = 1
party_member2 = 1
party_member3 = 1
langmode = 0
langmode2 = 0
langmode3 = 0
make_name1 = str()
make_name2 = str()
make_name3 = str()

# 初回使用時に小隊情報表示用チャンネルに小隊情報表示作成用メッセージ作成
async def make_platoon_info():
    channel = client.get_channel(CHANNEL_ID_PARTY_LOBBY)
    await channel.send('Platoon1 : 空')
    await channel.send('Platoon2 : 空')
    await channel.send('Platoon3 : 空')

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    activity = discord.Game(name="/hplahelp | /hplahelp -en")
    await client.change_presence(status=discord.Status.idle, activity=activity)
    # await make_platoon_info() #初回使用時だけ有効化する

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global party_status,party_status2,party_status3,party_member,party_member2,party_member3,langmode,langmode2,langmode3,make_name1,make_name2,make_name3
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if message.content == "/hplahelp":
        await message.author.send("/hplahelp -en： display english platoon cmd help\n/hmake [小隊名]：小隊を作成します\n/hjoin：小隊に参加します\n/hleave：小隊から抜けます\n/hstatus：メンバーを表示します\n/hbreak：小隊を解散します\n/hlja：言語モードを日本語にします\n/hlen：change lang mode english")

    if message.content == "/hplahelp -en":
        await message.author.send("/hmake [platoon name]：make a platoon\n/hjoin：join platoon\n/hleave：leave platoon\n/hstatus：display platoon member\n/hbreak：break platoon\n/hlja：change lang mode japanese\n/hlen：change lang mode english")

    # 小隊bot1
    if message.channel.id == CHANNEL_ID_PARTY_1:
        def check_user_exist():
            with open("party.txt") as temp_f:
                datafile = temp_f.readlines()
            for line in datafile:
                if str(message.author) in line:
                    return True
            return False
        make_name = str()

        if message.content == "/hlja":
            langmode = 0
            await message.channel.send("言語モードを日本語に設定しました")

        if message.content =="/hlen":
            langmode = 1
            await message.channel.send("Lang mode change english")

        if message.content.startswith("/hmake"):
            if party_status: 
                make_name = message.content[7:]
                party_status = False
                party_member = 1
                
        
                if langmode == 0:
                    await message.channel.send(str(message.author)+"さんが"+str(make_name)+"を作成しました ["+str(party_member)+"/5]")
                elif langmode == 1:
                    await message.channel.send(str(message.author)+" make a "+str(make_name)+" ["+str(party_member)+"/5]")                
                f = open("party.txt","w")
                f.write(str(message.author)+"\n")
                f.close()
            elif party_status == False:
                if langmode == 0:
                    await message.channel.send("既に小隊が存在します")
                elif langmode == 1:
                    await message.channel.send("platoon already exist")

        if message.content == "/hjoin":
            if check_user_exist():
                if langmode == 0:
                    await message.channel.send("既に参加しています")
                elif langmode == 1:
                    await message.channel.send("you already join a platoon")
            else:
                if party_status == False and party_member < 5:
                    party_member += 1
                    if langmode == 0: 
                        await message.channel.send(str(message.author)+"さんが小隊に参加しました ["+str(party_member)+"/5]")
                    elif langmode == 1:
                        await message.channel.send(str(message.author)+" join a platoon ["+str(party_member)+"/5]")                        
                    f = open("party.txt","a")
                    f.write(str(message.author)+"\n")
                    f.close()
                elif party_member >= 5:
                    if langmode == 0:    
                        await message.channel.send("満員のため参加できません")
                    elif langmode == 1:
                        await message.channel.send("you cant join because a platoon is full")
                elif party_status:
                    if langmode == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                    elif langmode == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")

        if message.content == "/hleave":
            if check_user_exist() == False:
                if langmode == 0:
                    await message.channel.send("あなたは小隊に参加していません")
                elif langmode == 1:
                    await message.channel.send("you arent join a platoon")
            else:
                if party_status == False and party_member > 1:
                    party_member -= 1
                    if langmode == 0:
                        await message.channel.send(str(message.author)+"さんが小隊を退出しました ["+str(party_member)+"/5]")
                    elif langmode == 1:
                        await message.channel.send(str(message.author)+" leave a party ["+str(party_member)+"/5]")
                    leave_user = str(message.author)
                    with open("party.txt","r") as f:
                        fileText = f.read()
                        after = fileText.replace(leave_user,"")
                    with open("party.txt","w") as f:
                        f.write(after)
                elif party_status == False and party_member <= 1:
                    if langmode == 0:
                        await message.channel.send("メンバーがいなくなったため解散します")
                    elif langmode == 1:
                        await message.channel.send("break a platoon because all member missed")
                    party_status = True
                elif party_status:
                    if langmode == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                    elif langmode == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")
                
        if message.content == "/hstatus":
            if party_status == False:
                f = open("party.txt","r")
                data = f.read()
                await message.channel.send(str(make_name)+"\n"+data+"\n["+str(party_member)+"/5]")
                f.close()
            elif party_status:
                if langmode == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                elif langmode == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")

        if message.content == "/hbreak":
            if check_user_exist():
                if party_status == False:
                    if langmode == 0:
                        await message.channel.send("正常に解散されました")
                    elif langmode == 1:
                        await message.channel.send("break a party successfully")
                    party_status = True
                elif party_status:
                    if langmode == 0:
                        await message.channel.send("小隊が存在しないため解散できません")
                    elif langmode == 1:
                        await message.channel.send("cant break a party because party doesnt exist")
            else:
                if langmode == 0:
                    await message.channel.send("あなたは小隊に参加していないため、小隊を解散することはできません")
                elif langmode == 1:
                    await message.channel.send("you cant break a party, because you arent join the party")

        make_name1 = make_name
        await change_platoon_info()

    # 小隊bot2
    elif message.channel.id == CHANNEL_ID_PARTY_2:
        def check_user_exist():
            with open("party2.txt") as temp_f:
                datafile = temp_f.readlines()
            for line in datafile:
                if str(message.author) in line:
                    return True
            return False
        make_name = str()
        if message.content == "/hlja":
            langmode2 = 0

        if message.content =="/hlen":
            langmode2 = 1

        if message.content.startswith("/hmake"):
            if party_status2: 
                make_name = message.content[7:]
                party_status2 = False
                party_member2 = 1
                if langmode2 == 0:
                    await message.channel.send(str(message.author)+"さんが"+str(make_name)+"を作成しました ["+str(party_member2)+"/5]")
                elif langmode2 == 1:
                    await message.channel.send(str(message.author)+" make a "+str(make_name)+" ["+str(party_member2)+"/5]")
                f = open("party2.txt","w")
                f.write(str(message.author)+"\n")
                f.close()
            elif party_status2 == False:
                if langmode2 == 0:
                    await message.channel.send("既に小隊が存在します")
                elif langmode2 == 1:
                    await message.channel.send("platoon already exist")

        if message.content == "/hjoin":
            if check_user_exist():
                if langmode2 == 0:
                    await message.channel.send("既に参加しています")
                elif langmode2 == 1:
                    await message.channel.send("you already join a platoon")
            else:
                if party_status2 == False and party_member2 < 5:
                    party_member2 += 1
                    if langmode2 == 0: 
                        await message.channel.send(str(message.author)+"さんが小隊に参加しました ["+str(party_member2)+"/5]")
                    elif langmode2 == 1:
                        await message.channel.send(str(message.author)+" join a platoon ["+str(party_member2)+"/5]")                        
                    f = open("party2.txt","a")
                    f.write(str(message.author)+"\n")
                    f.close()
                elif party_member2 >= 5:
                    if langmode2 == 0:    
                        await message.channel.send("満員のため参加できません")
                    elif langmode2 == 1:
                        await message.channel.send("you cant join because a platoon is full")
                elif party_status2:
                    if langmode2 == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                    elif langmode2 == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")

        if message.content == "/hleave":
            if check_user_exist() == False:
                if langmode2 == 0:
                    await message.channel.send("あなたは小隊に参加していません")
                elif langmode2 == 1:
                    await message.channel.send("you arent join a platoon")
            else:
                if party_status2 == False and party_member2 > 1:
                    party_member2 -= 1
                    if langmode2 == 0:
                        await message.channel.send(str(message.author)+"さんが小隊を退出しました ["+str(party_member2)+"/5]")
                    elif langmode2 == 1:
                        await message.channel.send(str(message.author)+" leave a party ["+str(party_member2)+"/5]")
                    leave_user = str(message.author)
                    with open("party2.txt","r") as f:
                        fileText = f.read()
                        after = fileText.replace(leave_user,"")
                    with open("party2.txt","w") as f:
                        f.write(after)
                elif party_status2 == False and party_member2 <= 1:
                    if langmode2 == 0:
                        await message.channel.send("メンバーがいなくなったため解散します")
                    elif langmode2 == 1:
                        await message.channel.send("break a platoon because all member missed")
                    party_status2 = True
                elif party_status2:
                    if langmode2 == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                    elif langmode2 == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")
                
        if message.content == "/hstatus":
            if party_status2 == False:
                f = open("party2.txt","r")
                data = f.read()
                await message.channel.send(str(make_name)+"\n"+data+"\n["+str(party_member2)+"/5]")
                f.close()
            elif party_status2:
                if langmode2 == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                elif langmode2 == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")

        if message.content == "/hbreak":
            if check_user_exist():
                if party_status2 == False:
                    if langmode2 == 0:
                        await message.channel.send("正常に解散されました")
                    elif langmode2 == 1:
                        await message.channel.send("break a party successfully")
                    party_status2 = True
                elif party_status2:
                    if langmode2 == 0:
                        await message.channel.send("小隊が存在しないため解散できません")
                    elif langmode2 == 1:
                        await message.channel.send("cant break a party because party doesnt exist")
            else:
                if langmode2 == 0:
                    await message.channel.send("あなたは小隊に参加していないため、小隊を解散することはできません")
                elif langmode2 == 1:
                    await message.channel.send("you cant break a party, because you arent join the party")
        
        make_name2 = make_name
        await change_platoon_info()

    # 小隊bot3            
    elif message.channel.id == CHANNEL_ID_PARTY_3:
        def check_user_exist():
            with open("party3.txt") as temp_f:
                datafile = temp_f.readlines()
            for line in datafile:
                if str(message.author) in line:
                    return True
            return False
        make_name = str()

        if message.content == "/hlja":
            langmode3 = 0

        if message.content =="/hlen":
            langmode3 = 1

        if message.content.startswith("/hmake"):
            if party_status3: 
                make_name = message.content[7:]
                party_status3 = False
                party_member3 = 1
                if langmode3 == 0:
                    await message.channel.send(str(message.author)+"さんが"+str(make_name)+"を作成しました ["+str(party_member3)+"/5]")
                elif langmode3 == 1:
                    await message.channel.send(str(message.author)+" make a "+str(make_name)+" ["+str(party_member3)+"/5]")
                f = open("party3.txt","w")
                f.write(str(message.author)+"\n")
                f.close()
            elif party_status3 == False:
                if langmode3 == 0:
                    await message.channel.send("既に小隊が存在します")
                elif langmode3 == 1:
                    await message.channel.send("platoon already exist")

        if message.content == "/hjoin":
            if check_user_exist():
                if langmode3 == 0:
                    await message.channel.send("既に参加しています")
                elif langmode3 == 1:
                    await message.channel.send("you already join a platoon")
            else:
                if party_status3 == False and party_member3 < 5:
                    party_member3 += 1
                    if langmode3 == 0: 
                        await message.channel.send(str(message.author)+"さんが小隊に参加しました ["+str(party_member3)+"/5]")
                    elif langmode3 == 1:
                        await message.channel.send(str(message.author)+" join a platoon ["+str(party_member3)+"/5]")                        
                    f = open("party3.txt","a")
                    f.write(str(message.author)+"\n")
                    f.close()
                elif party_member3 >= 5:
                    if langmode3 == 0:    
                        await message.channel.send("満員のため参加できません")
                    elif langmode3 == 1:
                        await message.channel.send("you cant join because a platoon is full")
                elif party_status3:
                    if langmode3 == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                    elif langmode3 == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")

        if message.content == "/hleave":
            if check_user_exist() == False:
                if langmode3 == 0:
                    await message.channel.send("あなたは小隊に参加していません")
                elif langmode3 == 1:
                    await message.channel.send("you arent join a platoon")
            else:
                if party_status3 == False and party_member3 > 1:
                    party_member3 -= 1
                    if langmode3 == 0:
                        await message.channel.send(str(message.author)+"さんが小隊を退出しました ["+str(party_member3)+"/5]")
                    elif langmode3 == 1:
                        await message.channel.send(str(message.author)+" leave a party ["+str(party_member3)+"/5]")
                    leave_user = str(message.author)
                    with open("party3.txt","r") as f:
                        fileText = f.read()
                        after = fileText.replace(leave_user,"")
                    with open("party3.txt","w") as f:
                        f.write(after)
                elif party_status3 == False and party_member3 <= 1:
                    if langmode3 == 0:
                        await message.channel.send("メンバーがいなくなったため解散します")
                    elif langmode3 == 1:
                        await message.channel.send("break a platoon because all member missed")
                    party_status3 = True
                elif party_status3:
                    if langmode3 == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                    elif langmode3 == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")
                
        if message.content == "/hstatus":
            if party_status3 == False:
                f = open("party3.txt","r")
                data = f.read()
                await message.channel.send(str(make_name)+"\n"+data+"\n["+str(party_member3)+"/5]")
                f.close()
            elif party_status3:
                if langmode3 == 0:
                        await message.channel.send("小隊が存在しません。/hmakeで小隊を作成してください")
                elif langmode3 == 1:
                        await message.channel.send("platoon doesnt exist. please make a platoon before")

        if message.content == "/hbreak":
            if check_user_exist():
                if party_status3 == False:
                    if langmode3 == 0:
                        await message.channel.send("正常に解散されました")
                    elif langmode3 == 1:
                        await message.channel.send("break a party successfully")
                    party_status3 = True
                elif party_status3:
                    if langmode3 == 0:
                        await message.channel.send("小隊が存在しないため解散できません")
                    elif langmode3 == 1:
                        await message.channel.send("cant break a party because party doesnt exist")
            else:
                if langmode3 == 0:
                    await message.channel.send("あなたは小隊に参加していないため、小隊を解散することはできません")
                elif langmode3 == 1:
                    await message.channel.send("you cant break a party, because you arent join the party")

        make_name3 = make_name
        await change_platoon_info()
    
    # 小隊緊急時用コマンド
    if message.channel.id == CHANNEL_ID_PARTY_1 or CHANNEL_ID_PARTY_2 or CHANNEL_ID_PARTY_3:
        if message.content == "/hclear":
            party_status = True
            party_status2 = True
            party_member3 = True

#小隊情報表示チャンネルの小隊情報表示用メッセージに小隊情報を表示
@client.event
async def change_platoon_info():
    channel= client.get_channel(CHANNEL_ID_PARTY_LOBBY)
    if party_status == False:
        msg= await channel.fetch_message(MSG_ID_1)
        await msg.edit(content="Platoon1 : ["+str(party_member)+"/5] "+"name："+make_name1)
    else:
        msg= await channel.fetch_message(MSG_ID_1)
        await msg.edit(content="Platoon1 : 空")
    if party_status2 == False:
        msg= await channel.fetch_message(MSG_ID_2)
        await msg.edit(content="Platoon2 : ["+str(party_member2)+"/5] "+"name："+make_name2)
    else:
        msg= await channel.fetch_message(MSG_ID_2)
        await msg.edit(content="Platoon2 : 空")
    if party_status3 == False:
        msg= await channel.fetch_message(MSG_ID_3)
        await msg.edit(content="Platoon3 : ["+str(party_member3)+"/5] "+"name："+make_name3)
    else:
        msg= await channel.fetch_message(MSG_ID_3)
        await msg.edit(content="Platoon3 : 空")

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
