# script to implement camera tracking
import cv2
from cv2 import aruco
import pandas as pd
import math
import numpy as np


def get_cordinates(ids, corners):
    print(ids)
    df = pd.DataFrame(columns=['id', 'px', 'py', 'radian'])
    try:
        if ids.any():
            try:        
                for i in range(len(ids)-1, -1, -1):
                    c = corners[i][0]
                    px, py = c[:, 0].mean(), c[:, 1].mean()
                    delta_y = c[1, 1] - c[0, 1]
                    delta_x = c[1, 0] - c[0, 0]
                    angleInRadian = math.atan2(delta_y, delta_x)
                    df = df.append({'id': ids[i][0], 'px': px, 'py': py, 'radian': angleInRadian}, ignore_index=True)    
            except:
                pass
    except:
        return
    df['id'] = df['id'].astype(np.int64)
    return df


if __name__ == '__main__':
    capture = cv2.VideoCapture(1)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_100)
    
    if capture.isOpened():
        frame_captured, frame = capture.read()
    else:
        frame_captured = False
    while frame_captured:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        df = get_cordinates(ids, corners)
        print(df)
        #frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        #cv2.imshow('Captured Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_captured, frame = capture.read()

    # release the video capture
    capture.release()
    cv2.destroyAllWindows()