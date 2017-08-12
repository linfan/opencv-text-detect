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
$ python3 text_detect_wrap.py /path/to/image.jpg [out-put-folder]
$ open result.jpg   # or out-put-folder/result.jpg
```

### 1.4 Detect text content

```bash
$ bash text-detect.sh /path/to/image.jpg [out-put-folder]
$ cat /path/to/image/result.trim.txt   # or out-put-folder/result.trim.txt
```

## 2. Build and run the service via docker


### 2.1 Generate tesseract packages
```bash
$ docker build -t t4-pkg -f docker/Dockerfile.pkg docker
$ docker run --rm -it -v $(pwd)/docker:/pkg t4-pkg
```

### 2.2 Build base image
```bash
$ docker build -t t4-base -f docker/Dockerfile.base docker
```

### 2.3 Build service image
```bash
$ docker build -t t4 .
```

### 2.4 Start service
```bash
$ docker run -dt --name t4 -p 5000:5000 t4
```

### 2.5 View detect result in browser

URL: `http://<IP>:5000/detect/<url-of-an-image-to-detect>`
