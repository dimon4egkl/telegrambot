import os

os.system("nohup python3.7 index.py &")
os.system("nohup python3.7 reminder_task.py > task.txt &")
os.system("nohup python3.7 reminder_video.py > video.txt &")
os.system("nohup python3.7 tasks_process.py > task_process.txt &")
os.system("nohup python3.7 report.py > report.txt &")

print("Started")