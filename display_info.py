import psutil
import GPUtil
import os
import time

while True:
    gpus = GPUtil.getGPUs()
    cpu_percentages = psutil.cpu_percent(interval=1, percpu=True)
    cpu_percentage = psutil.cpu_percent()

    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent

    memory_total = round(memory_info.total / (1024**3), 2)
    memory_available = round(memory_info.available / (1024**3), 2)
    memory_used = round(memory_info.used / (1024**3), 2)

    time.sleep(1)
    if os.name == 'nt':
        os.system('cls')
    else: 
        os.system('clear')

    print('-'*40)

    print(f'| CPU: {cpu_percentage:5}%{" "*26}|')

    for i, percentage in enumerate(cpu_percentages):
        if (i + 1) % 2 != 0: print('|', end='')
        print(f"{' '*2}Core {i+1}: {percentage:5}%", end= '')
        if (i + 1) % 2 == 0: print(' '*6 + '|')

    print('-'*40)

    print(f"| RAM: {memory_used:5.2f}/{memory_total:5.2f} ({memory_percent:5})% {' '*11}|")
    
    print('-'*40)

    for gpu in gpus:
        temp = gpu.temperature
        print(f"| {gpu.name}{' '*(40 - len(gpu.name) - 3)}|")
        print(f"|  Load: {gpu.load*100:5}%{' '*24}|")
        print(f"|  Temp: {temp:5}°C{' '*23}|")
        print(f"|  Vram: {gpu.memoryUsed:4.0f}MB / {gpu.memoryTotal:4.0f}MB ({(gpu.memoryUsed/gpu.memoryTotal)*100:5.1f}%){' '*6}|")
        
    print('-'*40)
    
# import psutil
# import GPUtil

# # Lấy nhiệt độ CPU
# if hasattr(psutil, "sensors_temperatures"):
#     temps = psutil.sensors_temperatures()
#     if "coretemp" in temps:
#         for entry in temps["coretemp"]:
#             print(f"CPU {entry.label}: {entry.current}°C")

# # Lấy nhiệt độ GPU
# gpus = GPUtil.getGPUs()
# for gpu in gpus:
#     print(f"GPU {gpu.name}: {gpu.temperature}°C")

# import psutil

# if hasattr(psutil, "sensors_temperatures"):
#     print("Có hỗ trợ cảm biến nhiệt độ")
# else:
#     print("Không hỗ trợ cảm biến nhiệt độ")
