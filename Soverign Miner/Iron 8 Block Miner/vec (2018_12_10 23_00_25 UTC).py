import mathx +
def loadVector):
    return map(int,raw_input("enter in a vector").split(" "))
def dotproduct(a,b):
    return sum([a[i]*b[i] for i in range(0,len(a))])
def zero(a,b):
    return [b[i]-a[i] for i in range(0,len(a))]
def mag(a):
    return math.sqrt(sum(map(lambda a:a**2,a)))
def triangleVector(a, b, c):
    b = zero(a,b)
    c = zero(a,c)
    print "Len of AB: "+str(mag(b))
    print "Len of AC: "+str(mag(c))
    return b,c
def getangle(a,b):
    return math.acos(dotproduct(a,b)/float(mag(a)*mag(b)))

def herons(a,b,c):
    p1 = mag(zero(a,b))
    p2 = mag(zero(b,c))
    p3 = mag(zero(c,d))
    s = (p1 + p2 + p3)/2.0
    return math.sqrt(s*(s-p1)*(s-p2)*(s-p3))
def tDeg(a):
    return a*(180/math.pi)
def crossproduct(qqq,qqqq):
    a,b,c = qqq
    d,e,f = qqqq
    return [(b*f) - (c*e),(c*d)-(a*f),(a*e)-(b*d)]
