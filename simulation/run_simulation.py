# Runner script to execute simulation steps
from env import FarmSimulationEnv

def run():
    print("Initializing agricultural environment...")
    env = FarmSimulationEnv()
    state = env.reset()
    print("Initial State:", state)
    
    # Run a simple step
    next_state, reward, done, info = env.step({"irrigate_liters": 10.0})
    print("After Step state:", next_state)
    print("Simulation execution skeleton verified.")

if __name__ == "__main__":
    run()
