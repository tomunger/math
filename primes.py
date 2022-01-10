from typing import List
import genprimesieve
import math
import numpy as np
import pandas as pd


def find_factors_fwdall(n: int) -> List[int]:
	"""Find integer factors of paremeter n by trying all integer candidates
	starting with 2.  

	Args:
		n (int): The integer to factor

	Returns:
		List[int]: List of factors, smallest first
	"""
	i = 2
	factors = []

	while i * i <= n:
		while n%i == 0:
			n = n // i
			factors.append(i)
		i = i + 1
	if n > 1:
		factors.append(n)
	return factors


def find_factors_rev(n: int, p: List[int]) -> List[int]:
	"""Find integer factors of parameter n by trying all primte candiates,
	starting with n//2 and proceeding through smaller prime numbers.

	Args:
		n (int): The integer to be factord
		p (List[int]): A list of prime numbers, in order, up to n//2

	Raises:
		Exception: Not enough prime numbers provided.

	Returns:
		List[int]: List of factors, smallest first
	"""
	for mpi in range(len(p)):
		if p[mpi] > n//2:
			break
	if mpi >= len(p):
		raise Exception ("Not enough primes provied")
	factors = []
	for pi in range(mpi, -1, -1):
		while n%p[pi] == 0:
			n = n // p[pi]
			factors.append(p[pi])
		if n == 1:
			break
	if n > 1:
		factors.append(n)
	return factors


def primes_to_powers(f: List[int], P: List[int]) -> List[int]:
	"""Convert a list of prime factors to a list of prime powers.

	Parameter f is a list of prime numbers, in order, such as 2,2,5,7,19.
	P is a list of prime numbers, including all that appear in f.
	The result, R, is the list re-expressed as powers of each prime.

	For prime p in P
	    R[index(p in P)] = count(p in f)

	For the above example, the result is: 2,0,1,1,0,0,0,1,0,0,0...
	which shows that there
	  2 of prime 2
	  0 of prime 3
	  1 of prime 5
	  1 of prime 7
	  ...
	  1 of prime 19
	  ...


	Args:
		f (List[int]): List of prime factors
		P (List[int]): List of prime numbers in order.

	Returns:
		List[int]: List of prime powers.
	"""
	powers = []
	fi = 0
	for pi in range(len(P)):
		powers.append(0)
		while fi < len(f) and f[fi] == P[pi]:
			powers[pi] += 1
			fi += 1
	return powers



nums = range(2, 100000)
P = genprimesieve.gen_primes_sieve_to(max(nums))
print (f"{len(P)} primes, max: {P[-1]}")


a = []
powers = []
for n in nums:
	if not n in P:
		a.append( (n, find_factors_fwdall(n)) )

for q in a:
	#print(f"{q[0]} factors {q[1]}")

	prod = 1
	for p in q[1]:
		if not p in P:
			print (f"Not prime {p}")
		prod *= p
	if prod != q[0]:
		print (f"  product of factors is not correct:  {prod}")

	revfactros = find_factors_rev(q[0], P)
	revfactros.sort()
	if revfactros != q[1]:
		print (f"  reverse factors are not correct:  {revfactros}")

	powers.append(primes_to_powers(q[1], P))


#
# Take the powers python array and make a pandas dataframe
# where columns are prime numbers, rows are integers, and cell values
# are the power of prime.  product of primes raised to powers are the 
# index integer.
#
# powersnp = np.array(powers)										# Make a numpy array
# df = pd.DataFrame(powers, columns=P, index=[q[0] for q in a])	# and then a dataframe
# print (df.shape)
# Pr = P.copy()													# Create a copy of the list of primes
# Pr.reverse()													# and reverse that 
# for p in Pr:													# so we can search from largest to smallest
# 	print (f"{p} {df[p].sum()}")		
# 	if df[p].sum() == 0:										# If the column contains no powers
# 		df.drop(p, axis='columns', inplace=True)				#   we drop that column
# 	else:
# 		break													#   otherwise, we have reached the largest prime used and exit the loop
# print (df.shape)
# df.to_csv("primefactors.csv")