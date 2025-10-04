import pycountry

class Currency:
    def __init__(self, code: str):
        obj = pycountry.currencies.get(alpha_3=code)
        if obj is None:
            raise ValueError(...)
        self._obj = obj
    
    @property
    def code(self) -> str:
        return self._obj.alpha_3

    @property
    def name(self) -> str:
        return self._obj.name
    
    def __str__(self):
        return self.code

    def __eq__(self, other):
        if isinstance(other, Currency):
            return self.code == other.code
        return False

    def __hash__(self):
        return hash(self.code)