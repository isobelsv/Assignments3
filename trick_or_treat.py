#!/usr/bin/env python3

import cmd, sys, textwrap, time

# define constant variables
DESC = 'desc'
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
HOUSE = 'house'
DOOR = 'door'
CANDY = 'candy'
STREET = 'street'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
GROUND = 'ground'
UP = 'up'
DOWN = 'down'
GROUNDDESC = 'grounddesc'
SHORTDESC = 'shortdesc'
LONGDESC = 'longdesc'
DESCWORDS = 'descwords'
FIGHTABLE = 'fightable'
POISONOUS = 'poisonous'
SPEAK = 'speak'
WORDS = 'words'
NOTFRIENDLY = 'notfriendly'

SCREEN_WIDTH = 80

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    RED = '\033[31m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

worldRooms = {
	'Sunny Street' : {
	DESC: 'Sunny Street is the cul-de-sac where you live. One one end, a park, Sunny Park. At the other end is a large house, some say is haunted....',
	NORTH: 'Sunny Park',
	EAST: 'Your house',
	WEST: 'Emerald House',
	SOUTH: 'Dirt Condos',
	GROUND: ['Owl']
	},
	'Your House' : {
	DESC: 'Your house is like many other houses on Sunny Street, compact and cozy, with a smoking chimney and a front porch.',
	NORTH: 'Sunny Park',
	SOUTH: 'Sunny Street',
	GROUND: ['Your costume']
	},
	'Sunny Park' : {
	DESC: 'Sunny Park is full of mist tonight, odd.',
	SOUTH: 'Sunny Street',
	EAST: 'Your house',
	GROUND: ['Bats']
	},
	'Emerald House' : {
	DESC: 'The Emerald house is a ghastly McMansion on Sunny Street: huge, new, and tasteless.',
	NORTH: 'Sunny Park',
	EAST: 'Your House',
	SOUTH: 'Haunted House',
	GROUND: ['Dog', 'Kit-Kats']
	},
	'Dirt Condos' : {
	DESC: 'Dirt Condos is a run-down budget apartment building.',
	NORTH: 'Your House',
	SOUTH: 'Haunted House',
	UP: 'Zombie Apartment',
	DOWN: 'Witch Apartment',
	GROUND: ['Jolly Rancher']
	},
	'Haunted House' : {
	DESC: 'A large scary old house at the dead-end of the street. Big iron gates shut it off from the rest of the neighborhood.',
	NORTH: 'Dirt Condos',
	SOUTH: 'Sunny Street',
	GROUND: ['Intercom', 'Candied apples']
	},
	'Zombie Apartment' : {
	DESC: 'Loud music and a funny smell waif out of this apartment.',
	DOWN: 'Witch Apartment',
	SOUTH: 'Haunted House',
	GROUND: ['Zombie', 'Brownie']
	},
	'Witch Apartment' : {
	DESC: 'We do not know how many cats she has. But it is many.',
	UP: 'Zombie Apartment',
	SOUTH: 'Haunted House',
	WEST: 'Sunny Street',
	GROUND: ['Witch', 'Caramel']
	}
}

