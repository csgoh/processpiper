from dataclasses import dataclass, field
from processpiper import shape


@dataclass
class Connection:
    target: shape = field(init=True)
    label: str = field(init=True)
    connection_type: str = field(init=True)
