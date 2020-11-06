def split(a):
    l = list(a)
    for h in range(len(l)):
        n = l[h]
        if n == 1:
            continue
        for i in range(1, int(n/2)+1):
            j = n - i

            new_l = []
            for k in range(h):
                new_l.append(l[k])
            new_l.append(i)
            new_l.append(j)
            for k in range(h, len(l)):
                new_l.append(l[k])

            t = tuple(new_l)
            approach.append(t)
            split(t)
    return


if __name__ == "__main__":
    book = [100]
    approach = []
    split(book)
    print(len(approach))
