from flet import (
    UserControl, 
    GestureDetector, 
    DragStartEvent, 
    DragUpdateEvent, 
    Paint,
    PaintingStyle,
    colors
)
import flet.canvas as cv
from state import State

class Canvas(UserControl):
    def __init__(self, page, state: "State"):
        super().__init__()
        self.page = page
        self.state = state
        self.cp = cv.Canvas(
            [],
            content=GestureDetector(
                on_pan_start=self.pan_start,
                on_pan_update=self.pan_update,
                drag_interval=10,
            ),
            expand=True,
            width=self.page.width,
            height=self.page.height,
            on_resize=self.on_resize
        )
    def build(self):
        return self.cp

    # お描き機能                  
    def pan_start(self, e: DragStartEvent):
        if self.state.mode == "drawer" or self.state.mode == "delete":
            self.state.x = e.local_x
            self.state.y = e.local_y

    def pan_update(self, e: DragUpdateEvent):
        if self.state.mode == "drawer":
            self.cp.shapes.append(
                cv.Line(
                    self.state.x, self.state.y, e.local_x, e.local_y, paint=Paint(color=colors.BLACK87 ,stroke_width=3)
                )
            )
            self.cp.update()
            self.state.x = e.local_x
            self.state.y = e.local_y
        elif self.state.mode == "delete":
            self.cp.shapes.append(
                cv.Line(
                    self.state.x, self.state.y, e.local_x, e.local_y, paint=Paint(color=colors.WHITE ,stroke_width=20, style=PaintingStyle.FILL)
                )
            )
            self.cp.update()
            self.state.x = e.local_x
            self.state.y = e.local_y
                        
    def on_resize(self, e):
        self.cp.width = self.page.width 
        self.cp.height = self.page.height
        self.cp.update()
        