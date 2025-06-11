# this is for experiments
import subprocess
import time
import algorithms
import csv
import os
import classes
import sys

# arguments: district, algorithm (random/hillclimber/annealing), itterations

def runexperiment(algorithm, total_time, sub_time):

    start_time = time.time()
    csv_file = store()

    while time.time() - start_time < total_time:
        process = subprocess.Popen(['python', 'subprocess_script.py'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)

        while time.time() - start_time < sub_time:
            line = process.stdout.readline()
            csv_file.store_data()
         
        n_runs += 1

class store:
    def __init__(self, path = "../../experiment/output.csv"):
        # Define the relative path (relative to the Python script)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Write to the CSV file
        self.file = open("output.csv", mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
    
    def store_data(self, time, line):
        step, cost, itterations = line.split(",")
        self.writer.writerow([time, step, cost, itterations])

     
    