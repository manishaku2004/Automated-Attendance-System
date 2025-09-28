# capture_images.py
import os
import cv2
import face_recognition
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--name", required=True, help="Name of the person (no spaces, e.g. John_Doe)")
ap.add_argument("-o", "--output", default="dataset", help="Output dataset folder")
ap.add_argument("-c", "--count", type=int, default=20, help="How many images to capture")
args = vars(ap.parse_args())

name = args["name"]
output_dir = os.path.join(args["output"], name)
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
print("Press 'q' to quit early. Look at the camera. Capturing faces...")

saved = 0
while saved < args["count"]:
    ret, frame = cap.read()
    if not ret:
        break
    # optional: flip frame if camera mirrored
    frame_small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    rgb_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
    # detect faces
    locations = face_recognition.face_locations(rgb_small)
    for (top, right, bottom, left) in locations:
        # scale back coordinates to original frame size
        top *= 2; right *= 2; bottom *= 2; left *= 2
        face_img = frame[top:bottom, left:right]
        if face_img.size == 0:
            continue
        fname = os.path.join(output_dir, f"{name}_{saved:03d}.jpg")
        cv2.imwrite(fname, face_img)
        saved += 1
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, f"Saved {saved}/{args['count']}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        break  # save one face per frame
    cv2.imshow("Capture (q to quit)", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print(f"Done. Saved {saved} images to {output_dir}")
