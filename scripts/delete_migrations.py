import os

def log(message):
    print(f"[INFO] {message}")

def main(base_uri: list):
    try:
        base_uri = os.sep.join(base_uri)
        print(base_uri)
        for path, folders, files in os.walk(base_uri):
            if all(condition in path for condition in ["migrations", "__pycache__", "django-simple-history", "venv"]):
                for file in files:
                    if not "__init__.py" in file:
                        delet_this = f"{path}{os.sep}{file}"
                        os.remove(delet_this)
                        log(delet_this)
    
    except Exception as e:
        log(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    base_uri = os.getcwd().split(os.sep)
    print(base_uri)
    if not base_uri[-1] == "django-template":
        log("Error: This script should be executed from the directory [./django-template/]")
        exit()
    else:
        main(base_uri)