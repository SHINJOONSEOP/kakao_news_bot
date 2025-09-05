# kakao_send.py
import time, ctypes, win32con, win32api, win32gui, win32clipboard as wcb

PBYTE256 = ctypes.c_ubyte * 256
_user32 = ctypes.WinDLL("user32")
GetKeyboardState = _user32.GetKeyboardState
SetKeyboardState = _user32.SetKeyboardState
PostMessage = win32api.PostMessage
SendMessage = win32gui.SendMessage
IsWindow = win32gui.IsWindow
GetCurrentThreadId = win32api.GetCurrentThreadId
GetWindowThreadProcessId = _user32.GetWindowThreadProcessId
AttachThreadInput = _user32.AttachThreadInput
MapVirtualKeyA = _user32.MapVirtualKeyA
MakeLong = win32api.MAKELONG
w = win32con

def PostKeyEx(hwnd, key, shift=None, specialkey=False):
    if shift is None:
        shift = []
    if not IsWindow(hwnd):
        raise RuntimeError("유효하지 않은 창 핸들")

    ThreadId = GetWindowThreadProcessId(hwnd, None)
    Iparam = MakeLong(0, MapVirtualKeyA(key, 0))
    if specialkey:
        Iparam |= 0x1000000

    if shift:
        pKeyBuffers = PBYTE256()
        pKeyBuffers_old = PBYTE256()
        SendMessage(hwnd, w.WM_ACTIVATE, w.WA_ACTIVE, 0)
        AttachThreadInput(GetCurrentThreadId(), ThreadId, True)
        GetKeyboardState(ctypes.byref(pKeyBuffers_old))
        for modkey in shift:
            pKeyBuffers[modkey] = 128
        SetKeyboardState(ctypes.byref(pKeyBuffers))
        time.sleep(0.01)

    PostMessage(hwnd, w.WM_KEYDOWN, key, Iparam)
    time.sleep(0.01)
    PostMessage(hwnd, w.WM_KEYUP, key, Iparam)

    if shift:
        SetKeyboardState(ctypes.byref(pKeyBuffers_old))
        time.sleep(0.01)
        AttachThreadInput(GetCurrentThreadId(), ThreadId, False)

def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

def copy_to_clipboard(text: str):
    wcb.OpenClipboard()
    wcb.EmptyClipboard()
    wcb.SetClipboardData(win32con.CF_UNICODETEXT, text)
    wcb.CloseClipboard()

def send_message_to_chatroom(room_name: str, text: str):
    hwndMain = win32gui.FindWindow(None, room_name)
    if not hwndMain:
        raise RuntimeError(f"채팅방 '{room_name}' 창을 찾을 수 없습니다. 먼저 열어두세요.")

    hwndInput = win32gui.FindWindowEx(hwndMain, None, "RICHEDIT50W", None)
    if not hwndInput:
        hwndInput = win32gui.FindWindowEx(hwndMain, None, "Edit", None)
    if not hwndInput:
        raise RuntimeError("채팅 입력창을 찾지 못했습니다.")

    copy_to_clipboard(text)
    time.sleep(0.3)
    PostKeyEx(hwndInput, ord('V'), [w.VK_CONTROL])
    time.sleep(0.3)
    SendReturn(hwndInput)
