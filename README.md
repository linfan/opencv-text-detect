# OpenCV Text Area Detect

Searching text in a image, an opencv based text area detect tool.

## 1. Run on local

### 1.1 Verified environment

- Python 3.6
- OpenCV 3.2
- Tesseract 4.0 Alpha

### 1.2 Preparation

```bash
$ pip3 install opencv-python
$ pip3 install opencv-contrib-python
```

### 1.3 Detect text area only

```bash
$ python3 text_detect_wrap.py /path/to/image.jpg
$ open result.jpg
```

### 1.4 Detect text content

```bash
$ bash text-detect.sh /path/to/image.jpg
```

## 2. Build and run the service via docker


### 2.1 Generate tesseract packages
```bash
$ docker build -t t4cmp tesseract
$ docker run --rm -it -v $(pwd):/pkg t4cmp
```

### 2.2 Download extra packages
```bash
cd pkg
wget http://ftp.us.debian.org/debian/pool/main/l/leptonlib/libleptonica-dev_1.74.1-1_amd64.deb
wget http://ftp.us.debian.org/debian/pool/main/l/leptonlib/liblept5_1.74.1-1_amd64.deb
wget http://ftp.us.debian.org/debian/pool/main/g/giflib/libgif7_5.1.4-0.4_amd64.deb
wget http://ftp.us.debian.org/debian/pool/main/libw/libwebp/libwebp6_0.5.2-1_amd64.deb
wget http://ftp.us.debian.org/debian/pool/main/libj/libjpeg-turbo/libjpeg62-turbo_1.5.1-2_amd64.deb
```

### 2.3 Build service image
```bash
$ docker build -t t4 .
```

### 2.4 Start service
```bash
$ docker run -dt --name t4 -p 5000:5000 t4
```
