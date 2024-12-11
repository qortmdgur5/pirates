import os
import socket
import subprocess
import platform

def check_port_availability(port: int) -> bool:
    """Check if a port is already in use (works on both Windows and Linux)."""
    system_platform = platform.system().lower()

    if system_platform == "windows":
        command = f"netstat -ano | findstr :{port}"
    else:
        command = f"lsof -i :{port}"

    try:
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return bool(result.stdout)
    except subprocess.CalledProcessError:
        return False  

if __name__ == "__main__":
    port = 9000
    if check_port_availability(port):
        print(f"Port {port} is already in use. Please choose another port.")
    else:
        try:
            workers = os.cpu_count() * 2 + 1
            subprocess.run(
                ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", str(workers),
                 "--reload", 
                 "-b", f"0.0.0.0:{port}", "app.main:app"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error starting gunicorn: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")