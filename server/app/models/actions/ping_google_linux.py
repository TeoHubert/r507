from models.host import Host

def run(host: Host, parametre: str = None) -> str:
    try:
        value = float(host.execute_ssh_command("ping -c 1 8.8.8.8 | grep 'time=' | awk -F'time=' '{print $2}' | awk '{print $1}'"))
        return value
    except Exception as e:
        return f"Error: {e}"