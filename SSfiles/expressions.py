import math

def calculate_position(x, a, v, t):
	return x + v * t + (1/2) * a * (t ** 2)

def calculate_bmi(w, k):
	return (w / k ** 2) * 703

def Prime(n):
	'''checks whtether n is prime or not''' 
	for i in range(2, int(math.sqrt(n)) + 1):
		if n % i == 0:
			return False
	return True

def main():
	'''
	x = float(input("position x "))
	t = float(input("time "))
	v = float(input("speed "))
	a = float(input("acceleration "))
	print("x is located at ",calculate_position(x, a, v, t))
	w = float(input("weight "))
	k = float(input("height in feet "))
	print("height ", k, "weight ", w, "bmi ", "%.1f" % calculate_bmi(w, k))
	print()
	'''
	print(Prime(47))
main()