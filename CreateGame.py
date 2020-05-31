import numpy as np
import createLevels
import os
import sys
import createRules

'''
    TODO: Check the amount of enemies when creating them, they can have different attributes depending 
    on their class. 
'''


def CreateGame(difficulty, gameNumber, probabilityTreasures = 0, probabilityGoal = 0.8, probResourceGGoal = 0.2,
               selector_levs = True, lvls = 50 , folder = 5, gameName = 'thesis0'):
    spriteSet = {'floor': 'floor > Immovable img=newset/floor2 hidden=True',
                 'sword': 'sword > OrientedFlicker limit=5 singleton=True img=oryx/slash1',
                 # Limit refers how long it stays in game.
                 'avatar': 'avatar  > ',
                 'enemy': 'enemy > ',
                 'resource': 'resource > Resource limit=',
                 'treasure': 'treasure > Immovable ',
                 'wall': 'wall > Immovable img=oryx/wall3 autotiling=True',
                 'goal': 'goal  > Immovable '}
    enemies = {'enemy1': 'enemy1 > ',
               'enemy2': 'enemy2 > ',
               'enemy3': 'enemy3 > '}
    levelMap = {'goal': 'g > floor goal',
                'enemy': '1 > floor enemy',
                'enemy1': '1 > floor enemy1',
                'enemy2': '2 > floor enemy2',
                'enemy3': '3 > floor enemy3',
                'resource': '4 > floor resource',
                'treasure': '5 > floor treasure',
                'avatar': 'A > floor avatar',
                'wall': 'w > wall',
                'floor': '. > floor'}
    interactionSet = {'avwa': 'avatar wall > stepBack',
                      'swen': 'enemy sword > killSprite scoreChange=2',
                      'enen': 'enemy enemy > stepBack',  # Need to check what is the best way to
                      # handle this section for multiple enemies.
                      'aven': 'avatar enemy > killSprite scoreChange=-1',
                      'trav': 'treasure avatar > killSprite scoreChange=1',
                      'enwa': 'enemy wall > stepBack',
                      'enwaA': 'enemy wall > reverseDirection',
                      'avre': 'resource avatar > collectResource  scoreChange=2',
                      'avgo': 'goal avatar  > killSprite scoreChange=2',
                      'avgoR': 'goal avatar  > killIfOtherHasMore resource=resource limit='}
    terminationSet = {'goal': 'SpriteCounter stype=goal    limit=0 win=True',
                      'enemy': 'SpriteCounter stype=enemy limit=0  win=True',
                      'avatar': 'SpriteCounter stype=avatar win=False'}
    sections = ['SpriteSet', 'LevelMapping', 'InteractionSet', 'TerminationSet']
    maxDifficulty = 5
    gridSize = (20, 20)

    # Could we make this general? I say yes, just make sure the general structure is saved.
    sprites = ['oryx/slime1', 'oryx/slime2', 'oryx/slime3', 'oryx/slime4', 'oryx/slime5', 'oryx/slime6']
    indices = np.arange(len(sprites))
    np.random.shuffle(indices)
    sprites = [sprites[i] for i in indices]
    avatarTypes = ['ShootAvatar', 'MovingAvatar']
    gameSprites = ['floor', 'wall', 'enemy', 'avatar']
    gameInteractions = ['avwa', 'aven']
    enemyTypes = ['Immovable', 'RandomNPC', 'Missile', 'Chaser']
    # counter = [2, 4, 8]  # Counter in randomnpc class.
    possibleSlimeSprites = ['avatar', 'enemy', 'goal', 'treasure', 'resource']
    specialTypeSprites = ['avatar', 'enemy']
    gameTerminations = ['avatar']
    gameSprites += ['sword']

    isGoal = False
    isResource = False
    isMissile = False
    isTreasure = False
    goalR = 0
    if np.random.random() < probabilityGoal:
        isGoal = True
        gameSprites += ['goal']
        gameTerminations += ['goal']
        if np.random.random() < probResourceGGoal:  # total probability of 0.16
            isResource = True
            gameSprites += ['resource']
            limitR, goalR = createRules.SetResource(difficulty, maxDifficulty)
            spriteSet['resource'] += str(limitR) + ' '
            interactionSet['avgoR'] += str(goalR)
            gameInteractions += ['avre', 'avgoR']
        else:
            gameInteractions += ['avgo']
    else:
        gameTerminations += ['enemy']  # TODO: Make this also have a probability of exist in certain difficulties.
        #tmpAvatarTy = avatarTypes.copy()
        avatarTypes.remove('MovingAvatar')

    if np.random.random() < probabilityTreasures:
        isTreasure = True
        gameSprites += ['treasure']
        gameInteractions += ['trav']

    differentEnemies = createRules.ChooseAmountEnemies(diff=difficulty)
    if differentEnemies > 1:
        gameInteractions += ['enen']
    # spriteWithTypes = ['avatar']
    # spriteWithTypes += ['enemy'+str(i+1) for i in range(differentEnemies)]

    # TODO: think what is better to be the avatar type when increasing difficulty

    avatarType = np.random.choice(avatarTypes, size=1)[0]

    enemyTy, enemyVar = createRules.SelectEnemyTypes(enemyTypes, differentEnemies,
                                                     isGoal, isMissile, difficulty, gameInteractions, interactionSet)
    # goTypes += enemyTy
    rules = createRules.createRules(differentEnemies, avatarType, enemyTy, enemyVar, gameSprites, gameTerminations,
                                    gameInteractions, possibleSlimeSprites, sections, levelMap, sprites, enemies,
                                    terminationSet, spriteSet, interactionSet)


    version = 0

    if sys.platform.startswith('win'):
        gamesPath = 'C:\\Users\\Lenovo\\Envs\\thesis1\\Lib\\site-packages\\gym_gvgai\\envs\\games\\'

    else:
        gamesPath = "/Users/larispardo/Downloads/GVGAI_GYM/gym_gvgai/envs/games/"

    if selector_levs:
        testPath = os.path.dirname(os.path.realpath(__file__)) + '/' + "data" + '/' + \
                   "test-levels"
        path01 = testPath + '/' + gameName + '/' + str(folder) + '/'
        path02 = gamesPath + gameName + "_v" + str(version) + "/"
    else:
        path01 = gamesPath + gameName + "_v" + str(version) + "/"
        path02 = gamesPath + gameName + "_v" + str(version + 1) + "/"

    # Create target directory & all intermediate directories if don't exists
    try:
        os.makedirs(path01)
        print("Directory ", path01, " Created ")
    except FileExistsError:
        print("Directory ", path01, " already exists")
    try:
        os.makedirs(path02)
        print("Directory ", path02, " Created ")
    except FileExistsError:
        print("Directory ", path02, " already exists")
    if selector_levs:
        rulepath = testPath + '/' + gameName +'/gamerules/'
        try:
            os.makedirs(rulepath)
            print("Directory ", rulepath, " Created ")
        except FileExistsError:
            print("Directory ", rulepath, " already exists")
        createRules.WriteRules(gameName, rules, path=path02)
        createRules.WriteRules(gameName+str(gameNumber), rules, path=rulepath)
    else:
        createRules.WriteRules(gameName, rules, path=path01)
        createRules.WriteRules(gameName, rules, path=path02)

    levelMap = {'goal': 'g',
                'enemy': '1',
                'enemy1': '1',
                'enemy2': '2',
                'enemy3': '3',
                'resource': '4',
                'treasure': '5',
                'avatar': 'A',
                'wall': 'w',
                'floor': '.'}


    enemyTy = ['enemy' + str(i + 1) for i in range(differentEnemies)]

    if selector_levs:
        for i in range(lvls):
            width, height, enemyAmount, resourceAmount, treasuresAmount = createLevels.GetDifficultyParameters(round(i / (lvls/5)),
                                                                                                               gridSize=gridSize,
                                                                                                               isGoal=isGoal,
                                                                                                               res=goalR)
            level = createLevels.CreateLevel(gridSize, width, height, enemyAmount, resourceAmount,
                                             treasuresAmount, levelMap=levelMap, gridSize=gridSize,
                                             enemyTypes=enemyTy, isGoal=isGoal, isResource=isResource, isTreasure=isTreasure)
            createLevels.WriteLevel(level, game=gameName+str(gameNumber), lvl=i, path=path01)
            if i == 0:
                createLevels.WriteLevel(level, game=gameName, lvl=i % 5, path=path02, change = False)
    else:
        ## TODO: This is overriding variable
        lvls = 10
        for i in range(lvls):
            width, height, enemyAmount, resourceAmount, treasuresAmount = createLevels.GetDifficultyParameters(round(i / 2),
                                                                                                               gridSize=gridSize,
                                                                                                               isGoal=isGoal,
                                                                                                               res=goalR)
            level = createLevels.CreateLevel(gridSize, width, height, enemyAmount, resourceAmount,
                                             treasuresAmount, levelMap=levelMap, gridSize=gridSize,
                                             enemyTypes=enemyTy, isGoal=isGoal, isResource=isResource, isTreasure=isTreasure)

            if i % 5 == 0:
                version += 1
            if version == 1:
                createLevels.WriteLevel(level, game=gameName, lvl=i % 5, path=path01)
            else:
                createLevels.WriteLevel(level, game=gameName, lvl=i % 5, path=path02)