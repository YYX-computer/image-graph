from PIL import Image
import numpy as np
import os
def make(imgMat):
	img = Image.new("RGB",(64 * len(imgMat),64 * len(imgMat[0])))
	for i in range(len(imgMat)):
		for j in range(len(imgMat[i])):
			imgMat[i][j] = imgMat[i][j].resize((64,64))
			img.paste(imgMat[i][j],(64 * i,64 * j))
	return img
def split(img,w,h):
	mat = []
	for i in range(h):
		l = []
		for j in range(w):
			box = (64 * i,64 * j,64 * i + 64,64 * j + 64)
			l.append(img.crop(box))
		mat.append(l)
	return mat
def mean_color(img):
	r,g,b,*_ = img.split()
	r = np.array(r)
	g = np.array(g)
	b = np.array(b)
	r = np.mean(r.flatten())
	g = np.mean(g.flatten())
	b = np.mean(b.flatten())
	return r,g,b
def distance(img1,img2):
	r,g,b = mean_color(img1)
	R,G,B = mean_color(img2)
	dr,dg,db = R - r,G - g,B - b
	return np.sqrt(dr ** 2 + dg ** 2 + db ** 2)
def choose(imglist,img):
	mindist = 500
	minImage = None
	for i in imglist:
		dist = distance(i,img)
		if(dist < mindist):
			mindist = dist
			minImage = i
	return minImage
def process(imgList,img,w,h):
	mat = split(img,w,h)
	res = []
	for i in mat:
		l = []
		for j in i:
			l.append(choose(imgList,j))
		res.append(l)
	return make(res)
def main():
	wh = input('how many images you want to fill the width and height?(w h):').strip()
	path = input('please input the directory you save the filling images:').strip()
	path_ori = input('please input the original image path:').strip()
	path_save = input('please input the path you want to save the image:').strip()
	h,w = wh.split(' ')
	w,h = int(w),int(h)
	imgList = []
	for i in os.listdir(path):
		try:
			i = os.path.join(path,i)
			img = Image.open(i)
			imgList.append(img)
		except:
			pass
	img = Image.open(path_ori)
	img = img.resize((64 * h,64 * w))
	res = process(imgList,img,w,h)
	res.save(path_save)
if(__name__ == '__main__'):
	main()
