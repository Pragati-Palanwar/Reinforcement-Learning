import random
from geopy.distance import geodesic
from config.constants import *

class LogisticsEnv:
    def __init__(self, num_riders=10, num_orders=50):
        self.num_riders = num_riders
        self.num_orders = num_orders
        self.orders = self.generate_orders()
        self.riders = self.generate_riders()
        self.time = 0  # Current simulation time in minutes
        self.done = False

    def generate_orders(self):
        # Randomly generate orders with location and time constraints
        return [{
            'id': i,
            'location': (random.uniform(*LAT_RANGE), random.uniform(*LON_RANGE)),
            'prep_time': random.randint(10, 20),  # minutes
            'ready_time': random.randint(0, 180),  # within 3 hours
            'weight': random.uniform(0.5, 1.0)  # in kg
        } for i in range(self.num_orders)]

    def generate_riders(self):
        # Randomly generate rider locations and availability
        return [{
            'id': i,
            'location': (random.uniform(*LAT_RANGE), random.uniform(*LON_RANGE)),
            'capacity': MAX_CAPACITY_KG,
            'active': True
        } for i in range(self.num_riders)]

    def reset(self):
        self.orders = self.generate_orders()
        self.riders = self.generate_riders()
        self.time = 0
        self.done = False
        return self.state()

    def state(self):
        # Return the current state (riders, orders, time)
        return {
            'time': self.time,
            'orders': self.orders,
            'riders': self.riders
        }

    def step(self, action):
        # Apply action, update state, and calculate reward
        rider_id, order_id = action
        reward = self.assign_order(rider_id, order_id)
        self.time += 1  # Increment time
        self.done = self.time > 720  # End simulation after 12 hours
        return self.state(), reward, self.done

    def assign_order(self, rider_id, order_id):
        # Assign an order to a rider and calculate reward
        rider = self.riders[rider_id]
        order = self.orders[order_id]

        # Check capacity
        if rider['capacity'] < order['weight']:
            return -10  # Penalty for exceeding capacity

        # Calculate distance and update rider location
        dist = geodesic(rider['location'], order['location']).km
        rider['location'] = order['location']
        rider['capacity'] -= order['weight']
        self.orders[order_id]['assigned'] = True

        # Reward for completing assignment efficiently
        reward = 100 - dist  # Shorter distances give higher reward
        return reward

