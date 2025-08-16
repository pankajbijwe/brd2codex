# brd2codex

Install dependencies:
  pip install openai azure-ai-formrecognizer azure-ai-textanalytics requests

Set Environment Variable
  export GITHUB_TOKEN=<github-pat>
  export GITHUB_REPO="org/repo"
  export GITHUB_USERNAME="username"


What this orchestrator solution does -
  * Clones your GitHub repo securely
  * Creates a timestamped feature branch
  * Scans all .java files for context
  * Uses GPT to generate enhancements
  * Applies changes to existing or new files
  * Commits and pushes to GitHub 
  * Creates a pull request to main 
