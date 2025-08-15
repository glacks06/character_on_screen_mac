import random
import constants as cons

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout


class CharacterWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img = Image(source=cons.idle_list[0])
        self.add_widget(self.img)

        self.state = 1
        self.img_idle_state = 0
        self.img_run_state = 0
        self.img_run_direction = 1

        self.now_x = cons.window_x
        self.now_y = cons.window_y

        # 창 이동
        self.speed = cons.window_move_speed
        self.max_x = cons.monitor_width
        self.max_y = cons.monitor_height

        self.goal_x = random.randint(0, self.max_x)
        self.goal_x -= self.goal_x % self.speed
        self.goal_y = random.randint(0, self.max_y)
        self.goal_y -= self.goal_y % self.speed


        Clock.schedule_interval(self.state_controler, cons.state_control_loop_interval)

    def all_timer_stop(self):
        Clock.unschedule(self.move_window)
        Clock.unschedule(self.idle_anim)
        Clock.unschedule(self.run_anim)


    def state_controler(self, dt):
        self.all_timer_stop()
        if self.state == 0:  # 제자리
            self.img_idle_state = random.randint(0, len(cons.idle_list)-1)
            Clock.schedule_interval(self.idle_anim, cons.idle_motion_loop_interval)
            self.state = 1
        elif self.state == 1:  # 이동+달리기
            self.setNewPositionGoal()
            Clock.schedule_interval(self.run_anim, cons.run_motion_loop_interval)
            Clock.schedule_interval(self.move_window, cons.window_move_loop_interval)
            self.state = 0

    def move_window(self, dt):
        temp_x = self.now_x
        temp_y = self.now_y
        if self.now_x < self.goal_x:
            self.now_x += self.speed
            self.img_run_direction = 1
        elif self.now_x > self.goal_x:
            self.now_x -= self.speed
            self.img_run_direction = -1

        if self.now_y < self.goal_y:
            self.now_y += self.speed
        elif self.now_y > self.goal_y:
            self.now_y -= self.speed

        # 실제 윈도우 창 위치 이동
        Window.left = self.now_x
        Window.top = self.now_y

        if temp_x == self.now_x and temp_y == self.now_y:
            self.setNewPositionGoal()

    def idle_anim(self, dt):
        self.img.source = cons.idle_list[self.img_idle_state]

    def run_anim(self, dt):
        # 두 이미지를 번갈아가며 사용
        # print(self.img_run_direction)
        if self.img_run_state == 0:
            self.img.source = cons.run_motion1_path[0] if self.img_run_direction == -1 else cons.run_motion1_path[1]
            print(cons.run_motion1_path[0] if self.img_run_direction == -1 else cons.run_motion1_path[1])
            self.img_run_state = 1
        else:
            self.img.source = cons.run_motion2_path[0] if self.img_run_direction == -1 else cons.run_motion2_path[1]
            print(cons.run_motion2_path[0] if self.img_run_direction == -1 else cons.run_motion2_path[1])
            self.img_run_state = 0
        
            
    def setNewPositionGoal(self):
        self.goal_x = random.randint(0, self.max_x - cons.window_size_x)
        self.goal_x -= self.goal_x % self.speed
        self.goal_y = random.randint(0, self.max_y - cons.window_size_y)
        self.goal_y -= self.goal_y % self.speed



class MovingCharacterApp(App):
    def build(self):
        Window.size = (cons.window_size_x, cons.window_size_y)
        Window.left = cons.window_x
        Window.top = cons.window_y
        Window.clearcolor = (0, 0, 0, 0)  # 완전 투명 배경
        Window.borderless = True  # 프레임/테두리 제거
        return CharacterWidget()

if __name__ == '__main__':
    MovingCharacterApp().run()

# def resource_path(relative_path):
#     base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# class CharacterWidget(Widget):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.now_x = cons.window_x
#         self.now_y = cons.window_y
#         self.state = 1  # 0: idle, 1: run

#         self.img_idle_state = 0
#         self.timer_idle_ev = None
#         self.timer_run_ev = None
#         self.timer_moving_ev = None

#         self.img_run_state = 0
#         self.img_run_direction = 1

