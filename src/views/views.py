import sys
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.core.window import Window

from src.views.styles import UIStyles
from src.controllers.main_controller import MainController

# Enforce standard responsive desktop screen size for Windows testing
Window.size = (400, 700)
Window.minimum_width = 350
Window.minimum_height = 600

class CanvasWidget(BoxLayout):
    """
    View Component: A layout box that draws a beautiful solid background color
    on its Kivy canvas.
    """
    def __init__(self, bg_color, radius=[0], **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            if self.radius[0] > 0:
                RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
            else:
                Rectangle(pos=self.pos, size=self.size)


class RoundedCard(CanvasWidget):
    """A sleek rounded container for cards and dashboards."""
    def __init__(self, **kwargs):
        super().__init__(bg_color=UIStyles.CARD_COLOR, radius=UIStyles.RADIUS_CARD, **kwargs)
        self.padding = UIStyles.PADDING_INNER


class GlowCard(BoxLayout):
    """
    View Component: A premium card drawn with a thin glowing neon border line,
    matching our mock-up designs.
    """
    def __init__(self, border_color=UIStyles.ACCENT_COLOR, **kwargs):
        super().__init__(**kwargs)
        self.border_color = border_color
        self.padding = [8, 10, 8, 10]
        self.spacing = 3
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Draw solid card background
            Color(*UIStyles.CARD_COLOR)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
            
            # Draw thin glowing neon border line
            Color(*self.border_color)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 12), width=1.3)


class CustomButton(Button):
    """Flat-designed button with custom active hover borders."""
    def __init__(self, bg_color=UIStyles.ACCENT_COLOR, text_color=UIStyles.TEXT_PRIMARY, radius=UIStyles.RADIUS_BUTTON, **kwargs):
        super().__init__(**kwargs)
        self.background_color = [0, 0, 0, 0]  # transparent default Kivy brush
        self.background_normal = ""
        self.bg_color = bg_color
        self.text_color = text_color
        self.radius = radius
        self.color = text_color
        self.font_size = "14sp"
        self.font_name = "Roboto"
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)


