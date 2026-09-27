import customtkinter as ctk
from database import init_db, register_user, verify_user
from ai_helper import AIAssistant

# Appearance Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI Assistant System")
        self.geometry("700x550")
        self.resizable(False, False)

        # Initialize local database
        init_db()
        self.ai = AIAssistant()

        # Build Login UI
        self.build_auth_screen()

    def build_auth_screen(self):
        """Build Tabview for Login and Registration."""
        self.auth_frame = ctk.CTkFrame(self)
        self.auth_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title_label = ctk.CTkLabel(self.auth_frame, text="Welcome Back", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(20, 10))

        self.tabview = ctk.CTkTabview(self.auth_frame, width=400, height=350)
        self.tabview.pack(pady=10)

        self.tab_login = self.tabview.add("Login")
        self.tab_register = self.tabview.add("Register")

        self.setup_login_tab()
        self.setup_register_tab()

        self.status_label = ctk.CTkLabel(self.auth_frame, text="", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=5)

    def setup_login_tab(self):
        self.login_user_entry = ctk.CTkEntry(self.tab_login, placeholder_text="Username", width=250)
        self.login_user_entry.pack(pady=15)

        self.login_pass_entry = ctk.CTkEntry(self.tab_login, placeholder_text="Password", show="*", width=250)
        self.login_pass_entry.pack(pady=15)

        btn = ctk.CTkButton(self.tab_login, text="Login", command=self.handle_login, width=250)
        btn.pack(pady=20)

    def setup_register_tab(self):
        self.reg_user_entry = ctk.CTkEntry(self.tab_register, placeholder_text="New Username", width=250)
        self.reg_user_entry.pack(pady=15)

        self.reg_pass_entry = ctk.CTkEntry(self.tab_register, placeholder_text="New Password", show="*", width=250)
        self.reg_pass_entry.pack(pady=15)

        btn = ctk.CTkButton(self.tab_register, text="Create Account", command=self.handle_register, width=250)
        btn.pack(pady=20)

    def handle_login(self):
        user = self.login_user_entry.get().strip()
        pwd = self.login_pass_entry.get().strip()
        success, message = verify_user(user, pwd)

        if success:
            self.auth_frame.destroy()
            self.build_dashboard_screen(user)
        else:
            self.status_label.configure(text=message, text_color="red")

    def handle_register(self):
        user = self.reg_user_entry.get().strip()
        pwd = self.reg_pass_entry.get().strip()
        success, message = register_user(user, pwd)

        color = "green" if success else "red"
        self.status_label.configure(text=message, text_color=color)

    def build_dashboard_screen(self, username):
        """Main Dashboard featuring the AI Assistant Chat interface."""
        self.dash_frame = ctk.CTkFrame(self)
        self.dash_frame.pack(padx=20, pady=20, fill="both", expand=True)

        header = ctk.CTkLabel(self.dash_frame, text=f"Hello, {username}! 👋", font=ctk.CTkFont(size=20, weight="bold"))
        header.pack(pady=10)

        # Chat display area
        self.chat_box = ctk.CTkTextbox(self.dash_frame, width=620, height=330, state="disabled", wrap="word")
        self.chat_box.pack(pady=10)

        # Input controls
        input_frame = ctk.CTkFrame(self.dash_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=10)

        self.prompt_entry = ctk.CTkEntry(input_frame, placeholder_text="Ask your AI assistant...", width=480)
        self.prompt_entry.pack(side="left", padx=(0, 10))

        send_btn = ctk.CTkButton(input_frame, text="Send", width=100, command=self.send_to_ai)
        send_btn.pack(side="right")

    def send_to_ai(self):
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            return

        self.append_chat(f"You: {prompt}\n")
        self.prompt_entry.delete(0, "end")

        # Get answer from Gemini service
        response = self.ai.ask(prompt)
        self.append_chat(f"AI: {response}\n\n")

    def append_chat(self, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", text)
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

if __name__ == "__main__":
    app = App()
    app.mainloop()