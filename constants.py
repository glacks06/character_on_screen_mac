import pyautogui

monitor_width, monitor_height = pyautogui.size()

window_x = 100
window_y = 100
window_size_x = 110
window_size_y = 110

close_button_x = 0
close_button_y = 0
close_button_size_x = 10
close_button_size_y = 10
close_button_text = 'x'
close_button_text_bg_color = 'red'
close_button_text_color = 'black'
close_button_border_radius = '10'

img_x = 10
img_y = 10
img_size_x = 100
img_size_y = 100

run_motion1_path = './run1.png'
run_motion2_path = './run2.png'
run_motion_loop_interval = 250

window_move_loop_interval = 10
window_move_speed = 5
monitor_width, monitor_height = pyautogui.size()
monitor_width -= img_size_x
monitor_height -= img_size_y