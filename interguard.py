import os
import sys
import winreg
from typing import List

def list_startup_programs() -> List[str]:
    """Lists all programs that run at Windows startup."""
    startup_programs = []
    registry_paths = [
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
    ]

    for reg_path in registry_paths:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
            for i in range(winreg.QueryInfoKey(key)[1]):
                name, _, _ = winreg.EnumValue(key, i)
                startup_programs.append(name)

    return startup_programs

def disable_startup_program(program_name: str) -> bool:
    """Disables a program from running at Windows startup."""
    registry_paths = [
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
    ]

    for reg_path in registry_paths:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, program_name)
                return True
        except FileNotFoundError:
            continue

    return False

def enable_startup_program(program_name: str, program_path: str) -> bool:
    """Enables a program to run at Windows startup."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, program_name, 0, winreg.REG_SZ, program_path)
            return True
    except Exception as e:
        print(f"Failed to enable program: {e}")
        return False

def main():
    print("InterGuard: Manage your Windows startup programs")
    while True:
        print("\nOptions:")
        print("1. List startup programs")
        print("2. Disable a startup program")
        print("3. Enable a startup program")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            programs = list_startup_programs()
            print("\nStartup Programs:")
            for program in programs:
                print(f"- {program}")

        elif choice == '2':
            program_name = input("Enter the program name to disable: ")
            if disable_startup_program(program_name):
                print(f"{program_name} has been disabled.")
            else:
                print(f"Failed to disable {program_name}.")

        elif choice == '3':
            program_name = input("Enter the program name to enable: ")
            program_path = input("Enter the full path to the program: ")
            if enable_startup_program(program_name, program_path):
                print(f"{program_name} has been enabled.")
            else:
                print(f"Failed to enable {program_name}.")

        elif choice == '4':
            print("Exiting InterGuard.")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()