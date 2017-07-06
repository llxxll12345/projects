import math

def prime(n):
	#check if n is prime 
	for i in range(2, int(math.sqrt(n)) + 1):
		if n % i == 0:
			return False
	return True

def perfect(n):
	#check if n is perfect
	sum = 0
	for i in range(1, n):
		if n % i == 0:
			sum += i
	return sum == n

def abundant(n):
	#check if n is abundant
	sum = 0
	for i in range(1, n):
		if n % i == 0:
			sum += i
	return sum > n

def narcissistic(str1):
	#check if n is narcissistic
	sum = 0
	lastDigit = int(str1[-1])
	for ch in str1:
		sum += int(ch) ** lastDigit
	return sum == int(str1)

def harshad(str1):
	#check if n is harshad
	sum = 0
	for ch in str1:
		sum += int(ch)
	return int(str1) % sum == 0

def main():
	n = input("Please enter a number ")
	if prime(int(n)):
		print(n + " is Prime.")
	else:
		print(n + " is not Prime.")
	if perfect(int(n)):
		print(n + " is Perfect.")
	else:
		print(n + " is not Perfect.")
	if abundant(int(n)):
		print(n + " is Abundant.")
	else:
		print(n + " is not Abundant.") 
	if narcissistic(n):
		print(n + " is Narcissistic.")
	else:
		print(n + " is not Narcissistic.")
	if harshad(n):
		print(n + " is Harshad.")
	else:
		print(n + " is not Harshad.")

main()