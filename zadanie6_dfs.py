import random
import copy
memory = []

# insert blocks to memory
for i in range(1, 16):
    memory.append((i, None, None))

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
        memory[mit] = (eid, lptr, rptr)

rootptr = None
for eit, e in enumerate(memory):
    if e[0] == 1:
        rootptr = eit

for i in range(1, 16):
    memory.append((None, None, None))


print("rootptr is")
print(rootptr)

def memdump(memory):
    print("from space:")
    for ei, e in enumerate(memory[:15]):
        print(ei, e)
    print("to space:")
    for ei, e in enumerate(memory[15:]):
        print(ei+15, e)

memdump(memory)

# DFS APPROACH
print("===========================================")
print("moving root blocks")

def forward(ptr, memory, next_):
    try:
        if ptr < 15: #pointer is in from space
            if memory[ptr][1] and memory[ptr][1] >= 15: #block is already moved
                print(f"bbbb {ptr} -> {memory[ptr][1]}")
                return (memory[ptr][1], memory, next_)
            else:
                memory[next_] = copy.deepcopy(memory[ptr]) #przenieś strukturę
                blkid, lptr, rptr = memory[ptr]
                memory[ptr] = (blkid, next_, None)
                return (memory[ptr][1], memory, next_ + 1)
        else:
            print("aaaa")
            return (ptr, memory, next_)
    except Exception as e:
        print(f"failed for {ptr} {memory[ptr]}")
        print("dumping heap")
        memdump(memory)
        exit(1)
    raise Exception
rootptr, memory, next_ = forward(rootptr, memory, 15)
memdump(memory)

def garbage_collector(pointer, memory, next_):
    nodeid, lpointer, rpointer = memory[pointer]
    # zakładam że ja już jestem przeniesiony.
    print(f"{pointer} -> {nodeid}, {lpointer}, {rpointer}")
    if lpointer == None:
        return (memory, next_)
    newl, memory, next_ = forward(lpointer, memory, next_)
    newr, memory, next_ = forward(rpointer, memory, next_)

    nodeid, _, _ = memory[pointer]
    memory[pointer] = (nodeid, newl, newr)
    print(f"exploring {newl} {newr}")
    if newl is not None:
        memory, next_ = garbage_collector(newl, memory, next_)
    if newr is not None:
        memory, next_ = garbage_collector(newr, memory, next_)
    
    return (memory, next_)

garbage_collector(rootptr, memory, next_)
memdump(memory)