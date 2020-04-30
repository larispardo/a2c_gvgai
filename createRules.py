import numpy as np

def SelectGame(games):
    ## uniformly random chooses a game from the options
    return np.random.choice(games, size=1)[0]


def ChooseAmountEnemies(maximum=2, diff=0):
    import math
    print(diff)
    return min(maximum, math.floor(np.random.random() * diff)) + 1


def AddCheckpoint():
    global gameSprites, gameInteractions, probExtra
    if np.random.random() < probExtra:
        del spriteSet['checkpoint']
    else:
        gameSprites += ['checkpoint']
        gameInteractions += ['chav']


def AddAvatarType(avType):
    global spriteSet, avatarTypes
    ty = np.random.choice(avType, size=1)[0]
    spriteSet['avatar'] = spriteSet['avatar'] + avatarTypes[ty] + ' '

def SelectEnemyTypes(types, amount, isGoal, isMissile, difficulty, gameInteractions, interactionSet):
    slowCool = 8  # From easier to most difficult
    fastCool = 2
    minSpeed = 0.1
    maxSpeed = 0.2
    orientations = ['LEFT', 'RIGHT']
    gametypes = []
    typeVariables = []
    if difficulty == 0 and isGoal:
        return [types[0]], [[None]]
    for i in range(amount):
        ty = np.random.choice(types, size=1)[0]  # Currently uniform distributed
        gametypes.append(ty)
        if ty == 'Immovable':
            types.remove(ty)
            typeVariables += [[None]]
        elif ty == 'RandomNPC':
            cooldown = round(slowCool - min(slowCool - fastCool, np.random.random() * difficulty * 2), 3)
            typeVariables += [[('cooldown', cooldown)]]
            key = 'enwa' + str(i + 1)
            interactionSet[key] = 'enemy' + str(i + 1) + ' wall > stepBack'
            gameInteractions += [key]

        elif ty == 'Missile':  # Now redundant, but could help to keep track of all variable types.
            speedScale = 30
            speed = round(minSpeed + min(maxSpeed - minSpeed, np.random.random() / speedScale * difficulty), 3)
            orientation = np.random.choice(orientations, size=1)[0]
            typeVariables += [[('orientation', orientation), ('speed', speed)]]
            isMissile = True
            key = 'enwa' + str(i + 1)
            interactionSet[key] = 'enemy' + str(i + 1) + ' wall > reverseDirection'
            gameInteractions += [key]
    return gametypes, typeVariables


def SetResource(difficulty, maxDifficulty):
    import math
    minResources = 3
    goalResources = minResources + math.floor(np.random.random() * difficulty)
    limitResources = goalResources + math.floor(np.random.random() * (maxDifficulty - difficulty) +
                                                minResources * (maxDifficulty - difficulty))
    return limitResources, goalResources


def createRules(differentEnemies, avatarType, enemyTy, enemyVar, gameSprites,
                gameTerminations, gameInteractions, possibleSlimeSprites, sections,
                levelMap, sprites, enemies, terminationSet, spriteSet, interactionSet):
    space = '  '
    rules = ''
    for section in sections:
        rules += space + section + '\n'
        if section == 'SpriteSet':
            for value in gameSprites:
                isEnemy = False
                if value == 'avatar':
                    if avatarType != 'ShootAvatar':
                        spriteSet[value] += 'ShootAvatar' + ' stype=sword '
                    else:
                        if 'swen' not in gameInteractions:
                            spriteSet[value] += avatarType + ' stype=sword '
                            gameInteractions += ['swen']
                elif value == 'enemy':
                    isEnemy = True
                    rules += space * 2 + spriteSet[value] + '\n'
                print(value, possibleSlimeSprites, value in possibleSlimeSprites)
                if (value in possibleSlimeSprites) and not isEnemy:
                    rules += space * 2 + spriteSet[value] + 'img=' + sprites.pop() + '\n'
                elif isEnemy:
                    for i in range(1, differentEnemies + 1):
                        if enemyVar[i - 1][0] is not None:
                            print("HERE: " + enemyTy[i - 1])
                            variables = [x[0] + '=' + str(x[1]) for x in enemyVar[i - 1]]
                            variables = ' '.join(variables)
                            rules += space * 3 + enemies[value + str(i)] + enemyTy[i - 1] + ' ' + variables \
                                     + ' ' + 'img=' + sprites.pop() + '\n'
                        else:
                            rules += space * 3 + enemies[value + str(i)] + enemyTy[i - 1] + ' ' \
                                     + 'img=' + sprites.pop() + '\n'
                else:
                    rules += space * 2 + spriteSet[value] + '\n'
        elif section == 'LevelMapping':
            for value in gameSprites:
                if value == 'sword':
                    continue
                if value == 'enemy':
                    for i in range(1, differentEnemies + 1):
                        rules += space * 2 + levelMap[value + str(i)] + '\n'
                else:
                    rules += space * 2 + levelMap[value] + '\n'
        if section == 'InteractionSet':
            for value in gameInteractions:
                rules += space * 2 + interactionSet[value] + '\n'
        if section == 'TerminationSet':
            for value in gameTerminations:
                rules += space * 2 + terminationSet[value] + '\n'
    return rules


def WriteRules(file, rules, path=""):

    f = open(path + file + '.txt', "w+")
    f.write('BasicGame\n')
    f.write(rules)
    f.close()



