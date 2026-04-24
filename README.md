# BRD2CodeX
Automate the end-to-end process of enhancing a Spring Boot Java application based on Business Requirement Documents (BRD). It leverages Azure OpenAI (GPT-4) to interpret rules and automatically generate, commit, and propose code changes via GitHub.

# Prerequisites
  Python 3.x
  Git installed and configured on the local machine.
  Dependencies: openai, requests.
  Azure OpenAI Instance: Specifically an active deployment of gpt-4.
  
# Install dependencies:
  pip install openai azure-ai-formrecognizer azure-ai-textanalytics requests

# Workflow Overview
  Clone: Pulls the latest source code from the repository.
  Branch: Creates a unique feature branch with a timestamp.
  Scan: Walks through the project directory to map all .java files.
  Generate: Sends the business rule and code context to Azure OpenAI.
  Apply: Parses the AI response and writes enhancements to the local files.
  Push: Commits the changes and pushes the new branch to the remote.
  PR: Automatically opens a Pull Request on GitHub for review.

# Configuration
  Before running the script, ensure the following variables/credentials are configured:
  Variable	Description
  REPO_URL	The URL of your Java repository.
  GITHUB_TOKEN	A Personal Access Token (PAT) with repo permissions.
  openai.api_key	Your Azure OpenAI API key.
  openai.api_base	Your Azure resource endpoint URL.

# Function Reference
  scan_java_project()
  Recursively scans the local directory for .java files and stores their content in a dictionary. To prevent token overflow, only the first 500 characters of each file are sent to the AI
  
  generate_enhancement(rule_text, code_map)
  The core logic engine. It constructs a prompt containing the business rule (e.g., "If customer has loyalty status ‘Gold’, apply 10% discount") and the existing code structure.
  
  apply_enhancements(text)
  Uses Regex to identify file paths and code blocks within the AI's response.
  Existing files: Appends the enhancement to the end of the file.
  New files: Creates the file and necessary directory structure.
