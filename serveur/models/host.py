from typing import Optional
from sqlmodel import Field, SQLModel
import paramiko
from tools.password_security import dechiffrer_mot_de_passe

class Host(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ip: str
    username: Optional[str] = None
    password: Optional[str] = None
    ssh_port: Optional[int] = 22

    def __str__(self):
        return f"#{self.id} | Host {self.name} d'ip {self.ip}"
    
    def __repr__(self):
        return f"<Host(id='{self.id}', name='{self.name}', ip='{self.ip}')>"
    
    def execute_ssh_command(self, command: str) -> str:
        """Establish an SSH connection and execute a command."""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.ip, port=self.ssh_port, username=self.username, password=dechiffrer_mot_de_passe(self.password))

            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            client.close()
            return output
        except Exception as e:
            raise Exception(f"SSH connection failed: {str(e)}")

def main():
    h1 = Host(name="PC", ip="127.0.0.1")
    print(h1)


if __name__ == "__main__":
    main()