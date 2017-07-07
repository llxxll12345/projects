def print_line(length):
	'''print long underlines
	in the box example 
	and the pyramid one
	'''
	str1 = ""
	for i in range(length):
		str1 += "-"
	print(str1)

def print_central(position):
	# print the central part of the box
	if(position == 0):
		print("|\/\/\/\/\/\/\/|")
	else:
		print("|/\/\/\/\/\/\/\|")

def print_box(n):
	# 1st task - print a box
	print_line(16)
	for i in range(n * 2):
		print_central(int(i / n))
	print_line(16)

def print_pyramid(n):
	# 2nd task - print a pyramid
	for i in range(n):
		str1 = ""
		for j in range(n - i - 1):
			str1 += " "
		str1 += "/"
		for j in range(i):
			str1 += "*="
		str1 += "\\"
		print(str1)
	print_line(n * 2)


def print_up(n):
	# the |/\| part of the rocket
	for i in range(n):
		str1 = "|"
		for j in range(n - i - 1):
			str1 += "."
		for j in range(i + 1):
			str1 += "/\\"
		for j in range((n - i - 1) * 2):
			str1 += "."
		for j in range(i + 1):
			str1 += "/\\"
		for j in range(n - i - 1):
			str1 += "."
		str1 += "|"
		print(str1)

def print_down(n):
	# the |\/| part of the rocket
	for i in range(n):
		str1 = "|"
		for j in range(i):
			str1 += "."
		for j in range(n - i):
			str1 += "\/"
		for j in range(i * 2):
			str1 += "."
		for j in range(n - i):
			str1 += "\/"
		for j in range(i):
			str1 += "."
		str1 += "|"
		print(str1)

def print_cone(n):
	# the top pyrimad of the rocket
	for i in range(n):
		str1 = ""
		for j in range(n - i):
			str1 += " "
		for j in range(i + 1):
			str1 += "/"
		str1 += "**"
		for j in range(i + 1):
			str1 += "\\"
		print(str1)

def print_rocket_line(n):
	# print the middle lines of the rocket
	str1 = ""
	str1 += "+"
	for i in range(n):
		str1 += "=*"
	str1 += "+"
	print(str1)

def print_rocket1():
	# print a fixed rocket
	print_cone(5)
	print_rocket_line(6)
	print_up(3)
	print_down(3)
	print_rocket_line(6)
	print_down(3)
	print_up(3)
	print_rocket_line(6)
	print_cone(5)

def print_rocket2(n):
	# print an accostumed rocket
	print_cone(n - 1)
	print_rocket_line(n)
	print_up(int(n / 2))
	print_down(int(n / 2))
	print_rocket_line(n)
	print_down(int(n / 2))
	print_up(int(n / 2))
	print_rocket_line(n)
	print_cone(int(n - 1))

def main():
	# box
	n = int(input("Input half of the height of the box: "))
	print_box(n - 1)
	print("\n")
	# pyrimad
	v = int(input("Input the height of the pyrimad: "))
	print_pyramid(v)
	print("\n")
	# fixed rocket
	print("The fixed rocket with height 3")
	print_rocket1()
	# print the accostumed rocket
	h = int(input("Input the height of the rocket: "))
	print_rocket2(h * 2)

main()