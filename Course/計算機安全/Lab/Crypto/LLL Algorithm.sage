# Lenstra–Lenstra–Lovász Algorithm
# Works in high dimensional

# Each row of L is a basis
L = random_matrix(Zmod(1000), 3, 3)
L = L.change_ring(ZZ)
# LLL tries to solve the shortest vector in L
L, L.LLL()