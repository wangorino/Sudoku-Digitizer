# Sudoku-Digitizer
Computer Vision / Backtracking application that digitizes an image of a Sudoku game that you can take from for example a newspaper. It solves the Sudoku and allows you to play a digital version of it.

The programm will run a local server on your PC upon startup. Run "main.py". You should get a confimation that the server is running. Once you pass an appropriate image to that server it will digitize the Sudoku. 
***To try it out you can send a POST request to the following URL via an API-Platform like Postman.***
http://127.0.0.1:8000/post_image


## Access via API-Platform: 
- set the type of request from *"GET"* to ***"POST"***
- Go to *"Body"*
- Change *"none"* to *"form-data"*
- add a *KEY* as *"File"* and name it **"file"**
- **select the file** you want to have evaluated in *"Value"*
- *Send*

## How to play the Game:
- Click on one of the tiles and type in the guessed number. (Numpad not supported)
- To lock in the number press Enter. If it's wrong you'll get a strike ;)

## Files included in the repository:
- A couple ***Images*** that you can use in your POST requests. 
- The ***python scripts***. (Run "main.py")
- The ***Model*** used for the evaluation. 
- Jupyter Notebook of the ***model training*** process.

## Disclaimers:
- The ***recognition of the Sudoku grid is still a bit fragile.*** In the future I'll probably implement something that will allow you to use a webcam/video feed to scan the Sudoku to make it more flexible. 
- It's ***hihgly recommended to manually crop the image beforehand*** and remove additional outlines. The programm looks for the outline of the biggest area which is supposed to be the grid. Images like this are guranteed to confuse it:
![](https://www.google.com/search?q=sudoku+newspaper&tbm=isch&ved=2ahUKEwjb3bim8J_2AhXPvSoKHWAYDeEQ2-cCegQIABAA&oq=sudoku&gs_lcp=CgNpbWcQARgBMgcIIxDvAxAnMgcIIxDvAxAnMgQIABBDMgUIABCABDIFCAAQgAQyCwgAEIAEELEDEIMBMgQIABBDMgUIABCABDIFCAAQgAQyBQgAEIAEUABYAGCnBmgAcAB4AIABR4gBR5IBATGYAQCqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=lG0bYtvDGs_7qgHgsLSIDg&bih=949&biw=958&client=firefox-b-d#imgrc=lJBA_MutYaR_ZM&imgdii=5olK8vIryeiWuM)
 
- The ***digit recognition model*** was trained with a mixture of a dataset reminiscent of the MNIST-Dataset and additional images I collected myself, since there were too few images of printed numbers which are more useful here. For that purpose Sudoku_Digitizer.py also has functions dedicated to saving test images. Getting "usefull" images is pretty tedious and requires a lot of manual curation especially at the start, so the model ***isn't as well trained I'd have liked it to be.*** I'll try to keep it updated.  
- For the time being I ***recommend using the test images I provided*** to play the actual game. They're confirmed to work. If a number is misclassified, it's liekly the programm won't find a valid solution meaning yuo can't lock in numbers.
