import sys
import os

# Add the project root directory to sys.path dynamically
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.views.views import SmartStudentPlannerApp

if __name__ == "__main__":
    # Boot the Model-View-Controller framework
    SmartStudentPlannerApp().run()
