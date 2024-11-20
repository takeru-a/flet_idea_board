# ポインタの状態を保存するクラス
class State():
    x: float
    y: float
    mode: str
    def __init__(self):
        self.x = 0
        self.y = 0
        self.mode = "none"
