from pypylon import pylon
import cv2

class BaslerCam:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            # Connecting to the first available camera
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
            self.camera.Open()

            # Grabbing Continuously (video) with minimal delay
            self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
            self.converter = pylon.ImageFormatConverter()

            # Converting to OpenCV BGR format
            self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    def show(self):
        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                # Access the image data
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                cv2.namedWindow("img", cv2.WINDOW_NORMAL)
                cv2.imshow("img", img)
                k = cv2.waitKey(1)
                if k == 27:
                    break
            grabResult.Release()
        self.camera.StopGrabbing()
        cv2.destroyAllWindows()

    def getFrame(self):
        if self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                img = image.GetArray()
                grabResult.Release()
                return img
        self.camera.StopGrabbing()
        return None

    def release_camera(self):
        self.camera.StopGrabbing()
        self.camera.Close()


if __name__ == "__main__":
    b = BaslerCam()
    b.show()
