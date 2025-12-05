from models.host import Host

def run(host: Host, parametre: str = None) -> str:
    try:
        value = (int(host.execute_ssh_command("free -m | grep Mem | awk '{print $3}'"))/int(host.execute_ssh_command("free -m | grep Mem | awk '{print $2}'"))*100)
        return value
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(run())