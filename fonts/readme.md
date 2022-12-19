# Creating the PILLOW fonts

The eink weather forecast script uses two fonts for the temperature and pressure.
The script provided uses the fonts VeraSe12 and VeraSe18, but they can be changed.
The following description expects a debian system (i.e. Raspberry Pi).

To create the pillow fonts a two step process has to be performed:
1. Create a BDF font from a OpenType font
2. Create a PIL font from the CDF font

# Prerequisites

The conversion requires the otf2bdf tool. This is installed with the otf2bdf package.
The font VeraSe.ttf is provided by the package ttf-bitstream-vera.

    sudo apt install ttf-bitstream-very otf2bdf

# Converting an TrueType/OpenType font

Find the path to the installed VeraSe OpenType font. In debian it is usually /usr/share/fonts/truetype/ttf-bitstream-vera/VeraSe.ttf

Convert two sizes of 12 and 18 pt:

    otf2bdf /usr/share/fonts/truetype/ttf-bitstream-vera/VeraSe.ttf -p 12 -o VeraSe12.bdf
    otf2bdf /usr/share/fonts/truetype/ttf-bitstream-vera/VeraSe.ttf -p 18 -o VeraSe18.bdf

# Converting the BDF fonts

The BDF font files have to be converted to Pillow fonts. Use the provided python script to perform the conversions:

    python converts.py VeraSe12.bdf
    python converts.py VeraSe18.bdf

