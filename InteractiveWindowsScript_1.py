import os 
import subprocess

"""

these functions are used for file searching within the system

"""

#Searches a given directory for a given type of file / files
def searchDirectory (rootDirectory, fileTypes):
    foundFiles = []

    #Checks if Directory exixts
    if not os.path.exists(rootDirectory):
        return (f"Invalid Directory")
    
    #Searches for files
    try:
        for fileType in fileTypes:
            for root, dirs, files in os.walk(rootDirectory):
                for file in files: 
                    if file.endswith(fileType): 
                        foundFiles.append(os.path.join(root, file))

    except:
        return (f"Error with file type searching")
    
    #Outputs found files
    return foundFiles 
        
#Searches for files with a keyword in the name of said file    
def keywordSearchExternal (rootDirectory, keyword):
    trueFiles = []

    #Checks if Directory exixts
    if not os.path.exists(rootDirectory):
        return(f"Directory does not exist.")
    
    #Searches for files w/ key word
    for root, dirs, files in os.walk(rootDirectory):
        for file in files: 
            if keyword in file:
                trueFiles.append(os.path.join(root,file))

    #Outputs found files
    return trueFiles

#Searches inside files for a specific key word
def keywordSearchInternal (rootDirectory, keyword): 
    trueFiles = []
    errorFiles = []

    #Checks if Directory Exists 
    if not os.path.exists(rootDirectory):  
        return (f"Invalid Directory")
    
    #Searches for files w/ key word
    for root, dirs, files in os.walk(rootDirectory):
        for file in files:
            filePath = os.path.join(root, file)
            try:
                with open(filePath, "r", encoding="utf-8") as file:
                    for lineNumber, line in enumerate(file, start=1):
                        if keyword in line:
                            trueFiles.append(filePath)

            except Exception as e:
                errorFiles.append(filePath)

    #Outputs found files
    return trueFiles

"""

functions related to user sorting and organization

"""

def get_local_users():
    powershell_script = r"""
    $allUsers = Get-LocalUser

    $adminUsernames = Get-LocalGroupMember -Group "Administrators" | Where-Object {
        $_.ObjectClass -eq 'User'

    } | ForEach-Object {
        ($_.Name -split '\\')[-1].ToLower()

    }

    $admins = @()
    $nonAdmins = @()

    foreach ($user in $allUsers) {
        if ($adminUsernames -contains $user.Name.ToLower()) {
            $admins += $user.Name

        } else {
            $nonAdmins += $user.Name

        }
    }

    Write-Output "ADMINS:"
    $admins
    Write-Output "NONADMINS:"
    $nonAdmins

    """

    result = subprocess.run(
        ["powershell", "-Command", powershell_script],
        capture_output=True,
        text=True

    )

    if result.returncode != 0:
        print("PowerShell error:", result.stderr)
        return [], []  # Avoid returning None

    lines = result.stdout.strip().splitlines()

    admins = []
    non_admins = []
    current = None

    for line in lines:
        line = line.strip()

        if line == "ADMINS:":
            current = "admins"
            continue

        elif line == "NONADMINS:":
            current = "non_admins"
            continue

        if current == "admins":
            admins.append(line)
    
        elif current == "non_admins":
            non_admins.append(line)

    return admins, non_admins

def remove_user(username):
    powershell_command = f"""
        $username = '{username}'

        if (Get-LocalUser -Name $username -ErrorAction SilentlyContinue) {{
            try {{
                Remove-LocalUser -Name $username
                Write-Output "User '$username' deleted successfully."

            }} catch {{
                Write-Output "Error deleting user '$username': $($_.Exception.Message)"

            }}

        }} else {{
            Write-Output "User '$username' not found."

        }}
        
    """

    result = subprocess.run(
        ["powershell", "-Command", powershell_command],
        capture_output=True,
        text=True

    )

    return result.stdout.strip()

def add_user(username, password):
    powershell_command = f"""
        $username = '{username}'
        $password = '{password}'

        New-LocalUser -Name $username -Password (ConvertTo-SecureString $password -AsPlainText -Force)

    """
    try:
        result = subprocess.run(
            ["powershell", "-Command", powershell_command],
            capture_output=True,
            text=True,
            check=True

        )

        return f"User '{username}' created successfully."

    except subprocess.CalledProcessError as e:
        return f"Failed to create user '{username}'. Error: {e}"
    
def disable_user(username):
    powershell_command = f"Get -LocalUser {username} | Disable-LocalUser"

    try:
        result = subprocess.run(
            ["powershell", "-Command", powershell_command],
            capture_output=True,
            text=True,
            check=True

        )

        return f"Successfully Disabled User: {username}."
    
    except subprocess.CalledProcessError as e:
        return f"Failed to Disable user: '{username}'. Error: '{e}'"

"""

sets local security policies 
NEEDS EXPANDED 

"""

def set_local_security_policies():
    results = []

    all_policies = {
        "policies": [
            # Account Lockout Policies 
            "/lockoutthreshold:5",
            "/lockoutduration:30",
            "/lockoutwindow:15",

            # Password Policies
            "/minpwlen:8",
            "/maxpwage:45",
            "/minpwage:30",
            "/uniquepw:3",

        ],
        
        "audit_policies": [
            "Account Logon",
            "Logon/Logoff",
            "Object Access",
            "Privilege Use",
            "Detailed Tracking",
            "Policy Change",
            "Account Management",
            
        ]
    }
    
    for key, policy_type in all_policies.items():
        for policy in policy_type:
            if key == "audit_policies":
                powershell_command = f'auditpol /set /category:"{policy}" /success:enable /failure:enable'

            elif key == "policies":
                powershell_command = f"net accounts {policy}"

            else:
                return "Error with set_local_security_policies function"

            result = subprocess.run(
                ["powershell", "-Command", powershell_command],
                capture_output=True, 
                text=True

            )

            results.append(f"{policy} " + result.stdout.strip())

    return results
