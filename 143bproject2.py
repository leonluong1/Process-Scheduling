from collections import deque


#A: Checks if all processes are done running
def check_remaining(remaining):
    return False if sum(remaining) == 0 else True #A


#A: Queue for holding uncompleted processes arrived at current time
#B: List of remaining time each process has left to complete
#C: Checks if processes have arrived
#D: Lowers remaining time of current process
#E: If current process is done, remove from queue and write down "real time"

#FIRST IN, FIRST OUT
def fifo(arrivals, totals, times):
    nproc = len(arrivals)
    time = 0
    queue = deque(maxlen = nproc) #A
    remaining = totals.copy() #B
    
    while (check_remaining(remaining)):
        for i in range(nproc):
            if (time == arrivals[i]): #C
                queue.append(i)
        time += 1
        if (len(queue) > 0):
            remaining[queue[0]] -= 1 #D
            if (remaining[queue[0]] == 0): #E
                times[queue[0]] = time - arrivals[queue[0]]
                queue.popleft()
    return 0


#A: Variable tracks if new process has longest total of all processes in queue
#If so, append it to the end of queue
#B: Checks if new process has shorter total time than process in queue
#C: Checks if new process has shorter total time than queue[0] and time is
#greater than arrival time of queue[0]. If so, queue[0] is currently running,
#so new process must wait till current process finishes because no preempt.

#SHORTEST JUMP FIRST (processes with less total time have highest priority)
def sjf(arrivals, totals, times):
    nproc = len(arrivals)
    time = 0
    queue = deque(maxlen = nproc)
    remaining = totals.copy()
    
    while (check_remaining(remaining)):
        for i in range(nproc):
            if (time == arrivals[i]):
                if (len(queue) == 0):
                    queue.append(i)
                else:
                    eoq = True #A
                    for j in range(len(queue)):
                        if (totals[i] < totals[queue[j]]): #B
                            if (j == 0 and time > arrivals[queue[0]]): #C
                                pass
                            else:
                                queue.insert(j, i)
                                eoq = False
                                break
                    if (eoq): #A
                        queue.append(i)
        time += 1
        if (len(queue) > 0):
            remaining[queue[0]] -= 1
            if (remaining[queue[0]] == 0):
                times[queue[0]] = time - arrivals[queue[0]]
                queue.popleft()
    return 0


#SHORTEST REMAINING TIME (processes with less remaining time have high priority)
def srt(arrivals, totals, times):
    nproc = len(arrivals)
    time = 0
    queue = deque(maxlen = nproc)
    remaining = totals.copy()
    
    while (check_remaining(remaining)):
        for i in range(nproc):
            if (time == arrivals[i]):
                if (len(queue) == 0):
                    queue.append(i)
                else:
                    eoq = True
                    for j in range(len(queue)):
                        if (remaining[i] < remaining[queue[j]]): 
                            queue.insert(j, i)
                            eoq = False
                            break
                    if (eoq):
                        queue.append(i)
        time += 1
        if (len(queue) > 0):
            remaining[queue[0]] -= 1
            if (remaining[queue[0]] == 0):
                times[queue[0]] = time - arrivals[queue[0]]
                queue.popleft()
    return 0


#A: Instantiate multi-level queue   #B: Append new processes to highest queue
#C: Find highest priority process
#D: If process at level 0, give it unlimited time (don't lower its level)
#E: Check if current process needs to lower its level

#MULTI-LEVEL FEEDBACK (each level is FIFO, new processes get highest priority
#(5 levels + level 0 gets unlimited time) If not finished in time, get knocked
#down a level with double time)
def mlf(arrivals, totals, times):
    nproc = len(arrivals)
    time = 0
    mlq = [None]*6 #A
    for level in range(6):
        mlq[level] = deque(maxlen = nproc)
    remaining = totals.copy()
    
    while (check_remaining(remaining)):
        for i in range(nproc):
            if (time == arrivals[i]):
                mlq[0].append(i) #B
        time += 1
        for level in range(6):
            if (len(mlq[level]) > 0): #C
                currProc = mlq[level][0]
                remaining[currProc] -= 1
                progress = totals[currProc] - remaining[currProc]
                if (remaining[currProc] == 0):
                    times[currProc] = time - arrivals[currProc]
                    mlq[level].popleft()
                elif (level == 5): #D
                    pass
                elif (progress == 2**(level+1) - 1): #E
                    mlq[level].popleft()
                    mlq[level+1].append(currProc)
                break
    return 0


#If processes come at same time, smallest process number runs first.
def schedule(out, l):
    algs = [fifo, sjf, srt, mlf]
    times = [int()]*int(len(l)/2)
    for alg in algs:
        alg(l[::2], l[1::2], times)
        avg = sum(times)/len(times)
        s = ""
        for time in times:
            s = s + "{} ".format(time)
        out.write("{:0.2f} {}\n".format(avg, s))
    return 0


def get_file():
    while True:
        try:
            fpath = input()
            pindex = fpath.rfind('\\')
            infile = open(fpath, "r")
            break
        except:    
            print("error")
    return fpath, pindex, infile


def main():
    fpath, pindex, infile = get_file()
    if (pindex == -1):
        out = open("69139013.txt", "w")
    else:
        out = open("{}69139013.txt".format(fpath[0:pindex+1]), "w")
    for line in infile:
        words = [int(word) for word in line.split()]
        schedule(out, words)
    out.close()
    return 0


main()
