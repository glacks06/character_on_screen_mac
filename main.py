import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QTransform
import random
import constants as cons



class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.now_x = cons.window_x
        self.now_y = cons.window_y
        self.setWindowTitle("배경만 투명, 위젯 불투명")
        self.setGeometry(self.now_x, self.now_y, cons.window_size_x, cons.window_size_y)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        btn = QPushButton(cons.close_button_text, self)
        btn.setGeometry(cons.close_button_x, cons.close_button_y, cons.close_button_size_x, cons.close_button_size_y)
        btn.setStyleSheet(f"background: {cons.close_button_text_bg_color}; color: {cons.close_button_text_color}; border-radius: {cons.close_button_border_radius}px;")
        btn.clicked.connect(self.close)  # 반드시 self.close로 시그널 연결

        self.label = QLabel(self)
        pixmap = QPixmap(cons.run_motion1_path)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.setGeometry(cons.img_x, cons.img_y, cons.img_size_x, cons.img_size_y)  # 원하는 위치와 크기로 조정

        # 달리기 애니메이션
        self.img_run_state = 0
        self.img_run_direction = 1
        self.timer_run = QTimer(self)
        self.timer_run.timeout.connect(self.run_anim)
        self.timer_run.start(cons.run_motion_loop_interval)  # 1000ms=1초


        # 창 이동
        self.speed = cons.window_move_speed
        self.max_x = cons.monitor_width
        self.max_y = cons.monitor_height

        self.goal_x = random.randint(0, self.max_x)
        self.goal_x -= self.goal_x % self.speed
        self.goal_y = random.randint(0, self.max_y)
        self.goal_y -= self.goal_y % self.speed

        self.timer_moving = QTimer(self)
        self.timer_moving.timeout.connect(self.move_window)
        self.timer_moving.start(cons.window_move_loop_interval)  # 0.5초마다 창 이동

    def run_anim(self):
        if self.img_run_state == 0:
            pixmap = QPixmap(cons.run_motion1_path)
            self.img_run_state = 1
        else:
            pixmap = QPixmap(cons.run_motion2_path)
            self.img_run_state = 0

        if self.img_run_direction == -1: # 좌우 반전
            transform = QTransform().scale(-1, 1)  # 좌우 반전용 transform 생성
            pixmap = pixmap.transformed(transform)
        self.label.setPixmap(pixmap)

    def move_window(self):
        temp_x = self.now_x
        temp_y = self.now_y
        if self.now_x < self.goal_x: 
            self.now_x += self.speed
            self.img_run_direction = -1
        elif self.now_x > self.goal_x: 
            self.now_x -= self.speed
            self.img_run_direction = 1

        if self.now_y < self.goal_y: 
            self.now_y += self.speed
        elif self.now_y > self.goal_y: 
            self.now_y -= self.speed

        if temp_x == self.now_x and temp_y == self.now_y: # 목표지점에 도달함
            self.goal_x = random.randint(0, self.max_x)
            self.goal_x -= self.goal_x % self.speed
        if temp_y == self.now_y: # 목표지점에 도달함
            self.goal_y = random.randint(0, self.max_y)
            self.goal_y -= self.goal_y % self.speed
        
        self.move(self.now_x, self.now_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())