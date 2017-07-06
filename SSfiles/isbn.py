import math

def check(str1):
	sum = 0
	for i in range(len(str1) - 1):
		sum += int(str1[i]) * (i + 1)
	return sum % 11

def main():
	print('''This program checks to see if an ISBN code is valid.
It can process ISBN-10 codes.''')
	str1 = input("input an ISBN ")
	print("Is " + str1 + " a valid ISBN-10 numbetr?")
	if (check(str1) == 10 and str1[-1] == "X"):
		print(str1 + " is a valid ISBN-10 number.")
	elif check(str1) == int(str1[-1]):
		print(str1 + " is a valid ISBN-10 number.")
	else:
		print(str1 + " is not a valid ISBN-10 number.")
		print("Expected", check(str1),", but found",int(str1[-1]))

main()