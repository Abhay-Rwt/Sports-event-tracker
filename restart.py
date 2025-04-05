import os
import sys
import subprocess
import time
import signal
import platform

def find_python_process():
    """Find the Python process running app.py"""
    system = platform.system()
    
    if system == 'Windows':
        try:
            # Use tasklist to find python processes running app.py
            output = subprocess.check_output(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/FO', 'CSV']).decode()
            for line in output.splitlines():
                if 'app.py' in line:
                    # Extract PID from CSV format
                    pid = line.split(',')[1].strip('"')
                    return int(pid)
        except Exception as e:
            print(f"Error finding Python process: {e}")
    else:
        try:
            # Use ps for Unix-like systems
            output = subprocess.check_output(['ps', 'aux']).decode()
            for line in output.splitlines():
                if 'python' in line and 'app.py' in line and 'grep' not in line:
                    pid = int(line.split()[1])
                    return pid
        except Exception as e:
            print(f"Error finding Python process: {e}")
    
    return None

def kill_flask_server():
    """Kill the running Flask server"""
    pid = find_python_process()
    
    if pid:
        print(f"Found Flask server running with PID: {pid}")
        try:
            if platform.system() == 'Windows':
                subprocess.call(['taskkill', '/F', '/PID', str(pid)])
            else:
                os.kill(pid, signal.SIGTERM)
            print("Flask server terminated successfully")
            time.sleep(1)  # Wait for the process to terminate
        except Exception as e:
            print(f"Error terminating Flask server: {e}")
    else:
        print("No running Flask server found")

def start_flask_server():
    """Start the Flask server"""
    print("Starting Flask server...")
    
    try:
        # Use Popen to start without blocking
        subprocess.Popen([sys.executable, 'app.py'])
        print("Flask server started successfully")
    except Exception as e:
        print(f"Error starting Flask server: {e}")

def main():
    """Main function to restart the Flask server"""
    print("Restarting Flask server...")
    
    # Kill the running server if any
    kill_flask_server()
    
    # Start a new server
    start_flask_server()
    
    print("Restart completed")

if __name__ == "__main__":
    main() 