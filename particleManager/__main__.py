import subprocess

if __name__ == '__main__':
    try:
        subprocess.check_call(['sudo', 'python3', 'particleManager/manager.py'])
    except subprocess.CalledProcessError:
        print("Error: particleManager/manager.py exited with non-zero status code")