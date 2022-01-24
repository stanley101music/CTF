# Lucas sequence: V_0=2, V_1=a, V_j=a*V_{j-1}-V_{j-2}, where all operations are performed modulo N
# Return the nth lucas number characterize by a
def Lucas_n(a, n):
    # Initial parameter
    v0, v1 = 2, a
    
    # Get the ring of a to automatically performed modulo N on each operations
    R = a.base_ring()
    
    # Matrix multiplication to accelerate the process
    # M^(n-1) * [v_1, v_0] = [v_n, v_{n-1}]
    # M = [[a,-1], [1,0]]
    """
    Verifying Correctness of M
        v0 = 2
        v1 = a
        M = | a -1 |
            | 1  0 |
        
        M * | v1 | = | v1*a - v0 | = | v2 |
            | v0 |   |     v1    |   | v1 |
    """
    M = matrix(R, [[a,-1], [1,0]])
    vn, _ = M^(n-1) * vector(R, [v1, v0])
    return vn

# https://en.wikipedia.org/wiki/Williams%27s_p_%2B_1_algorithm
# p+1's biggest prime factor <= B
def Williams(n, B_factorial):
    # Choose some integer a greater than 2 which characterizes the Lucas sequence
    # For different values of nth lucas number we calculate gcd(N,vn-2)
    for a in prime_range(3, 10000):
        # We use Mod(a, n), to make sure the parameter is IntegerModRing(n), or we can use a = IntegerModRing(n)(a)
        lucas = Lucas_n(Mod(a,n), B_factorial)
        d = gcd(n, lucas-2)
        # When the result is not equal to 1 or to N, we have found a non-trivial factor of N
        if 1<d<n: return d # p = d