#         self.speed = cons.window_move_speed
#         self.max_x = cons.monitor_width
#         self.max_y = cons.monitor_height

#         # 캐릭터 이미지
#         self.label = Image(
#             source=resource_path(cons.idle_list[0]),
#             size=(cons.img_size_x, cons.img_size_y),
#             pos=(cons.img_x, cons.img_y),
#             allow_stretch=True,
#         )
#         self.add_widget(self.label)

#         self.setNewPositionGoal()

#         # 애니메이션, 상태, 이동 타이머 시작
#         self.timer_state_controler_ev = Clock.schedule_interval(self.state_controler, cons.state_control_loop_interval)

#         # 키 입력 리스너 추가
#         Window.bind(on_key_down=self._on_key_down)

#     def all_timer_stop(self):
#         if self.timer_idle_ev:
#             self.timer_idle_ev.cancel()
#             self.timer_idle_ev = None
#         if self.timer_run_ev:
#             self.timer_run_ev.cancel()
#             self.timer_run_ev = None
#         if self.timer_moving_ev:
#             self.timer_moving_ev.cancel()
#             self.timer_moving_ev = None

#     def state_controler(self, dt):
#         self.all_timer_stop()
#         if self.state == 0:  # 제자리
#             self.img_idle_state = random.randint(0, len(cons.idle_list)-1)
#             self.timer_idle_ev = Clock.schedule_interval(self.idle_anim, cons.idle_motion_loop_interval)
#             self.state = 1
#         elif self.state == 1:  # 이동+달리기
#             self.setNewPositionGoal()
#             self.timer_run_ev = Clock.schedule_interval(self.run_anim, cons.run_motion_loop_interval)
#             self.timer_moving_ev = Clock.schedule_interval(self.move_window, cons.window_move_loop_interval)
#             self.state = 0

#     def idle_anim(self, dt):
#         self.label.source = resource_path(cons.idle_list[self.img_idle_state])

#     def run_anim(self, dt):
#         # 두 이미지를 번갈아가며 사용
#         if self.img_run_state == 0:
#             path = resource_path(cons.run_motion1_path)
#             self.img_run_state = 1
#         else:
#             path = resource_path(cons.run_motion2_path)
#             self.img_run_state = 0
#         # 좌우 반전(수동. Kivy는 horizontal flip 기본 지원이 없어 이미지 전처리 필요)
#         self.label.source = path
#         # Kivy에서 실시간으로 flip하려면, 별도 커스텀 이미지 처리 필요

#     def move_window(self, dt):
#         temp_x = self.now_x
#         temp_y = self.now_y
#         if self.now_x < self.goal_x:
#             self.now_x += self.speed
#             self.img_run_direction = -1
#         elif self.now_x > self.goal_x:
#             self.now_x -= self.speed
#             self.img_run_direction = 1

#         if self.now_y < self.goal_y:
#             self.now_y += self.speed
#         elif self.now_y > self.goal_y:
#             self.now_y -= self.speed

#         # 실제 윈도우 창 위치 이동
#         Window.left = self.now_x
#         Window.top = self.now_y

#         if temp_x == self.now_x and temp_y == self.now_y:
#             self.setNewPositionGoal()

#     def setNewPositionGoal(self):
#         self.goal_x = random.randint(0, self.max_x - cons.window_size_x)
#         self.goal_x -= self.goal_x % self.speed
#         self.goal_y = random.randint(0, self.max_y - cons.window_size_y)
#         self.goal_y -= self.goal_y % self.speed

#     def _on_key_down(self, window, key, scancode, codepoint, modifier):
#         # 'q' key 종료
#         if codepoint.lower() == 'q':
#             App.get_running_app().stop()

# class TransparentWindowApp(App):
#     def build(self):
#         # 윈도우 창 설정: 완전 투명 & 프레임 없음
#         Window.size = (cons.window_size_x, cons.window_size_y)
#         Window.left = cons.window_x
#         Window.top = cons.window_y
#         Window.clearcolor = (0, 0, 0, 0)  # 완전 투명 배경
#         Window.borderless = True  # 프레임/테두리 제거
#         return CharacterWidget()

# if __name__ == "__main__":
#     TransparentWindowApp().run()