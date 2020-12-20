# FaceFilter
<h1 align="center">
  <img src="https://github.com/SoorenGhodsi/FaceFilter/blob/main/screenshots/Cover.jpg" alt="FaceFilter" width="500">
</h1>
Face Filter is a program that places select filters onto faces that are detected in the given image or the live feed.

## Motivation
We were inspired by popular Instagram and Snapchat filters and wanted to see if we could create a makeshift version of them in only two days for the 2020 Winter Hacklympics Hackathon hosted by MLH.

## Screenshots
![Face Recognition](https://github.com/SoorenGhodsi/FaceFilter/blob/main/screenshots/Face%20Recognition.jpg)
![Flower](https://github.com/SoorenGhodsi/FaceFilter/blob/main/screenshots/Flower%20Filter.jpg)
![Helmet](https://github.com/SoorenGhodsi/FaceFilter/blob/main/screenshots/Helmet%20Filter.jpg)
![Live](https://github.com/SoorenGhodsi/FaceFilter/blob/main/screenshots/Live%20Filter.jpg)


## Features
Face Filter uses live facial detection and image processing operations and places a filter onto each face detected by the device camera. Through a number of calculations, it determines the optimal placement, scale, and angle of the filter mask dependent on each individual face.

## Installation
### Windows
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cv2, numpy 1.19.13, and scipy in command prompt.
```
pip install opencv-contrib-python
pip uninstall numpy
pip install numpy==1.19.3
pip install scipy
```

### Mac OS
coming soon...

## Usage
### Image Filter
1. Open the `filter.py` file to edit
2. Change these lines to include the name of the image and the respective filter that you want to use.
```python
#read images
img = cv2.imread('assets/image_name.jpg')
fltr = cv2.imread('assets/filter_name.png')
``` 
3. Run the `filter.py` file
4. Press any keyboard button to exit

### Live Video Filter
1. Open the `live_filter.py` file to edit
2. Change this line to include the name of the filter that you want to use.
```python
#read images
fltr = cv2.imread('assets/filter_name.png')
``` 
3. Run the `live_filter.py` file
4. Press any keyboard button to exit

## Credits
Sooren Ghodsi, Ethan Li, Seth Eshraghi, Joseph Gong, and [Mitchell Kireger](https://mitchellkrieger.medium.com/)

## License
[MIT](https://choosealicense.com/licenses/mit/) © Sooren Ghodsi
