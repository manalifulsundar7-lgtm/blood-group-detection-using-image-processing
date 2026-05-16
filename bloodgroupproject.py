# Function to check agglutination (clotting)
def detect_agglutination(image_path):
    # Read image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Thresholding to detect clots
    _, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours (clumps)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Count significant contours
    clot_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # threshold area for clot detection
            clot_count += 1

    # If clots detected → Positive reaction
    return clot_count > 0


# Function to determine blood group
def detect_blood_group(antiA_img, antiB_img, antiD_img):
    antiA = detect_agglutination(antiA_img)
    antiB = detect_agglutination(antiB_img)
    antiD = detect_agglutination(antiD_img)

    if antiA and not antiB:
        group = "A"
    elif antiB and not antiA:
        group = "B"
    elif antiA and antiB:
        group = "AB"
    else:
        group = "O"

    rh = "+" if antiD else "-"

    return group + rh


# Example usage
antiA_img = "antiA.jpg"
antiB_img = "antiB.jpg"
antiD_img = "antiD.jpg"

blood_group = detect_blood_group(antiA_img, antiB_img, antiD_img)

print("Detected Blood Group:", blood_group)