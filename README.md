# BOSSA 2.0.0


BOSSA is a flash programming utility for Atmel's SAM family of flash-based ARM microcontrollers.
The motivation behind BOSSA is to create a simple, easy-to-use, open source utility to replace Atmel's SAM-BA software.
BOSSA is an acronym for Basic Open Source SAM-BA Application to reflect that goal.

The software was created by Scott Shumate with contributions from several
[contributors](https://github.com/shumatech/BOSSA/graphs/contributors).

[Arduino](https://www.arduino.cc/) has added support for the Nordic nrf52 controller.

[hm2dev](https://github.com/hm2dev) has added support for redirecting the communnication over ethernet on the command line.

The software is released under the terms of the BSD license as specified in the LICENSE file.

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
   * nrf52 (Support added by [Arduino](https://www.arduino.cc/)
     
## Device families which are not tested for each release and could stop working.

Do you want to help make sure a device family is tested or do you want to see a new device family added?  Then contribute a development board with a device from that family to the BOSSA project to make it happen.  Contact scott at shumatech.com if you are interested in helping the project.

The following individuals and companies graciously provided development boards to assist the BOSSA project.
 * Atmel Corporation (SAM3N, SAM3S, SAM3U)
 * David Crocker (SAM4E, SAM4S)
 * Adafruit Industries (SAMD21, SAMD51)


# Building Bossa

## Linux build for bossac only

````
sudo apt install -y build-essential
make clean
WX_CONFIG=/bin/false make WX=0 bossac

````

 ## Linux cross build of bossac.exe for Windows only

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