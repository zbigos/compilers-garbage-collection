import random
import copy
memory = []

# insert blocks to memory
for i in range(1, 16):
    memory.append((i, None, None))
print(len(memory))
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

if len(memory) != 30:
    print(f"WRONG MEMORY LENGTH {len(memory)}")
    exit(1)


memdump(memory)

# DFS APPROACH
print("===========================================")
print("moving root blocks")

def chase(ptr, memory, next_):
    while True:
        blkid, lptr, rptr = memory[ptr]
        print(f"reading {ptr}->{memory[ptr]}")
        blkseek = None
        # przepisz strukturę.
        memory[ptr] = (next_, None, None)
        memory[next_] = (blkid, lptr, rptr)
        for ptr in [lptr, rptr]:
            if ptr is not None and ptr < 15:
                blkseek = ptr
        
        if not blkseek:
            memory[next_] = (blkid, lptr, rptr)
            return (memory, next_ + 1)
        else:
            print(f"new seek pointer {blkseek}")
            if ptr == lptr and lptr is not None:
                memory[next_] = (blkid, next_+1, rptr)
            if ptr == rptr and rptr is not None:
                memory[next_] = (blkid, lptr, next_+1)
            ptr = blkseek
            next_ += 1


def forward(ptr, memory, next_):
    try:
        if ptr < 15: #pointer is in from space
            if memory[ptr][1] is not None and memory[ptr][1] >= 15: #block is already moved
                print(f"bbbb {ptr} -> {memory[ptr][1]}")
                return (memory[ptr][1], memory, next_)
            else:
                print(f"starting chase {ptr} -> {memory[ptr]}")
                memory, next_ = chase(ptr, memory, next_)
                print(f"post chase {ptr} -> {memory[ptr]}")
                return (memory[ptr][0], memory, next_)
        else:
            print("aaaa")
            return (ptr, memory, next_)
    except Exception as e:
        print(ptr, next_, memory)
        memdump(memory)
        raise Exception

'''
_, memory, next_ = forward(rootptr, memory, 16)
memdump(memory)
print(rootptr)
for memp in range(16, 32):
    print("=-============")
    dptr, memory, next_ = forward(memp, memory, next_)
    #memdump(memory)
'''
rootptr, memory, next_ = forward(rootptr, memory, 15)

print("===========================================")
print("iterating over memory")
for memp in range(15, 30):
    print("===========================================")
    print(len(memory), memp)
    blkid, lptr, rptr = memory[memp]
    if lptr is not None and lptr is not None: 
        print(f"got block {memp} -> {memory[memp]} with pointers to {lptr} {rptr}")
        print(f"fetched for pointer {lptr} memory underneath is {memory[lptr]}.")
        nlptr, memory, next_ = forward(lptr, memory, next_)
        print(f"The block is now in {nlptr}, next is {next_}")
        print(f"fetched for pointer {rptr} memory underneath is {memory[rptr]}.")
        npptr, memory, next_ = forward(rptr, memory, next_)
        print(f"The block is now in {npptr}")
        memory[memp] = (blkid, nlptr, npptr)

memdump(memory)