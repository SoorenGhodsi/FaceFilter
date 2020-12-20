# FaceFilter

Face Filter is a program that places select filters onto faces that are detected in the given image or the live feed.

## Motivation
We were inspired by popular Instagram and Snapchat filters and wanted to see if we could create a makeshift version of them in only two days.

## Screenshots
Images here.

## Setup
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cv2, numpy 1.19.13, and scipy.
```
pip install opencv-contrib-python
pip uninstall numpy
pip install numpy==1.19.3
pip install scipy
```

## Image Filter Usage
Edit these two lines with the name of the image and the respective filter that you want to use.
```python
#read images
img = cv2.imread('assets/image_name.jpg')
fltr = cv2.imread('assets/filter_name.png')
``` 

## Live Video Filter Usage
Edit this line with the name of the filter that you want to use.
```python
#read images
fltr = cv2.imread('assets/filter_name.png')
``` 

## Credits
Sooren Ghodsi, Ethan Li, Seth Eshraghi, Joseph Gong, and [Mitchell Kireger](https://towardsdatascience.com/how-to-make-your-own-instagram-filter-with-facial-recognition-from-scratch-using-python-d3a42029e65b)

## License
[MIT](https://choosealicense.com/licenses/mit/)
