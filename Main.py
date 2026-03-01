import simpy
import numpy as np

def arrivals_generator(env:simpy.Environment, interval:float, random_seed=None):
    rng = np.random.default_rng(random_seed)

    while True:
        inter_arrival_time = rng.exponential(1.0 / interval)

        yield env.timeout(inter_arrival_time)
        print(f"Proceso se genera en: {env.now}")

RUN_LENGTH = 50

env = simpy.Environment()
env.process(arrivals_generator(env, 10))

env.run(RUN_LENGTH)
print("End of the run")