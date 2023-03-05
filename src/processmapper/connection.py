from dataclasses import dataclass, field
from processmapper import shape


@dataclass
class Connection:
    target: shape = field(init=True)
    label: str = field(init=True)
    connection_type: str = field(init=True)
