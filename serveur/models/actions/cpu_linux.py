from models.host import Host

def run(host: Host) -> str:
    try:
        value = float(host.execute_ssh_command("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"))
        return value
    except Exception as e:
        return f"Error: {e}"