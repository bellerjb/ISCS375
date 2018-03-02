#!/usr/bin/python

from flask import Flask, redirect, render_template, request
from random import randint

app = Flask(__name__)
app.secret_key = '23psHVWbxBYHYoeKYQp2'

health = 20
power = 0
weapons = {'missile' : 2, 'burst' : 1}#, 'ion' : 3, 'flak' : 9}
money = 20
location = 1
state = 0
stopped = 0
enemy = {'health' : 10, 'stopped' : 0, 'weapons' : {'missile' : 3, 'burst' : 2, 'ion' : -1, 'flak' : -1}, 'reward' : 20}
travel = {1 : {'    UP    ' : '2', '   DOWN   ' : '4'},
          2 : {'   NEXT   ' : '3', '   BACK   ' : '1'},
          3 : {'   NEXT   ' : '7', '   BACK   ' : '2'},
          4 : {'    UP    ' : '5', '   DOWN   ' : '6', '   BACK   ' : '1'},
          5 : {'   NEXT   ' : '7', '   BACK   ' : '4'},
          6 : {'   NEXT   ' : '8', '   BACK   ' : '4'},
          7 : {'   NEXT   ' : '9', ' BACK TOP ' : '3', ' BACK BOT ' : '5'},
          8 : {'   NEXT   ' : '9', '   BACK   ' : '6'},
          9 : {'   NEXT   ' : '10', ' BACK TOP ' : '7', ' BACK BOT ' : '8'},
          10 : {'   END    ' : '10'}}
done = {2 : False, 3 : False, 4 : False, 5 : False, 6 : False, 7 : False, 8 : False, 9 : False}

CLOSEPOPPUP = 'javascript:void(document.getElementById("message").style.display="none");'

