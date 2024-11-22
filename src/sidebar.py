from flet import (
    Column,
    Container,
    IconButton,
    Text,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    TextField,
    alignment,
    border_radius,
    colors,
    icons,
    padding,
    margin,
)
from data_store import DataStore

class Sidebar(Container):

    def __init__(self, app_layout, store: DataStore):
        self.store: DataStore = store
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.top_nav_items = [
            NavigationRailDestination(
                label_content=Text("New Board"),
                label="New Board",
                icon=icons.ADD_BOX,
                selected_icon=icons.ADD_BOX
            ),
            NavigationRailDestination(
                label_content=Text("Document"),
                label="Document",
                icon=icons.MENU_BOOK_ROUNDED,
                selected_icon=icons.MENU_BOOK_ROUNDED
            ),
        ]

        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.INDIGO_400,
            extended=True,
            height=110,
        )
        
        self.bottom_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.bottom_nav_change,
            extended=True,
            expand=True,
            bgcolor=colors.INDIGO_400,
        )
        self.toggle_nav_rail_button = IconButton(icons.BOOK_OUTLINED)

        super().__init__(
            content=Column([
                self.top_nav_rail,
                # 水平線
                Container(
                    bgcolor=colors.BLACK26,
                    border_radius=border_radius.all(30),
                    height=1,
                    alignment=alignment.center_right,
                    width=220
                ),
                self.bottom_nav_rail
            ], tight=True),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            bgcolor=colors.INDIGO_400,
            visible=self.nav_rail_visible,
        )

    # サイドバーに表示されるボード
    def sync_board_destinations(self):
        boards = self.store.get_boards()
        self.bottom_nav_rail.destinations = []
        for i in range(len(boards)):
            b = boards[i]
            self.bottom_nav_rail.destinations.append(
                NavigationRailDestination(
                    label_content=TextField(
                        value=b.name,
                        hint_text=b.name,
                        text_size=12,
                        read_only=True,
                        on_focus=self.board_name_focus,
                        on_blur=self.board_name_blur,
                        border="none",
                        height=50,
                        width=150,
                        text_align="start",
                        data=i
                    ),
                    label=b.name,
                    selected_icon=icons.BOOK_OUTLINED,
                    icon=icons.BOOK_OUTLINED
                )
            )
        self.update()

    def toggle_nav_rail(self, e):
        self.visible = not self.visible
        self.update()
        self.page.update()

    def board_name_focus(self, e):
        e.control.read_only = False
        e.control.border = "outline"
        e.control.update()

    def board_name_blur(self, e):
        self.store.update_board(self.store.get_boards()[e.control.data], {
            'name': e.control.value})
        self.app_layout.hydrate_all_boards_view()
        e.control.read_only = True
        e.control.border = "none"
        self.page.update()

    def top_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.bottom_nav_rail.selected_index = None
        self.top_nav_rail.selected_index = index
        self.update()
        if index == 0:
            self.page.route = "/create/board"
        elif index == 1:
            self.page.route = "/docs"
        self.page.update()

    def bottom_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        self.top_nav_rail.selected_index = None
        self.bottom_nav_rail.selected_index = index
        self.page.route = f"/board/{index}"
        self.update()
        self.page.update()