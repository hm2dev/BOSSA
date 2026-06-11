# BOSSA 2.0.0

BOSSA is a flash programming utility for Atmel's SAM family of flash-based ARM microcontrollers.
The motivation behind BOSSA is to create a simple, easy-to-use, open source utility to replace Atmel's SAM-BA software.
BOSSA is an acronym for Basic Open Source SAM-BA Application to reflect that goal.

The software was created by Scott Shumate with contributions from several
[contributors](https://github.com/shumatech/BOSSA/graphs/contributors).

The official [ShumaTech BOSSA Website](https://www.shumatech.com/web/products/bossa) hosts (potentially) outdated documentation.
The source code was first hosted on [Sourceforge](https://sourceforge.net/projects/b-o-s-s-a/) and now resides on [GitHub](https://github.com/shumatech/BOSSA).

[Arduino](https://www.arduino.cc/) forked the original GitHub repository and added support for the Nordic nrf52 controller [Source Code][https://github.com/arduino/BOSSA)].

[hm2dev](https://github.com/hm2dev) forked the Arduino fork and added/documented support for redirecting the communnication over ethernet on the command line [Source Code](https://github.com/hm2dev/BOSSA).

The software is released under the terms of the BSD license as specified in the LICENSE file.

## Usage

BOSSA comes as 

1) BOSSA GUI Application
2) BOSSA Shell (bossah, seemingly no loger part of the latest builds)
3) BOSSA Command Line Utility (bossac)

A (potentially outdated) documentation of all three BOSSA programs can be found at the original [ShumaTech BOSSA Website](https://www.shumatech.com/web/products/bossa).

Run `bossac -h` or `bossac --help` for the currently supported list of command line options of the bossac utility.

## Supported Device Families

 * Atmel
   * SAM7S
   * SAM7SE
   * SAM7X
   * SAM7XC
   * SAM3N
   * SAM3S
   * SAM3U
   * SAM4E
   * SAM4S
   * SAMD21
   * SAMD51
   * SAM3X\*
   * SAM3A\*
   * SAM7L\*
   * SAM9XE\*
   * SAMR21\*
   * SAML21\*
   * SAME51\*
   * SAME53\*
   * SAME54\*
   * SAME70\*
   * SAMS70\*
   * SAMV70\*
   * SAMV71\*
* Nordic
   * nrf52 (Support added by [Arduino](https://www.arduino.cc/))
     
In the list above \* used to mark device families which are were tested for each release and could stop working.
In [this, the hm2devBOSSA repo](https://github.com/hm2dev/BOSSA) development is mostly related to a specific project and no other devices are actively tested and supported due to a lack of time and hardware.

If you want support for the other devices, the following paragraphs from the original ShumaTech Readme are kept here for reference:

Do you want to help make sure a device family is tested or do you want to see a new device family added?  Then contribute a development board with a device from that family to the BOSSA project to make it happen. Contact scott at shumatech.com if you are interested in helping the project.

The following individuals and companies graciously provided development boards to assist the BOSSA project.

* Atmel Corporation (SAM3N, SAM3S, SAM3U)
* David Crocker (SAM4E, SAM4S)
* Adafruit Industries (SAMD21, SAMD51)

# Building Bossa

To build only the bossac tool from the sources the following commands can be used.

## Linux build for bossac only

````
sudo apt install -y build-essential
make clean
WX_CONFIG=/bin/false make WX=0 bossac
````

 ## Linux cross build of bossac.exe only for Windows 

````
sudo apt install mingw-w64

cd BOSSA

make clean

WX_CONFIG=/bin/false make OS=MINGW32 WX=0 \
    CC=x86_64-w64-mingw32-gcc \
    CXX=x86_64-w64-mingw32-g++ \
    LDFLAGS="-static" \
    bossac \
    -j8
````

## Tools

BOSSA only supports programming binary files.
To be able to also program intel hex (.hex) files there is a python script `split_hex.py` in the tools folder that is able convert hex to bin files.

Simple conversion could also be done using objcopy from the [GNU binutils package](https://www.gnu.org/software/binutils/).
````
objcopy --input-target=ihex --output-target=binary input.hex output.bin
````
The python script creates separate files for any segments in the hex file.
This means that empty gaps are not part of the resulting bin file(s).
Instead the script provides the corresponding offsets and sizes required for programming the files.

Run it as `python split_hex.py hexfile [alignment] [min_gap]`, where alingment specfifies the alignment to memory boundaries and the min_gap specifies if sections should be threated as one if the gap is small.

The following converts input.hex to binary format, aligns it to 64kiB and also fills any gaps smaller than 64kiB with 0xFF.

````
python split_hex.py input.hex 0x1000 0x1000
````

The script requires the packet `intelhex` to be installed.