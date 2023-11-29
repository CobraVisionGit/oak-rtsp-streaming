import threading
# import gst
from oak import Oak
from constants import SERVER_PORT, SERVER_ADDRESS


import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GLib

# Gst.init()

class RtspSystem(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(RtspSystem, self).__init__(**properties)
        self.data = None
        # factory.set_launch('videotestsrc is-live=1 ! video/x-raw,width=320,height=240,framerate=30/1 ! nvvidconv ! nvv4l2h264enc insert-sps-pps=1 idrinterval=30 insert-vui=1 ! rtph264pay name=pay0 pt=96 )')
        # self.launch_string = '(videotestsrc is-live=1 ! video/x-h264,width=320,height=240,framerate=30/1 ! insert-sps-pps=1 idrinterval=30 insert-vui=1 ! rtph264pay name=pay0 pt=96 )'
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ! h265parse ! rtph265pay name=pay0 config-interval=1 name=pay0 pt=96'
        # self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ! h264parse ! rtph264pay name=pay0 config-interval=1 name=pay0 pt=96'
        # self.launch_string = 'appsrc name=source ! capsfilter name=m_capsfilter ! videoconvert ! x265enc ! h265parse ! rtph265pay config-interval=1 ! udpsink name=m_udpsink'
        # self.launch_string = 'appsrc name=source ! capsfilter name=m_capsfilter ! videoconvert ! -l h264parse ! rtph264pay config-interval=1 ! udpsink name=m_udpsink'

    def send_data(self, data):
        self.data = data
        # print(self.data)

    def start(self):
        t = threading.Thread(target=self._thread_rtsp)
        t.start()

    def _thread_rtsp(self):
        loop = GLib.MainLoop()
        loop.run()

    def on_need_data(self, src, length):
        if self.data is not None:
            retval = src.emit('push-buffer', Gst.Buffer.new_wrapped(self.data.tobytes()))
            if retval != Gst.FlowReturn.OK:
                print(retval)

    # def do_create_element(self, url):
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)

    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)

class AuthSystem(GstRtspServer.RTSPAuth):
    def __init__(self, **properties):
        super(AuthSystem, self).__init__(**properties)
        # self.new()
        # print(self.new())
    


class RTSPServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(RTSPServer, self).__init__(**properties)
        self.rtsp = RtspSystem()
        # self.auth = AuthSystem()
        self.rtsp.set_shared(True)
        self.create_source()
        # self.create_socket()
        self.set_address(SERVER_ADDRESS)
        self.set_service(SERVER_PORT)
        # self.set_auth(auth=self.auth)
        self.get_mount_points().add_factory("/preview", self.rtsp)

        self.attach(None)
        Gst.init(None)
        
        # print(self.get_address())
        # print(self.get_bound_port())
        # print(self.get_mount_points())
        self.rtsp.start()

    def send_data(self, data):
        self.rtsp.send_data(data)
        # print(data)
    def get_stream_info(self):
        return {"ip": self.get_address(), "port": self.get_bound_port(), "auth": self.get_auth(), "session pool": self.get_session_pool, "thread pool": self.get_thread_pool}

if __name__ == "__main__":
    import depthai as dai

    server = RTSPServer()
    # ip, port, auth = server.get_stream_info()
    stream_info = server.get_stream_info()
    print(stream_info)
    
    # print(ip, port, auth)

    oak = Oak(fps=20)
    pipeline = oak.get_pipeline()
    device_infos = oak.get_device_info()

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
        print(f"Setup finished, RTSP stream available under \"rtsp://{stream_info['ip']}:{stream_info['port']}/preview\"")
        while True:
            data = encoded.get().getData()
            # print(data)
            server.send_data(data)
