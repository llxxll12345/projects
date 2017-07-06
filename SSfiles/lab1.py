def printFirstLine():
	print("I'm in love with a girl named Fred.")

def printClap():
	print("Clap clap, clap clap, clap clap clap clap, clap, clap clap!")

def printBravo():
	print("Bravo!  Bravo!  Bravissimo bravo!  Bravissimo!")

def printLa():
	print("La la la la, la la la la, la la la la la!")

def printFill():
	print('''Fill the bowl to overflowing.  Raise the goblet high!
With a \"F\" and a \"R\" and an \"E\" and a \"D\"
And a \"F-R-E-D\" Fred!  Yeah!\n''')

def printFill1():
	print('''With a \"F\" and a \"R\" and an \"E\" and a \"D\"
And a \"F-R-E-D\" Fred!  Yeah!\n''')

def printStrum():
	print("Strum strum, strum strum, strum strum strum strum strum, strum.")

def printVerse(num):
	if num == 1:
		print('''I like you, Fred, I like you!
You're just saying those words to be kind.
No, I mean it.  I like... I mean I love you, Fred!
He is out of his medieval mind!
I'm perfectly sane and sound!  I never felt better in my life!
Everybody... everybody, everybody!  Come on!  And meet my incipient wife!\n''')
	elif num == 2:
		print('''My reasons must be clear.
When she shows you all how strong she is you'll stand right up and cheer!''')
	elif num == 3:
		print('''She drinks just like a lord!
So sing a merry drinking song and let the wine be poured!''')
	elif num == 4:
		print('''She sings just like a bird!
You'll be left completely speechless when her gentle voice is heard!''')
	elif num == 5:
		print('''She wrestles like a Greek!
You will clap your hands in wonder at her fabulous technique!''')
	elif num == 6:
		print('''She dances with such grace!
You are bound to sing her praises 'til you're purple in the face!''')
	elif num == 7:
		print('''She's musical to boot!
She will set your feet a-tapping when she plays upon her lute!''')
	elif num == 8:
		print('''A clever, clownish wit!
When she does her funny pantomime your sides are sure to split!
Ha ha ha ha, ho ho ho ho, ha ha ha ha ho!''')

	else:
		print('''I'm in love with a girl.
He's in love with a girl named "F-R-E-D" Fred!''')


def main():
	printVerse(1)
	for i in range(2, 9):
		printFirstLine()
		printVerse(i)
		if i == 2:
			printFill1()
		else:
			if i == 7 or i == 8:
				printStrum()
			if i >= 6 and i <= 8:
				printBravo()
			if i >= 5 and i <= 8:
				printClap()
			if i != 3:
				printLa()
			printFill()
	printVerse(9)

main()