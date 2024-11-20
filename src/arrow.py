from flet import (
    UserControl,
    GestureDetector,
    DragUpdateEvent,
    ScaleUpdateEvent,
    ScaleStartEvent,
    MouseCursor,
    Paint,
    PaintingStyle,
    colors
)
import flet.canvas as cv
from state import State
import math

class Arrow(UserControl):
    def __init__(self, page, state: "State", board, id: int, top: float, left: float):
        super().__init__()
        self.page = page
        self.board = board
        self.state = state
        self.double_tap = False
        self.arrow_id = id
        self.arrow: "Arrow" = cv.Canvas(
                        [
                        # 矢印の軸を描画
                        cv.Path(
                            [
                                cv.Path.MoveTo(50, 50),  # 矢印の元
                                cv.Path.LineTo(150, 50),  # 矢印の軸
                                cv.Path.LineTo(140, 40),  # 矢印の頭の上部分
                                cv.Path.MoveTo(150, 50),  # 矢印の元に戻る
                                cv.Path.LineTo(140, 60),  # 矢印の頭の下部分
                            ],
                            paint=Paint(
                                stroke_width=3,
                                color=colors.BLACK,
                                style=PaintingStyle.STROKE,
                            ),
                        ),
                        ],
                        content=GestureDetector(
                            mouse_cursor=MouseCursor.CLICK,
                            on_pan_update=self.update_arrow,
                            on_double_tap=self.change_control,
                            on_tap=self.delete_arrow,
                            on_scale_start=self.rotate_arrow_before,
                            on_scale_update=self.rotate_arrow,
                            drag_interval=10,
                            width=150,
                            height=100,
                        ),
                        top=top,
                        left=left,
                        rotate=0, # 2πで360度
        )
    def build(self) -> "Arrow":
        return self.arrow

    # 矢印の更新
    def update_arrow(self, e: DragUpdateEvent):

        # 矢印の長さを変更
        if self.state.mode == "pointer" and self.double_tap == True:
            
            height = e.control.height
            width = max(0, e.control.width + e.delta_x)
            e.control.width = width
            self.arrow.shapes.clear()
            self.arrow.shapes.append(
                cv.Path(
                    [
                        cv.Path.MoveTo(50, height/2),  # 矢印の元
                        cv.Path.LineTo(width, height/2),  # 矢印の軸
                        cv.Path.LineTo(width-10, height/2-10),  # 矢印の頭の上部分
                        cv.Path.MoveTo(width, height/2),  # 矢印の元に戻る
                        cv.Path.LineTo(width-10, height/2+10),  # 矢印の頭の下部分
                    ],
                    paint=Paint(
                        stroke_width=3,
                        color=colors.BLACK,
                        style=PaintingStyle.STROKE,
                    ),
                )
            )
            self.arrow.update()
        # 矢印の移動
        elif self.state.mode == "pointer" and self.double_tap == False:
            # sinθ, cosθを算出
            cos_theta = math.cos(self.arrow.rotate)
            sin_theta = math.sin(self.arrow.rotate)
            
            # 回転に対応したdelta_x, delta_y
            delta_x_rotated = e.delta_x * cos_theta - e.delta_y * sin_theta
            delta_y_rotated = e.delta_x * sin_theta + e.delta_y * cos_theta
            
            self.arrow.top = min(self.page.height - 100, max(0, self.arrow.top + delta_y_rotated))
            self.arrow.left = min(self.page.width, max(0, self.arrow.left + delta_x_rotated))
            self.arrow.update()

    # 矢印のコントロール方法を変更
    def change_control(self, e):
        if self.state.mode == "pointer":
            self.double_tap = not self.double_tap
            self.update()
            
    # 矢印削除
    def delete_arrow(self, e):
        if self.state.mode == "delete":
            self.board.controls = [control for control in self.board.controls if not (isinstance(control, Arrow) and control.arrow_id == self.arrow_id)]
            self.board.update()
    
    # 矢印の回転の準備
    def rotate_arrow_before(self, e: ScaleStartEvent):
        if self.state.mode == "pointer":
            self.state.x = e.focal_point_x
            self.state.y = e.focal_point_y
    
    # 矢印の回転
    def rotate_arrow(self, e: ScaleUpdateEvent):
        if self.state.mode == "pointer":
            end_x = e.focal_point_x
            end_y = e.focal_point_y
            # ベクトルを算出
            vec_ab = [self.state.x - self.arrow.left, self.state.y - self.arrow.top]
            vec_ac = [end_x - self.arrow.left, end_y - self.arrow.top]
            
            # 外積を計算して回転方向を判定
            cross_product = vec_ab[0] * vec_ac[1] - vec_ab[1] * vec_ac[0]
            
            # cosθを算出
            cos_theta = (vec_ab[0]*vec_ac[0] + vec_ab[1]*vec_ac[1]) / (math.sqrt(vec_ab[0]**2 + vec_ab[1]**2) * math.sqrt(vec_ac[0]**2 + vec_ac[1]**2))
            
            if (cross_product > 0 and ((-math.pi/2.0 <= self.arrow.rotate <= math.pi/2.0) or (3*math.pi/2.0 <= self.arrow.rotate <= 2*math.pi/2.0) or (-2*math.pi <= self.arrow.rotate <= -3*math.pi/2.0)))\
                or (cross_product < 0 and ((math.pi/2.0 <= self.arrow.rotate <= 3*math.pi/2.0) or (-3*math.pi/2.0 <= self.arrow.rotate <= -math.pi/2.0))):
                self.arrow.rotate += math.acos(cos_theta) * 2*math.pi
                self.arrow.rotate = (self.arrow.rotate + 2*math.pi) % (4*math.pi) - 2*math.pi
            else:
                self.arrow.rotate -= math.acos(cos_theta) * 2*math.pi
                self.arrow.rotate = (self.arrow.rotate + 2*math.pi) % (4*math.pi) - 2*math.pi
            self.arrow.update()
            self.state.x = end_x
            self.state.y = end_y
    