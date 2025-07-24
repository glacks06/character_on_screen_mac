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
        self.setWindowTitle("도로롱")
        self.setGeometry(self.now_x, self.now_y, cons.window_size_x, cons.window_size_y)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 1);")  # 거의 투명한 배경
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        self.state = 1 # 0: 제자리, 1: 이동
        self.label = QLabel(self)
        pixmap = QPixmap(cons.idle_list[0])
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.label.setGeometry(cons.img_x, cons.img_y, cons.img_size_x, cons.img_size_y)  # 원하는 위치와 크기로 조정

        # 상태 변경 (idle -> run)
        self.timer_state_controler = QTimer(self)
        self.timer_state_controler.timeout.connect(self.state_controler)
        self.timer_state_controler.start(cons.state_control_loop_interval)

        # idle 애니메이션
        self.img_idle_state = 0
        self.timer_idle = QTimer(self)
        self.timer_idle.timeout.connect(self.idle_anim)

        # 달리기 애니메이션
        self.img_run_state = 0
        self.img_run_direction = 1
        self.timer_run = QTimer(self)
        self.timer_run.timeout.connect(self.run_anim)

        # 창 이동
        self.speed = cons.window_move_speed
        self.max_x = cons.monitor_width
        self.max_y = cons.monitor_height
        self.setNewPositionGoal()

        self.timer_moving = QTimer(self)
        self.timer_moving.timeout.connect(self.move_window)

    def all_timer_stop(self):
        self.timer_idle.stop()
        self.timer_moving.stop()
        self.timer_run.stop()

    def state_controler(self):
        self.all_timer_stop()

        if self.state == 0: # 제자리
            self.img_idle_state = random.randint(0, len(cons.idle_list)-1)
            self.timer_idle.start(cons.idle_motion_loop_interval)
            self.state += 1
            self.state %= cons.state_cnt
            
        elif self.state == 1: # 이동+달리기모션
            self.setNewPositionGoal()
            self.timer_run.start(cons.run_motion_loop_interval)
            self.timer_moving.start(cons.window_move_loop_interval)
            self.state += 1
            self.state %= cons.state_cnt

    
    def idle_anim(self):
        pixmap = QPixmap(cons.idle_list[self.img_idle_state])
        self.label.setPixmap(pixmap)

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
            self.setNewPositionGoal()
        
        self.move(self.now_x, self.now_y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q: self.close()

    def setNewPositionGoal(self):
        self.goal_x = random.randint(0, self.max_x)
        self.goal_x -= self.goal_x % self.speed
        self.goal_y = random.randint(0, self.max_y)
        self.goal_y -= self.goal_y % self.speed



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())