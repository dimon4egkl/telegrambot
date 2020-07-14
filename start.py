import os

os.system("nohup python3.7 index.py &")
os.system("nohup python3.7 reminder_task.py > task.out &")
os.system("nohup python3.7 reminder_video.py > video.out &")
os.system("nohup python3.7 reminder_list.py > list.out &")
os.system("nohup python3.7 tasks_process.py > task_process.out &")
os.system("nohup python3.7 report.py > report.out &")

print("Started")