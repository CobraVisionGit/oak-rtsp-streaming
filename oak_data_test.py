import depthai as dai



pipeline = dai.Pipeline()

FPS = 30
colorCam = pipeline.create(dai.node.ColorCamera)
colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
colorCam.setInterleaved(False)
colorCam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
colorCam.setFps(FPS)

videnc = pipeline.create(dai.node.VideoEncoder)
videnc.setDefaultProfilePreset(FPS, dai.VideoEncoderProperties.Profile.MJPEG)
colorCam.video.link(videnc.input)

veOut = pipeline.create(dai.node.XLinkOut)
veOut.setStreamName("encoded")
videnc.bitstream.link(veOut.input)

device_infos = dai.Device.getAllAvailableDevices()
if len(device_infos) == 0:
    raise RuntimeError("No DepthAI device found!")
else:
    print("Available devices:")
    for i, info in enumerate(device_infos):
        print(f"[{i}] {info.getMxId()} [{info.state.name}]")
    if len(device_infos) == 1:
        device_info = device_infos[0]
    else:
        val = input("Which DepthAI Device you want to use: ")
        try:
            device_info = device_infos[int(val)]
        except:
            raise ValueError("Incorrect value supplied: {}".format(val))

if device_info.protocol != dai.XLinkProtocol.X_LINK_USB_VSC:
    print("Running RTSP stream may be unstable due to connection... (protocol: {})".format(device_info.protocol))

with dai.Device(pipeline, device_info) as device:
    encoded = device.getOutputQueue("encoded", maxSize=30, blocking=True)
    print("Setup finished, RTSP stream available under \"rtsp://localhost:8554/preview\"")
    while True:
        data = encoded.get().getData()
        print(data)
        # send = server.send_data(data)
        # print(send)