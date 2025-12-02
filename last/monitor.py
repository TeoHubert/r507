from pydantic import BaseModel,computed_field
import os,json,re,requests

## ANCIEN CODE AVANT LA BASE DE DONNEES AVEC JSON, A GARDER POUR REFERENCE ##

# Regex nécéssaires au programme
cpu_model_regex = re.compile(r"model name.*: (?P<model>.*)")
ip_address_regex = re.compile(r"\b(?P<ip>(?:(?:[1-9]?\d|1\d{2}|2(?:[0-4][0-9]|5[0-4]))\.){3}(?:[1-9]?\d|1\d{2}|2(?:[0-4][0-9]|5[0-4])))\b/(?P<mask>\d{1,2})")
mac_address_regex = re.compile(r"link/ether (?P<mac>(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})")
interfaces_regex = re.compile(r"\d+: (?P<name>\w+): <")
ping_regex = re.compile(r"(?P<res>\d) received")

nb_ping_try = 1


class IPAddress(BaseModel):
    ip: str = None
    mask: str = None
    joignable: bool = False

    def model_post_init(self, __context):
        self.test_joignable()
    
    def test_joignable(self):
        cmd = os.popen(f"ping -c {nb_ping_try} {self.ip}")
        res = cmd.read()
        matchs = ping_regex.search(res)
        self.joignable = False
        if int(matchs.group("res")) == nb_ping_try:
            self.joignable = True

    @computed_field
    @property
    def ville(self) -> str:
        r = requests.get(f"http://ip-api.com/json/{self.ip}")
        if r.status_code == 200 and r.json()['status'] == "success": return r.json()['city']
        return "Unknown"
    
    @computed_field
    @property
    def pays(self) -> str:
        r = requests.get(f"http://ip-api.com/json/{self.ip}")
        if r.status_code == 200 and r.json()['status'] == "success": return r.json()['country']
        return "Unknown"


class MacAddress(BaseModel):
    mac: str = None
    
    @computed_field
    @property
    def constructeur(self) -> str:
        r = requests.get(f"https://api.macvendors.com/{self.mac}")
        if r.status_code == 200: return r.text
        return "Unknown"


class NetworkInterface(BaseModel):
    name: str = None
    ip_addresses: list[IPAddress] = []
    mac_addresses: list[MacAddress] = []


class Cpu(BaseModel):
    model: str = None

    def model_post_init(self, __context):
        self.init_model()

    def init_model(self):
        cmd = os.popen("cat /proc/cpuinfo")
        matchs = cpu_model_regex.search(cmd.read())
        self.model = matchs.group("model")


class Memory(BaseModel):
    total: str = None
    used: str = None
    free: str = None

    def model_post_init(self, __context):
        self.init_memory()

    def init_memory(self):
        cmd = os.popen("free -h")
        lines = cmd.readlines()
        mem_line = lines[1].split()
        self.total = mem_line[1]
        self.used = mem_line[2]
        self.free = mem_line[3]


class Partition(BaseModel):
    name: str = None
    total: str = None
    used: str = None
    free: str = None


class Disk(BaseModel):
    name: str = None
    partitions: list[Partition] = []


class Ordinateur(BaseModel):
    hostname: str = None
    cpu: Cpu = Cpu()
    memory: Memory = Memory()
    network_interfaces: list[NetworkInterface] = []
    disk: list[Disk] = []

    def model_post_init(self, __context):
        self.init_hostname()
        self.init_network_interfaces()
        self.init_disk()

    def init_hostname(self):
        cmd = os.popen("hostname")
        self.hostname = cmd.read().strip()

    def init_network_interfaces(self):
        cmd = os.popen("ip link show")
        interfaces = interfaces_regex.findall(cmd.read())
        for interface in interfaces:
            network_interface = NetworkInterface(name=interface)
            # Récupération des addresses IP
            cmd_ip = os.popen(f"ip addr show {interface}")
            ips = ip_address_regex.findall(cmd_ip.read())
            for ip in ips:
                ip_address = IPAddress(ip=ip[0], mask=ip[1])
                network_interface.ip_addresses.append(ip_address)
            # Récupération des addresses MAC
            cmd_ip = os.popen(f"ip addr show {interface}")
            macs = mac_address_regex.findall(cmd_ip.read())
            for mac in macs:
                mac_address = MacAddress(mac=mac)
                network_interface.mac_addresses.append(mac_address)
            # Ajout de l'interface réseau à l'ordinateur
            self.network_interfaces.append(network_interface)
            
    def init_disk(self):
        cmd = os.popen("lsblk -o NAME,SIZE,TYPE")
        disks_info = cmd.readlines()[1:]
        current_disk = None
        for line in disks_info:
            parts = line.split()
            name, type = parts[0], parts[2]
            if type == "disk":
                if current_disk: self.disk.append(current_disk)
                current_disk = Disk(name=name, partitions=[])
            elif type == "part" and current_disk:
                cmd = os.popen(f"df -h /dev/{name[2:]}")
                df_info = cmd.readlines()[1].split()
                current_disk.partitions.append(Partition(name=name[2:], total=df_info[1], used=df_info[2], free=df_info[3]))
        self.disk.append(current_disk)

if __name__ == "__main__":
    cp_list = list()
    cp_list.append(Ordinateur())

    temp = [cp.model_dump() for cp in cp_list]
    with open("datas.json", "w") as outfile:
        json.dump(temp, outfile, indent=4)