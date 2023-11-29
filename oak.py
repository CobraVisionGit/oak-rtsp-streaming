import depthai as dai

class Oak():
  def __init__(self, fps):
    self.pipeline = dai.Pipeline()
    self.device_infos = dai.Device.getAllAvailableDevices()
    self.colorCam = self.pipeline.create(dai.node.ColorCamera)
    self.videnc = self.pipeline.create(dai.node.VideoEncoder)
    self.veOut = self.pipeline.create(dai.node.XLinkOut)
    self.fps = fps

    self._create_color_cam()
    self._create_encoder()

  def _create_color_cam(self):
    self.colorCam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    self.colorCam.setInterleaved(False)
    self.colorCam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
    self.colorCam.setFps(self.fps)
  
  def _create_encoder(self):
    self.videnc.setDefaultProfilePreset(self.fps, dai.VideoEncoderProperties.Profile.H265_MAIN)
    self.colorCam.video.link(self.videnc.input)
    self.veOut.setStreamName("encoded")
    self.videnc.bitstream.link(self.veOut.input)
    
  def get_pipeline(self):
    return self.pipeline
  
  def get_device_info(self):
    return self.device_infos

  def get_device_state(self):
    pass