worldItems = {
	'Kit-Kats': {
	GROUNDDESC: 'Wow, a whole basket of halloween kit-kats for the taking!',
	SHORTDESC: 'kit-kats',
	LONGDESC: 'Do you have to take only one?',
	FIGHTABLE : False,
	POISONOUS: False, 
	DESCWORDS: ['kitkat', 'kit-kats', 'kit-kat', 'basket', 'halloween kit-kats', 'halloween kit-kat', 'kit kat', 'kit kats']
	},
	'Dog': {
	GROUNDDESC: 'How cute! There is a little dog in the front lawn of the Emerald House. She looks sweet at first... but then she starts to growl...',
	SHORTDESC: 'little dog',
	LONGDESC: 'In the vast front lawn of the Emerald House, a little bulldog, not much older than a pup, with a pink collar and a silver bone pendant that says: Tulip', 
	FIGHTABLE: True,
	SPEAK: True,
	NOTFRIENDLY: True,
	WORDS: 'GRRRRRRR BRRRRRRAAAIIINNS',
	DESCWORDS: ['dog', 'little dog', 'pup', 'puppy', 'Tulip', 'bulldog']
	},
	'Jolly Rancher': {
	GROUNDDESC: 'Colorful wrapped jolly rancher on the ground lead the way to the end of the dark coridor',
	SHORTDESC: 'suspicious candy trail',
	LONGDESC: 'Not sure I feel too good about this stray jolly rancher path....', 
	FIGHTABLE: False,
	POISONOUS: True,
	DESCWORDS: ['stray candy', 'jolly rancher', 'jolly ranchers', 'jolly']
	},
	'Intercom': {
	GROUNDDESC: 'In order to enter the iron Haunted House gates, you need to identify yourself over the intercom',
	SHORTDESC: 'gate intercom',
	LONGDESC: 'Next to the locked gate doors, a crackling intercom, with a modern green camera light shining through the old intercom grills', 
	FIGHTABLE: False,
	SPEAK: True,
	NOTFRIENDLY: True,
	WORDS:'THE MASTER WILL NOT BE DISTURBED...',
	DESCWORDS: ['intercom', 'interphone', 'inter', 'phone', 'bell', 'security', 'camera']
	},
	'Owl': {
	GROUNDDESC: 'Hoot hoot! Although it is not that late, you look up to see an owl sitting in a tree.',
	SHORTDESC: 'dark howl with yellow eyes'	,
	LONGDESC: 'The owl is perched in the tree, waiting.... Did it just say something?',
	FIGHTABLE: True,
	SPEAK: True,
	NOTFRIENDLY: True,
	WORDS: 'HOOOOOOOT COMING FOR YOOOOOOOOUUU!',
	DESCWORDS: ['owl']
	},
	'Bats': {
	GROUNDDESC: 'There are evil bats flying around in the mist. They look strangely familiar....',
	SHORTDESC: 'bad bats',
	LONGDESC: 'Something about these bats reminds you of something. But where is everyone else?', 
	FIGHTABLE: True,
	SPEAK: True,
	NOTFRIENDLY: True,
	WORDS: 'KREEEEKKK WE\'LL SUCK YOUR BLOOD!',
	DESCWORDS: ['bat', 'bats']
	},
	'Your costume' : {
	GROUNDDESC: 'Your mom made you a Fly-Guy superhero costume for Halloween.',
	SHORTDESC: 'Fly-Guy costume',
	LONGDESC: 'It is red, white, blue, and so shiny and cool!', 
	FIGHTABLE: False,
	DESCWORDS: ['costume', 'Fly-Guy']
	},
	'Candied apples' : {
	GROUNDDESC: 'Yummy! Sticking out of a pretty box holder with a ribbon on it, is a candied apple!',
	SHORTDESC: 'candied apple',
	FIGHTABLE: False,
	POISONOUS: True, 
	DESCWORDS: ['candied apple', 'apple']
	},
	'Zombie' : {
	GROUNDDESC: 'Oh no! A zombie is coming straight at you!',
	SHORTDESC: 'zombie',
	FIGHTABLE: True,
	SPEAK: True,
	WORDS: 'HI THERE LITTLE DUDE! I MADE THESE BROWNIES MYSELF IF YOU WOULD LIKE ONE.',
	DESCWORDS: ['zombie', 'band']
	},
	'Brownie': {
	GROUNDDESC: 'There is a plate of freshly baked chocolate brownies next to a carved pumpkin',
	SHORTDESC: 'fudgy brownie',
	POISONOUS: False,
	DESCWORDS: ['brownies', 'brownie']
	},
	'Witch': {
	GROUNDDESC: 'A witch waits at the door... but where are all the cats?',
	SHORTDESC: 'wicked witch',
	FIGHTABLE: True,
	SPEAK: True, 
	WORDS: 'MIMSIE? MARIGOLD? MITTENS? WHERE ARE YOU MY LITTLE PUMPKINS?',
	DESCWORDS: ['witch', 'wicked witch', 'cat lady', 'lady']	
	},
	'Caramel' :{
	GROUNDDESC: 'She hold out a caramel... your favorite... but is it safe?',
	SHORTDESC: 'caramel',
	POISONOUS: False,
	DESCWORDS: ['caramel', 'camarel', 'carmel', 'camel', 'carmel']
	}
}

