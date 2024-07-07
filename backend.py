import sys
import os
import socket
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
import sqlite3
from cryptography.fernet import Fernet
# Connect to SQLite database
conn = sqlite3.connect('system_metrics.db')
cursor = conn.cursor()
# Function to collect system metrics using psutil and Unix/Linux APIs
def collect_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    # Add more metrics as needed (disk usage, network stats, etc.)
    return cpu_usage, memory_usage

# Function to encrypt data using AES encryption
def encrypt_data(data):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data, key
# Create table for storing system metrics
cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY,
        cpu_usage REAL,
        memory_usage REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Function to insert metrics into SQLite database
def insert_metrics(cpu_usage, memory_usage):
    cursor.execute('''
        INSERT INTO metrics (cpu_usage, memory_usage)
        VALUES (?, ?)
    ''', (cpu_usage, memory_usage))
    conn.commit()

# Example usage:
cpu_usage, memory_usage = collect_system_metrics()
insert_metrics(cpu_usage, memory_usage)
