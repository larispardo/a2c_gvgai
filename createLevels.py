import numpy as np

def GetDifficultyParameters(difficulty, gridSize, isGoal, res):
    import math
    maxTreasures = 4
    # TODO: 18 is assuming the grid is 20 by 20
    width = math.floor((gridSize[0] - 18) * difficulty + 4 * np.random.random()) + 5
    height = math.floor((gridSize[1] - 18) * difficulty + 4 * np.random.random()) + 5
    if isGoal:
        enemyAmount = difficulty + math.floor(np.random.random()*difficulty/2)
    else:
        enemyAmount = 1 + difficulty + math.floor(np.random.random()*difficulty)
    # TODO: replace Magic numbers with resource amount
    resourceAmount = res + (5-round(difficulty*np.random.random()))
    treasuresAmount = np.random.randint(maxTreasures)
    return width, height, enemyAmount, resourceAmount, treasuresAmount


def CreateLevel(grid, width, height, enemies, resources, treasures, enemyTypes,
                gridSize, levelMap, isGoal, isTreasure, isResource):
    import math
    levelm = levelMap.copy()
    del levelm['wall']
    del levelm['floor']
    goPositions = []
    level = []
    vertMid = math.floor(grid[0]/2)
    horMid = math.floor(grid[1]/2)
    realVMid = math.floor(height/2)
    realHMid = math.floor(width/2)
    vertPlayArea = (vertMid - realVMid, vertMid + (height - realVMid))
    horPlayArea = (horMid - realHMid, horMid + (width - realHMid))
    # TODO: Change this to make the random variable be dependent on position instead of the list of keys
    #  Use range 10
    for row in range(grid[0]):
        if row < vertPlayArea[0] or row >= vertPlayArea[1]:
            level += [levelMap['wall']]*grid[1]+['\n']
            continue
        for col in range(grid[1]):
            if col < horPlayArea[0] or col >= horPlayArea[1]:
                level += [levelMap['wall']]
            else:
                level += [levelMap['floor']]
        level += ['\n']
    vertical = list(range(vertPlayArea[0], vertPlayArea[1]))
    horizontal = list(range(horPlayArea[0], horPlayArea[1]))
    avPos = GetPositions(1, vertical, horizontal, goPositions, level, ['avatar'],
                         gridSize=gridSize, levelMap=levelMap)
    goPositions += avPos
    enPos = GetPositions(enemies, vertical, horizontal, goPositions, level, enemyTypes,
                         gridSize=gridSize, levelMap=levelMap)
    goPositions += enPos
    if isGoal:
        goalPos = GetPositions(1, vertical, horizontal, goPositions, level, ['goal'],
                               gridSize=gridSize, levelMap=levelMap)
        goPositions += goalPos
    if isTreasure:
        trPos = GetPositions(treasures, vertical, horizontal, goPositions, level, ['treasure'],
                             gridSize=gridSize, levelMap=levelMap)
        goPositions += trPos
    if isResource:
        rePos = GetPositions(resources, vertical, horizontal, goPositions, level, ['resource'],
                             gridSize=gridSize, levelMap=levelMap)
        goPositions += rePos
    return level


def GetPositions(amount, vpos, hpos, goPos, level, keyVals, gridSize, levelMap):
    # TODO: now is not impossible to get all values in same line blocking avatar if all are enemies.
    vertPos = np.random.choice(vpos, size=amount)
    horPos = np.random.choice(hpos, size=amount)
    positions = [(x, y) for x, y in zip(vertPos, horPos)]
    while True:
        counter = 0
        for i in range(len(positions)):
            pos = positions[i]
            tmpPositions = positions.copy()
            tmpPositions.remove(pos)
            if (pos in goPos) or (pos in tmpPositions):
                vtmp = np.random.choice(vpos, size=1)[0]
                htmp = np.random.choice(hpos, size=1)[0]
                positions[i] = (vtmp, htmp)
                continue
            elif len(goPos) != 0:
                if goPos[0][0] - 1 <= pos[0] <= goPos[0][0] + 1 and goPos[0][1] - 1 <= pos[1] <= goPos[0][1] + 1:
                    print(pos, goPos[0])
                    # This assumes that the avatar position is in gpos[0] and
                    # is to make the avatar do not have items in a surrounding square.
                    vtmp = np.random.choice(vpos, size=1)[0]
                    htmp = np.random.choice(hpos, size=1)[0]
                    positions[i] = (vtmp, htmp)
                    continue
            counter += 1
        if counter == len(positions):
            break
    for pos in positions:
        i = pos[0] * (gridSize[0]+1) + pos[1]
        val = np.random.choice(keyVals, size=1)[0]
        level[i] = levelMap[val]
    return positions


def WriteLevel(level, path="", game="thesis0", lvl = 0):
    file = path + game + "_lvl" + str(lvl) + ".txt"
    f = open(file, "w+")
    f.write(''.join(level))
    f.close()


'''levelMap = {'goal': 'g',
            'enemy': '1',
            'enemy1': '1',
            'enemy2': '2',
            'enemy3': '3',
            'resource': '4',
            'treasure': '5',
            'avatar': 'A',
            'wall': 'w',
            'floor': '.'}

gridSize = (20, 20)
onlyOne = ['avatar', 'goal']
width, height, enemyAmount, resourceAmount, treasuresAmount = GetDifficultyParameters(5)
level = CreateLevel(gridSize, width, height, enemyAmount, resourceAmount, treasuresAmount)
WriteLevel(level, lvl=4)'''

