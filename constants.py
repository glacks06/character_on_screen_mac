import pyautogui

monitor_width, monitor_height = pyautogui.size()

window_x = 100
window_y = 100
window_size_x = 100
window_size_y = 100

img_x = 0
img_y = 0
img_size_x = 100
img_size_y = 100

state_control_loop_interval = 5000
state_cnt = 2 # 상태 개수 (현재: idle, run)(2개)

idle_list = ['idle1.png', 'idle2.png']
idle_motion_loop_interval = 250

run_motion1_path = 'run1.png'
run_motion2_path = 'run2.png'
run_motion_loop_interval = 250

window_move_loop_interval = 10
window_move_speed = 5
monitor_width, monitor_height = pyautogui.size()
monitor_width -= img_size_x
monitor_height -= img_size_y