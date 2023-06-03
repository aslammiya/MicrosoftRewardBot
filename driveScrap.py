import platform

def check_os():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Linux":
        return "Linux"
    else:
        return "Unknown"

# Call the function to check the OS
os_type = check_os()
print("Operating System:", os_type)
