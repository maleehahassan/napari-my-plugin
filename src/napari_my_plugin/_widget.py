"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget
from napari.types import ImageData

if TYPE_CHECKING:
    import napari


class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Click me!")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")


@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")


# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
from napari.types import ImageData, LayerDataTuple

def segment_image2(image: ImageData) -> LayerDataTuple:
    """Apply thresholding and connected component analysis"""
    from skimage.filters import threshold_otsu
    from skimage.measure import label
    
    binary = image > threshold_otsu(image)
    label_image = label(binary)
    
    output_tuple = (label_image, # first parameter of the tuple: data
                    {'name': 'Output Label Image', 'opacity': 0.3}, # second parameter of the tuple: layer properties
                    'labels') # third parameter of the tuple: layer type
    
    return output_tuple