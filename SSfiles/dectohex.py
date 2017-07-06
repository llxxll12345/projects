import math

def change(num):
	str1 = ""
	while(True):
		digit = num % 16
		if(digit >= 10):
			if(digit == 10):
				str1 += "A"
			elif(digit == 11):
				str1 += "B"
			elif(digit == 12):
				str1 += "C"
			elif(digit == 13):
				str1 += "D"
			elif(digit == 14):
				str1 += "E"
			else:
				str1 += "F"
		else:
			str1 += str(digit)
		num = int(num / 16)
		if(num == 0):
			break
	str1 = str1[::-1]
	return str1

def change1(str1):
	num = 0
	for i in range(1, len(str1) + 1):
		if str1[-i] == "A":
			num += 10 * (16 ** (i - 1))
		elif str1[-i] == "B":
			num += 11 * (16 ** (i - 1))
		elif str1[-i] == "C":
			num += 12 * (16 ** (i - 1))
		elif str1[-i] == "D":
			num += 13 * (16 ** (i - 1))
		elif str1[-i] == "E":
			num += 14 * (16 ** (i - 1))
		elif str1[-i] == "F":
			num += 15 * (16 ** (i - 1))
		else:
			num += int(str1[-i]) * (16 ** (i - 1))
	return num

def main():
	num = int(input("input a decimal number "))
	print(change(num))
	str1 = input("input a hex number ")
	print(change1(str1))

main()