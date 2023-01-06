"""roomieMatter Particle IoT Manager"""
import roomieMatter.particleManager.particleManager
import subprocess
import os

subprocess.run(["pkill", "-f", "particleManager.py"])
subprocess.run(["rm", "-f", "var/log/particleManager.log"])
if not os.path.exists("var/log"):
    os.mkdir("var/log")
subprocess.Popen(["sudo", "python3", "roomieMatter/particleManager/particleManager.py", "--host", 
                  "172.31.28.171", "--port", "1002", "--logfile", "var/log/particleManager.log"])