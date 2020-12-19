import cv2

# We need the backgroud image of when there is no object present
# sow e can compare the motion video and the backgroud image

# Loading Image
backgroung = cv2.imread('background2.png')
backgroung = cv2.cvtColor(backgroung, cv2.COLOR_BGR2GRAY)
backgroung = cv2.GaussianBlur(backgroung, (21, 21), 0)

video = cv2.VideoCapture('test3.avi')

# Creating video capture loop

while True:
    status, frame = video.read()
    # Changing color profile to gray for processing efficency
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # To remove unnecce=ary line the would be present in the video
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Calculating the absolute differnce between the images
    diff = cv2.absdiff(backgroung, gray)

    # In order to remove all order noice we need a threshold
    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    cnts, res = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow('Final Display', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
