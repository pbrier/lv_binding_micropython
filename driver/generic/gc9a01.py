"""Generic ILI9xxx drivers.

This code is licensed under MIT license.

Adapted from:
    https://github.com/rdagger/micropython-ili9341

The following code snippet will instantiate the driver and
automatically register it to lvgl. Adjust the SPI bus and
pin configurations to match your hardware setup::

    from gc9a01 import GC9A01
    from machine import SPI, Pin
    spi = SPI(0, baudrate=24_000_000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    drv = GC9A01(spi=spi, dc=15, cs=17, rst=14)
"""
from micropython import const

import st77xx

# Command constants from ILI9341 datasheet
_NOP = const(0x00)  # No-op
_SWRESET = const(0x01)  # Software reset
_RDDID = const(0x04)  # Read display ID info
_RDDST = const(0x09)  # Read display status
_SLPIN = const(0x10)  # Enter sleep mode
_SLPOUT = const(0x11)  # Exit sleep mode
_PTLON = const(0x12)  # Partial mode on
_NORON = const(0x13)  # Normal display mode on
_RDMODE = const(0x0A)  # Read display power mode
_RDMADCTL = const(0x0B)  # Read display MADCTL
_RDPIXFMT = const(0x0C)  # Read display pixel format
_RDIMGFMT = const(0x0D)  # Read display image format
_RDSELFDIAG = const(0x0F)  # Read display self-diagnostic
_INVOFF = const(0x20)  # Display inversion off
_INVON = const(0x21)  # Display inversion on
_GAMMASET = const(0x26)  # Gamma set
_DISPLAY_OFF = const(0x28)  # Display off
_DISPLAY_ON = const(0x29)  # Display on
_SET_COLUMN = const(0x2A)  # Column address set
_SET_PAGE = const(0x2B)  # Page address set
_WRITE_RAM = const(0x2C)  # Memory write
_READ_RAM = const(0x2E)  # Memory read
_PTLAR = const(0x30)  # Partial area
_VSCRDEF = const(0x33)  # Vertical scrolling definition
_MADCTL = const(0x36)  # Memory access control
_VSCRSADD = const(0x37)  # Vertical scrolling start address
_PIXFMT = const(0x3A)  # COLMOD: Pixel format set
_WRITE_DISPLAY_BRIGHTNESS = const(0x51)  # Brightness hardware dependent!
_READ_DISPLAY_BRIGHTNESS = const(0x52)
_WRITE_CTRL_DISPLAY = const(0x53)
_READ_CTRL_DISPLAY = const(0x54)
_WRITE_CABC = const(0x55)  # Write Content Adaptive Brightness Control
_READ_CABC = const(0x56)  # Read Content Adaptive Brightness Control
_WRITE_CABC_MINIMUM = const(0x5E)  # Write CABC Minimum Brightness
_READ_CABC_MINIMUM = const(0x5F)  # Read CABC Minimum Brightness
_FRMCTR1 = const(0xB1)  # Frame rate control (In normal mode/full colors)
_FRMCTR2 = const(0xB2)  # Frame rate control (In idle mode/8 colors)
_FRMCTR3 = const(0xB3)  # Frame rate control (In partial mode/full colors)
_INVCTR = const(0xB4)  # Display inversion control
_DFUNCTR = const(0xB6)  # Display function control
_PWCTR1 = const(0xC0)  # Power control 1
_PWCTR2 = const(0xC1)  # Power control 2
_PWCTRA = const(0xCB)  # Power control A
_PWCTRB = const(0xCF)  # Power control B
_VMCTR1 = const(0xC5)  # VCOM control 1
_VMCTR2 = const(0xC7)  # VCOM control 2
_RDID1 = const(0xDA)  # Read ID 1
_RDID2 = const(0xDB)  # Read ID 2
_RDID3 = const(0xDC)  # Read ID 3
_RDID4 = const(0xDD)  # Read ID 4
_GMCTRP1 = const(0xE0)  # Positive gamma correction
_GMCTRN1 = const(0xE1)  # Negative gamma correction
_DTCA = const(0xE8)  # Driver timing control A
_DTCB = const(0xEA)  # Driver timing control B
_POSC = const(0xED)  # Power on sequence control
_ENABLE3G = const(0xF2)  # Enable 3 gamma control
_PUMPRC = const(0xF7)  # Pump ratio control

_MADCTL_MY = const(0x80)  # page address order (0: top to bottom; 1: bottom to top)
_MADCTL_MX = const(0x40)  # column address order (0: left to right; 1: right to left)
_MADCTL_MV = const(0x20)  # page/column order (0: normal mode 1; reverse mode)
_MADCTL_ML = const(
    0x10
)  # line address order (0: refresh to to bottom; 1: refresh bottom to top)
_MADCTL_BGR = const(0x08)  # colors are BGR (not RGB)
_MADCTL_RTL = const(0x04)  # refresh right to left

_MADCTL_ROTS = (
    const(_MADCTL_MX),  # 0 = portrait
    const(_MADCTL_MV),  # 1 = landscape
    const(_MADCTL_MY),  # 2 = inverted portrait
    const(_MADCTL_MX | _MADCTL_MY | _MADCTL_MV),  # 3 = inverted landscape
)

