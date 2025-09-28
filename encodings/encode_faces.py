# encode_faces.py
import os
import pickle
import face_recognition

DATASET_DIR = "dataset"
OUTPUT = "encodings"
os.makedirs(OUTPUT, exist_ok=True)
encodings_list = []
names_list = []

for person_name in os.listdir(DATASET_DIR):
    person_dir = os.path.join(DATASET_DIR, person_name)
    if not os.path.isdir(person_dir):
        continue
    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        try:
            image = face_recognition.load_image_file(img_path)
            # get encodings (may return empty list if face not found)
            encs = face_recognition.face_encodings(image)
            if len(encs) == 0:
                print("WARNING: No face found in", img_path)
                continue
            encodings_list.append(encs[0])
            names_list.append(person_name)
        except Exception as e:
            print("Error processing", img_path, e)

data = {"encodings": encodings_list, "names": names_list}
with open(os.path.join(OUTPUT, "encodings.pickle"), "wb") as f:
    pickle.dump(data, f)
print("Saved encodings to encodings/encodings.pickle")
