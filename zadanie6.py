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
        if ptr < 16: #pointer is in from space
            if memory[ptr][1] and memory[ptr][1] >= 16: #block is already moved
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

print("===========================================")
print("iterating over memory")
for memp in range(15, 30):
    blkid, lptr, rptr = memory[memp]
    if lptr is not None and rptr is not None:
        print(f"got block {memory[memp]} with pointers to {lptr} {rptr}")
        print(f"fetched for pointer {lptr} memory underneath is {memory[lptr]}.")
        nlptr, memory, next_ = forward(lptr, memory, next_)
        print(f"The block is now in {nlptr}, next is {next_}")
        print(f"fetched for pointer {rptr} memory underneath is {memory[rptr]}.")
        npptr, memory, next_ = forward(rptr, memory, next_)
        print(f"The block is now in {npptr}")
        memory[memp] = (blkid, nlptr, npptr)

memdump(memory)