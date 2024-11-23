from flet import (
    UserControl,
    Row,
    Container,
    Icon,
    icons,
    colors,
    MainAxisAlignment,
    HoverEvent,
    BoxShadow,
    TapEvent,
    ContainerTapEvent,
)

from state import State

class ControlBar(UserControl):
    def __init__(self, state: "State"):
        super().__init__()
        self.state = state
        self.state.mode = "pointer"
        self.data = [
                    Container(
                        key="pointer",
                        content=Icon(icons.TRANSIT_ENTEREXIT, color=colors.BLACK),
                        bgcolor=colors.INDIGO_300,
                        border_radius=10,
                        width=40,
                        height=40,
                        ink=True,
                        on_hover=self.on_hover,
                        on_click=self.on_click
                ),
                    Container(
                        key="drawer",
                        content=Icon(icons.DRAW_ROUNDED, color=colors.BLACK),
                        bgcolor=colors.GREY_300,
                        border_radius=10,
                        width=40,
                        height=40,
                        ink=True,
                        on_hover=self.on_hover,
                        on_click=self.on_click
                ),
                    Container(
                        key="delete",
                        content=Icon(icons.DELETE, color=colors.BLACK),
                        bgcolor=colors.GREY_300,
                        border_radius=10,
                        width=40,
                        height=40,
                        ink=True,
                        on_hover=self.on_hover,
                        on_click=self.on_click
                ),
                    Container(
                        key="squares",
                        content=Icon(icons.CROP_SQUARE_SHARP, color=colors.BLACK),
                        bgcolor=colors.GREY_300,
                        border_radius=10,
                        width=40,
                        height=40,
                        ink=True,
                        on_hover=self.on_hover,
                        on_click=self.on_click
                ),
                    Container(
                        key="circle",
                        content=Icon(icons.CIRCLE, color=colors.BLACK),
                        bgcolor=colors.GREY_300,
                        border_radius=10,
                        width=40,
                        height=40,
                        ink=True,
                        on_hover=self.on_hover,
                        on_click=self.on_click
                ),
                    Container(
                        key="arrow",
                        content=Icon(icons.ARROW_RIGHT_ALT, color=colors.BLACK),
                        bgcolor=colors.GREY_300,
                        border_radius=10,
                        width=40,
                        height=40,
                        ink=True,
                        on_hover=self.on_hover,
                        on_click=self.on_click
                )             
        ]
        
    def build(self):
        return Row(
            controls=self.data,
            alignment=MainAxisAlignment.CENTER,
            width=400,
            height=70,
            top=0,
            right=0,
        )
    
    def on_hover(self, e:HoverEvent):
        if e.data == "true":
            e.control.shadow = BoxShadow(color=colors.GREY_500, spread_radius=1, blur_radius=1, offset=(1, 1))
        else:
            e.control.shadow = 0
        self.update()
    
    def on_click(self, e:ContainerTapEvent):
        self.state.mode = e.control.key
        for data in self.data:
            data.bgcolor = colors.GREY_300
        e.control.bgcolor = colors.INDIGO_300
        self.update()
    
    # オブジェクト追加後処理
    def add_obj_after(self):
        for data in self.data:
            data.bgcolor = colors.GREY_300
        self.data[0].bgcolor = colors.INDIGO_300
        self.update()
