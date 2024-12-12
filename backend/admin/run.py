import os
import subprocess
import platform
import psutil
import uvicorn

# def check_port_availability(port: int) -> bool:
#     """Check if a port is already in use (works on both Windows and Linux)."""
#     for conn in psutil.net_connections(kind='inet'):
#         if conn.laddr.port == port:
#             return True
#     return False


# def start_server(port: int):
#     """Start the server using uvicorn (Windows) or gunicorn (Linux)."""
#     try:
#         workers = os.cpu_count() * 2 + 1
#         if platform.system() == 'Windows': 
#             print("Starting server with uvicorn (Windows)...")

#             uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
#         else:  
#             print("Starting server with gunicorn (Linux)...")
#             subprocess.run(
#                 ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", str(workers),
#                  "--reload", "-b", f"0.0.0.0:{port}", "app.main:app"],
#                 check=True
#             )
#     except subprocess.CalledProcessError as e:
#         print(f"Error starting server: {e}")
#     except Exception as e:
#         print(f"Unexpected error: {e}")

# if __name__ == "__main__":
#     port = 9000
#     if check_port_availability(port):
#         print(f"Port {port} is already in use. Please choose another port.")
#     else:
#         start_server(port)

if __name__ == "__main__":
    port = 9000
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)