class GradientPillButton(Button):
    """
    View Component: A pill-shaped, premium launch button with an electric-violet
    background and an outer neon-cyan glowing outline, matching the design mock-up.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = [0, 0, 0, 0]
        self.background_normal = ""
        self.color = [1, 1, 1, 1]
        self.font_size = "15sp"
        self.bold = True
        self.font_name = "Roboto"
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Draw solid Pill (Radius size set to half of button height, e.g. 24)
            Color(*UIStyles.ACCENT_COLOR)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[24])
            
            # Draw Neon Cyan glowing border around the pill shape
            Color(*UIStyles.LOW_PRIORITY)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 24), width=1.6)


# --- INDIVIDUAL SCREENS ---

class OnboardingScreen(Screen):
    """View Layer: Redesigned premium welcoming screen matching the design mock-up layout."""
    def __init__(self, controller: MainController, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

        # Deep Slate-Black startup background
        root = CanvasWidget(bg_color=[0.04, 0.04, 0.05, 1.0], orientation="vertical")
        root.padding = [16, 20, 16, 20]
        root.spacing = 15

        # 1. Main Desk Illustration Image
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            illustration_img = Image(
                source=logo_path,
                size_hint_y=0.42,
                allow_stretch=True,
                keep_ratio=True,
                pos_hint={"center_x": 0.5}
            )
            root.add_widget(illustration_img)
        else:
            logo_placeholder = Label(text="🎓", font_size="70sp", size_hint_y=0.35)
            root.add_widget(logo_placeholder)

        # 2. App Branding Header
        header_box = BoxLayout(orientation="vertical", size_hint_y=None, height=55, spacing=2)
        title_lbl = Label(
            text="SMART PLANNER",
            font_size="24sp",
            bold=True,
            color=UIStyles.TEXT_PRIMARY,
            font_name="Roboto",
            halign="center"
        )
        tagline_lbl = Label(
            text="Your AI-powered Academic Command Center",
            font_size="13sp",
            color=[0.70, 0.61, 0.84, 1.0],  # Soft purple tint
            font_name="Roboto",
            halign="center"
        )
        header_box.add_widget(title_lbl)
        header_box.add_widget(tagline_lbl)
        root.add_widget(header_box)

        # 3. Bullet Point Value Statements (with glowing blue bullets)
        bullets_box = BoxLayout(orientation="vertical", size_hint_y=None, height=80, spacing=4)
        bullets_box.padding = [40, 0, 40, 0]
        
        b1 = Label(text="[color=#00E5FF]•[/color]  Plan smarter.", markup=True, font_size="14sp", bold=True, halign="left")
        b1.bind(size=b1.setter('text_size'))
        b2 = Label(text="[color=#00E5FF]•[/color]  Study better.", markup=True, font_size="14sp", bold=True, halign="left")
        b2.bind(size=b2.setter('text_size'))
        b3 = Label(text="[color=#00E5FF]•[/color]  Achieve more.", markup=True, font_size="14sp", bold=True, halign="left")
        b3.bind(size=b3.setter('text_size'))
        
        bullets_box.add_widget(b1)
        bullets_box.add_widget(b2)
        bullets_box.add_widget(b3)
        root.add_widget(bullets_box)

        # 4. Dot Carousel Indicators
        carousel_lbl = Label(
            text="[color=#7C4DFF]•[/color] [color=#7C4DFF]•[/color] [color=#353540]•[/color]",
            markup=True,
            font_size="16sp",
            size_hint_y=None,
            height=15,
            halign="center"
        )
        root.add_widget(carousel_lbl)

        # 5. Features Glowing Grids (Horizontal Row of 3 Cards)
        grid_layout = GridLayout(cols=3, size_hint_y=None, height=65, spacing=8)
        
        # Card 1: Courses
        courses_card = GlowCard(border_color=UIStyles.ACCENT_COLOR, orientation="vertical")
        c_title = Label(text="📚 Courses", font_size="12sp", bold=True, color=UIStyles.TEXT_PRIMARY, halign="center")
        c_sub = Label(text="Organize tasks", font_size="9sp", color=UIStyles.TEXT_SECONDARY, halign="center")
        courses_card.add_widget(c_title)
        courses_card.add_widget(c_sub)
        
        # Card 2: Analytics
        analytics_card = GlowCard(border_color=UIStyles.LOW_PRIORITY, orientation="vertical")
        a_title = Label(text="📊 Analytics", font_size="12sp", bold=True, color=UIStyles.TEXT_PRIMARY, halign="center")
        a_sub = Label(text="Track goals", font_size="9sp", color=UIStyles.TEXT_SECONDARY, halign="center")
        analytics_card.add_widget(a_title)
        analytics_card.add_widget(a_sub)
        
        # Card 3: Sync
        sync_card = GlowCard(border_color=UIStyles.ACCENT_COLOR, orientation="vertical")
        s_title = Label(text="☁️ Sync", font_size="12sp", bold=True, color=UIStyles.TEXT_PRIMARY, halign="center")
        s_sub = Label(text="Auto backup", font_size="9sp", color=UIStyles.TEXT_SECONDARY, halign="center")
        sync_card.add_widget(s_title)
        sync_card.add_widget(s_sub)
        
        grid_layout.add_widget(courses_card)
        grid_layout.add_widget(analytics_card)
        grid_layout.add_widget(sync_card)
        root.add_widget(grid_layout)

        # Bottom spacer
        root.add_widget(BoxLayout(size_hint_y=None, height=5))

        # 6. Primary Launch Action Button (Gradient Pill style)
        launch_btn = GradientPillButton(
            text="Launch My Planner  ➔",
            size_hint_y=None,
            height=48,
            on_press=self.go_to_login
        )
        root.add_widget(launch_btn)

        self.add_widget(root)

    def go_to_login(self, instance):
        # Route to Login screen
        self.manager.current = "login"


class LoginScreen(Screen):
    """View Layer: Handles user logins and registrations."""
    def __init__(self, controller: MainController, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

        # Root Dark layout
        root = CanvasWidget(bg_color=UIStyles.BG_COLOR, orientation="vertical")
        root.padding = UIStyles.PADDING_OUTER * 1.5
        root.spacing = UIStyles.SPACING_GUTTER

        # Logo Header Block (Centered Logo)
        logo_layout = BoxLayout(orientation="vertical", size_hint_y=0.35, spacing=5)
        
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            logo_img = Image(
                source=logo_path,
                size_hint=(None, None),
                size=(110, 110),
                pos_hint={"center_x": 0.5}
            )
            logo_layout.add_widget(logo_img)
        else:
            logo_placeholder = Label(text="🎓", font_size="48sp", size_hint_y=None, height=90)
            logo_layout.add_widget(logo_placeholder)

        logo_label = Label(
            text="SMART PLANNER",
            font_size="22sp",
            bold=True,
            color=UIStyles.TEXT_PRIMARY,
            font_name="Roboto",
            size_hint_y=None,
            height=28
        )
        sub_label = Label(
            text="Secure Academic Credentials Gate",
            font_size="12sp",
            color=UIStyles.TEXT_SECONDARY,
            font_name="Roboto",
            size_hint_y=None,
            height=16
        )
        logo_layout.add_widget(logo_label)
        logo_layout.add_widget(sub_label)
        root.add_widget(logo_layout)

        # Form Inputs Panel
        form_card = RoundedCard(orientation="vertical", size_hint_y=0.45, spacing=12)
        
        # Username Input
        u_box = BoxLayout(orientation="vertical", spacing=4)
        u_label = Label(text="Username", font_size="12sp", color=UIStyles.TEXT_SECONDARY, size_hint_y=None, height=18, halign="left")
        u_label.bind(size=u_label.setter('text_size'))
        self.u_input = TextInput(
            text="",
            multiline=False,
            write_tab=False,
            background_color=UIStyles.BG_COLOR,
            foreground_color=UIStyles.TEXT_PRIMARY,
            font_size="14sp"
        )
        u_box.add_widget(u_label)
        u_box.add_widget(self.u_input)
        form_card.add_widget(u_box)

        # Password Input
        p_box = BoxLayout(orientation="vertical", spacing=4)
        p_label = Label(text="Password (min 6 characters)", font_size="12sp", color=UIStyles.TEXT_SECONDARY, size_hint_y=None, height=18, halign="left")
        p_label.bind(size=p_label.setter('text_size'))
        self.p_input = TextInput(
            text="",
            multiline=False,
            password=True,
            write_tab=False,
            background_color=UIStyles.BG_COLOR,
            foreground_color=UIStyles.TEXT_PRIMARY,
            font_size="14sp"
        )
        p_box.add_widget(p_label)
        p_box.add_widget(self.p_input)
        form_card.add_widget(p_box)

        # Error notification label
        self.err_label = Label(text="", font_size="12sp", color=UIStyles.ERROR_RED, size_hint_y=None, height=22)
        form_card.add_widget(self.err_label)
        root.add_widget(form_card)

        # Buttons Control Panel
        btns_layout = BoxLayout(orientation="vertical", size_hint_y=0.2, spacing=8)
        
        login_btn = CustomButton(text="LOG IN", size_hint_y=0.5, on_press=self.do_login)
        register_btn = CustomButton(
            text="CREATE ACCOUNT", 
            bg_color=UIStyles.CARD_COLOR, 
            text_color=UIStyles.ACCENT_COLOR, 
            size_hint_y=0.5, 
            on_press=self.do_register
        )
        
        btns_layout.add_widget(login_btn)
        btns_layout.add_widget(register_btn)
        root.add_widget(btns_layout)
        
        self.add_widget(root)

    def do_login(self, instance):
        username = self.u_input.text.strip()
        password = self.p_input.text
        
        success, msg = self.controller.login(username, password)
        if success:
            self.err_label.text = ""
            self.p_input.text = ""
            # Route to Dashboard
            self.manager.current = "dashboard"
            self.manager.get_screen("dashboard").refresh_data()
        else:
            self.err_label.color = UIStyles.ERROR_RED
            self.err_label.text = msg

    def do_register(self, instance):
        username = self.u_input.text.strip()
        password = self.p_input.text
        
        success, msg = self.controller.register(username, password)
        if success:
            self.err_label.color = UIStyles.SUCCESS_GREEN
            self.err_label.text = msg
            self.p_input.text = ""
        else:
            self.err_label.color = UIStyles.ERROR_RED
            self.err_label.text = msg


class DashboardScreen(Screen):
    """View Layer: Synthesizes progress stats and lists critical upcoming deadlines."""
    def __init__(self, controller: MainController, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

        # Main Layout
        self.root = CanvasWidget(bg_color=UIStyles.BG_COLOR, orientation="vertical")
        self.root.padding = UIStyles.PADDING_OUTER
        self.root.spacing = UIStyles.SPACING_GUTTER

        # Top Header Bar
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=50)
        self.user_label = Label(text="👤 Hello Student", font_size="16sp", bold=True, color=UIStyles.TEXT_PRIMARY, halign="left")
        self.user_label.bind(size=self.user_label.setter('text_size'))
        settings_btn = CustomButton(text="⚙️", size_hint=(None, None), size=(40, 40), bg_color=UIStyles.CARD_COLOR, on_press=self.go_settings)
        header.add_widget(self.user_label)
        header.add_widget(settings_btn)
        self.root.add_widget(header)

        # Progress Stats Card
        self.stats_card = RoundedCard(orientation="vertical", size_hint_y=0.25, spacing=5)
        self.stats_label = Label(text="ACADEMIC PROGRESS", font_size="12sp", bold=True, color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=20)
        self.stats_label.bind(size=self.stats_label.setter('text_size'))
        self.metrics_label = Label(text="0% Complete (0 Tasks Active)", font_size="14sp", color=UIStyles.TEXT_PRIMARY, halign="left", size_hint_y=None, height=25)
        self.metrics_label.bind(size=self.metrics_label.setter('text_size'))
        
        # Horizontal visual progress meter
        self.progress_bar_box = BoxLayout(size_hint_y=None, height=12)
        self.progress_bar_box.bind(pos=self.draw_progress, size=self.draw_progress)
        
        self.stats_card.add_widget(self.stats_label)
        self.stats_card.add_widget(self.metrics_label)
        self.stats_card.add_widget(self.progress_bar_box)
        self.root.add_widget(self.stats_card)

        # Priorities Split Cards
        priority_layout = GridLayout(cols=2, size_hint_y=0.15, spacing=10)
        self.high_card = RoundedCard(orientation="vertical")
        self.high_num = Label(text="0", font_size="24sp", bold=True, color=UIStyles.HIGH_PRIORITY)
        self.high_lbl = Label(text="High Urgency", font_size="11sp", color=UIStyles.TEXT_SECONDARY)
        self.high_card.add_widget(self.high_num)
        self.high_card.add_widget(self.high_lbl)
        
        self.med_card = RoundedCard(orientation="vertical")
        self.med_num = Label(text="0", font_size="24sp", bold=True, color=UIStyles.MED_PRIORITY)
        self.med_lbl = Label(text="Med/Low Urgency", font_size="11sp", color=UIStyles.TEXT_SECONDARY)
        self.med_card.add_widget(self.med_num)
        self.med_card.add_widget(self.med_lbl)
        
        priority_layout.add_widget(self.high_card)
        priority_layout.add_widget(self.med_card)
        self.root.add_widget(priority_layout)

        # Section label: Upcoming Deadlines
        sec_label = Label(text="🕒 CRITICAL DEADLINES (< 48h)", font_size="12sp", bold=True, color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=20)
        sec_label.bind(size=sec_label.setter('text_size'))
        self.root.add_widget(sec_label)

        # Deadlines Scroll list
        self.scroll = ScrollView(size_hint_y=0.35)
        self.list_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter('height'))
        self.scroll.add_widget(self.list_box)
        self.root.add_widget(self.scroll)

        # Navigation Action Panel
        nav_panel = BoxLayout(orientation="horizontal", size_hint_y=0.12, spacing=10)
        task_list_btn = CustomButton(text="📑 MY TASKS", size_hint_x=0.5, bg_color=UIStyles.CARD_COLOR, text_color=UIStyles.ACCENT_COLOR, on_press=self.go_task_list)
        add_task_btn = CustomButton(text="➕ ADD TASK", size_hint_x=0.5, on_press=self.go_add_task)
        nav_panel.add_widget(task_list_btn)
        nav_panel.add_widget(add_task_btn)
        self.root.add_widget(nav_panel)

        self.add_widget(self.root)
        self.ratio = 0

    def draw_progress(self, *args):
        self.progress_bar_box.canvas.clear()
        with self.progress_bar_box.canvas:
            # Draw track
            Color(*UIStyles.BG_COLOR)
            RoundedRectangle(pos=self.progress_bar_box.pos, size=self.progress_bar_box.size, radius=[6])
            
            # Draw fill
            if self.ratio > 0:
                Color(*UIStyles.ACCENT_COLOR)
                fill_w = (self.progress_bar_box.width * self.ratio) / 100
                RoundedRectangle(pos=self.progress_bar_box.pos, size=(fill_w, self.progress_bar_box.height), radius=[6])

    def refresh_data(self):
        user = self.controller.get_logged_in_user()
        if not user:
            return
            
        self.user_label.text = f"👤 Welcome, {user}"
        self.controller.sync_load()

        # Fetch active metrics
        m = self.controller.get_dashboard_metrics()
        self.ratio = m["ratio"]
        self.metrics_label.text = f"{m['ratio']}% Complete ({m['pending']} pending / {m['total']} total)"
        self.draw_progress()

        # Update Urgency numbers
        self.high_num.text = str(m["high_priority_pending"])
        self.med_num.text = str(m["medium_priority_pending"] + m["low_priority_pending"])

        # Fetch upcoming deadlines (< 48h)
        self.list_box.clear_widgets()
        upcoming = self.controller.get_upcoming_tasks(48)
        
        if not upcoming:
            empty_lbl = Label(text="🎉 No urgent deadlines! Enjoy your study flow.", font_size="13sp", color=UIStyles.TEXT_SECONDARY, size_hint_y=None, height=50)
            self.list_box.add_widget(empty_lbl)
        else:
            for t in upcoming:
                item = RoundedCard(orientation="horizontal", size_hint_y=None, height=55, spacing=10)
                item.padding = [10, 5, 10, 5]
                
                # Priority Indicator Bullet
                bullet = CanvasWidget(bg_color=UIStyles.get_priority_color(t.priority), radius=[10], size_hint=(None, None), size=(12, 12), pos_hint={"center_y": 0.5})
                
                # Task Text Info
                txt_box = BoxLayout(orientation="vertical")
                title_lbl = Label(text=t.title, font_size="13sp", bold=True, color=UIStyles.TEXT_PRIMARY, halign="left")
                title_lbl.bind(size=title_lbl.setter('text_size'))
                meta_lbl = Label(text=f"{t.module} • Due: {t.due_date}", font_size="11sp", color=UIStyles.TEXT_SECONDARY, halign="left")
                meta_lbl.bind(size=meta_lbl.setter('text_size'))
                txt_box.add_widget(title_lbl)
                txt_box.add_widget(meta_lbl)
                
                item.add_widget(bullet)
                item.add_widget(txt_box)
                self.list_box.add_widget(item)

    def go_settings(self, instance):
        self.manager.current = "settings"
        self.manager.get_screen("settings").refresh_data()

    def go_task_list(self, instance):
        self.manager.current = "task_list"
        self.manager.get_screen("task_list").refresh_data()

    def go_add_task(self, instance):
        form = self.manager.get_screen("task_form")
        form.set_mode(edit_task=None)
        self.manager.current = "task_form"


class TaskListScreen(Screen):
    """View Layer: Displays scrollable lists of tasks, supports live-searching and filter chips."""
    def __init__(self, controller: MainController, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.active_chip = "All"

        root = CanvasWidget(bg_color=UIStyles.BG_COLOR, orientation="vertical")
        root.padding = UIStyles.PADDING_OUTER
        root.spacing = UIStyles.SPACING_GUTTER

        # Top Header Bar
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=45)
        back_btn = CustomButton(text="◀ BACK", size_hint=(None, None), size=(70, 38), bg_color=UIStyles.CARD_COLOR, text_color=UIStyles.ACCENT_COLOR, on_press=self.go_back)
        title_lbl = Label(text="📑 MY ACADEMIC TASKS", font_size="16sp", bold=True, color=UIStyles.TEXT_PRIMARY, halign="center")
        header.add_widget(back_btn)
        header.add_widget(title_lbl)
        header.add_widget(BoxLayout(size_hint_x=None, width=70))  # balance spacer
        root.add_widget(header)

        # Dynamic Search Bar
        search_card = RoundedCard(orientation="horizontal", size_hint_y=None, height=50)
        search_card.padding = [10, 5, 10, 5]
        self.search_input = TextInput(
            hint_text="🔍 Search tasks, modules, notes...",
            multiline=False,
            write_tab=False,
            background_color=[0,0,0,0],
            foreground_color=UIStyles.TEXT_PRIMARY,
            hint_text_color=UIStyles.TEXT_SECONDARY,
            font_size="14sp",
            pos_hint={"center_y": 0.5}
        )
        self.search_input.bind(text=self.on_search_change)
        search_card.add_widget(self.search_input)
        root.add_widget(search_card)

        # Filter Chips Panel (Horizontal Buttons)
        chips_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=8)
        self.chips = {}
        for level in ["All", "High", "Medium", "Low"]:
            btn = CustomButton(
                text=level, 
                bg_color=UIStyles.ACCENT_COLOR if level == "All" else UIStyles.CARD_COLOR,
                text_color=UIStyles.TEXT_PRIMARY if level == "All" else UIStyles.TEXT_SECONDARY,
                on_press=self.make_chip_callback(level)
            )
            self.chips[level] = btn
            chips_layout.add_widget(btn)
        root.add_widget(chips_layout)

        # Scroll list of active student tasks
        self.scroll = ScrollView()
        self.list_box = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter('height'))
        self.scroll.add_widget(self.list_box)
        root.add_widget(self.scroll)

        # Floating Bottom Add Action
        add_btn = CustomButton(text="➕ ADD NEW TASK", size_hint_y=None, height=48, on_press=self.go_add_task)
        root.add_widget(add_btn)

        self.add_widget(root)

    def go_back(self, instance):
        self.manager.current = "dashboard"
        self.manager.get_screen("dashboard").refresh_data()

    def go_add_task(self, instance):
        form = self.manager.get_screen("task_form")
        form.set_mode(edit_task=None)
        self.manager.current = "task_form"

    def make_chip_callback(self, level):
        return lambda instance: self.toggle_filter_chip(level)

    def toggle_filter_chip(self, selected_level):
        self.active_chip = selected_level
        
        # Recolor active chip
        for level, btn in self.chips.items():
            if level == selected_level:
                btn.bg_color = UIStyles.ACCENT_COLOR
                btn.text_color = UIStyles.TEXT_PRIMARY
            else:
                btn.bg_color = UIStyles.CARD_COLOR
                btn.text_color = UIStyles.TEXT_SECONDARY
            btn.redraw()
            
        self.refresh_data()

    def on_search_change(self, instance, value):
        self.refresh_data()

    def refresh_data(self):
        self.list_box.clear_widgets()
        keyword = self.search_input.text
        
        # Load filtered queries
        matches = self.controller.search_tasks(keyword, self.active_chip)
        
        # Sort by urgency (earliest first)
        matches.sort(key=lambda t: t.due_date)

        if not matches:
            no_lbl = Label(text="No matching tasks found.", font_size="13sp", color=UIStyles.TEXT_SECONDARY, size_hint_y=None, height=60)
            self.list_box.add_widget(no_lbl)
            return

        for t in matches:
            # Card Panel
            card = RoundedCard(orientation="horizontal", size_hint_y=None, height=75, spacing=8)
            card.padding = [10, 8, 10, 8]
            
            # Checkbox Box Layout
            check_box_layout = BoxLayout(size_hint_x=None, width=35, pos_hint={"center_y": 0.5})
            chk = CheckBox(active=t.completed, size_hint=(None, None), size=(30, 30))
            chk.bind(active=self.make_toggle_callback(t.task_id))
            check_box_layout.add_widget(chk)
            card.add_widget(check_box_layout)

            # Task Detail Section
            txt_box = BoxLayout(orientation="vertical")
            title_lbl = Label(
                text=t.title, 
                font_size="13sp", 
                bold=True, 
                color=UIStyles.TEXT_PRIMARY if not t.completed else UIStyles.TEXT_MUTED,
                halign="left"
            )
            title_lbl.bind(size=title_lbl.setter('text_size'))
            
            meta_lbl = Label(
                text=f"{t.module} • Due: {t.due_date}", 
                font_size="11sp", 
                color=UIStyles.TEXT_SECONDARY if not t.completed else UIStyles.TEXT_MUTED,
                halign="left"
            )
            meta_lbl.bind(size=meta_lbl.setter('text_size'))
            txt_box.add_widget(title_lbl)
            txt_box.add_widget(meta_lbl)
            card.add_widget(txt_box)

            # Priority Badge & Action buttons
            actions_box = BoxLayout(orientation="horizontal", size_hint_x=None, width=110, spacing=5, pos_hint={"center_y": 0.5})
            
            # Edit Button
            edit_btn = CustomButton(text="✏️", size_hint=(None, None), size=(32, 32), bg_color=UIStyles.CARD_COLOR, on_press=self.make_edit_callback(t))
            # Delete Button
            del_btn = CustomButton(text="🗑️", size_hint=(None, None), size=(32, 32), bg_color=UIStyles.CARD_COLOR, text_color=UIStyles.ERROR_RED, on_press=self.make_delete_callback(t.task_id))
            # Priority badge bar
            badge = CanvasWidget(bg_color=UIStyles.get_priority_color(t.priority), radius=[6], size_hint=(None, None), size=(10, 32))
            
            actions_box.add_widget(edit_btn)
            actions_box.add_widget(del_btn)
            actions_box.add_widget(badge)
            card.add_widget(actions_box)

            self.list_box.add_widget(card)

    def make_toggle_callback(self, task_id):
        return lambda instance, value: self.toggle_task(task_id)

    def toggle_task(self, task_id):
        self.controller.toggle_task_completion(task_id)
        self.refresh_data()

    def make_edit_callback(self, task_obj):
        return lambda instance: self.edit_task(task_obj)

    def edit_task(self, task_obj):
        form = self.manager.get_screen("task_form")
        form.set_mode(edit_task=task_obj)
        self.manager.current = "task_form"

    def make_delete_callback(self, task_id):
        return lambda instance: self.delete_task(task_id)

    def delete_task(self, task_id):
        self.controller.delete_task(task_id)
        self.refresh_data()


class TaskFormScreen(Screen):
    """View Layer: Manages Add / Edit properties inputs with pre-filled sanitizations."""
    def __init__(self, controller: MainController, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.editing_task_id = None

        root = CanvasWidget(bg_color=UIStyles.BG_COLOR, orientation="vertical")
        root.padding = UIStyles.PADDING_OUTER
        root.spacing = UIStyles.SPACING_GUTTER

        # Header Bar
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=45)
        self.header_title = Label(text="📝 CREATE NEW TASK", font_size="16sp", bold=True, color=UIStyles.TEXT_PRIMARY)
        header.add_widget(self.header_title)
        root.add_widget(header)

        # Form Scroll Area
        form_scroll = ScrollView()
        form_box = BoxLayout(orientation="vertical", spacing=12, size_hint_y=None)
        form_box.bind(minimum_height=form_box.setter('height'))

        # Title Field
        t_box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=65)
        t_lbl = Label(text="Task Title *", font_size="12sp", color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=18)
        t_lbl.bind(size=t_lbl.setter('text_size'))
        self.title_in = TextInput(hint_text="e.g. Draft dissertation structure", multiline=False, background_color=UIStyles.CARD_COLOR, foreground_color=UIStyles.TEXT_PRIMARY, font_size="13sp")
        t_box.add_widget(t_lbl)
        t_box.add_widget(self.title_in)
        form_box.add_widget(t_box)

        # Module Field
        m_box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=65)
        m_lbl = Label(text="Academic Module *", font_size="12sp", color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=18)
        m_lbl.bind(size=m_lbl.setter('text_size'))
        self.module_in = TextInput(hint_text="e.g. LDC6004M", multiline=False, background_color=UIStyles.CARD_COLOR, foreground_color=UIStyles.TEXT_PRIMARY, font_size="13sp")
        m_box.add_widget(m_lbl)
        m_box.add_widget(self.module_in)
        form_box.add_widget(m_box)

        # Due Date Field (with pre-filled format reference)
        d_box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=65)
        d_lbl = Label(text="Due Date * (YYYY-MM-DD)", font_size="12sp", color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=18)
        d_lbl.bind(size=d_lbl.setter('text_size'))
        self.date_in = TextInput(hint_text="e.g. 2026-06-11", multiline=False, background_color=UIStyles.CARD_COLOR, foreground_color=UIStyles.TEXT_PRIMARY, font_size="13sp")
        d_box.add_widget(d_lbl)
        d_box.add_widget(self.date_in)
        form_box.add_widget(d_box)

        # Priority Toggle Selection
        p_box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=70)
        p_lbl = Label(text="Task Priority *", font_size="12sp", color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=18)
        p_lbl.bind(size=p_lbl.setter('text_size'))
        
        # Priority Buttons Group
        p_row = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=40)
        self.p_buttons = {}
        self.selected_priority = "Medium"
        for priority in ["High", "Medium", "Low"]:
            btn = CustomButton(
                text=priority,
                bg_color=UIStyles.ACCENT_COLOR if priority == "Medium" else UIStyles.CARD_COLOR,
                text_color=UIStyles.TEXT_PRIMARY if priority == "Medium" else UIStyles.TEXT_SECONDARY,
                on_press=self.make_priority_callback(priority)
            )
            self.p_buttons[priority] = btn
            p_row.add_widget(btn)
        p_box.add_widget(p_lbl)
        p_box.add_widget(p_row)
        form_box.add_widget(p_box)

        # Notes Field
        n_box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=120)
        n_lbl = Label(text="Syllabus Notes / Details", font_size="12sp", color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=18)
        n_lbl.bind(size=n_lbl.setter('text_size'))
        self.notes_in = TextInput(hint_text="Enter task instructions or syllabus references...", multiline=True, background_color=UIStyles.CARD_COLOR, foreground_color=UIStyles.TEXT_PRIMARY, font_size="13sp")
        n_box.add_widget(n_lbl)
        n_box.add_widget(self.notes_in)
        form_box.add_widget(n_box)

        # Feedback Panel
        self.err_lbl = Label(text="", font_size="12sp", color=UIStyles.ERROR_RED, size_hint_y=None, height=25)
        form_box.add_widget(self.err_lbl)

        form_scroll.add_widget(form_box)
        root.add_widget(form_scroll)

        # Bottom Actions
        actions_panel = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=10)
        cancel_btn = CustomButton(text="CANCEL", size_hint_x=0.5, bg_color=UIStyles.CARD_COLOR, text_color=UIStyles.ACCENT_COLOR, on_press=self.do_cancel)
        save_btn = CustomButton(text="SAVE TASK", size_hint_x=0.5, on_press=self.do_save)
        actions_panel.add_widget(cancel_btn)
        actions_panel.add_widget(save_btn)
        root.add_widget(actions_panel)

        self.add_widget(root)

    def set_mode(self, edit_task=None):
        """Switches form layouts between fresh Add actions vs pre-filled Edit bindings."""
        self.err_lbl.text = ""
        
        if edit_task is None:
            self.editing_task_id = None
            self.header_title.text = "📝 CREATE NEW TASK"
            self.title_in.text = ""
            self.module_in.text = ""
            self.date_in.text = datetime.now().strftime("%Y-%m-%d")  # pre-fill today
            self.notes_in.text = ""
            self.select_priority("Medium")
        else:
            self.editing_task_id = edit_task.task_id
            self.header_title.text = "📝 EDIT ACADEMIC TASK"
            self.title_in.text = edit_task.title
            self.module_in.text = edit_task.module
            self.date_in.text = edit_task.due_date
            self.notes_in.text = edit_task.notes
            self.select_priority(edit_task.priority)

    def make_priority_callback(self, priority):
        return lambda instance: self.select_priority(priority)

    def select_priority(self, selected_p):
        self.selected_priority = selected_p
        for priority, btn in self.p_buttons.items():
            if priority == selected_p:
                btn.bg_color = UIStyles.get_priority_color(priority)
                btn.text_color = UIStyles.TEXT_PRIMARY
            else:
                btn.bg_color = UIStyles.CARD_COLOR
                btn.text_color = UIStyles.TEXT_SECONDARY
            btn.redraw()

    def do_cancel(self, instance):
        if self.editing_task_id:
            self.manager.current = "task_list"
            self.manager.get_screen("task_list").refresh_data()
        else:
            self.manager.current = "dashboard"
            self.manager.get_screen("dashboard").refresh_data()

    def do_save(self, instance):
        t = self.title_in.text
        m = self.module_in.text
        d = self.date_in.text
        p = self.selected_priority
        n = self.notes_in.text
        
        if self.editing_task_id:
            success, msg = self.controller.edit_task(self.editing_task_id, t, m, d, p, n)
        else:
            success, msg = self.controller.add_task(t, m, d, p, n)
            
        if success:
            self.err_lbl.text = ""
            if self.editing_task_id:
                self.manager.current = "task_list"
                self.manager.get_screen("task_list").refresh_data()
            else:
                self.manager.current = "dashboard"
                self.manager.get_screen("dashboard").refresh_data()
        else:
            self.err_lbl.text = msg


class SettingsScreen(Screen):
    """View Layer: Renders credentials profile stats, Purge features, and Harvard citations."""
    def __init__(self, controller: MainController, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

        root = CanvasWidget(bg_color=UIStyles.BG_COLOR, orientation="vertical")
        root.padding = UIStyles.PADDING_OUTER
        root.spacing = UIStyles.SPACING_GUTTER

        # Header Bar
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=45)
        back_btn = CustomButton(text="◀ BACK", size_hint=(None, None), size=(70, 38), bg_color=UIStyles.CARD_COLOR, text_color=UIStyles.ACCENT_COLOR, on_press=self.go_back)
        title_lbl = Label(text="⚙️ SYSTEM SETTINGS", font_size="16sp", bold=True, color=UIStyles.TEXT_PRIMARY, halign="center")
        header.add_widget(back_btn)
        header.add_widget(title_lbl)
        header.add_widget(BoxLayout(size_hint_x=None, width=70))
        root.add_widget(header)

        # Profile Card
        profile_card = RoundedCard(orientation="vertical", size_hint_y=0.22, spacing=5)
        self.profile_lbl = Label(text="STUDENT PROFILE", font_size="12sp", bold=True, color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=18)
        self.profile_lbl.bind(size=self.profile_lbl.setter('text_size'))
        self.username_lbl = Label(text="👤 Username: -", font_size="14sp", color=UIStyles.TEXT_PRIMARY, halign="left", size_hint_y=None, height=22)
        self.username_lbl.bind(size=self.username_lbl.setter('text_size'))
        self.inst_lbl = Label(text="🏫 Institution: York St John University", font_size="13sp", color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=22)
        self.inst_lbl.bind(size=self.inst_lbl.setter('text_size'))
        profile_card.add_widget(self.profile_lbl)
        profile_card.add_widget(self.username_lbl)
        profile_card.add_widget(self.inst_lbl)
        root.add_widget(profile_card)

        # Systems Info Card
        sys_card = RoundedCard(orientation="vertical", size_hint_y=0.25, spacing=5)
        self.sys_title = Label(text="DATA STORAGE STATS", font_size="12sp", bold=True, color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=18)
        self.sys_title.bind(size=self.sys_title.setter('text_size'))
        self.tasks_lbl = Label(text="💾 Scoped Database Records: 0", font_size="13sp", color=UIStyles.TEXT_PRIMARY, halign="left", size_hint_y=None, height=22)
        self.tasks_lbl.bind(size=self.tasks_lbl.setter('text_size'))
        self.format_lbl = Label(text="🗄️ Save Format: Atomic JSON", font_size="13sp", color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=22)
        self.format_lbl.bind(size=self.format_lbl.setter('text_size'))
        self.file_lbl = Label(text="📂 DB Path: storage.json", font_size="11sp", color=UIStyles.TEXT_MUTED, halign="left", size_hint_y=None, height=22)
        self.file_lbl.bind(size=self.file_lbl.setter('text_size'))
        sys_card.add_widget(self.sys_title)
        sys_card.add_widget(self.tasks_lbl)
        sys_card.add_widget(self.format_lbl)
        sys_card.add_widget(self.file_lbl)
        root.add_widget(sys_card)

        # Academic Citation Card (Distinction criteria for Professional Practice)
        cite_card = RoundedCard(orientation="vertical", size_hint_y=0.33, spacing=5)
        cite_title = Label(text="🎓 ACADEMIC REFERENCE STANDARDS", font_size="11sp", bold=True, color=UIStyles.TEXT_SECONDARY, halign="left", size_hint_y=None, height=18)
        cite_title.bind(size=cite_title.setter('text_size'))
        self.cite_desc = Label(
            text="* Citation standard: York St John Harvard Style.\n"
                 "* UI guidelines: Material Design 3 guidelines.\n"
                 "* Development: MVC Pattern (SoC verification).\n"
                 "* Security: Salted SHA-256 local registry.\n"
                 "* Framework dependencies: Kivy v2.3.1.",
            font_size="11sp",
            color=UIStyles.TEXT_SECONDARY,
            halign="left",
            valign="top"
        )
        self.cite_desc.bind(size=self.cite_desc.setter('text_size'))
        cite_card.add_widget(cite_title)
        cite_card.add_widget(self.cite_desc)
        root.add_widget(cite_card)

        # Controls
        ctrls = BoxLayout(orientation="vertical", size_hint_y=0.2, spacing=10)
        self.clear_btn = CustomButton(text="🚨 PURGE ALL USER DATA", bg_color=UIStyles.CARD_COLOR, text_color=UIStyles.ERROR_RED, size_hint_y=0.5, on_press=self.do_clear_storage)
        logout_btn = CustomButton(text="LOG OUT", size_hint_y=0.5, on_press=self.do_logout)
        ctrls.add_widget(self.clear_btn)
        ctrls.add_widget(logout_btn)
        root.add_widget(ctrls)

        self.add_widget(root)
        self.confirm_state = False

    def go_back(self, instance):
        self.manager.current = "dashboard"
        self.manager.get_screen("dashboard").refresh_data()

    def refresh_data(self):
        user = self.controller.get_logged_in_user()
        self.username_lbl.text = f"👤 Username: {user if user else 'Guest'}"
        self.controller.sync_load()
        records_count = len(self.controller.get_user_tasks())
        self.tasks_lbl.text = f"💾 Scoped Database Records: {records_count}"
        self.clear_btn.text = "🚨 PURGE ALL USER DATA"
        self.clear_btn.bg_color = UIStyles.CARD_COLOR
        self.clear_btn.redraw()
        self.confirm_state = False

    def do_logout(self, instance):
        self.controller.logout()
        self.manager.current = "login"

    def do_clear_storage(self, instance):
        if not self.confirm_state:
            # First tap: prompt confirmation
            self.clear_btn.text = "⚠️ TAP AGAIN TO CONFIRM PURGE"
            self.clear_btn.bg_color = UIStyles.ERROR_RED
            self.clear_btn.redraw()
            self.confirm_state = True
        else:
            # Second tap: execute wipe
            user = self.controller.get_logged_in_user()
            if user:
                # Remove all tasks belonging to user
                users_tasks = self.controller.get_user_tasks()
                for t in users_tasks:
                    self.controller.delete_task(t.task_id)
            self.controller.logout()
            self.manager.current = "login"
            self.confirm_state = False


# --- CORE APP MANAGER ---

class SmartStudentPlannerApp(App):
    """View Layer: The main Kivy Application class that runs the screen router."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = MainController("storage.json")

    def build(self):
        self.title = "Smart Student Planner"
        self.icon = "src/views/logo.png"  # Set professional generated brand icon!

        # Screen Manager
        sm = ScreenManager()
        
        # Instantiate and add screens (Starting with the new visual Onboarding Screen!)
        sm.add_widget(OnboardingScreen(self.controller, name="onboarding"))
        sm.add_widget(LoginScreen(self.controller, name="login"))
        sm.add_widget(DashboardScreen(self.controller, name="dashboard"))
        sm.add_widget(TaskListScreen(self.controller, name="task_list"))
        sm.add_widget(TaskFormScreen(self.controller, name="task_form"))
        sm.add_widget(SettingsScreen(self.controller, name="settings"))

        return sm

if __name__ == "__main__":
    SmartStudentPlannerApp().run()
