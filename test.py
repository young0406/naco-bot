def H(n): #n : Natural number
    if n == 1:  return 1
    if n > 1:
        return H(n-1) + 4*(n-1)
