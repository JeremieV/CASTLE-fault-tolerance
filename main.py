import asyncio
import cluster

async def ticker(delay, to):
    """Yield numbers from 0 to `to` every `delay` seconds."""
    for i in range(to):
        yield i
        await asyncio.sleep(delay)

async def main():
    async for t in ticker(1, 10):
        print(t)
        # process(t)

def best_selection(t): 
    E = set()
    for C_j in gamma:
        e = Enlargement(C_j, t)
        E.add(e)
    _min_ = min(E)
    


def delay_constraint(t):
    pass

def ouptput_cluster(t):
    pass

def split(C):
    pass

async def castle(stream, k, delta, beta):
    gamma = set() # set of k_s anonymized clusters
    omega = set() # set of non k_s anonymized clusters
    tau = 0
    async for t in stream():
        C = best_selection(t)
        if C is None:
            gamma.add(Cluster(t))
        else:
            C.add(t)
        t_prime = t.p - delta # ??
        if t_prime has not yet been output:
            delay_constraint(t_prime)


if __name__ == "__main__":
    asyncio.run(main())

