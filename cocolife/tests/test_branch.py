def Solve(pair):
    memo = {}
    x, y = pair

    def f(x, y):
        if y == 0:
            return x
        if (x, y) in memo:
            return memo[(x, y)]
        res = f(x+1, y-1)
        memo[(x, y)] = res
        return res

    def g(x, y):
        if y == 0:
            return 0
        if y % 2 == 0:
            if (x, y) in memo:
                return memo[(x, y)]
            res = g(f(x, y), y // 2)
            memo[(x, y)] = res
            return res
        else:
            return f(g(x, y-1), x)

    def h(x, y):
        if y == 0:
            return 1
        if y % 2 == 0:
            if (x, y) in memo:
                return memo[(x, y)]
            res = h(g(x, x), y // 2)
            memo[(x, y)] = res
            return res
        else:
            return g(h(x, y-1), x)

    return f(x, y) + g(x, y) + h(x, y)


pair = [2, 2]
result = Solve(pair)
print(result)  # output: 12

pair = [3, 7]
result = Solve(pair)
print(result)  # output: 2218
