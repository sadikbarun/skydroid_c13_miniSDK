# skydroid_c13_miniSDK (Unofficial)
Unofficial, reverse-engineered network notes + minimal Python helpers for **Skydroid C13** camera (three-light gimbal version).
> ⚠️ No official SDK/API was found at the time of writing; everything here is based on network observation and may vary by firmware.

## What works (current status)

###  Video
- RGB stream via RTSP (port **554**)
- Thermal stream via RTSP (port **555**)

###  Gimbal / PTZ
- UDP control (port **5000**)
- Several PTZ commands confirmed working (see table below)


### Known PTZ command mapping

These commands were observed to work on at least one C13 firmware.

| Action | Command |
|---|---|
| Gimbal down | `#TPUG2wPTZ026C` |
| Center | `#TPUG2wPTZ056F` |
| Pitch + | `#TPUG2wPTZ0E7F` |
| Pitch − | `#TPUG2wPTZ0F80` |
| Yaw + | `#TPUG2wPTZ106B` |
| Yaw − | `#TPUG2wPTZ116C` |
| Roll + | `#TPUG2wPTZ126D` |
| Roll − | `#TPUG2wPTZ136E` |

###  LRF (Laser Range Finder)
- Hardware may provide range data, but the telemetry channel/format is **not fully decoded** yet.

# Safety & disclaimer 🚨

This is unofficial and reverse-engineered.

Commands may behave differently across firmware/hardware revisions.

Use at your own risk — especially if the camera is mounted on a drone/vehicle.

