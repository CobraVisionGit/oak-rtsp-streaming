# oak-rtsp-streaming

The oak-rtsp-streaming project is meant to create a means for users to connect to and ingest the live streams from deployed oak cameras. It allows for users to monitor 
in their sites in real time. This is especially useful for users who have pre-existing VMS software who are looking to integrate oak camera streams for monitoring purposes. 

This main function of the project instantiates an rtsp streaming server utilizing gstreamer backend. The script connects to an oak device and feeds the encoded frames into the rtsp server. 
The stream can be configured to generate multiple stream types both h264 and h265 encoding has been tested. Once the camera and the server has been initialized the rtsp stream is setup
can be consumed remotely.

## Project Structure

```
├── constants.py             basic config file for setting stream IP and port
├── instructions.txt         
├── oak.py                   helper class for initializing Oak Camera
├── README.md
├── requirements.txt         
├── rtsp-server.py           main file to generate rtsp stream
├── rtsp_viewer.py           utility file to view and monitor stream
└── tests
    ├── gst_test.py
    └── oak_data_test.py
```

## Installation

### Gstreamer System Dependencies
```
sudo apt-get install ffmpeg gstreamer-1.0 gir1.2-gst-rtsp-server-1.0 libgirepository1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-plugins-good gstreamer1.0-plugins-base
```

### Pycario System Dependencies
```
sudo apt install libcairo2-dev pkg-config python3-dev
```
### Python Dependencies
```
python3 -m venv /path/to/env
source /path/to/env/bin/activate
python3 -m pip install -r requirements.txt
```

### Start RTSP Server

Start the RTSP server by running:

```
python3 rtsp-server.py
```

### View RTSP Stream

To view the stream you can run:
```
python3 rtsp_viewer.py
```
or using ffplay from ffmpeg:
```
ffplay -fflags nobuffer -fflags discardcorrupt -flags low_delay -framedrop rtsp://{IP}:{port}/preview

ffplay -fflags discardcorrupt -framedrop rtsp://{IP}:{port}/preview
```

### Sources
Script was built off an old demo provided by Luxonis:

Original script source: https://github.com/luxonis/depthai-experiments/tree/master/gen2-rtsp-streaming
