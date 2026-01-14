import algorithms
import classes
import functions
import cProfile
import time
import sys
import subprocess
import os
import csv

experiment = True
start_time = 0
algorithm = algorithms.random

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


if __name__ == "__main__":

    if experiment == False:
        None
    else:
        grid, algorithm, itteration_limit = functions.process_input(sys.argv)
        


    