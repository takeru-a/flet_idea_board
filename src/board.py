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
    Paint,
    PaintLinearGradient,
    GestureDetector,
    ScaleUpdateEvent,
    ScrollEvent,
    DragStartEvent,
    DragUpdateEvent
)
from data_store import DataStore
import flet.canvas as cv


class State:
    x: float
    y: float

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
        self.cp = cv.Canvas(
            [
                cv.Fill(
                    Paint(
                        gradient=PaintLinearGradient(
                            (0, 0), (600, 600), colors=[colors.WHITE, colors.WHITE10]
                        )
                    )
                ),
            ],
            content=GestureDetector(
                on_pan_start=self.pan_start,
                on_pan_update=self.pan_update,
                drag_interval=10,
            ),
            expand=True,
            width=self.page.width,
            height=self.page.height
        )
        
        overlay_container = GestureDetector(
                mouse_cursor=MouseCursor.MOVE,
                drag_interval=10,
                on_pan_update=self.drag_update,
                on_scale_update=self.object_resize,
                on_scroll=self.scroll_resize,
                top=0,
                left=0,
                width=100,
                height=100,
                content=Container(
                    content=TextField("This is a container", color=colors.WHITE, multiline=True, border="None"),
                    bgcolor=colors.RED_ACCENT_700,
                    padding=10,
                    width=100,
                    height=100,
                )
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
                overlay_container
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
        
    # オブジェクト移動
    def drag_update(self, e: DragUpdateEvent):
        # 対象のコントロールの位置をドラッグイベントの移動量に応じて更新
        e.control.top = min(self.page.height - 100, max(0, e.control.top + e.delta_y))
        e.control.left = min(self.page.width, max(0, e.control.left + e.delta_x))
        e.control.update()
        
    # オブジェクトリサイズ
    def object_resize(self, e: ScaleUpdateEvent):
        # 対象のコントロールのサイズをドラッグイベントの移動量に応じて更新
        e.control.width = max(0, e.control.width + e.focal_point_delta_x)
        e.control.height = max(0, e.control.height + e.focal_point_delta_y)
        e.control.update()
        
    # オブジェクトリサイズ
    def scroll_resize(self, e: ScrollEvent):
        # 対象のコントロールのサイズをドラッグイベントの移動量に応じて更新
        e.control.width = max(0, e.control.width + e.scroll_delta_x)
        e.control.height = max(0, e.control.height + e.scroll_delta_y)
                   
    # お描き機能                  
    def pan_start(self, e: DragStartEvent):
        self.state.x = e.local_x
        self.state.y = e.local_y

    def pan_update(self, e: DragUpdateEvent):
        self.cp.shapes.append(
            cv.Line(
                self.state.x, self.state.y, e.local_x, e.local_y, paint=Paint(color=colors.BLACK87 ,stroke_width=3)
            )
        )
        
        self.cp.update()
        self.state.x = e.local_x
        self.state.y = e.local_y
    
    def resize(self, nav_rail_extended, width, height):
        self.width = (
            width - 310) if nav_rail_extended else (width - 50)
        self.height = height
        self.cp.width = self.page.width 
        self.cp.height = self.page.height
        self.board.width = self.page.width
        self.board.height = self.page.height
        self.update()
    