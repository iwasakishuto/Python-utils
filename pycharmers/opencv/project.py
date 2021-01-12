#coding: utf-8
import os
import cv2
import numpy as np

from . import cvui
from ._path import PYCHARMERS_OPENCV_VIDEO_DIR
from .editing import resize_aspect
from .video_image_handler import VideoCaptureCreate
from ..utils.generic_utils import now_str
from ..utils.subprocess_utils import get_monitor_size
from ..utils._colorings import toBLUE
from ..__meta__ import __project_name__

class cv2Project():
    """OpenCV project wrapper with useful GUI tools.

    Args:
        args (Namespace) : Simple object for storing attributes. ()

    Notes:
        * Image object ( ``np.ndarray`` ) has the shape ( ``height`` , ``width`` , ``channel`` )
        * ``XXX_size`` attributes are formatted as ( ``width`` , ``height`` )

    Attributes:        
        cap (VideoCapture)      : VideoCapture (mimic) object. See :meth:`VideoCaptureCreate <pycharmers.opencv.video_image_handler.VideoCaptureCreate>`
        monitor (np.ndarray)    : Background image. shape= ( ``monitor_height`` , ``monitor_width``, 3)
        monitor_height          : The height of monitor.
        monitor_width           : The width of monitor.
        original_height (int)   : The height of original frame.
        original_width (int)    : The width of original frame.
        frame_height (int)      : The height of resized frame.
        frame_width (int)       : The width of resized frame.
        frame_dsize (tuple)     : ( ``frame_width`` , ``frame_height`` )
        frame_halfsize (tuple)  : ( ``frame_width//2`` , ``frame_height//2`` )
        gui_x (int)             : ``frame_width`` + ``gui_margin``
        fps (int)               : Frame per seconds.
        video (cv2.VideoWriter) : Video Writer.
        video_fn (str)          : The file name of video.

    OtherAttributes:
        See :py:class:`cv2ArgumentParser <pycharmers.utils.argparse_utils.cv2ArgumentParser>` .
    """
    def __init__(self, args, **kwargs):
        self.__dict__.update(args.__dict__)
        self.__dict__.update(kwargs)
        self.init()

    def init(self):
        """Initialize VideoCapture (mimic) object and GUI tools.

        Notes: To run this method, ``self`` must be has these attributes.

            * winname (str)                     : Window name.
            * path (str)                        : Path to video or image.
            * cam (int)                         : The ID of the web camera.
            * ext (str)                         : The extension for saved image.
            * gui_width (int)                   : The width of the GUI tools.
            * gui_margin (int)                  : The margin of GUI control tools.
            * monitor_size (ListParamProcessor) : Monitor size. ( ``width`` , ``height`` )
            * autofit (bool)                    : Whether to fit display size to window size.
            * twitter (bool)                    : Whether you want to run for tweet. ( ``display_size`` will be () )
            * capture (bool)                    : Whether you want to save as video.
        """
        cap = VideoCaptureCreate(path=self.path, cam=self.cam)
        if self.autofit:
            monitor_width, monitor_height = get_monitor_size()
        elif self.twitter:
            monitor_width, monitor_height = (1300, 733)
        else:
            monitor_width, monitor_height = self.monitor_size
        monitor = np.zeros(shape=(monitor_height, monitor_width, 3), dtype=np.uint8)
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        original_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height, frame_width = resize_aspect(src=np.zeros(shape=(original_height, original_width, 1), dtype=np.uint8), dsize=(monitor_width-self.gui_width, monitor_height)).shape[:2]
        frame_dsize    = (frame_width,    frame_height)
        frame_halfsize = (frame_width//2, frame_height//2)
        gui_x = frame_width + self.gui_margin
        fps = cap.get(cv2.CAP_PROP_FPS)
        video_path = now_str()+".mp4"
        video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc('m','p','4','v'), fps, (monitor_width, monitor_height))
        cvui.init(self.winname)
        cv2.moveWindow(winname=self.winname, x=0, y=0)

        defined_args = locals(); defined_args.pop("self")
        self.__dict__.update(defined_args)

    def wrap(self, func):
        """Wrap the function.

        Args:
            func (function) : A function that receives and returns ``frame``.
        """
        params = self.__dict__
        while (True):
            self.monitor[:] = (49, 52, 49)
            ret, frame = self.cap.read()
            if not ret: break
            frame = func(frame=frame, **params)
            if cvui.button(where=self.monitor, x=self.gui_x, y=self.frame_height-155, label="&Stop" if self.capture else "&Capture" ): 
                self.capture = not self.capture
            if cvui.button(where=self.monitor, x=self.gui_x, y=self.frame_height-120, label="&Quit"): 
                break
            if cvui.button(where=self.monitor, x=self.gui_x, y=self.frame_height-85, label="&Save"): 
                filename = now_str() + self.ext
                cv2.imwrite(filename=filename, img=frame)
                cv2.imshow(winname=filename, mat=resize_aspect(cv2.imread(filename), dsize=self.frame_halfsize))
                print(f"Saved {toBLUE(filename)}")
            if cvui.button(where=self.monitor, x=self.gui_x, y=self.frame_height-50, label="&FullScreen"):
                cv2.setWindowProperty(
                    winname=self.winname,
                    prop_id=cv2.WND_PROP_FULLSCREEN,
                    prop_value=1-cv2.getWindowProperty(
                        winname=self.winname,
                        prop_id=cv2.WND_PROP_FULLSCREEN,
                    )
                )
            cvui.text(where=self.monitor, x=self.gui_x, y=self.frame_height-20, text=__project_name__)

            cvui.beginRow(where=self.monitor, x=0, y=0)
            cvui.image(image=cv2.resize(src=frame, dsize=self.frame_dsize))
            cvui.endRow()

            cvui.update()
            cv2.imshow(self.winname, self.monitor)
            if self.capture:
                self.video.write(self.monitor)
            if cv2.waitKey(1) == cvui.ESCAPE:
                break
        self.release()

    def release(self):
        """Do the necessary processing at the end"""
        cv2.destroyAllWindows()
        self.cap.release()
        if os.path.getsize(self.video_path) <= 1000:
            os.remove(self.video_path)
            print(f"Deleted {toBLUE(self.video_path)}")
        else:
            print(f"Deleted {toBLUE(self.video_path)}")
