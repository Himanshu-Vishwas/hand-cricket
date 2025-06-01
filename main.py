import cv2
import random
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Initialize the video capture for the webcam
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)  # Set confidence level and max number of hands

# Initialize variables for score and result
player_score = 0
computer_score = 0
result = "Waiting....."  # Default message before any result

# Variables for timing and computer move
start_time = time.time()
computer_count = random.randint(0, 6)  # Initialize with a random number
computer_final_move = False  # To know when to stop random changes
player_final_move = False
hand_detected = False  # Flag to check if a hand was detected


# Game loop with 5 seconds per input
while True:
    # Read the frame from the camera
    success, img = cap.read()
    if not success:
        break

    # Resize the frame to half its original width (for split screen)
    img = cv2.resize(img, (640, 480))

    # Create a blank image with a blue gradient background for the right half
    right_img = np.zeros_like(img)  # Same size as the camera feed
    right_img[:] = (0, 0, 255)  # Red background for contrast

    # Display current scores on the left half (camera feed)
    cv2.putText(right_img, f"Score: {player_score}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    # cv2.putText(right_img, f"Computer Score: {computer_score}", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    cv2.putText(right_img, result, (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
    cv2.putText(right_img, "press q to exit", (30, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)


    # Find hands and count the fingers
    hands, img = detector.findHands(img)  # With drawing

    if hands:
        hand_detected = True  # Hand is detected
        hand = hands[0]
        fingers = detector.fingersUp(hand)  # List of 0 or 1 for each finger up

        # Determine the player's current move
        if not player_final_move:
            # print(fingers)
            if sum(fingers) == 1 and fingers[0] == 1:
                player_move = "6"  # If only thumb is up, count as 6
            elif sum(fingers) == 2 and (fingers[1] == 1 and fingers[4]==1):
                break
            else:
                player_move = str(sum(fingers))  # Normal finger count

        # Display the player's move on the left half
        cv2.putText(right_img, f"You: {player_move}", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

        # Check if the game is in progress (5-second cycle)
        elapsed_time = time.time() - start_time

        if elapsed_time < 5:
            # If within the first 4 seconds, change the computer move randomly every second
            if not computer_final_move:
                computer_count = random.randint(0, 6)

            # Stop changing the number at the 3rd second and display the final number
            if elapsed_time > 3:
                computer_final_move = True  # Stop changing the number
                player_final_move = True

            # Display the computer's move on the right half (red background)
            cv2.putText(right_img, f"Computer: {computer_count}", (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

        else:
            # At the 5th second, compare the player and computer move
            if hand_detected:
                # Convert player_move to numerical value
                player_count = 6 if player_move == "6" else int(player_move)

                # Display the player's move on the left half
                cv2.putText(right_img, f"You: {player_count}", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

                # Check if it's a tie (out condition)
                if player_count == computer_count:
                    result = "Out!"
                    player_score = 0
                    computer_score = 0
                else:
                    # Compare the counts to determine the winner
                    player_score += player_count
                    # if player_count > computer_count:
                    #     player_score += player_count  # Increment by the number of fingers
                    #     result = f"You Wins! +{player_count} points"
                    # else:
                    #     computer_score += computer_count  # Increment by the computer's random number
                    #     result = f"Computer Wins! +{computer_count} points"

                # Display the result
                cv2.putText(right_img, result, (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            else:
                # No hand detected, display appropriate message
                result = "No hand detected....."
                cv2.putText(right_img, result, (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)

            # Reset for the next round after the comparison
            start_time = time.time()  # Reset round timer
            computer_final_move = False  # Allow random changes again
            hand_detected = False  # Reset hand detection flag
            player_final_move = False

    else:
        hand_detected = False  # No hand detected
        elapsed_time = 0

    # Combine the two halves (left: camera, right: red background with computer move)
    combined_img = np.hstack((img, right_img))

    # Show the combined video feed with results
    cv2.imshow("Hand Cricket Game", combined_img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
