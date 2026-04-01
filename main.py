import cv2
from modules.camera import Camera
from modules.detector import Detector
from modules.fence import VirtualFence
from modules.decision import DecisionEngine
from modules.events import EventManager
from utils.draw import draw_boxes, draw_fence

camera = Camera("video.mp4")
detector = Detector()
fence = VirtualFence()
decision = DecisionEngine()
events = EventManager()

drawing = False
ix, iy = -1, -1

def mouse_callback(event, x, y, flags, param):
    global ix, iy, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        fence.set_box((ix, iy, x, y))
        print("Fence set:", (ix, iy, x, y))

cv2.namedWindow("Virtual Fencing System")
cv2.setMouseCallback("Virtual Fencing System", mouse_callback)

while True:
    frame = camera.get_frame()
    if frame is None:
        break

    frame = cv2.resize(frame, (640, 480))

    detections = detector.detect(frame)

    status = decision.evaluate(detections, fence)

    event = events.create_event(status, frame)
    events.handle_event(event)

    draw_boxes(frame, detections)
    draw_fence(frame, fence.box, status == "UNSAFE")

    # display status
    cv2.putText(frame, status, (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0,255,0) if status=="SAFE" else (0,0,255), 2)

    cv2.putText(frame,
                "F: Toggle | C: Clear | Q: Quit",
                (20,80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,0), 2)

    cv2.imshow("Virtual Fencing System", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('f'):
        fence.toggle()
        print("Fence Enabled:", fence.enabled)
    elif key == ord('c'):
        fence.clear()
        print("Fence Cleared")

camera.release()
cv2.destroyAllWindows()