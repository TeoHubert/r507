from models.host import Host
import json

def run(host: Host, parametre: str = None) -> str:
    try:
        result = host.execute_ssh_command("vtysh -c 'show interface brief json'")
        result = result.replace("'", '"')
        data = json.loads(result)
        status = data[parametre['interface']]['status']
        if status == "up": status = 2
        elif status == "down": status = 1
        else: status = 0
        return status
    except Exception as e:
        print(f"Erreur lors de la récupération du statut de l'interface: {e}")
        return 0

if __name__ == "__main__":
    print(run())