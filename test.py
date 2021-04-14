var1 = 0


def test():
    global var1
    var1 += 2
    return var1


test()
print(var1)
