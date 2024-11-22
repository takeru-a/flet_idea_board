import flet
from layout import AppLayout
from board import Board
from data_store import DataStore
from flet import (
    AlertDialog,
    AppBar,
    Column,
    ElevatedButton,
    Icon,
    Page,
    Row,
    TemplateRoute,
    Text,
    TextField,
    View,
    colors,
    icons,
    padding,
    theme,
)
from memory_store import InMemoryStore

# メインアプリケーションクラス
class IdeaBoardApp(AppLayout):
    def __init__(self, page: Page, store: DataStore):
        self.page = page
        self.store: DataStore = store
        self.page.on_route_change = self.route_change
        self.boards = self.store.get_boards()

        self.appbar = AppBar(
            leading=Icon(icons.DEVELOPER_BOARD),
            leading_width=100,
            title=Text(f"Idea Board", font_family="Pacifico", size=32, text_align="start"),
            center_title=False,
            toolbar_height=60,
            color=colors.WHITE,
            bgcolor=colors.INDIGO_500,
        )
        self.page.appbar = self.appbar
        self.page.update()
        super().__init__(
            self,
            self.page,
            self.store,
            tight=True,
            expand=True,
            vertical_alignment="start",
        )

    def initialize(self):
        self.page.views.append(
            View(
                "/",
                [self.appbar, self],
                padding=padding.all(0),
                bgcolor=colors.WHITE,
            )
        )
        self.page.update()
        self.page.go("/")

    # ルーティング設定 
    def route_change(self, e):
        troute = TemplateRoute(self.page.route)
        if troute.match("/"):
            self.page.go("/docs")
        elif troute.match("/board/:id"):
            if int(troute.id) > len(self.store.get_boards()):
                self.page.go("/")
                return
            self.set_board_view(int(troute.id))
        elif troute.match("/create/board"):
            self.set_all_boards_view()
        elif troute.match("/docs"):
            self.set_display_docs()
        self.page.update()

    # ボードを追加する
    def add_board(self, e):
        def close_dlg(e):
            if (hasattr(e.control, "text") and not e.control.text == "Cancel") or (
                type(e.control) is TextField and e.control.value != ""
            ):
                self.create_new_board(dialog_text.value)
            dialog.open = False
            self.page.update()

        def textfield_change(e):
            if dialog_text.value == "":
                create_button.disabled = True
            else:
                create_button.disabled = False
            self.page.update()

        dialog_text = TextField(
            label="New Board Name", on_submit=close_dlg, on_change=textfield_change
        )
        create_button = ElevatedButton(
            text="Create", bgcolor=colors.INDIGO, on_click=close_dlg, color=colors.WHITE, disabled=True
        )
        dialog = AlertDialog(
            title=Text("Name your new board"),
            content=Column(
                [
                    dialog_text,
                    Row(
                        [
                            ElevatedButton(text="Cancel", on_click=close_dlg),
                            create_button,
                        ],
                        alignment="spaceBetween",
                    ),
                ],
                tight=True,
            ),
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        dialog_text.focus()

    def create_new_board(self, board_name):
        new_board = Board(self, self.store, board_name, self.page)
        self.store.add_board(new_board)
        self.hydrate_all_boards_view()

    def delete_board(self, e):
        self.store.remove_board(e.control.data)
        self.set_all_boards_view()


def main(page: Page):

    page.title = "Flet Idea Board"
    page.padding = 0
    page.theme = theme.Theme(font_family="Verdana")
    page.theme_mode = "light"
    page.theme.page_transitions.windows = "cupertino"
    page.fonts = {"Pacifico": "Pacifico-Regular.ttf"}
    app = IdeaBoardApp(page, InMemoryStore())
    page.add(app)
    page.update()
    app.initialize()

flet.app(target=main)