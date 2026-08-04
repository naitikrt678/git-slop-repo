import os
import random
import subprocess
from datetime import datetime, timedelta

def get_commit_count():
    # Triangular distribution: min=0, mode=5, max=20
    # Produces rare 0s and rare 17+ values
    count = int(random.triangular(0, 20, 5))
    return max(0, min(count, 25))

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)

def main():
    count = get_commit_count()
    if count == 0:
        print("0 commits generated for today.")
        return

    log_file = "log.txt"
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("0")

    now = datetime.utcnow()
    
    for i in range(count):
        with open(log_file, "r") as f:
            val = int(f.read().strip() or "0")
        
        val += 1
        
        with open(log_file, "w") as f:
            f.write(str(val))

        # Distribute commit timestamps across the preceding 18 hours
        offset_minutes = random.randint(0, 1080)
        commit_time = (now - timedelta(minutes=offset_minutes)).isoformat() + "Z"

        env_prefix = f'GIT_AUTHOR_DATE="{commit_time}" GIT_COMMITTER_DATE="{commit_time}"'
        
        run_cmd("git add log.txt")
        run_cmd(f'{env_prefix} git commit -m "update counter: {val}"')

    print(f"Successfully created {count} commits.")

if __name__ == "__main__":
    main()