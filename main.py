from env.logistics_env import LogisticsEnv
from agent.dqn_agent import DQNAgent
from pprint import pprint
# Initialize environment
env = LogisticsEnv()

# Initialize agent
state_size = 10  # Placeholder: define based on your state representation
action_size = 5  # Placeholder: define based on possible actions
agent = DQNAgent(state_size, action_size)

# Test the environment
state = env.reset()
print("Initial State:")
pprint(state)