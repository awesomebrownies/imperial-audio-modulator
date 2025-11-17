package main

import (
	"fmt"
	"github.com/sstallion/go-hid"
)

func main() {
	fmt.Printf(hid.GetVersionStr())
}
