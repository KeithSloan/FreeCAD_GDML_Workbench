import FreeCAD
import FreeCADGui
import os
import subprocess

class gitInfo:
    
    def __init__(self):
        # Specify the path to your workbench directory
        self.workbench_path = self.get_workbench_path("GDML")
    
    def get_workbench_path(self, workbench_name):
        # Check if the workbench is loaded
        if workbench_name not in FreeCADGui.listWorkbenches():
            print(f"Workbench '{workbench_name}' is not found.")
            return None

        # Get the workbench object
        self.workbench = FreeCADGui.getWorkbench(workbench_name)

        # Get the directory where the workbench is located
        self.workbench_path = os.path.dirname(self.workbench.__file__)
        return self.workbench_path


    # Function to run a git command and get the output
    def run_git_command(self, command, repo_path):
        try:
            result = subprocess.check_output(['git'] + command, cwd=repo_path).strip().decode('utf-8')
            return result
        except subprocess.CalledProcessError:
            return None

    # Get the branch name
    def get_branch_name(self):
        return(self.run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'], self.workbench_path))

    # Get the latest commit hash
    def get_commit_hash(self):
        return(self.run_git_command(['rev-parse', 'HEAD'], self,workbench_path))
    
def test_functions():
    gInfo = getInfo()
    print(f"Branch Name {gInfo.get_branch_name()}")
    print(f"Commit Hash: {gInfo.get_commit_hash()}")
