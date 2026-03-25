import cv2
import mediapipe as mp
import pygame
import os

# --- Configuration ---
# Adjust this threshold if needed. 
# Lower = requires you to look further down. Higher = more sensitive.
LOOK_DOWN_THRESHOLD = 0.85 
AUDIO_FILE = "rock.mp3"

def main():
    # 1. Initialize Pygame Mixer (The "Actuator")
    if not os.path.exists(AUDIO_FILE):
        print(f"Error: Could not find '{AUDIO_FILE}'. Please add an mp3 file to the directory.")
        return

    pygame.mixer.init()
    pygame.mixer.music.load(AUDIO_FILE)
    pygame.mixer.music.play(-1) # Play on loop
    pygame.mixer.music.pause()  # Start paused
    is_playing = False

    # 2. Initialize MediaPipe FaceMesh (The "Sensor")
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # 3. Initialize Webcam
    cap = cv2.VideoCapture(0) # Change to 1 if webcam is not found
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("RockLook initialized! Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a selfie-view display
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame with MediaPipe
        results = face_mesh.process(rgb_frame)

        ratio = 0.0
        status_text = "No face detected"
        color = (0, 0, 255) # Red

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                h, w, _ = frame.shape
                
                # Get coordinates for Forehead (10), Nose Tip (1), and Chin (152)
                y_forehead = face_landmarks.landmark[10].y * h
                y_nose = face_landmarks.landmark[1].y * h
                y_chin = face_landmarks.landmark[152].y * h

                # Calculate vertical distances
                dist_forehead_nose = y_nose - y_forehead
                dist_nose_chin = y_chin - y_nose

                # Prevent division by zero
                if dist_forehead_nose > 0:
                    # The threshold math:
                    # When looking down, nose-to-chin distance gets visually smaller 
                    # while forehead-to-nose gets visually larger.
                    ratio = dist_nose_chin / dist_forehead_nose

                # Threshold Check (The "Relay")
                if ratio > 0 and ratio < LOOK_DOWN_THRESHOLD:
                    status_text = "ROCK ON! (Looking Down)"
                    color = (0, 255, 0) # Green
                    
                    if not is_playing:
                        pygame.mixer.music.unpause()
                        is_playing = True
                else:
                    status_text = "Paused (Looking Up)"
                    color = (0, 255, 255) # Yellow
                    
                    if is_playing:
                        pygame.mixer.music.pause()
                        is_playing = False

        # 4. Display Info on Screen
        cv2.putText(frame, status_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        cv2.putText(frame, f"Current Ratio: {ratio:.2f}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Threshold: {LOOK_DOWN_THRESHOLD}", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow('RockLook', frame)

        # Quit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()

if __name__ == "__main__":
    main()