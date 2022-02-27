import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os

            
IMAGE_SIZE = 324 # pixel size of extracted grid
COMB = IMAGE_SIZE//9
DIRECTORY = cwd = os.getcwd()


def get_contours(img, original_img):
    """
    Identify the Sudoku board and generate a clear image from it
    :param img: preprocessed image
    :param original_img: original image
    :return: cropped image of the board
    """
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 40000: # only draw contour of the main/biggest object(Sudoku Grid)
            cv2.drawContours(original_img, cnt, -1, (0,255,0), 2)
            
            # get the corners of the grid 
            peri =  cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            
            ax = approx.item(0)
            ay = approx.item(1)
            bx = approx.item(2)
            by = approx.item(3)
            cx = approx.item(4)
            cy = approx.item(5)
            dx = approx.item(6)
            dy = approx.item(7)
            
            # Maps the grid onto a new picture            
            pts1 = np.float32([[ax, ay], [dx, dy], [bx, by], [cx, cy]])
            pts2 = np.float32([[0, 0], [IMAGE_SIZE, 0], [0, IMAGE_SIZE], [IMAGE_SIZE, IMAGE_SIZE]])

            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            img_corners = cv2.warpPerspective(original_img, matrix, (IMAGE_SIZE,IMAGE_SIZE))
            try:
                img_corners = cv2.cvtColor(img_corners, cv2.COLOR_BGR2GRAY) # image might already be in grayscale
            except:
                pass
            cv2.imshow("Detected Sudoku", img_corners)

            ''' # Turn Grayscale Image into Black and White Image
            for x in range(0, IMAGE_SIZE): 
                for y in range(0, IMAGE_SIZE):
                    if img_corners[x][y] < 100:
                        img_corners[x][y] = 0
                    else:
                        img_corners[x][y] = 255 # 1 if direct resize desired
            '''
            
            # initial cropping of the thick outer boundary lines
            crop_amount = 2 
            img_corners = img_corners[
                        crop_amount : IMAGE_SIZE - crop_amount,
                        crop_amount : IMAGE_SIZE - crop_amount
                    ]

    try:
        return img_corners
    except ReferenceError:
        print("Sudoku Grid not detected. Try holding it closer to the camera / have it take up more of the image.")



def get_cells(img_corners):
    """
    Cuts the initial image from get_contours into individual cells
    :param img_corners: image from get_contours.
    :return: list of cells
    """
    crop_amount = 4
    
    cells = []

            
    for y in range(1,10): 
        for x in range(1,10):
            cell = img_corners[
                y*COMB - COMB+crop_amount : y*COMB - crop_amount,
                x*COMB - COMB+crop_amount : x*COMB - crop_amount
            ]

            '''# plot cells
            plt.imshow(cell)
            plt.show()
            print(digit.shape)'''
            
            cells.append(cell)
            

    return cells     



def save_images(cells, board, saving_method=None):
    """
    Save images for later model training
    :param cells: list of images
    :param board: filled out sudoku board to determine where to save to
    :param saving_method:   #    None = don't,
                            #   "manual" = order images by hand from a single folder,
                            #   "grid_array"  = fill in grid_test_img,
                            #   "auto" = use existing model to order them -> manual corrections might be necessary
    :return:
    """

    if saving_method is None:
        return 
    location = f"{DIRECTORY}\\digits\\"
    
    numbers = []          



    # "grid_array"  = fill in grid_test_img
    if saving_method == "grid_array":
        for i in range(0, 9):
            for j in range(0, 9):
                        
                grid_test_img = [[4,2,6,9,3,5,8,1,7], 
                                [8,8,1,7,2,4,6,9,5],
                                [7,9,5,8,1,6,2,4,3],
                                [9,3,8,2,5,7,1,6,4],
                                [3,5,4,1,6,8,3,7,9],
                                [1,6,7,4,9,3,5,2,8],
                                [3,7,2,5,4,1,9,8,6],
                                [6,4,9,3,8,2,7,5,1],
                                [5,8,1,6,7,9,4,3,2]]
                
                numbers.append(grid_test_img[i][j]) # iterate the name of the saved file
                amount = numbers.count(grid_test_img[i][j])
                
                cv2.imwrite(f"{location+str(grid_test_img[i][j])}\\img_{amount}.png".format((i+1)*(j+1)), cells[i*9 + j])

                
            # "manual" = order images by hand from a single folder
    elif saving_method == "manual":
        for i in range(0, 9):
            for j in range(0, 9):
                cv2.imwrite(f"{DIRECTORY}\\test\\my\\img_{i*9+j}.png".format((i+1)*(j+1)), cells[i*9 + j])

                
            # "auto" = use existing model to order them -> manual corrections might be necessary!!!    
    elif saving_method == "auto":
        for i in range(0, 9):
            for j in range(0, 9):
                cv2.imwrite(f"{location+str(board[i][j])}\\img_31{i*9+j}.png".format((i+1)*(j+1)), cells[i*9 + j])

    print("Saved Images to respective folders.")



def get_board(image, saving_method=None):
    # save images of individual cells for further model training
    # saving_method = how to save the images


    model = tf.keras.models.load_model(DIRECTORY+"/model/Digit_Classifier")
    CLASS_NAMES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    img = image

    # Bit of preprocessing and Canny Edge Detection
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # image might already be in grayscale
    except:
        pass
    img_blurred = cv2.GaussianBlur(img, (5,5), 2)
    img_canny = cv2.Canny(img_blurred, 50, 50)

    img_copy = img.copy()
    table = get_contours(img_canny, img_copy) #Getting outer contours of Grid


    cells = get_cells(table)
    cells_array = np.array(cells)

    show_digits = False # plot cells and their respective predicted digits
    board = [] # Digitized Sudoku board as 2D array
    row = []   # rows of the board
    i = 0


    for cell in cells_array:
        cell_batch = np.expand_dims(cell, 0)

        digit_prediction = model.predict(cell_batch)
        row.append(np.argmax(digit_prediction))


        if show_digits is True:
            plt.imshow(cell)
            plt.show()
            #print(cell)
            print(f"predicted digit: {row[-1]}")

        i += 1
        # add  rows to the board
        if i // 9 == 1:
            board.append(row)
            row = []
            i = 0

    save_images(cells, board)
    return board

def init():
    # initialize Sudoku_Digitizer.py before local_server.py
    return



