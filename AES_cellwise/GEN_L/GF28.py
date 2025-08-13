# AES 中的模多项式：x^8 + x^4 + x^3 + x + 1 => 0x11b
MOD_POLY = 0x11b

# 有限域乘法
def gf_mul(a, b):
    result = 0
    while b:
        if b & 1:               # 如果最低位为1，则累加 a
            result ^= a
        a <<= 1                 # 相当于乘以 x
        if a & 0x100:           # 如果 a 超过 8 位，需要模 0x11b
            a ^= MOD_POLY
        b >>= 1
    return result & 0xFF        # 保证结果仍为 8 位

# 快速指数，用于求逆（a^254）
def gf_pow(a, power):
    result = 1
    while power:
        if power & 1:
            result = gf_mul(result, a)
        a = gf_mul(a, a)
        power >>= 1
    return result

# 求逆元 a^(-1) = a^254
def gf_inv(a):
    if a == 0:
        raise ZeroDivisionError("0 has no multiplicative inverse in GF(2^8)")
    return gf_pow(a, 254)

# 除法 a / b = a * b^(-1)
def gf_div(a, b):
    return gf_mul(a, gf_inv(b))

if __name__=="__main__":
    # for i in range(256):
    #     if(i==0):
    #         print("no inv")
    #     else:
    #         print("inv of ",i," is ", gf_inv(i) )
    print(gf_mul(2,2))
    print(gf_mul(204,2))
    print(136^145^154^131)