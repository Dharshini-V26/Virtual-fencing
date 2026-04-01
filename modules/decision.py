class DecisionEngine:
    def evaluate(self, detections, fence):
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]

            px = (x1 + x2) // 2
            py = (y1 + y2) // 2

            if fence.is_inside(px, py):
                return "UNSAFE"

        return "SAFE"