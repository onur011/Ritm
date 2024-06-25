import time
import tracemalloc
import matplotlib.pyplot as plt
from functions import solomon_marcus, mihai_dinu, vasile_vasile

# Lista fișierelor de intrare
file_paths = ["2k.txt", "6k.txt", "10k.txt", "20k.txt", "50k.txt", "100k.txt"]
# Lista funcțiilor
functions = [solomon_marcus, mihai_dinu, vasile_vasile]

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def measure_performance(func, data, param):
    tracemalloc.start() 
    start_time = time.time()
    
    func(data, param)
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory() 
    tracemalloc.stop() 
    
    time_taken = end_time - start_time
    mem_used = peak / 10**6
    
    return time_taken, mem_used

if __name__ == "__main__":
    results = []

    for file_path in file_paths:
        data = read_file(file_path)
        for func in functions:
            time_taken, mem_used = measure_performance(func, data, "frază")
            results.append({
                "file": file_path,
                "function": func.__name__,
                "time_taken": time_taken,
                "mem_used": mem_used
            })


    files = list(set(result["file"] for result in results))
    files = sorted(files, key=lambda x: int(x.replace('k.txt', '')))
    functions = list(set(result["function"] for result in results))
    time_data = {func: [] for func in functions}
    memory_data = {func: [] for func in functions}

    for func in functions:
        for file in files:
            for result in results:
                if result["function"] == func and result["file"] == file:
                    time_data[func].append(result["time_taken"])
                    memory_data[func].append(result["mem_used"])


    plt.figure(figsize=(12, 6))
    for func in functions:
        plt.plot(files, time_data[func], marker='o', label=func)
    plt.xlabel('Fișier')
    plt.ylabel('Timp de execuție (s)')
    plt.title('Timp de execuție pentru fiecare funcție și fișier')
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    for func in functions:
        plt.plot(files, memory_data[func], marker='o', label=func)
    plt.xlabel('Fișier')
    plt.ylabel('Memorie utilizată (MB)')
    plt.title('Memorie utilizată pentru fiecare funcție și fișier')
    plt.legend()
    plt.tight_layout()
    plt.show()
    print(time_data)
    print(memory_data)