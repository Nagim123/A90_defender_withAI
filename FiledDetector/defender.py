import numpy as np
from window_finder import get_window_rect
from mss import mss
from PIL import Image
from model_runner import ModelRunner
from stopper import temp_stop_player

def defender_run(conn):
    try:
        # INIT
        sct = mss()
        detector = ModelRunner(256)
        wind_rect = get_window_rect("Roblox")
        x, y, w, h = wind_rect[0], wind_rect[1], wind_rect[2] - wind_rect[0], wind_rect[3] - wind_rect[1]
        bounding_box = {'top': y + 40, 'left': x, 'width': w, 'height': h - 40} # -40 to not capture title part of Window's window

        # LOOP
        while True:
            
            screenShot = sct.grab(bounding_box)
            img = Image.frombytes(
                'RGB', 
                (screenShot.width, screenShot.height), 
                screenShot.rgb, 
            )

            result = detector.detect(np.array(img))
            if not result is None:
                if result:
                    temp_stop_player()
                    conn.send([0, "Attack"])
    except Exception as e:
        conn.send([1, str(e)])