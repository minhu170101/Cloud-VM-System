import pyautogui
import UI

def show_error():
    pyautogui.alert("Không tìm thấy địa chỉ IP", "Lỗi")

if UI.access_info != {}:
    UI.run()
else:
    show_error()

