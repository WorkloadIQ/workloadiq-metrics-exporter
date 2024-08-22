# src/metrics_exporter.py
from prometheus_client import start_http_server, Gauge, Info
import random
import time
from datetime import datetime, timedelta
import os

# Create metrics
login_time = Gauge('user_login_time', 'User login time', ['user_id', 'role'])
logout_time = Gauge('user_logout_time', 'User logout time', ['user_id', 'role'])
session_duration = Gauge('user_session_duration', 'User session duration in seconds', ['user_id', 'role'])
cpu_usage = Gauge('user_cpu_usage', 'User CPU usage in percentage', ['user_id', 'role'])
ram_usage = Gauge('user_ram_usage', 'User RAM usage in MB', ['user_id', 'role'])
user_info = Info('user_profile', 'User profile information', ['user_id'])

def generate_user_data():
    roles = ['admin', 'developer', 'manager', 'analyst']
    for user_id in range(1000):
        role = random.choice(roles)
        login_datetime = datetime.now() - timedelta(hours=random.randint(1, 24))
        logout_datetime = login_datetime + timedelta(minutes=random.randint(30, 480))
        
        login_timestamp = login_datetime.timestamp()
        logout_timestamp = logout_datetime.timestamp()
        duration = logout_timestamp - login_timestamp
        
        login_time.labels(user_id=str(user_id), role=role).set(login_timestamp)
        logout_time.labels(user_id=str(user_id), role=role).set(logout_timestamp)
        session_duration.labels(user_id=str(user_id), role=role).set(duration)
        cpu_usage.labels(user_id=str(user_id), role=role).set(random.uniform(0, 100))
        ram_usage.labels(user_id=str(user_id), role=role).set(random.uniform(100, 16000))
        
        user_info.labels(user_id=str(user_id)).info({
            'name': f'User{user_id}',
            'email': f'user{user_id}@example.com',
            'department': random.choice(['IT', 'HR', 'Finance', 'Marketing']),
            'location': random.choice(['New York', 'London', 'Tokyo', 'Sydney'])
        })

def update_data():
    while True:
        generate_user_data()
        time.sleep(60)  # Update every 60 seconds

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    start_http_server(port)
    print(f"Metrics server started on port {port}")
    generate_user_data()
    update_data()