# FaceFilter

Face Filter is a program that places select filters onto faces that are detected in the given image or the live feed.

### Installation
To use Face Filters, you must install numpy version 1.19.13, cv2, and scipy.

```
pip install opencv-contrib-python
pip uninstall numpy
pip install numpy==1.19.3
pip install scipy
```

## Usage

Edit these two lines with the path of the image and the respective filter that you want to use.
```python
#read images
img = cv2.imread('assets/people1.jpg')
fltr = cv2.imread('assets/dog.png')
``` 


## Credits
Sooren Ghodsi, Seth Eshraghi, Joseph Gong, Ethan Li
