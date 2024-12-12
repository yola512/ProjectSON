from typing import List, Dict

class MockCSVStorage:
    def __init__(self):
        self.data = []

    def write(self, rows: List[Dict[str, str]]):
        self.data = rows
    
    def read(self) -> List[Dict[str, str]]:
        return self.data
    
    def append(self, row: Dict[str, str]):
        self.data.append(row)

#added cause i cant import sth from main.py to test_main.py 
#and then from test_main.py to main.py 'cause they're mutually dependent