import face_recognition
import json


my_picture = face_recognition.load_image_file("TIN_Wilson.jpeg")
my_face_encoding = face_recognition.face_encodings(my_picture)[0]
print(json.dumps(my_face_encoding.tolist()))


unknown_picture = face_recognition.load_image_file("me.jpg")
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]


results = face_recognition.compare_faces(
    [my_face_encoding], unknown_face_encoding, tolerance=0.5)

print(results)
if results[0]:
    print("It's Wilson!")
else:
    print("It's not Wilson!")
