from GUI.login import LoginWindow
from GUI.dashboard import Dashboard

if __name__ == "__main__":

    login = LoginWindow()

    usn = login.run()

    if usn:
        dashboard = Dashboard(usn)
        dashboard.run()
        
    else:
        print("Login cancelled.")