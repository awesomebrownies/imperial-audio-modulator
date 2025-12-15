package main

import (
	"fmt"
	"log"
	"os/exec"
	"time"

	"github.com/sstallion/go-hid"
)

const (
	VID           = 0x2886
	PID           = 0x0042
	TOGGLE_REPORT = 0x10
	USAGE_PAGE    = 0xFF00 // Vendor-defined usage page
	USAGE         = 0x10   // Our custom usage
)

func main() {
	if err := hid.Init(); err != nil {
		log.Fatal(err)
	}
	defer hid.Exit()

	for {
		var targetDevice *hid.DeviceInfo

		err := hid.Enumerate(VID, PID, func(info *hid.DeviceInfo) error {
			fmt.Printf("%s: ID %04x:%04x Usage:%04x UsagePage:%04x %s %s\n",
				info.Path,
				info.VendorID,
				info.ProductID,
				info.Usage,
				info.UsagePage,
				info.MfrStr,
				info.ProductStr)

			if info.UsagePage == USAGE_PAGE && info.Usage == USAGE {
				targetDevice = info
			}
			return nil
		})

		if err != nil {
			log.Println("HID enumerate error:", err)
			time.Sleep(time.Second)
			continue
		}

		if targetDevice == nil {
			time.Sleep(time.Second)
			continue
		}

		dev, err := hid.OpenPath(targetDevice.Path)
		if err != nil {
			log.Println("Failed to open device:", err)
			time.Sleep(time.Second)
			continue
		}

		fmt.Println("Connected to toggle device")

		lastState := byte(0xFF)

		for {
			buf := make([]byte, 2)
			n, err := dev.Read(buf)
			if err != nil {
				fmt.Println("Device disconnected")
				dev.Close()
				break // go back to enumeration loop
			}

			if n < 2 || buf[0] != TOGGLE_REPORT {
				continue
			}

			state := buf[1]
			switch state {
			case 0b10000000:
				fmt.Println("Mute Toggle Pressed")
			case 0b11000001:
				volume(lastState, "+")
			case 0b11000000:
				volume(lastState, "-")
			default:
				if state != lastState {
					handleToggleChange(lastState, state)
					lastState = state
				}
			}
		}

		time.Sleep(time.Second)
	}
}

func volume(state byte, direction string) {
	if (state>>0)&1 == 1 {
		cmd := fmt.Sprintf("wpctl set-volume \"$(wpctl status | awk '/Streams:/ {f=1} f && /spotify/ {print $1; exit}')\" 0.05%s", direction)
		exec.Command("sh", "-c", cmd).Output()
	}
	if (state>>1)&1 == 1 {
		cmd := fmt.Sprintf("wpctl set-volume \"$(wpctl status | awk '/Streams:/ {f=1} f && /Firefox/ {print $1; exit}')\" 0.05%s", direction)
		exec.Command("sh", "-c", cmd).Output()
		cmd = fmt.Sprintf("wpctl set-volume \"$(wpctl status | awk '/Streams:/ {f=1} f && /Discord/ {print $1; exit}')\" 0.05%s", direction)
		exec.Command("sh", "-c", cmd).Output()
	}
	if (state>>2)&1 == 1 {
		cmd := fmt.Sprintf("wpctl set-volume \"$(wpctl status | awk '/Streams:/ {f=1} f && /java/ {print $1; exit}')\" 0.05%s", direction)
		exec.Command("sh", "-c", cmd).Output()
	}
}

func handleToggleChange(old, new byte) {
	for i := 0; i < 3; i++ {
		oldOn := (old>>i)&1 == 1
		newOn := (new>>i)&1 == 1
		if oldOn != newOn {
			if newOn {
				onToggleEnabled(i)
			} else {
				onToggleDisabled(i)
			}
		}
	}
}

func onToggleEnabled(i int) {
	fmt.Println("Toggle", i, "ENABLED")
}

func onToggleDisabled(i int) {
	fmt.Println("Toggle", i, "DISABLED")
}
