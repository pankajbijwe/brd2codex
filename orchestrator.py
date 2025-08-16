import os, subprocess, json, re
from datetime import datetime
import requests
import openai

# === CONFIG ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
LOCAL_DIR = "repo"

# === STEP 1: Clone Repo ===
def clone_repo():
    subprocess.run(["git", "clone", REPO_URL, LOCAL_DIR])
    os.chdir(LOCAL_DIR)

# === STEP 2: Create Feature Branch ===
def create_feature_branch():
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    branch_name = f"feature/brd-enhancement-{timestamp}"
    subprocess.run(["git", "checkout", "-b", branch_name])
    return branch_name

# === STEP 3: Scan Project ===
def scan_java_project():
    structure = {}
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".java"):
                path = os.path.join(root, file)
                with open(path) as f:
                    structure[path] = f.read()
    return structure

# === STEP 4: Generate Enhancement ===
def generate_enhancement(rule_text, code_map):
    context = "\n".join([f"File: {p}\n{c[:500]}" for p, c in code_map.items()])
    prompt = f"""
You are enhancing a Spring Boot Java app. Current codebase:

{context}

Implement this rule:
"{rule_text}"

Generate enhancements with file paths and code blocks.
"""
    openai.api_type = "azure"
    openai.api_base = "https://<your-openai-endpoint>"
    openai.api_version = "2023-07-01-preview"
    openai.api_key = "<your-openai-key>"

    response = openai.ChatCompletion.create(
        engine="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=3000
    )
    return response['choices'][0]['message']['content']

# === STEP 5: Apply Enhancements ===
def apply_enhancements(text):
    blocks = re.split(r"File:\s*(.+?)\n", text)
    for i in range(1, len(blocks), 2):
        path = blocks[i].strip()
        code = blocks[i+1].strip()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            with open(path, "a") as f:
                f.write("\n\n// Enhancement\n" + code)
        else:
            with open(path, "w") as f:
                f.write(code)

# === STEP 6: Commit & Push ===
def commit_and_push(branch_name):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Add BRD-based enhancement"])
    subprocess.run(["git", "push", "--set-upstream", "origin", branch_name])

# === STEP 7: Create Pull Request ===
def create_pull_request(branch_name):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "title": f"BRD Enhancement - {branch_name}",
        "head": branch_name,
        "base": "main",
        "body": "This PR adds enhancements based on the latest BRD document using Azure AI."
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f" PR created: {response.json()['html_url']}")
    else:
        print(f" Failed to create PR: {response.text}")

# === MAIN ORCHESTRATOR ===
def run_pipeline(brd_rule):
    clone_repo()
    branch = create_feature_branch()
    code_map = scan_java_project()
    enhancement = generate_enhancement(brd_rule, code_map)
    apply_enhancements(enhancement)
    commit_and_push(branch)
    create_pull_request(branch)

# === RUN ===
if __name__ == "__main__":
    brd_rule = "If customer has loyalty status ‘Gold’, apply 10% discount."
    run_pipeline(brd_rule)
