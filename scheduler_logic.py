
import pandas as pd
import os
import requests 


DATASET_URL = 'https://www.orlib.bham.ac.uk/files/alp_10_1.txt'
DATASET_FILE = 'alp_10_1.txt'

def download_dataset():
    if not os.path.exists(DATASET_FILE):
        print(f"Downloading genuine dataset from {DATASET_URL}...")
        try:
            response = requests.get(DATASET_URL)
            response.raise_for_status() 
            with open(DATASET_FILE, 'w') as f:
                f.write(response.text)
            print(f"Successfully downloaded {DATASET_FILE}.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading dataset: {e}")
            return False
    else:
        print(f"Using existing dataset: {DATASET_FILE}")
    return True

def load_real_dataset(filename):
    planes = []
    separation_matrix = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    num_planes = int(lines[0].strip())
    
    for i in range(1, num_planes + 1):
        parts = lines[i].strip().split()
        
        plane = {
            'FlightID': f"FL{i-1}",
            'original_index': i - 1,   
            'ELT': int(parts[2]),            
            'TLT': int(parts[3]),            
            'LLT': int(parts[4]),            
            'EarlyPenalty': float(parts[5]), 
            'LatePenalty': float(parts[6]),  
        }
        
        planes.append(plane)
        
    for i in range(num_planes + 1, num_planes * 2 + 1):
        row = [int(s) for s in lines[i].strip().split()]
        separation_matrix.append(row)
        
    return planes, separation_matrix

def schedule_landings_real_data(planes_list, sep_matrix):
    final_schedule = []
    diverted_flights = []
    
    planes_sorted = sorted(planes_list, key=lambda p: p['LLT'])
    
    last_landed_time = 0
    last_landed_original_index = -1
    total_penalty_cost = 0

    print(f"\nScheduling {len(planes_sorted)} flights...")
    
    for plane in planes_sorted:
        current_original_index = plane['original_index']
        
        if last_landed_original_index == -1:
            separation_needed = 0
        else:
            separation_needed = sep_matrix[last_landed_original_index][current_original_index]
        
        earliest_possible_time = last_landed_time + separation_needed
        actual_landing_time = max(plane['ELT'], earliest_possible_time)
        
        if actual_landing_time <= plane['LLT']:
            deviation_cost = 0
            if actual_landing_time < plane['TLT']:
                deviation_cost = (plane['TLT'] - actual_landing_time) * plane['EarlyPenalty']
            elif actual_landing_time > plane['TLT']:
                deviation_cost = (actual_landing_time - plane['TLT']) * plane['LatePenalty']
            
            total_penalty_cost += deviation_cost
            
            schedule_entry = plane.copy()
            schedule_entry.update({
                'ActualLandingTime': actual_landing_time,
                'DeviationCost': round(deviation_cost, 2)
            })
            final_schedule.append(schedule_entry)
            
            last_landed_time = actual_landing_time
            last_landed_original_index = current_original_index
            
        else:
            diverted_flights.append(plane)
            
    return final_schedule, diverted_flights, total_penalty_cost



def run_scheduler():
    """
    This single function runs the whole process and returns the data.
    This is what app.py will call.
    """
    if not download_dataset():
        
        return [], [], 0 
    
    planes_to_schedule, separation_matrix = load_real_dataset(DATASET_FILE)
    
    if planes_to_schedule:
        schedule, diverted, total_cost = schedule_landings_real_data(
            planes_to_schedule, separation_matrix
        )
        return schedule, diverted, total_cost
    else:
        return [], [], 0


if __name__ == "__main__":
    schedule, diverted, total_cost = run_scheduler()
    print("\n--- FINAL SCHEDULE ---")
    print(pd.DataFrame(schedule).to_string())
    print("\n--- DIVERTED FLIGHTS ---")
    print(pd.DataFrame(diverted).to_string())
    print(f"\nTotal Cost: ${total_cost:,.2f}")