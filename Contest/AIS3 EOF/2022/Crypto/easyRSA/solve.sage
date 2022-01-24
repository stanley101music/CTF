n1, c1 = (7125334583032019596749662689476624870348730617129072883601037230619055820557600004017951889099111409301501025414202687828034854486218006466402104817563977, 4129148081603511890044110486860504513096451540806652331750117742737425842374298304266296558588397968442464774130566675039127757853450139411251072917969330)
n2, c2 = (2306027148703673165701737115582071466907520373299852535893311105201050695517991356607853174423460976372892149320885781870159564414187611810749699797202279, 600009760336975773114176145593092065538518609408417314532164466316030691084678880434158290740067228766533979856242387874408357893494155668477420708469922)
n3, c3 = (9268888642513284390417550869139808492477151321047004950176038322397963262162109301251670712046586685343835018656773326672211744371702420113122754069185607, 5895040809839234176362470150232751529235260997980339956561417006573937337637985480242398768934387532356482504870280678697915579761101171930654855674459361)
n4, c4 = (6295574851418783753824035390649259706446806860002184598352000067359229880214075248062579224761621167589221171824503601152550433516077931630632199823153369, 3120774808318285627147339586638439658076208483982368667695632517147182809570199446305967277379271126932480036132431236155965670234021632431278139355426418)
e = 65537

# p-1's biggest prime factor <= B
# p-1 | B! = 1*2*...*B
# 2**(B!) = 2**(k(p-1)) = 1 (mod p)
# GCD(2**(B!) - 1, n) > 1
def Pollard(n, B_factorial):
    a = power_mod(2, B_factorial, n)
    d = gcd(a-1, n)
    if 1<d<n: return d # p = d
    
# Solve level 1
# n1 = p1 * q1
# n2 = p2 * q2
# (p1-1)//2 = p2
# p1-1 = 2*p2
# 2*n2 = 2*p2*q2 = (p1-1)*q2
# p1-1 | 2*n2
p1 = Pollard(n1, 2*n2)
p2 = (p1-1)//2
q1 = n1 // p1
q2 = n2 // p2
d1 = inverse_mod(e, (p1-1)*(q1-1))
d2 = inverse_mod(e, (p2-1)*(q2-1))
m1 = long_to_bytes(power_mod(c1, d1, n1))[:11]
m2 = long_to_bytes(power_mod(c2, d2, n2))[:11]


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

# Solve level 2
# p4 = (p3+1)//2
# 2*p4 = p3+1
# 2*n4 = 2*p4*q4 = (p3+1) * q4
# p3+1 | 2*n4
p3 = Williams(n3, n4*2)
p4 = (p3+1)//2
q3 = n3 // p3
q4 = n4 // p4
d3 = inverse_mod(e, (p3-1)*(q3-1))
d4 = inverse_mod(e, (p4-1)*(q4-1))
m3 = long_to_bytes(power_mod(c3, d3, n3))[:11]
m4 = long_to_bytes(power_mod(c4, d4, n4))[:11]

flag = m1+m2+m3+m4
print(flag)