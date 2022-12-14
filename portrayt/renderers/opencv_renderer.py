from pathlib import Path

from portrayt.renderers import BaseRenderer

try:
    import cv2
except ImportError:
    pass


class OpenCVRenderer(BaseRenderer):
    def _render(self, image_path: Path) -> None:
        image_bgr = cv2.imread(str(image_path))

        # For some godawful reason, if this isn't called each render then gnome freezes up...
        # Since this renderer is entirely for testing purposes, it'll do.
        cv2.destroyAllWindows()

        # Render the image
        cv2.imshow("Portrayt", image_bgr)
        cv2.waitKey(500)
