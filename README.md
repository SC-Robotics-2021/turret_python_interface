# Turret python interface

This python library provides a programmatic interface to the [turret monitor firmware](https://github.com/SC-Robotics-2021/turret_monitor_firmware/blob/feature/output/book_src/interface.md).

The aim is to provide a pythonic interface for interacting with this device.


## Example usage
```py
from turret_python_interface.interface import Interface

from pathlib import Path

# Assuming a RPi is the host running this code,
# and that the builtin USART header is to be used.
serial_path = Path(r'/') / "dev" / "ttyS0"

with Interface(serial_path=serial_path, baud=115200, timeout=5) as iface:
    # NOTE: Thread-blocking call.
    print(iface.get_telemetry())
```