# AEVY Visualiser (TouchDesigner) - notes for Claude

## Comments on the code
- `aevy_audio_source.py` is a one-shot setup script. Run it inside TouchDesigner (Text DAT > Run Script). It builds an `audio_source` panel beside the project's Audio Device In CHOP.
- **Untested inside TouchDesigner.** The `.toe` lives on the user's PC and was not readable from the cloud session. Only the auto-detect logic was tested, against mocks. Parameter names were checked against docs.derivative.ca (`driver`, `device`, `menuSource`, `bindExpr`, `appendMenu`, `appendPulse`, Parameter Execute DAT `onpulse`, Execute DAT `start`).
- Likely cause of "no sound on friend's laptop": the Audio Device In CHOP captures an *input* device only. It cannot record what the speakers play unless the machine has a loopback input (Stereo Mix, VB-Cable, VoiceMeeter). Many laptops ship with Stereo Mix disabled, and the saved device name does not exist on another PC.
- The panel's Driver/Device menus are bound two-way to the CHOP. The Auto-detect button and the on-start check pick a loopback-style device by name keyword, and fall back to `default` if the saved device is missing.
- Assumptions: one Audio Device In CHOP per project (set `TARGET` at the top of the script otherwise), TouchDesigner 2022 or newer.

## Working rules
1. Think before coding: state assumptions, surface tradeoffs, ask when unclear.
2. Simplicity first: minimum code, nothing speculative.
3. Surgical changes: touch only what the request needs; mention unrelated dead code, don't delete it.
4. Goal-driven: define success criteria and verify them.
