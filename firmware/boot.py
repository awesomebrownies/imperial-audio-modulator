import usb_hid

# Custom HID descriptor for toggle switches
TOGGLE_REPORT_DESCRIPTOR = bytes((
    0x06, 0x00, 0xFF,  # Usage Page (Vendor Defined)
    0x09, 0x10,        # Usage (0x10)
    0xA1, 0x01,        # Collection (Application)
    0x85, 0x10,        #   Report ID (16)
    0x09, 0x01,        #   Usage (Vendor Usage 1)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0xFF,        #   Logical Maximum (255)
    0x75, 0x08,        #   Report Size (8 bits)
    0x95, 0x01,        #   Report Count (1)
    0x81, 0x02,        #   Input (Data, Variable, Absolute)
    0xC0,              # End Collection
))

toggle_device = usb_hid.Device(
    report_descriptor=TOGGLE_REPORT_DESCRIPTOR,
    usage_page=0xFF00,
    usage=0x10,
    report_ids=(0x10,),
    in_report_lengths=(1,),
    out_report_lengths=(0,),
)

# Enable keyboard, mouse, consumer control, and custom toggle device
usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     usb_hid.Device.CONSUMER_CONTROL,
     toggle_device)
)