#-*- coding: utf-8 -*-

class Rand(object):
    """
    Classe base dos geradores de numeros aleatorios
    """
    def __init__(self, seed=None):
        if seed is None:
            import time
            self.seed = long(time.time())
        else: 
            self.seed = seed

    def random(self):
        pass

class LinearCongruential(Rand):
    """
    Linear Congruential Generator
    Uma implementacao simples de um gerador sequencial de numeros pseudo-aleatorios
    Deriva da equacao de recorrencia
        Ij+1 = a*Ij + c % m
    onde:
        a é um inteiro positivo chamado multiplicador
        c é um inteiro positivo chamado incremento
        m é o modulo
        I é o seed
    http://www.fizyka.umk.pl/nrbook/bookcpdf.html
    """

    def __init__(self, seed=None, a=1664525, m=2**32, c=1013904223):
        """
        Parametros iniciais propostos por Knuth
        """
        super(LinearCongruential,self).__init__(seed)
        self.a = a
        self.m = m
        self.c = c

    def seed(self,seed):
        self.seed = seed

    def next(self):
        self.seed = ((self.seed * self.a) + self.c) % self.m
        num = self.seed * (1.0/self.m)#convertendo pra real 0 < I < 1
        return num 

    def random(self):
        return self.next()

class ParkMiller(LinearCongruential):
    """
    Um caso especial do Linear Congruential
    http://en.wikipedia.org/wiki/Park%E2%80%93Miller_RNG
    """
    def __init__(self, seed=None, a=16807, m=(2**31)-1):
        super(ParkMiller,self).__init__(seed)
        self.a = a
        self.m = m
        self.c = 0

class MersenneTwister(Rand):
    """
    Gerador bem popular
    Traducao C -> python
    http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/VERSIONS/C-LANG/991029/mt19937-1.c
    """

    #Numeros magicos... nao mude
    N = 624
    M = 397

    MATRIX_A = 0x9908b0df
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7fffffff
    
    TEMPERING_MASK_B = 0x9d2c5680
    TEMPERING_MASK_C = 0xefc60000

    def TEMPERING_SHIFT_U(self, y):
        return y >> 11
    
    def TEMPERING_SHIFT_S(self,y):
        return y << 7
    
    def TEMPERING_SHIFT_T(self,y):
        return y << 15
    
    def TEMPERING_SHIFT_L(self,y):
        return y >> 18
    

    def __init__(self, seed=None): 
        super(MersenneTwister, self).__init__(seed)
        self.mt = []
        self.mti = self.N + 1
    
    def sgenrand(self, seed=None):
        """
        Inicializa o gerador
        """
        if seed is not None:
            self.seed = seed

        self.mt = [0]*self.N
        for i in xrange(self.N):
            self.mt[i] = seed & 0xffff0000
            seed = 69069 * seed + 1
            self.mt[i] |= (seed & 0xffff0000) >> 16
            seed = 69069 * seed + 1
        self.mti = self.N

    def random(self):
        i = 0L
        mag01 = (0x0, self.MATRIX_A)
        if self.mti >= self.N: #Generate N words at one time
            if self.mti == self.N+1:
                self.sgenrand(4357)

            for kk in xrange(self.N-self.M):
                y = (self.mt[kk]&self.UPPER_MASK) | (self.mt[kk+1]&self.LOWER_MASK)
                self.mt[kk] = self.mt[kk+self.M] ^ (y >> 1) ^ mag01[y & 0x1]
            for kk in xrange(kk,self.N-1):
                y = (self.mt[kk]&self.UPPER_MASK) | (self.mt[kk+1]&self.LOWER_MASK)
                self.mt[kk] = self.mt[kk+(self.M-self.N)] ^ (y >> 1) ^ mag01[y & 0x1]
            y = (self.mt[self.N-1]&self.UPPER_MASK) | (self.mt[0]&self.LOWER_MASK)
            self.mt[self.N-1] = self.mt[self.M-1] ^ (y >> 1) ^ mag01[y & 0x1]
            self.mti = 0

        y = self.mt[self.mti]
        self.mti += 1
        y ^= self.TEMPERING_SHIFT_U(y)
        y ^= self.TEMPERING_SHIFT_S(y) & self.TEMPERING_MASK_B
        y ^= self.TEMPERING_SHIFT_T(y) & self.TEMPERING_MASK_C
        y ^= self.TEMPERING_SHIFT_L(y)
        return float(y) / 0xffffffffL #para real

if __name__ == '__main__':
    rand = LinearCongruential()
    
    print "="*20
    for j in xrange(1000):
        print rand.random(),
        if (j%8) == 7:
            print
    
    print "="*20
    rand = ParkMiller()
    for j in xrange(1000):
        print rand.random(),
        if (j%8) == 7:
            print

    print "="*20
    rand = MersenneTwister()
    for j in xrange(1000):
        print rand.random(),
        if (j%8) == 7:
            print
