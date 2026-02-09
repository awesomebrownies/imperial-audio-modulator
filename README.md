The Imperial Audio Modulator routes audio channels with toggle switches and adjusts them using a rotary encoder. Engineered in the silhouette of a TIE-class craft, it communicates over HID on Linux using a compact Go backend.

<p align="center">
  <img src="https://github.com/user-attachments/assets/ff1bc9c6-f030-46c2-b067-bc6daa644821" width="34%" />
  <img src="https://github.com/user-attachments/assets/03c8ee63-c59f-45d6-a167-d88fa54f9fe9" width="30%" />
  <img src="https://github.com/user-attachments/assets/33aec13f-bbc5-4705-b6f0-45871536fb3b" width="50%" />
</p>

<p>
  <img src="https://github.com/user-attachments/assets/ab797b40-a91b-43a2-a2e5-af7b554f7805" width="50%" />
  <a href="https://youtu.be/CjEDwnVIn9c">
    <img src="https://img.youtube.com/vi/CjEDwnVIn9c/0.jpg" width="500">
  </a>
</p>

## Inspiration & Lessons

The idea Imperial-AM is to be an audio controller which has toggle switches for different applications. It's in the form of a tiefighter to give it more character!

After tackling this project, I learned how to properly create tolerances and to always TRIPLE check measurements for each part. This was also my first routed PCB I ever created! As such, I learned all about routing, setting up key matrixes, and setting up working firmware to complete the project.

## Specifications

BOM:

* 6x Cherry MX Switches
* 1x XIAO RP2040
* 6x Blank DSA White Keycaps
* 4x M3x15mm screws
* 4x M3 Nuts
* 3x MTS-101 mini toggle switches [Amazon Link](https://www.amazon.com/MTS-101-Position-Miniature-Toggle-Switch/dp/B0799LBFNY)

Others:

* CircuitPython with KMK for firmware
* Go with go-hid for backend

## Compiling from Source

* Clone this repository to your intended file location
```bash
cd Downloads
git clone https://github.com/awesomebrownies/imperial-audio-modulator
```
* (Installation Step) If you don't have Go installed go ahead and do that at
https://go.dev/doc/install
* Use the compile command inside the backend folder
```bash
cd backend
go build imperial-audio-modulator.go
```

## Backend Setup for Linux

Store the executable at /usr/local/bin/imperial-audio-modulator

After acquiring the go executable, you will set up a systemd user service.

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/imperial-audio-modulator.service
```

```ini
[Unit]
Description=Imperial Audio Modulator
After=pipewire.service wireplumber.service

[Service]
ExecStart=/usr/local/bin/imperial-audio-modulator
Restart=always
Environment=XDG_RUNTIME_DIR=/run/use/%U
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%U/bus

[Install]
WantedBy=default.target
```

```
systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user enable imperial-audio-modulator
systemctl --user start imperial-audio-modulator
```

You're all set up now!
