##Object being tracked: Referee. Since the background is dynamic, I found it
##hard to deal with, so I chose the referee to track because he's running
##on the pitch, which doesn't change too much and has red colored shirt. 

import cv2
import numpy as np
import sys


(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

print(major_ver, minor_ver, subminor_ver)

print(__name__)

if __name__ == '__main__' :

    #Set up trackers

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD',
                     'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    #Choose tracker type. In this case, our best result was Median Flow.
    tracker_type = tracker_types[4]
    print(tracker_type)

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type =='BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == 'CSRT':
            tracker = cv2.TrackerCSRT_create()
    #Read video
    video = cv2.VideoCapture(r'C:\Users\PC\Desktop\Gol de Breno Lopes, gol do título do Palmeiras da Copa Libertadores 2020_Trim.mp4')
    #Check to see if video doesnt open. In that case, exit.
    if not video.isOpened():
        print('Could not open video')
        sys.exit()
    #Read first frame
    ret, frame = video.read()
    #If it cant read first frame, exit. 
    if not ret:
        print('Cannot read video')
        sys.exit()
        
    #GUI to select the object to be tracked. In this case, it would be the ref.
    bbox = cv2.selectROI(frame, fromCenter = True)
    print(bbox)
    #Initialize tracker with the first frame and the bounding box created.
    ok = tracker.init(frame, bbox)
    while True:
        
        ret, frame = video.read()

        #Check to see if it reads frame, if not then exit.
        if not ret:
            print('Cannot receive frame')
            break

        #Start timer
        timer = cv2.getTickCount()
        #Update tracker
        ret, bbox = tracker.update(frame)
        #Calculate the number of Frames per second.
        fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer);

        #Draw bounding box
        if ret:
            #Tracking points and then draws rectangle.
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1]+ bbox[3]))
            cv2.rectangle(frame, p1,p2,(255,0,0),2,1)
        else:
            #When tracker fails, display message.
            cv2.putText(frame,"Tracking failure detected", (100,80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        #Display tracker type
        cv2.putText(frame, tracker_type + " Tracker", (100,20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        #Display FPS
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        
        cv2.imshow('Gol', frame)
        #To exit, press q
        if cv2.waitKey(20) == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
    
##Results
    #Boosting -- No tracking failures detected, but there is a False Postive on
    #            for a long period, and doesnt autocorrect. Normal speed
    #MIL -- No tracking failures dtected, but False Postive on end. Too slow
    #KCF -- Tracking Failures detected very early and doesnt autocorrect.
    #TLD -- A lot of False Positives.
    #Median Flow -- Good speed, very accurate tracking and failure detected
    #               only at the end when referee disappears from scene.
    #GOTURN -- Slow speed, bounding box tracker varies a lot in size and
    #          doesnt detected failure at the end when referee disappears,
    #          instead False Positive.
    #MOSSE -- Tracking failure happened when the background changes fast,
    #         when the ball is crossed, then a FP is present until the end.
    #CSRT -- Slow speed, very accurate tracking right up to the end when there
    #        is a failure and then it detects a FP.  
##After considering all the tracker types, the best output was given by the
##Media Flow tracker.
        
        