def renderGame(title, content, options):
    return render_template('game/game.html', title=title, location=location, symbol='*', health=health, power=power//2, destinations=travel[location],weapons=weapons , money=money, content=content, options=options)

def incrementCooldown():
    global power
    global stopped
    for key in weapons:
        if (weapons[key] > 0):
            weapons[key] = weapons[key] - 1
    for key in enemy['weapons']:
        if (enemy['weapons'][key] > 0):
            enemy['weapons'][key] = enemy['weapons'][key] - 1
    if (power < 20):
        power = power + 1
    if (stopped > 0):
        stopped = stopped - 1
    if (enemy['stopped'] > 0):
        enemy['stopped'] = enemy['stopped'] - 1

def initBattle(enabled):
    if (enabled == True):
        for key in weapons:
            if (key == 'missile'):
                weapons[key] = 2
            if (key == 'burst'):
                weapons[key] = 1
            if (key == 'ion'):
                weapons[key] = 3
            if (key == 'flak'):
                weapons[key] = 9
    else:
        for key in weapons:
            weapons[key] = -1

def battle(action):
    global health
    global state
    global stopped
    global location
    global money
    text = ''
    title = ''
    options = {'Close' : CLOSEPOPPUP}
    if (stopped == 0):
        if (action == 'missile'):
            text = text + 'Your pegasus missile landed and dealt two damage to the enemy hull. '
            enemy['health'] = enemy['health'] - 2
            weapons['missile'] = 2
        if (action == 'burst'):
            random = randint(0, 3)
            text = text + 'Your burst lasers dealt ' + {0:'zero',1:'one',2:'two',3:'three'}[random] + ' damage to the enemy hull. '
            enemy['health'] = enemy['health'] - random
            weapons['burst'] = 1
        if (action == 'ion'):
            random = randint(1, 3)
            if (random > 1):
                text = text + 'Your heavy ion blaster hit and disabled the enemy for a bit. '
                enemy['stopped'] = random
            else:
                text = text + 'Your heavy ion blaster missed. '
            weapons['ion'] = 3
        if (action == 'flak'):
            random = randint(1, 2)
            text = text + 'Your flak gun dealt ' + {1:'seven',2:'fourteen'}[random] + ' damage to the enemy hull. '
            enemy['health'] = enemy['health'] - (7 * random)
            weapons['flak'] = 9
    else:
        text = text + 'You are still disabled from the enemy ion blast. '
    if (enemy['stopped'] == 0):
        if (enemy['weapons']['missile'] == 0 and randint(0,1) == 1):
            text = text + 'The enemy pegasus missile landed and dealt one damage to your hull. '
            enemy['weapons']['missile'] = 3
            health = health - 2
        elif (enemy['weapons']['burst'] == 0 and randint(0,1) == 1):
            random = randint(0, 2)
            text = text + 'The enemy lasers dealt ' + {0:'zero',1:'one',2:'two'}[random] + ' damage to your hull. '
            health = health - random
            enemy['weapons']['burst'] = 2
        elif (enemy['weapons']['ion'] == 0 and randint(0,1) == 1):
            random = randint(0, 2)
            if (random > 0):
                text = text + 'The enemy heavy ion blaster hit and disabled the you for a bit. '
            else:
                text = text + 'The enemy heavy ion blaster fired, but missed. '
            stopped = random
            enemy['weapons']['ion'] = 4
        elif (enemy['weapons']['flak'] == 0 and randint(0,1) == 1):
            random = randint(1, 2)
            text = text + 'The enemy flak gun dealt ' + {1:'four',2:'eight'}[random] + ' damage to your hull. '
            health = health - (4 * random)
            enemy['weapons']['missile'] = 10
    else:
        text = text + 'The enemy is still disabled from the ion blast. '
    if (enemy['health'] < 1):
        state = 2
        done[location] = True
        money = money + enemy['reward']
    return renderGame(title, text, options)

def read():
    global power
    global state
    global enemy
    global health
    global money
    if (location == 1):
        initBattle(False)
        power = 20
        title = 'Slower Than Light!'
        content = 'You load into a game that seems strangely familiar to <a href="https://www.gog.com/game/faster_than_light">another game</a> but you quickly realise that that would be silly, because no one would rip-off <a href="http://store.steampowered.com/app/212680/FTL_Faster_Than_Light/">another game</a> so shamelessly without attribution. If there was a fantastic <a href="https://itunes.apple.com/us/app/ftl-faster-than-light/id833951143?mt=8">indie game</a> like this, (which there <a href="https://www.humblebundle.com/store/ftl-faster-than-light">totally isn\'t</a>) it would definitely be more interesting than this anyways. This web game, which looks quite similar to the authors previous works, throws you directly into the action by telling you that you are piloting a ship with critical information gathered by spies that would help the resistance a lot. With the Galactic Federation hot on your tail, you must reach home-base quickly. Jump to the next point.'
        options = {'Embark' : CLOSEPOPPUP}
        return renderGame(title, content, options)
    elif (location == 2):
        if (state == 2):
            initBattle(False)
            power = 20
            title = 'Victory! | Slower Than Light!'
            content = 'Your final shot flies into the drone. A small puff of gas shoots out of its exhaust before the drone explodes into a massive cloud of metal and gas. You grab $20 out of the wreckage. This sector should be clear. Our journey has only just started and we have many more trials ahead of us.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        elif (state == 3):
            initBattle(False)
            power = 20
            title = 'Sector 2 | Slower Than Light!'
            content = 'The sector is completely empty. No life can be found. Some of the debris from the scout is still floating around.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        else:
            initBattle(True)
            power = 0
            enemy = {'health' : 10, 'stopped' : 0, 'weapons' : {'missile' : 3, 'burst' : 2, 'ion' : -1, 'flak' : -1}, 'reward' : 20}
            title = 'Scout Drone | Slower Than Light!'
            content = 'After that confusing introduction and totally not cliche "start with forked paths" deal out of the way, you scan around the system you just juped too. Your scanners quickly notice a Federation drone scout about three AU away. You can\'t let the Federation find you. Destroy that ship.'
            options = {'Ready the Guns!' : '?action=pass'}
            state = 1
            return renderGame(title, content, options)
    elif (location == 3):
        if (state == 2):
            initBattle(False)
            power = 20
            title = 'Victory! | Slower Than Light!'
            content = 'The hull to the fighter suddenly rips open and the ship implodes on itself. You feel tempted to search the wreckage for any intel or weapons, but out of fear for more ships warping in, you grab $15 and get going.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        elif (state == 3):
            initBattle(False)
            power = 20
            title = 'Sector 3 | Slower Than Light!'
            content = 'The sector remains quiet. You hurry past the planet that the fighter warped to out of fear than more might be coming.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        else:
            initBattle(True)
            power = 0
            enemy = {'health' : 8, 'stopped' : 0, 'weapons' : {'missile' : 2, 'burst' : 1, 'ion' : 3, 'flak' : -1}, 'reward' : 15}
            title = 'Federation Fighter | Slower Than Light!'
            content = 'Your day just keeps getting worse. An advanced Federation Fighter just warped into this system. You try to evade it, but it quickly locates you and sets it\'s guns. The Federation is clearly looking for you.'
            options = {'Ready the Guns!' : '?action=pass'}
            state = 1
            return renderGame(title, content, options)
    elif (location == 4):
        if (state == 2):
            initBattle(False)
            power = 0
            title = 'Weapons Test | Slower Than Light!'
            content = 'You fire the missile, and sure enough it is destroyed by the sheild. The crew of the ship thanks you and sends over a small reward.'
            options = {'Next' : 'do?state=4'}
            return renderGame(title, content, options)
        elif (state == 3):
            initBattle(False)
            power = 20
            title = 'Sector 4 | Slower Than Light!'
            content = 'Your ship pauses for a bit as your crew admires the wonderful sheilds on the research vessel.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        elif (state == 4):
            initBattle(False)
            power = 20
            title = 'Sector 4 | Slower Than Light!'
            content = 'Your ship pauses for a bit as your crew admires the wonderful sheilds on the research vessel.'
            options = {'Close' : CLOSEPOPPUP}
            money = money + 20
            done[location] = True
            return renderGame(title, content, options)
        else:
            initBattle(False)
            power = 20
            title = 'Distress Signal | Slower Than Light!'
            content = 'You heasitantly approach this next system to inquire about the distress signal. The ship notices you and phones in with a strange request: shoot a missile at their ship. Aparently they are testing a new kind of sheild that is resistant to missiles.'
            options = {'Fire the Missile' : 'do?state=2', 'Leave' : CLOSEPOPPUP}
            return renderGame(title, content, options)
    elif (location == 5):
        if (state == 3):
            initBattle(False)
            power = 20
            title = 'Sector 5 | Slower Than Light!'
            content = 'You dial into Trader-Bot, but get redirected. I guess it is closed for now.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        elif (state == 2):
            initBattle(False)
            power = 0
            title = ''
            content = ''
            if (money >= 60) :
                title = 'TRANSACTION SUCCESSFUL | Slower Than Light!'
                content = 'You wire the $60 to Trader-Bot, and a small delivery drone flies over to your ship to deliver your new <b>Flak Gun II</b>. Your engineers quickly scramble to install it and it fits perfectly. It was smaller than you imagined, however.'
                money = money - 60
                weapons['flak'] = 9
                done[5] = True
            else:
                title = 'TRANSACTION FAILED | Slower Than Light!'
                content = 'You attempt to wire $60 to Trader-Bot, but you quickly realize that you do not have that. Come back later when you can afford the <b>Flak Gun II</b>.'
            options = {'Next' : '5'}
            return renderGame(title, content, options)
        else:
            initBattle(False)
            power = 20
            title = 'Shop | Slower Than Light!'
            content = 'This next system is the domain of the famous Trader-Bot. You phone in to the bot to see what is in store. Trader-Bot offers a new class of weapon: the <b>Flak Weapon</b>. This weapon is capable of massive damage, but it takes a while to charge up. Trader-Bot wants $60 for it.'
            options = {'Buy the Flak Gun II' : 'do?state=2', 'Leave' : CLOSEPOPPUP}
            return renderGame(title, content, options)
    elif (location == 6):
        if (state == 3):
            initBattle(False)
            power = 20
            title = 'Sector 6 | Slower Than Light!'
            content = 'The mysterious trading vessel is gone now.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        elif (state == 2):
            initBattle(False)
            power = 0
            title = ''
            content = ''
            if (money >= 45) :
                title = 'Transaction Successful| Slower Than Light!'
                content = 'You wire the $45 to the mysterious ship, and a beam request pings. You accept it, and a small, four legged creature scurries off the pad, drops your new <b>Heavy Ion Cannon</b> and quickly beams back. Your engineers install it.'
                money = money - 45
                weapons['ion'] = 3
                done[6] = True
            else:
                title = 'Transaction Failed | Slower Than Light!'
                content = 'You attempt to wire $45 to the mysterious ship, but you realize that you do not have that much. You tell the ship that you might come back when you have enough to buy the <b>Heavy Ion Cannon</b>.'
            options = {'Next' : '6'}
            return renderGame(title, content, options)
        else:
            initBattle(False)
            power = 20
            title = 'Blackmarket | Slower Than Light!'
            content = 'As you warp into the system you get a mysterious transmission. Another ship nearby is offering to sell you confidential Federation weapons for pretty cheap. You don\'t know if you can trust them, but a <b>Heavy Ion Cannon</b> for only $45 is a great deal.'
            options = {'Buy the Heavy Ion Cannon' : 'do?state=2', 'Leave' : CLOSEPOPPUP}
            return renderGame(title, content, options)
    elif (location == 7):
        if (state == 2):
            initBattle(False)
            power = 0
            title = 'Helping Hand | Slower Than Light!'
            loss = 15
            if (money < loss):
                loss = money
            content = 'You send a crewmember over, but as soon as he confirms that he is on their ship his transmission is cut off. The ship suddently jumps away. He was carrying ${}'.format(loss)
            options = {'Next' : 'do?state=4'}
            return renderGame(title, content, options)
        elif (state == 3):
            initBattle(False)
            power = 20
            title = 'Sector 7 | Slower Than Light!'
            content = 'The air smells like lies. You still feel angry even though $15 isn\'t that much.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        elif (state == 4):
            initBattle(False)
            power = 20
            title = 'Sector 7 | Slower Than Light!'
            content = 'The air smells like lies. You still feel angry even though $15 isn\'t that much.'
            options = {'Close' : CLOSEPOPPUP}
            loss = 15
            if (money < loss):
                loss = money
            money = money - loss
            done[7] = True
            return renderGame(title, content, options)
        else:
            initBattle(False)
            power = 20
            title = 'Distress Signal | Slower Than Light!'
            content = 'A nearby ship is signalling for help. They claim that there is a creature onboard hiding in their air-system. Their claim reminds you of the plot of a certain movie and you fear that this situation might be similar.'
            options = {'Send a Crewmember Over' : 'do?state=2', 'Leave' : CLOSEPOPPUP}
            return renderGame(title, content, options)
    elif (location == 8):
        if (state == 2):
            initBattle(False)
            power = 20
            title = 'Victory! | Slower Than Light!'
            content = 'The fighter explodes in a beautiful blast. You loot $30 out of the debris. This ship was really strong, so you know that they are close on you. Thankfully you are almost in the safe area.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        elif (state == 3):
            initBattle(False)
            power = 20
            title = 'Sector 8 | Slower Than Light!'
            content = 'A good battle was fought here today. You feel a sense of pride.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        else:
            initBattle(True)
            power = 0
            enemy = {'health' : 15, 'stopped' : 0, 'weapons' : {'missile' : 1, 'burst' : 0, 'ion' : 3, 'flak' : -1}, 'reward' : 30}
            title = 'Elite Federation Fighter | Slower Than Light!'
            content = 'Your sensors suddenly shut off. After a brief period, the turn back on only to reveal an Elite Federation Fighter charging up its missiles.  You prepare to attack.'
            options = {'Ready the Guns!' : '?action=pass'}
            state = 1
            return renderGame(title, content, options)
    elif (location == 9):
        if (state == 3):
            new = 10;
            if (health > 10):
                new = 20 - health
            health = health + new
            done[location] = True
            return redirect('~student23/Lab6/do?state=2')
        elif (state == 2):
            initBattle(False)
            power = 20
            title = 'Sector 9 | Slower Than Light!'
            content = 'You can almost see your target. Just one jump away.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        else:
            initBattle(False)
            power = 0
            title = 'Repairs | Slower Than Light!'
            content = 'You are only one jump away from your target. Suddenly, your sensors pick up a new ship approaching. A transmission comes in and the ship is friendly! The new ship offers to repair some of your hull.'
            options = {'Accept the Offer' : 'do?state=3', 'Leave' : CLOSEPOPPUP}
            return renderGame(title, content, options)
    elif (location == 10):
        if (state == 2):
            initBattle(False)
            power = 0
            title = 'Victory! | Slower Than Light!'
            content = 'The Flagship is ripped apart, piece by piece. The fireball sends a sense of satisfaction and joy across your face. Your quest is over.'
            options = {'Next' : 'do?state=3'}
            return renderGame(title, content, options)
        elif (state == 3):
            initBattle(False)
            power = 0
            title = 'Winner! | Slower Than Light!'
            content = 'Congratulations! You won! Thank you for playing my game. I hope you enjoyed it, and if you haven\'t played FTL: Faster Than Light yet, I <i>highly</i> recommend it.'
            options = {'Close' : CLOSEPOPPUP}
            return renderGame(title, content, options)
        else:
            initBattle(True)
            power = 0
            enemy = {'health' : 25, 'stopped' : 0, 'weapons' : {'missile' : 3, 'burst' : 2, 'ion' : 4, 'flak' : 10}, 'reward' : 100}
            title = 'Federation Flagship | Slower Than Light!'
            content = 'If that free heal wasn\'t obvious enoughi, you are going to be in for a big fight. The Federation Flagship has arrived! I am a kind game creator, so this will not be the insane boss battle of the source game, but I will still make it tough for you. Good luck, Commander!'
            options = {'Ready the Guns!' : '?action=pass'}
            state = 1
            return renderGame(title, content, options)
    else:
        initBattle(False)
        power = 0
        return renderGame('I AM ERROR', 'I AM ERROR', {})

@app.route("/")
def game():
    global health
    global power
    if (health <= 0):
        power = 0
        title = 'Game Over | Slower Than Light!'
        content = 'You have died!<script>void(document.getElementById("ship").style.display = "none");</script>'
        options = {'Close' : CLOSEPOPPUP}
        return renderGame(title, content, options)
    incrementCooldown()
    if (state == 1):
        return battle(request.args.get('action'))
    else:
        return read()

@app.route("/<int:newLoc>")
def jump(newLoc):
    global power
    global location
    global state
    global stopped
    power = 0
    location = newLoc
    state = 0
    stopped = 0
    if (location in done and done[location]):
        state = 3
    return redirect('/~student23/Lab6/')

@app.route("/do")
def states():
    global state
    incrementCooldown()
    state = int(request.args.get('state'))
    return redirect('/~student23/Lab6/')

app.run(host='0.0.0.0', port=5123, debug=True)
