import tkinter as tk
from tkinter import messagebox

from data.students import students


class LoginWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Student Expert System")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.logged_in_usn = None

        self.build_ui()

    def build_ui(self):

        title = tk.Label(
            self.root,
            text="Student Expert System",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            self.root,
            text="Enter your USN",
            font=("Arial", 12)
        )
        subtitle.pack()

        self.usn_entry = tk.Entry(
            self.root,
            width=30,
            font=("Arial", 12)
        )
        self.usn_entry.pack(pady=15)

        login_btn = tk.Button(
            self.root,
            text="Login",
            width=15,
            command=self.login
        )
        login_btn.pack(pady=10)

    def login(self):

        usn = self.usn_entry.get().strip().upper()

        if usn in students:

            self.logged_in_usn = usn

            messagebox.showinfo(
                "Success",
                f"Welcome {students[usn]['name']}"
            )

            self.root.destroy()

        else:

            messagebox.showerror(
                "Error",
                "USN Not Registered"
            )

    def run(self):

        self.root.mainloop()

        return self.logged_in_usn