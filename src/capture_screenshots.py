import sys
import os

# Add the project root directory to sys.path dynamically
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from kivy.app import App
from kivy.clock import Clock
from src.views.views import SmartStudentPlannerApp

class ScreenshotApp(SmartStudentPlannerApp):
    """
    Automated utility subclass of SmartStudentPlannerApp designed to programmatically
    navigate through all screens, capture their visuals, and save them.
    """
    def build(self):
        sm = super().build()
        # Create folder
        os.makedirs("documentation/screenshots", exist_ok=True)
        
        # Schedule the screenshot sequence
        Clock.schedule_once(lambda dt: self.capture_onboarding(sm), 0.5)
        return sm

    def capture_onboarding(self, sm):
        print("[CAPTURE] Capturing Onboarding Screen...")
        sm.get_screen("onboarding").export_to_png("documentation/screenshots/1_onboarding.png")
        
        # Transition to Login
        sm.current = "login"
        Clock.schedule_once(lambda dt: self.capture_login(sm), 0.5)

    def capture_login(self, sm):
        print("[CAPTURE] Capturing Login Screen...")
        sm.get_screen("login").export_to_png("documentation/screenshots/2_login.png")
        
        # Log in programmatically with seeded credentials to prepare the dashboard/list states
        success, msg = self.controller.login("student", "password123")
        if not success:
            # Fallback if DB was purged/reset
            self.controller.register("student", "password123")
            self.controller.login("student", "password123")
            
        # Transition to Dashboard
        sm.current = "dashboard"
        sm.get_screen("dashboard").refresh_data()
        Clock.schedule_once(lambda dt: self.capture_dashboard(sm), 0.5)

    def capture_dashboard(self, sm):
        print("[CAPTURE] Capturing Dashboard Screen...")
        sm.get_screen("dashboard").export_to_png("documentation/screenshots/3_dashboard.png")
        
        # Transition to Task List
        sm.current = "task_list"
        sm.get_screen("task_list").refresh_data()
        Clock.schedule_once(lambda dt: self.capture_task_list(sm), 0.5)

    def capture_task_list(self, sm):
        print("[CAPTURE] Capturing Task List Screen...")
        sm.get_screen("task_list").export_to_png("documentation/screenshots/4_task_list.png")
        
        # Set up Task Form Screen (Add mode)
        form = sm.get_screen("task_form")
        form.set_mode(edit_task=None)
        
        # Transition to Task Form
        sm.current = "task_form"
        Clock.schedule_once(lambda dt: self.capture_task_form(sm), 0.5)

    def capture_task_form(self, sm):
        print("[CAPTURE] Capturing Task Form Screen...")
        sm.get_screen("task_form").export_to_png("documentation/screenshots/5_task_form.png")
        
        # Transition to Settings
        sm.current = "settings"
        sm.get_screen("settings").refresh_data()
        Clock.schedule_once(lambda dt: self.capture_settings(sm), 0.5)

    def capture_settings(self, sm):
        print("[CAPTURE] Capturing Settings Screen...")
        sm.get_screen("settings").export_to_png("documentation/screenshots/6_settings.png")
        
        # Clean shutdown of the App
        print("[CAPTURE] All screen layouts successfully captured in documentation/screenshots/")
        App.get_running_app().stop()

if __name__ == "__main__":
    ScreenshotApp().run()
