import paramiko
from pydantic import BaseModel

class SSHTunneling(BaseModel):
    ip: str
    port: int = 22
    username: str
    password: str

    def execute_ssh_command(self, command: str) -> str:
        """Establish an SSH connection and execute a command."""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password)

            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            client.close()
            return output
        except Exception as e:
            raise Exception(f"SSH connection failed: {str(e)}")