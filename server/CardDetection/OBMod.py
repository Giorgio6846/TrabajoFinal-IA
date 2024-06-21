from ultralytics import YOLO

def detectCard(path):
    model = YOLO("./last.pt")

    results = model([path])
    print(results)

    for result in results:
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        obb = result.obb
        result.save(filename=path+"OD.jpg")