location = 'Your House' 
bucket = []
cred = 0
showFullExits = True

def displayLocation(loc):
    """Displays the area's description and exits."""
    # Print the room name.
    time.sleep(1)
    print(colors.HEADER + loc + colors.ENDC)
    print('=' * len(loc))

    # Print the room's description
    print('\n')
    print('\n'.join(textwrap.wrap(worldRooms[loc][DESC], SCREEN_WIDTH)))

    # Print all the items on the ground.
    if len(worldRooms[loc][GROUND]) > 0:
        print()
        for item in worldRooms[loc][GROUND]:
        	print('\n')
        	print(worldItems[item][GROUNDDESC])

    # Print all the exits.
    exits = []
    for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
        if direction in worldRooms[loc].keys():
            exits.append(direction.title())
    print()
    if showFullExits:
        for direction in (NORTH, SOUTH, EAST, WEST, UP, DOWN):
            if direction in worldRooms[location]:
                print('{0}, {1}'.format(direction.title(), worldRooms[location][direction]))
    else:
        print('Exits: {0}.'.format(exits))


def moveDirection(direction):
    """A helper function that changes the location of the player."""
    global location

    if direction in worldRooms[location]:
        print('You move {0}.'.format(direction))
        location = worldRooms[location][direction]
        displayLocation(location)
    else:
        print('You cannot move in that direction')

def getAllItemsMatchingDesc(desc, itemList):
    itemList = list(set(itemList)) # make itemList unique
    matchingItems = []
    for item in itemList:
        if desc in worldItems[item][DESCWORDS]:
            matchingItems.append(item)
    return matchingItems

