from typing import Optional
from sqlmodel import Field, SQLModel

class Action(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    script_path: Optional[str] = Field(default=None)
    min_value: Optional[float] = Field(default=0)
    max_value: Optional[float] = Field(default=100)
    ssh_error_default_value: Optional[float] = Field(default=0)
    unite: Optional[str] = Field(default="%")
    rounding: Optional[int] = Field(default=2)

    def exec_script(self, host) -> str:
        if not self.script_path:
            return "Aucun script_path défini pour cette action."
        try:
            module = __import__(self.script_path, fromlist=[''])
            if hasattr(module, 'run'):
                return module.run(host)
            else:
                return f"Le module {self.script_path} ne possède pas de fonction 'run' nécéssaire à l'exécution."
        except ImportError as e:
            return f"Erreur dans l'import de l'action {self.script_path}: {e}"

    def __str__(self):
        return f"#{self.id} | Action {self.name} de script {self.script_path}"

    def __repr__(self):
        return f"<Action(id='{self.id}', name='{self.name}', script_path='{self.script_path}')>"
    
def main():
    a1 = Action(name="Memory Check", script_path="actions.memory_linux")
    print(a1)
    print(a1.exec_script())

if __name__ == "__main__":
    main()