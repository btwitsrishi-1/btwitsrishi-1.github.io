# AEVY Visualiser - audio source selector (TouchDesigner 2022+)
#
# Drag this file into your network (it becomes a Text DAT), then
# right-click it > Run Script. It finds your Audio Device In CHOP and builds
# an "audio_source" panel next to it with:
#   - Driver / Device dropdowns (two-way bound to the CHOP)
#   - Auto-detect button: picks a "system sound out" capture device
#     (Stereo Mix, VB-Cable, VoiceMeeter, ...)
# On every project start it also auto-detects when the saved device does not
# exist on this machine (e.g. a friend's laptop) or is set to "default".
# Safe to re-run: it replaces the old panel.

# Set to a path like '/project1/audiodevin1' if you have several Audio Device In CHOPs.
TARGET = None

AUTODETECT_CODE = '''
# Device names that capture what the speakers play (Windows has no direct
# loopback in the Audio Device In CHOP, so it needs one of these inputs).
KEYWORDS = ('stereo mix', 'what u hear', 'wave out', 'loopback',
            'cable output', 'voicemeeter out', 'voicemeeter output')

def pick(force=False):
    p = op(parent().par.Chop.eval()).par.device
    current = p.eval()
    if not force and current != 'default' and current in p.menuNames:
        return  # saved device exists on this machine, keep the user's choice
    for name, label in zip(p.menuNames, p.menuLabels):
        if any(k in (name + ' ' + label).lower() for k in KEYWORDS):
            p.val = name
            print('[audio_source] using', label)
            return
    if current not in p.menuNames:
        p.val = 'default'  # saved device is not on this machine
    print('[audio_source] No system-output capture device found. Enable '
          '"Stereo Mix" in Windows Sound settings or install VB-Cable, '
          'then press Auto-detect. Devices seen:', list(p.menuLabels))
'''

chops = [op(TARGET)] if TARGET else root.findChildren(type=audiodeviceinCHOP)
if not chops:
    print('[audio_source] No Audio Device In CHOP found in this project.')
else:
    chop = chops[0]
    if len(chops) > 1:
        print('[audio_source] Several found, using', chop.path,
              '- set TARGET to pick another:', [c.path for c in chops])
    net = chop.parent()
    if net.op('audio_source'):
        net.op('audio_source').destroy()

    panel = net.create(containerCOMP, 'audio_source')
    panel.nodeX, panel.nodeY = chop.nodeX + 200, chop.nodeY
    panel.par.w, panel.par.h = 420, 110
    panel.viewer = True

    page = panel.appendCustomPage('Audio')
    chop_par = page.appendStr('Chop', label='Audio CHOP')[0]
    chop_par.val = chop.path
    chop_par.readOnly = True
    for name, src in (('Driver', 'driver'), ('Device', 'device')):
        p = page.appendMenu(name)[0]
        expr = "op('{}').par.{}".format(chop.path, src)
        p.menuSource = expr
        p.bindExpr = expr
        p.mode = ParMode.BIND
    page.appendPulse('Autodetect', label='Auto-detect Sound Out')

    ui = panel.create(parameterCOMP, 'ui')
    ui.par.op = '..'
    ui.par.builtin = False
    ui.par.custom = True
    ui.par.hmode = 'fill'
    ui.par.vmode = 'fill'

    autodetect = panel.create(textDAT, 'autodetect')
    autodetect.text = AUTODETECT_CODE

    on_pulse = panel.create(parameterexecuteDAT, 'on_autodetect')
    on_pulse.par.op = '..'
    on_pulse.par.pars = 'Autodetect'
    on_pulse.par.valuechange = False
    on_pulse.par.onpulse = True
    on_pulse.text = "def onPulse(par):\n\top('autodetect').module.pick(force=True)\n"

    on_start = panel.create(executeDAT, 'on_start')
    on_start.par.start = True
    on_start.text = "def onStart():\n\top('autodetect').module.pick()\n"

    for i, o in enumerate((ui, autodetect, on_pulse, on_start)):
        o.nodeX, o.nodeY = 0, -150 * i

    autodetect.module.pick()
    print('[audio_source] Panel created at', panel.path, '- save the .toe.')
