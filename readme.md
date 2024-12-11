# MediaPipe Python Api

## Dev

- Make `venv` and activate
- Install requirements
- Run `app.py`

## Api usage

curl -X POST -F "file=@img1.jpeg" \
http://127.0.0.1:5001/detect_face


curl -X POST -F "file=@img2.png" \
http://127.0.0.1:5001/detect_face\?return_image\=true -o out.img2.png


## Use docker

```bash
docker run --rm --name mediapipe -p 5001:5000 vuthaihoc/mediapipe-face-detect-api
```