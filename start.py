import subprocess
import webbrowser
import time
import os
import sys

def main():
    print("="*50)
    print("Starting Zomato AI App...")
    print("="*50)
    
    print("\n[1/2] Building frontend UI...")
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    
    # Run npm install and build with cmd wrapper for Windows compatibility
    npm_cmd = "cmd /c npm" if os.name == "nt" else "npm"
    subprocess.run(f"{npm_cmd} install", shell=True, cwd=frontend_dir)
    build_result = subprocess.run(f"{npm_cmd} run build", shell=True, cwd=frontend_dir)
    
    if build_result.returncode != 0:
        print("\n[ERROR] Frontend build failed! Please check the output above.")
        return
        
    print("\n[2/2] Starting backend server...")
    server = subprocess.Popen([sys.executable, "-m", "src.main", "--server"])
    
    # Wait a few seconds for FastAPI to fully start
    print("Waiting for server to spin up...")
    time.sleep(4)
    
    url = "http://127.0.0.1:8000"
    print(f"\nOpening browser to {url} ...")
    webbrowser.open(url)
    
    print("\nServer is running! Keep this window open.")
    print("Press Ctrl+C to stop the server.")
    
    try:
        server.wait()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.terminate()
        server.wait()
        print("Server stopped.")

if __name__ == "__main__":
    main()
