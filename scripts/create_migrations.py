import time
import platform
import subprocess

def log(message):
    print(f"[INFO] {message}")

def run_command(command, error_message):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        log(error_message)
        log(e.stderr.decode())
        raise e

def main():
    try:
        time_start = time.perf_counter()
        log("Detecting platform...")
        current_platform = platform.system()
        log(f"Platform detected: {current_platform}")

        log("Collecting static files...")
        run_command("py manage.py collectstatic --no-input", "Failed to collect static files")

        log("Initializing migrations...")
        run_command("py manage.py makemigrations", "Failed to make migrations")
        run_command("py manage.py migrate", "Failed to migrate")

        log("Making migrations...")
        apps = ""
        for app in apps.split():
            log(f"Making migrations for {app}...")
            run_command(f"py manage.py makemigrations {app}", f"Failed to make migrations for {app}")
            run_command(f"py manage.py migrate {app}", f"Failed to migrate {app}")

        log("Ending migrations...")
        run_command("py manage.py makemigrations", "Failed to make migrations")
        run_command("py manage.py migrate", "Failed to migrate")

        log("Importing data...")
        run_command("py manage.py loaddata data/content/json/admin_interface_theme.json", "Failed to migrate admin_interface_theme")

        time_end = time.perf_counter()
        log(f"Completed in {time_end - time_start:.2f} seconds")

    except Exception as e:
        log(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()