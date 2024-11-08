import cv2

def check_if_specific_key_pressed_cv2(key_sign, waitKey):
    return cv2.waitKey(waitKey) & 0xFF == ord(key_sign)