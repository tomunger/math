from typing import List



# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/

def gen_primes_sieve():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}
    
    # The running integer that's checked for primeness
    q = 2
    
    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            # 
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next 
            # multiples of its witnesses to prepare for larger
            # numbers
            # 
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        
        q += 1


def gen_primes_sieve_to(n: int) -> List[int]:
	L = []
	for p in gen_primes_sieve():
		if p > n: 
			break
		L.append(p)
	return L


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
		List[int]: List of factors, largest first
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


