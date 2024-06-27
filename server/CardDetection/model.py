from ultralytics import YOLO


model = YOLO("./server/CardDetection/last.pt")

def detectCards(path):
    results = model([path])
    #print(results)

    for result in results:
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        obb = result.obb
        names = result.names
        result.save(filename=path+"OD.jpg")

    cardsDealer, cardsPlayer = parseBoxes(boxes, names)
    return cardsDealer, cardsPlayer
    
def parseBoxes(boxes, names):
    cards = []

    if len(boxes) == 0:
        return cards

    cardsDealer = []
    cardsPlayer = []

    orig_shapeX, orig_shapeY = boxes[0].orig_shape

    print(orig_shapeX)
    print(orig_shapeY)

    # It is going to return the type in which it is being considered and the type

    print(names)

    for box in boxes:
        print("Type Card")
        TypeCard = names[int(box.cls.item())]
        print(TypeCard)

        print("Confidence")
        Confidence = round(box.conf.item(), 2)
        print(Confidence)

        # Card Dictionary
        card = {"Conf": Confidence, "TypeCard": TypeCard}

        # From a box
        # X1Y1
        #       X2Y2
        print("Coordinates")
        # It prints like (X1)
        print(box.xyxy.numpy())
        Coordinates = box.xyxy.numpy()[0]
        X1 = Coordinates[0]
        Y1 = Coordinates[1]
        X2 = Coordinates[2]
        Y2 = Coordinates[3]

        if Y1 > orig_shapeX / 2 or Y2 > orig_shapeX / 2:
            cardsDealer.append(card)
        else:
            cardsPlayer.append(card)

        print(X1, X2, Y1, Y2)

    return cardsDealer, cardsPlayer
