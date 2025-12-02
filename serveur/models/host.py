from typing import Optional
from sqlmodel import Field, SQLModel

class Host(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    ip: str

    def __str__(self):
        return f"#{self.id} | Host {self.name} d'ip {self.ip}"
    
    def __repr__(self):
        return f"<Host(id='{self.id}', name='{self.name}', ip='{self.ip}')>"

def main():
    h1 = Host(name="PC", ip="127.0.0.1")
    print(h1)


if __name__ == "__main__":
    main()