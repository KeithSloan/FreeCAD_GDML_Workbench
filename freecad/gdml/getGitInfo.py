import FreeCAD
import FreeCADGui
import os
import subprocess

class gitInfo:
    def __init__(self, wbName, reproName):
        self.workbenchName = wbName
        # Specify the path to your workbench directory
        self.workbench_path = self.get_workbench_path(reproName)
    
    #def get_workbench_path(self):
    def get_workbench_path(self, name):

        # Check if the workbench is loaded
        if self.workbenchName not in FreeCADGui.listWorkbenches():
            print(f"Workbench '{self.workbenchName}' is not found.")
            return None

        modPath = os.path.join(FreeCAD.ConfigGet("UserAppData"), "Mod")
        return os.path.join(modPath, name)
        # ALL chatgpt suggestions failed now commented out
        # Get the workbench object
        # workbench = FreeCADGui.getWorkbench(self.workbenchName)
        #print(dir(workbench))
        #
        # Get the directory where the workbench is located
        # self.workbench_path = os.path.dirname(workbench.__file__)
        # return self.workbench_path

        # Try to get the module associated with the workbench
        # try:
        #    # Get the module name from the workbench class
        #    module_name = workbench.__class__.__module__

        #   # Import the module to access its __file__ attribute
        #   workbench_module = __import__(module_name)
        #    self.workbench_path = os.path.dirname(workbench_module.__file__)
        #    print(f"workbench path {self.workbench_path}")
        #    return self.workbench_path
        #except (AttributeError, ImportError) as e:
        #    print(f"Error determining the path for workbench '{self.workbenchName}': {e}")
        #    return None

        # Get the directory where the workbench is located
        # self.workbench_path = os.path.dirname(workbench.__file__)
        # return self.workbench_path


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
        return(self.run_git_command(['rev-parse', 'HEAD'], self.workbench_path))
    
def test_functions():
    gI = gitInfo("GDML_Workbench","GDML")
    print(dir(gitInfo))
    print(f"Branch Name: {gI.get_branch_name()}")
    print(f"Commit Hash: {gI.get_commit_hash()}")
