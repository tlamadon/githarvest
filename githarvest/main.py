import subprocess
import json

def get_git_status(repo_path="."):
    """
    Gets the git status of the specified repository.

    :param repo_path: Path to the git repository. Defaults to the current directory.
    :return: Dictionary with the status of the repository.
    """
    # Change to the repo directory if not current
    original_cwd = subprocess.os.getcwd()
    subprocess.os.chdir(repo_path)

    # Run git status command
    result = subprocess.run(["git", "status", "-sb"], capture_output=True, text=True)
    
    # Change back to the original directory
    subprocess.os.chdir(original_cwd)

    # Process the git status output
    lines = result.stdout.strip().split('\n')
    status = {
        "staged": [],
        "not_staged": [],
        "untracked": [],
        "status": lines[0]
    }

    for line in lines:
        if line.startswith('??'):
            status["untracked"].append(line[3:])
        elif line.startswith('A '):
            status["staged"].append(line[3:])
        elif line.startswith(' M') or line.startswith('M '):
            status["not_staged"].append(line[3:])
    
    return status

def save_status_to_json(status, filename="git_status.json"):
    """
    Saves the git status to a JSON file.

    :param status: Git status to save.
    :param filename: Name of the JSON file to save the status to.
    """
    with open(filename, 'w') as f:
        json.dump(status, f, indent=4)

if __name__ == "__main__":
    status = get_git_status()  # You can pass a repo_path if necessary
    save_status_to_json(status)
    print(f"Git status saved to git_status.json")
