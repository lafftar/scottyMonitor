from dataclasses import dataclass


@dataclass
class Product:
    name: str
    url: str
    price: str
    image: str

    def __repr__(self) -> str:
        return '\n' + '\n'.join((f'{key:30s}:  {val}' for key, val in vars(self).items()
                                 if not key.startswith('_'))) + '\n'