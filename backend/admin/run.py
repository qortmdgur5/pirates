import subprocess
import os

def check_port_availability(port: int) -> bool:
    """Check if a port is already in use."""
    try:
        result = subprocess.run(
            ["lsof", "-i", f":{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
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


