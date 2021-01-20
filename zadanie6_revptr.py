import random
import copy
memory = []

# insert blocks to memory
for i in range(1, 16):
    memory.append([i, None, None])

random.shuffle(memory)

for mit, element in enumerate(memory):
    eid, el, ep = element
    if eid < 8:
        seekl = eid*2
        seekp = eid*2+1
        lptr = 0
        rptr = 0
        for menum, e in enumerate(memory):
            ed, _, _ = e
            if seekl == ed:
                lptr = menum
            if seekp == ed:
                rptr = menum
        memory[mit] = [eid, lptr, rptr]

rootptr = None
for eit, e in enumerate(memory):
    if e[0] == 1:
        rootptr = eit

for i in range(1, 16):
    memory.append([None, None, None])


print("rootptr is")
print(rootptr)

def memdump(memory, marked, done):
    print("from space:")
    for ei, e in enumerate(memory[:15]):
        print(ei, marked[ei], done[ei], e)
    print("to space:")
    for ei, e in enumerate(memory[15:]):
        print(ei+15, marked[ei], done[ei], e)


marked = [False for _ in memory]
done = [0 for _ in memory]

def dfs(ptr, memory, marked, done):
    t = None
    marked[ptr] = True
    done[ptr] = 0
    while True:
        i = done[ptr]
        if i < 2:
            y = memory[ptr][i + 1]
            if y is not None and not marked[y]:
                memory[ptr][i + 1] = t
                t = ptr
                ptr = y
                marked[ptr] = True
                done[ptr] = 0
            else:
                done[ptr] += 1
        else:
            y = ptr
            ptr = t
            if ptr is None:
                return (ptr, memory, marked, done)
            i = done[ptr]
            t = memory[ptr][i + 1]
            memory[ptr][i + 1] = y
            done[ptr] = i + 1

_, memory, marked, done = dfs(rootptr, memory, marked, done)
memdump(memory, marked, done)