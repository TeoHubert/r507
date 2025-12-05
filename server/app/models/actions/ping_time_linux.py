from models.host import Host

def run(host: Host, parametre: str = None) -> str:
    try:
        dest = parametre["dest"] if parametre and "dest" in parametre else "8.8.8.8"
        brute_value = host.execute_ssh_command(f"ping -c 1 {dest} | grep 'time=' | awk -F'time=' '{{print $2}}' | awk '{{print $1}}'")
        value = float(brute_value)
        return value
    except Exception as e:
        print(f"Error in ping_time_linux action: {e}")
        return 1000.0