ILI9XXX_PORTRAIT = st77xx.ST77XX_PORTRAIT
ILI9XXX_LANDSCAPE = st77xx.ST77XX_LANDSCAPE
ILI9XXX_INV_PORTRAIT = st77xx.ST77XX_INV_PORTRAIT
ILI9XXX_INV_LANDSCAPE = st77xx.ST77XX_INV_LANDSCAPE


class GC9A01_hw(st77xx.St77xx_hw):
    def __init__(self, **kw):
        """ILI9341 TFT Display Driver.

        Requires ``LV_COLOR_DEPTH=16`` when building lv_micropython to function.
        """
        super().__init__(
            res=(240, 240),
            suppRes=[
                (240, 240),
            ],
            model=None,
            suppModel=None,
            bgr=False,
            **kw,
        )

    def config_hw(self):
        self._run_seq( [
            ( 0xEF,  bytes([0])),
            ( 0xEB,  bytes([0x14])),
            ( 0xFE,  bytes([0])),
            ( 0xEF,  bytes([0])),
            ( 0xEB,  bytes([0x14])),
            ( 0x84,  bytes([0x40])),
            ( 0x85,  bytes([0xFF])),
            ( 0x86,  bytes([0xFF])),
            ( 0x87,  bytes([0xFF])),
            ( 0x88,  bytes([0x0A])),
            ( 0x89,  bytes([0x21])),
            ( 0x8A,  bytes([0x00])),
            ( 0x8B,  bytes([0x80])),
            ( 0x8C,  bytes([0x01])),
            ( 0x8D,  bytes([0x01])),
            ( 0x8E,  bytes([0xFF])),
            ( 0x8F,  bytes([0xFF])),
            ( 0xB6,  bytes([0x00, 0x00])), 
            ( 0x36,  bytes([0x48])),
            ( self.rot,  bytes([0])),
            ( 0x3A,  bytes([0x05])),
            ( 0x90,  bytes([0x08, 0x08, 0x08, 0x08])),
            ( 0xBD,  bytes([0x06])),
            ( 0xBC,  bytes([0x00])),
            ( 0xFF,  bytes([0x60, 0x01, 0x04])),
            ( 0xC3,  bytes([0x13])),
            ( 0xC4,  bytes([0x13])),
            ( 0xC9,  bytes([0x22])),
            ( 0xBE,  bytes([0x11])),
            ( 0xE1,  bytes([0x10, 0x0E])),
            ( 0xDF,  bytes([0x21, 0x0c, 0x02])),
            ( 0xF0,  bytes([0x45, 0x09, 0x08, 0x08, 0x26, 0x2A])),
            ( 0xF1,  bytes([0x43, 0x70, 0x72, 0x36, 0x37, 0x6F])),
            ( 0xF2,  bytes([0x45, 0x09, 0x08, 0x08, 0x26, 0x2A])),
            ( 0xF3,  bytes([0x43, 0x70, 0x72, 0x36, 0x37, 0x6F])),
            ( 0xED,  bytes([0x1B, 0x0B])),
            ( 0xAE,  bytes([0x77])),
            ( 0xCD,  bytes([0x63])),
            ( 0x70,  bytes([0x07, 0x07, 0x04, 0x0E, 0x0F, 0x09, 0x07, 0x08, 0x03])),
            ( 0xE8,  bytes([0x34])),
            ( 0x62,  bytes([0x18, 0x0D, 0x71, 0xED, 0x70, 0x70, 0x18, 0x0F, 0x71, 0xEF, 0x70, 0x70])),
            ( 0x63,  bytes([0x18, 0x11, 0x71, 0xF1, 0x70, 0x70, 0x18, 0x13, 0x71, 0xF3, 0x70, 0x70])),
            ( 0x64,  bytes([0x28, 0x29, 0xF1, 0x01, 0xF1, 0x00, 0x07])),
            ( 0x66,  bytes([0x3C, 0x00, 0xCD, 0x67, 0x45, 0x45, 0x10, 0x00, 0x00, 0x00])),
            ( 0x67,  bytes([0x00, 0x3C, 0x00, 0x00, 0x00, 0x01, 0x54, 0x10, 0x32, 0x98])),
            ( 0x74,  bytes([0x10, 0x85, 0x80, 0x00, 0x00, 0x4E, 0x00])),
            ( 0x98,  bytes([0x3e, 0x07])),
            ( 0x35,  bytes([0])),
            ( 0x21,  bytes([0])),
            ( 0x11,  bytes([0]), 20),
            ( 0x29,  bytes([0]), 120)
        ])

       
    def apply_rotation(self, rot):
        self.rot = rot
        if (self.rot % 2) == 0:
            self.width, self.height = self.res
        else:
            self.height, self.width = self.res
        self.write_register(
            _MADCTL,
            bytes([_MADCTL_BGR | _MADCTL_ROTS[self.rot % 4]]),
        )


class GC9A01(GC9A01_hw, st77xx.St77xx_lvgl):
    def __init__(self, doublebuffer=True, factor=4, **kw):
        """See :obj:`Ili9341_hw` for the meaning of the parameters."""
        import lvgl as lv

        GC9A01_hw.__init__(self, **kw)
        st77xx.St77xx_lvgl.__init__(self, doublebuffer, factor)
