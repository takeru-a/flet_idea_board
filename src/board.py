import itertools
from flet import (
    Row,
    Page,
    Container,
    TextField,
    Container,
    Stack,
    colors,
    MouseCursor,
    padding,
    margin,
    GestureDetector,
    ScaleUpdateEvent,
    TapEvent,
    DragUpdateEvent,
    BoxShape,
    BoxShadow,
    alignment,
    border,
)
from data_store import DataStore
from state import State
from controlbar import ControlBar
from canvas import Canvas as canvas
from arrow import Arrow

class Board(Container):
    id_counter = itertools.count()

    def __init__(self, app, store: DataStore, name: str, page: Page):
        self.page = page
        self.board_id = next(Board.id_counter)
        self.store: DataStore = store
        self.app = app
        self.name = name
        self.state = State()

        # ボードの描画エリア
        self.cp = canvas(self.page, self.state)

        # 7個コンテナ
        self.controlbar = ControlBar(self.state)
        self.bg = GestureDetector(
                    on_tap_down=self.add_obj,
                    on_tap_up=self.add_obj_after,
                    width=(self.page.width),
                    height=(self.page.height),
                    top=70,
                    )

        # ボードメインエリア
        self.board = Stack(
            controls = [
                Row(
                    controls = [self.cp],
                    vertical_alignment="start",
                    scroll="auto",
                    expand=True,
                ),
                self.bg,
                self.controlbar,
            ],
            expand=True,
            width=(self.page.width),
            height=(self.page.height),
        )

        super().__init__(
            content=self.board,
            data=self,
            margin=margin.all(0),
            padding=padding.only(top=10, right=0),
            height=self.page.height,
        )

    # オブジェクト追加
    def add_obj(self, e: TapEvent):
        # 矩形のオブジェクトを追加
        if self.state.mode == "squares":
            id = len(self.board.controls) - 1
            self.board.controls.insert(id, GestureDetector(
                mouse_cursor=MouseCursor.MOVE,
                drag_interval=10,
                on_pan_update=self.move_obj,
                on_scale_update=self.resize_obj,
                on_tap=self.delete_obj,
                content=Container(
                    content=TextField("", color=colors.BLACK, multiline=True, border="None"),
                    bgcolor=colors.GREY_50,
                    border_radius=2,
                    border=border.all(1, colors.BLACK),
                    shadow=BoxShadow(color=colors.GREY_400, spread_radius=0.2, blur_radius=0.2, offset=(1, 1)),
                    alignment=alignment.center,
                ),
                width=100,
                height=100,
                top=e.local_y,
                left=e.local_x,
            ))
        # 円形のオブジェクトを追加
        elif self.state.mode == "circle":
            id = len(self.board.controls) - 1
            self.board.controls.insert(id, GestureDetector(
                mouse_cursor=MouseCursor.MOVE,
                drag_interval=10,
                on_pan_update=self.move_obj,
                on_scale_update=self.resize_obj,
                on_tap=self.delete_obj,
                content=Container(
                    content=TextField("", color=colors.BLACK, multiline=True, border="None"),
                    bgcolor=colors.GREY_50,
                    shape=BoxShape.CIRCLE,
                    border=border.all(1, colors.BLACK),
                    shadow=BoxShadow(color=colors.GREY_400, spread_radius=0.2, blur_radius=0.2, offset=(1, 1)),
                    alignment=alignment.center,
                ),
                width=100,
                height=100,
                top=e.local_y,
                left=e.local_x,
            ))
        # 矢印のオブジェクトを追加
        elif self.state.mode == "arrow":
            id = len(self.board.controls) - 1
            arrow = Arrow(self.page, self.state, self.board, id, top=e.local_y, left=e.local_x)
            self.board.controls.insert(id, arrow)
        
        # 画像を追加
        elif self.state.mode == "image":
            id = len(self.board.controls) - 1
            self.board.controls.insert(id, GestureDetector(
                mouse_cursor=MouseCursor.MOVE,
                drag_interval=10,
                on_pan_update=self.move_obj,
                on_scale_update=self.resize_obj,
                on_tap=self.delete_obj,
                content=Container(
                    content=TextField("", color=colors.BLACK, multiline=True, border="None"),
                    bgcolor=colors.GREY_50,
                    border_radius=2,
                    border=border.all(1, colors.BLACK),
                    shadow=BoxShadow(color=colors.GREY_400, spread_radius=0.2, blur_radius=0.2, offset=(1, 1)),
                    alignment=alignment.center,
                ),
                width=100,
                height=100,
                top=e.local_y,
                left=e.local_x,
            ))
        
        self.update()

    # オブジェクト追加後処理
    def add_obj_after(self, e: TapEvent):
        self.state.mode = "pointer"
        self.controlbar.add_obj_after()

    # オブジェクト削除
    def delete_obj(self, e: TapEvent):
        if self.state.mode == "delete":
            self.board.controls.remove(e.control)
            self.update()

    # オブジェクト移動
    def move_obj(self, e: DragUpdateEvent):
        # 対象のコントロールの位置をドラッグイベントの移動量に応じて更新
        e.control.top = min(self.page.height - 100, max(0, e.control.top + e.delta_y))
        e.control.left = min(self.page.width, max(0, e.control.left + e.delta_x))
        e.control.update()

    # オブジェクトリサイズ
    def resize_obj(self, e: ScaleUpdateEvent):
        # 対象のコントロールのサイズをドラッグイベントの移動量に応じて更新
        e.control.width = max(0, e.control.width + e.focal_point_delta_x)
        e.control.height = max(0, e.control.height + e.focal_point_delta_y)
        e.control.update()

    # ボードのリサイズ
    def resize(self, nav_rail_extended, width, height):
        self.width = (
            width - 310) if nav_rail_extended else (width - 50)
        self.height = height
        self.board.width = self.page.width
        self.board.height = self.page.height
        self.bg.width = self.page.width
        self.bg.height = self.page.height
        self.update()
