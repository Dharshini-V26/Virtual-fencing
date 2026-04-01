import cv2

def draw_boxes(frame, detections):
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 2)

        px = (x1 + x2) // 2
        py = (y1 + y2) // 2
        cv2.circle(frame, (px, py), 4, (0,0,255), -1)

def draw_fence(frame, box, alert=False):
    if box:
        x1, y1, x2, y2 = box
        color = (0,0,255) if alert else (0,255,0)
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)