class TextAdventureCmd(cmd.Cmd):
    prompt = '\n> '

    # The default() method is called when none of the other do_*() command methods match.
    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    def do_quit(self, arg):
        """Quit the game."""
        print('\n')
        print('You ended up with ' + colors.RED + '{0} street cred points'.format(cred) + colors.ENDC)
        time.sleep(1)
        if cred > 19:
        	print('\n' + 'Thank you for keeping the streets safe HALLOWEEN HERO!' + '\n')
        else: 
        	print('\n' + 'These neighborhood monsters are tough. Better luck next time!' + '\n')
        return True

    def do_north(self, arg):
        """Go to the area to the north, if possible."""
        moveDirection('north')

    def do_south(self, arg):
        """Go to the area to the south, if possible."""
        moveDirection('south')

    def do_east(self, arg):
        """Go to the area to the east, if possible."""
        moveDirection('east')

    def do_west(self, arg):
        """Go to the area to the west, if possible."""
        moveDirection('west')

    def do_up(self, arg):
        """Go to the area upwards, if possible."""
        moveDirection('up')

    def do_down(self, arg):
        """Go to the area downwards, if possible."""
        moveDirection('down')

    def do_exits(self, arg):
        """Toggle showing full exit descriptions or brief exit descriptions."""
        global showFullExits
        showFullExits = not showFullExits
        if showFullExits:
            print('Showing full exit descriptions.')
        else:
            print('Showing brief exit descriptions.')

    def do_cred(self, arg):
        """Calculate player's street cred points."""
        global cred
        if cred == 0:
        	print('\n You have no street cred yet.')
        	return
        elif cred < 0:
        	print('You have a negative number of street cred. Sad.') 
        	return
        elif cred > 40:
        	print('You have {0} street cred right now. Mad street cred!'.format(cred))
        	return
        else:
        	print('You have {0} street cred points so far, way to get respect!'.format(cred))
        	return

    def do_fight(self, arg):
    	""" Fight foes, get street cred. """
    	global cred
    	itemToFight = arg.lower()
    	cantfight = False

    	for item in getAllItemsMatchingDesc(itemToFight, worldRooms[location][GROUND]):
    		if worldItems[item].get(FIGHTABLE, True) == False:
    			cantfight = True
    			continue 
    		elif NOTFRIENDLY not in worldItems[item]:
    			print('That was not nice! The {0} was a good-guy!'.format(worldItems[item][SHORTDESC]))
    			print('No street cred for that one.')
    			worldRooms[location][GROUND].remove(item)
    			return
    		else:
    			time.sleep(1)
    			print(colors.BOLD + 'KAPOOOOWWW! You fight the {0}!!!'.format(worldItems[item][SHORTDESC]) + colors.ENDC)
    			worldRooms[location][GROUND].remove(item) #so the monster is no longer there if you come back
    			cred = cred + 10
    			time.sleep(1) 
    			print('Monster defeated. You earned some street cred. Bravo!')
    			return

    	if cantfight:
    		print('No. The {0} cannot fight back. Maybe you should eat some candy instead?'.format(itemToFight))
    		return	

    def do_eat(self, arg):
    	""" Eat candy: get cred or loose cred. """
    	global cred
    	itemToEat = arg.lower()
    	cantpoison = False

    	for item in getAllItemsMatchingDesc(itemToEat, worldRooms[location][GROUND]):
    		if POISONOUS not in worldItems[item]:
    			print('That is not candy. Are you turning into a zombie?')
    			return
    		if worldItems[item].get(POISONOUS, True) == False:
    			cantpoison = True
    			continue
    		else:
    			print('Uh oh, the {0} was poisoned candy, you loose major street cred for falling for that one.'.format(worldItems[item][SHORTDESC]))
    			cred = cred - 15
    			worldRooms[location][GROUND].remove(item)
    			print('You now have {0} street cred points'.format(cred))
    			return
    	
    	if cantpoison: 
    		print('YUMMY! Halloween is for fighting monsters ' + colors.UNDERLINE +  'and' + colors.ENDC + ' eating candy!')
    		cred = cred + 15
    		print('You just earned 20 street cred points! You now have {0} points.'.format(cred))
    		for item in getAllItemsMatchingDesc(itemToEat, worldRooms[location][GROUND]):
    			worldRooms[location][GROUND].remove(item) # since the candy is eaten
    			return

    def do_talk(self, arg):
    	""" Hear what the neighborhood monsters have to say. """
    	global cred
    	itemToSpeak = arg.lower()
    	for item in getAllItemsMatchingDesc(itemToSpeak, worldRooms[location][GROUND]):
    		if SPEAK not in worldItems[item]:
    			print('The {0} cannot talk to you.'.format(worldItems[item][SHORTDESC]))
    			return
    		elif NOTFRIENDLY in worldItems[item]:
    			print('\n')
    			print('{0}: {1}'.format(item, worldItems[item][WORDS]))
    			print('\n')
    			print('Talking to monsters is not a good idea...')
    			cred = cred - 25
    			print('You just lost cred.')
    			time.sleep(1)

    			return
    		else:
    			print('{0}: {1}'.format(item, worldItems[item][WORDS]))
    			cred = cred + 40 
    			print('Yes! The {0} is a good-guy. Talking instead of fighting just earned you mad street cred!'.format(worldItems[item][SHORTDESC]))
    			worldRooms[location][GROUND].remove(item) # so that the player can't come back and fight them
    			return

if __name__ == '__main__':
	print('\n' + 'Trick or Treat Game!' + '\n')
	print('Where ANYONE can be a HALLOWEEN HERO: fighting monsters and eating candy!' + '\n')
	print('Your mission is to get as much street cred as possible, fighting monsters and eating candy.')
	print('You can talk to people too!' + '\n')
	print('=========================================================================')
	print('\n' + '(Type "help" for commands.)' + '\n')
	print(colors.OKGREEN + 'Loading...' + colors.ENDC)
	time.sleep(1)
	print(colors.OKGREEN + 'Loading...' + colors.ENDC)
	time.sleep(1)
	print(colors.OKGREEN + 'Loaded.' + colors.ENDC)
	time.sleep(1)
	print('\n')
	displayLocation(location)
	TextAdventureCmd().cmdloop()
