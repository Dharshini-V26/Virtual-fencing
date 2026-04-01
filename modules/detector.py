from ultralytics import YOLO

class Detector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        results = self.model(frame, verbose=False)
        detections = []

        for r in results:
            for b in r.boxes:
                if int(b.cls[0]) == 0:  # person
                    x1, y1, x2, y2 = map(int, b.xyxy[0])
                    conf = float(b.conf[0])

                    detections.append({
                        "bbox": (x1, y1, x2, y2),
                        "confidence": conf
                    })

        return detections