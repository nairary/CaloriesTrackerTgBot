import json
from datetime import time

class User:
    def set(self, username, weight, height, age, activity, city, target_calories=None, target_water=None, logged_calories=None, logged_water=None):
        self.data = {
            'username': username,
            'weight': weight,
            'height': height,
            'age': age,
            'activity': activity,
            'city': city,
            'target_calories': target_calories,
            'target_water': target_water,
            'logged_calories': logged_calories,
            'logged_water': logged_water,
            'logged_calories': 0,
            'logged_water': 0,
            'water_logs': {},
            'food_logs': {}
            }
            
    async def add_water(self, drinked_water, time_str):
        self.data['logged_water'] += drinked_water
        time_dt = time.fromisoformat(time_str)
        self.data['water_logs'][time_dt] = self.data['logged_water']
        return self.data['target_water'] - self.data['logged_water']
    
    async def add_water_for_workout(self, water_to_drink, time_str):
        self.data['logged_water'] -= water_to_drink
        time_dt = time.fromisoformat(time_str)
        self.data['water_logs'][time_dt] = self.data['logged_water']
        return self.data['target_water'] - self.data['logged_water']

    async def add_calories(self, eaten_calories, time_str):
        self.data['logged_calories'] += eaten_calories
        time_dt = time.fromisoformat(time_str)
        self.data['food_logs'][time_dt] = self.data['logged_calories']
        return self.data['target_calories'] - self.data['logged_calories']
    
    async def remove_calories(self, burnt_calories, time_str):
        self.data['logged_calories'] -= burnt_calories
        time_dt = time.fromisoformat(time_str)
        self.data['food_logs'][time_dt] = self.data['logged_calories']
        print(self.data['food_logs'])
        return self.data['target_calories'] - self.data['logged_calories']

    async def get_info(self):
        return self.data
    
global user
user = User()