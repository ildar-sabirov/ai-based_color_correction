import cv2
import numpy as np

def glare_shadow(img, u =240, l = 150,process=cv2.INPAINT_TELEA):
        height, weight, _ = img.shape
        # thresholding with upper and lower values
        upper = (u, u, u)
        lower = (l, l, l)
        thresh = cv2.inRange(img, lower, upper)
        # apply morphology close and open to make mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25,25))
        morph = cv2.morphologyEx(morph, cv2.MORPH_DILATE, kernel, iterations=1)

        # floodfill the outside with black
        black = np.zeros([height + 2, weight + 2], np.uint8)
        mask = morph.copy()
        mask = cv2.floodFill(mask, black, (0,0), 0, 0, 0, flags=8)[1]

        '''
        if process != None:
                #mask = cv2.bitwise_not(mask)
                result = cv2.inpaint(img, mask, 101, process)
        else:
                result = img.copy()
                
        print(f'Mask shape {mask.shape}, result shape {result.shape}')
        '''        
        result = img.copy()
        print(f'Mask shape {mask.shape}, result shape {result.shape}')
        return mask, result

img = cv2.imread('/mnt/e/Hackatons/Camera_Calibration/Test_img/1.jpg')
mask,result_image = glare_shadow(img, 240, 150)
cv2.imshow("IMAGE", result_image)
cv2.imshow("Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()