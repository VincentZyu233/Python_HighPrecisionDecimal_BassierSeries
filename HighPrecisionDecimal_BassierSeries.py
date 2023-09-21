# -*- coding: utf-8 -*-
import numpy as np

class ZeroDenominatorError(Exception): #除以零异常
    def __init__(self, message="Denominator cannot be zero."):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f"ZeroDenominatorError: {self.message}"

class HighPrecisionDecimal:
    def __init__( self, x, y, z ):
        self.numerator = int(x) #分子
        self.denominator = int(y) #分母
        self.precision_places = int(z) #精度_小数点后的位数
        
        self.intPart = int( 0 ) #整数部分
        self.decPart = np.zeros( self.precision_places, dtype=int ) #小数部分
        if ( self.denominator != 0 ):
            self.update_value()
        else:
            raise ZeroDenominatorError()
            
    def update_value(self):
        #计算整数部分:
        self.intPart = int( self.numerator / self.denominator )
        
        #计算小数部分:
        t = self.numerator % self.denominator
        for i in range(0, self.precision_places):
            self.decPart[i] = 10 * t / self.denominator
            t = (10*t) % self.denominator
    
    def to_string(self):
        #返回这个小数的字符串
        intStr = str( int(self.intPart) )
        decStr = ''.join( str(digit) for digit in self.decPart )
        return ( f"{intStr}.{decStr}" )
    
    def to_float(self):
        #返回这个小数的float
        return float(self.to_string)
    
    def __add__(self, other): #重载加号运算符
        #首先确保另一个变量也是高精度小数类
        if not isinstance(other, HighPrecisionDecimal):
            raise TypeError("Variable both should be type 'HighPrecisionDecimal', "
                            f"but found {type(other)}.")
        if ( len(self.decPart) != len(other.decPart) ):
            raise TypeError("Precision of both HighPrecisionDecimal should be same.")
        
        #整数部分直接相加
        self.intPart = self.intPart + other.intPart
        
        #小数部分先全部相加
        self.decPart = self.decPart + other.decPart
        #然后再从低到高处理进位
        
        for i in reversed ( range (1, len(self.decPart)) ):
            self.decPart[i-1] += self.decPart[i] / 10
            self.decPart[i] %= 10
        #循环部分处理到小数点后第二位（下标1）， 然后第一位的进位给整数部分
        self.intPart += int ( self.decPart[0] / 10 )
        self.decPart[0] %= 10
        
        return self
    

def main():
    # print("main func here qwq!")
    precision_HPD = 1111 #小数点后的位数
    sum_BassierSeries = HighPrecisionDecimal(0,1,precision_HPD) #级数和初始化为0
    num_BassierTerms = 114514 #级数的项数
    for i in range (1,num_BassierTerms+1):
        sum_BassierSeries += HighPrecisionDecimal(1, i*i, precision_HPD)
    
    print("Exact: %s" %( str( np.pi * np.pi / 6 ) )[:11] )
    print("Approximate: %s" %( sum_BassierSeries.to_string()[:11] ) )
    
if __name__ == "__main__":
    main()