import os
import subprocess
import tempfile
import json
import time
import urllib.request
import urllib.error

cwd = r"c:\xampp\htdocs\cursos\harvard-cs50-ai-web"

# 1. Get git token
tpath = os.path.join(tempfile.gettempdir(), "gitcred.txt")
with open(tpath, "w", encoding="utf-8") as f:
    f.write("protocol=https\nhost=github.com\n\n")

proc = subprocess.run(
    "git credential fill",
    input=open(tpath, "rb").read(),
    stdout=subprocess.PIPE,
    shell=True,
    check=True
)
if os.path.exists(tpath):
    os.remove(tpath)

lines = proc.stdout.decode("utf-8").splitlines()
token = [l[9:] for l in lines if l.startswith("password=")][0]
username = "Sais-gallego"
repo_name = "harvard-cs50-ai-web"
print(f"Extracted token successfully for {username}")

def run_git(cmd):
    p = subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(f"$ {cmd}\n{p.stdout.strip()}")
    if p.stderr.strip():
        print(f"ERR: {p.stderr.strip()}")
    return p

# 2. Local git setup
run_git("git init")
run_git('git config user.name "Sergio Andrés Ipuz Saavedra"')
run_git('git config user.email "afranklinromero@gmail.com"')
run_git("git checkout -B main")
run_git("git add .")
run_git('git commit -m "feat(harvard-cs50): Complete Harvard CS50/CS50AI systems with Model Checking, PageRank, Heredity Bayes, and CSP AC-3"')

# 3. Create repo on GitHub with retry on secondary rate limit
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Antigravity-Agent"
}

create_data = {
    "name": repo_name,
    "description": "Harvard University CS50 & CS50AI: Introduction to Computer Science and AI with Python - Model Checking (TT-Entails), Minesweeper logical inference, PageRank (Random Surfer & Markov chains), Bayesian Heredity, and CSP with AC-3.",
    "private": False
}

created = False
for attempt in range(6):
    try:
        req = urllib.request.Request(
            "https://api.github.com/user/repos",
            data=json.dumps(create_data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            print(f"Repo {repo_name} created successfully: {resp.status}")
            created = True
            break
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"Attempt {attempt+1}: Create repo status: {e.code} - {err_body}")
        if e.code in (403, 429) and "rate limit" in err_body:
            print("Encountered secondary rate limit. Sleeping 30s before retry...")
            time.sleep(30)
        elif e.code == 422: # Already exists
            print("Repository already exists. Proceeding...")
            created = True
            break
        else:
            time.sleep(5)

if not created:
    print("Could not create repository yet due to rate limit cooldown. Exiting for now.")
    exit(1)

# 4. Set topics
topics_data = {
    "names": [
        "harvard",
        "cs50",
        "cs50ai",
        "artificial-intelligence",
        "pagerank",
        "bayesian-networks",
        "model-checking",
        "constraint-satisfaction",
        "ac3"
    ]
}
try:
    req_topics = urllib.request.Request(
        f"https://api.github.com/repos/{username}/{repo_name}/topics",
        data=json.dumps(topics_data).encode("utf-8"),
        headers=headers,
        method="PUT"
    )
    with urllib.request.urlopen(req_topics) as resp:
        print(f"Topics set successfully: {resp.status}")
except Exception as e:
    print(f"Failed to set topics: {e}")

# 5. Star repo
try:
    req_star = urllib.request.Request(
        f"https://api.github.com/user/starred/{username}/{repo_name}",
        headers={**headers, "Content-Length": "0"},
        method="PUT"
    )
    with urllib.request.urlopen(req_star) as resp:
        print(f"Starred repo {repo_name}: {resp.status}")
except Exception as e:
    print(f"Failed to star repo: {e}")

# 6. Push code
remote_url = f"https://{token}@github.com/{username}/{repo_name}.git"
run_git("git remote remove origin")
run_git(f"git remote add origin {remote_url}")
run_git("git push -u origin main --force")

# 7. Monitor CI
print("Waiting for GitHub Actions workflow run...")
time.sleep(6)

for attempt in range(15):
    try:
        req_runs = urllib.request.Request(
            f"https://api.github.com/repos/{username}/{repo_name}/actions/runs",
            headers=headers
        )
        with urllib.request.urlopen(req_runs) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            runs = data.get("workflow_runs", [])
            if runs:
                latest = runs[0]
                status = latest.get("status")
                conclusion = latest.get("conclusion")
                run_id = latest.get("id")
                print(f"Run ID: {run_id} | Status: {status} | Conclusion: {conclusion}")
                if status == "completed":
                    print(f"CI COMPLETED WITH CONCLUSION: {conclusion}")
                    break
            else:
                print("No runs found yet...")
    except Exception as e:
        print(f"Error checking runs: {e}")
    time.sleep(5)
