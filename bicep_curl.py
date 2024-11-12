import cv2
import math
import mediapipe as mp

# Function to calculate the angle between the shoulder, elbow, and wrist
def calculate_angle(shoulder, elbow, wrist):
    # Calculate vectors
    vector1 = [elbow[0] - shoulder[0], elbow[1] - shoulder[1]]
    vector2 = [wrist[0] - elbow[0], wrist[1] - elbow[1]]
    
    # Dot product and magnitudes
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    
    # Calculate cosine of the angle
    cos_angle = dot_product / (magnitude1 * magnitude2)
    cos_angle = min(1.0, max(cos_angle, -1.0))  # To avoid floating point errors
    
    # Get the angle in radians, then convert to degrees
    angle_radians = math.acos(cos_angle)
    return math.degrees(angle_radians)

# Initialize Mediapipe Pose Model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize video capture
cap = cv2.VideoCapture(0)

# Rep counting variables for both arms
left_rep_count = 0
right_rep_count = 0
left_in_rep = False
right_in_rep = False

# Set counting variables
left_set_count = 1
right_set_count = 1

# Thresholds for angle (adjust these to suit the exercise)
angle_threshold_lower = 50   # Arm fully bent (threshold to start rep)
angle_threshold_upper = 160  # Arm fully extended (threshold to end rep)

# Number of reps per set
reps_per_set = 13

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the image to RGB (Mediapipe requires RGB format)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Get the pose landmarks
    results = pose.process(frame_rgb)
    
    if results.pose_landmarks:
        # Get the coordinates for the left arm (shoulder, elbow, wrist)
        left_shoulder = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * frame.shape[1], 
                         results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * frame.shape[0])
        left_elbow = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x * frame.shape[1], 
                      results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y * frame.shape[0])
        left_wrist = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * frame.shape[1], 
                      results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * frame.shape[0])

        # Get the coordinates for the right arm (shoulder, elbow, wrist)
        right_shoulder = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * frame.shape[1], 
                          results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * frame.shape[0])
        right_elbow = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x * frame.shape[1], 
                       results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y * frame.shape[0])
        right_wrist = (results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * frame.shape[1], 
                       results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * frame.shape[0])

        # Calculate angles for both arms
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        
        # Rep counting logic for left arm
        if left_angle > angle_threshold_upper and not left_in_rep:
            left_in_rep = True
        elif left_angle < angle_threshold_lower and left_in_rep:
            left_rep_count += 1
            left_in_rep = False
            if left_rep_count == reps_per_set:  # Reset after 15 reps
                left_rep_count = 0
                left_set_count += 1

        # Rep counting logic for right arm
        if right_angle > angle_threshold_upper and not right_in_rep:
            right_in_rep = True
        elif right_angle < angle_threshold_lower and right_in_rep:
            right_rep_count += 1
            right_in_rep = False
            if right_rep_count == reps_per_set:  # Reset after 15 reps
                right_rep_count = 0
                right_set_count += 1

    # Display rep count and set count for both arms
    cv2.putText(frame, f'Left Reps: {left_rep_count} / Set {left_set_count}', 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Right Reps: {right_rep_count} / Set {right_set_count}', 
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    
    # Show the frame with the counts
    cv2.imshow('Exercise Form and Reps', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
