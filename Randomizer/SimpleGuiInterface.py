import os.path

import PySimpleGUI as sg

use_custom_titlebar = True if sg.running_trinket() else False

NAME_SIZE = 23


def name(_name):
    dots = NAME_SIZE - len(_name) - 2
    return sg.Text(_name + ' ' + '•' * dots, size=(NAME_SIZE, 1), justification='r', pad=(0, 0), font='Courier 10')

inStr = ""
outStr = ""
inKey = "In"
outKey = "In"

layout = [
    [sg.Text("Megaman Randomizer")],
    [sg.Text(inStr), sg.FileBrowse("Browse Input File", key=inKey)],
    [sg.Text(outStr)],
    [sg.Text("Randomization Options")],
    [sg.Checkbox('Weapon Rando', default=True)],
    [sg.Checkbox('Palette Rand', default=True)],
    [sg.Checkbox('Main boss weakness Rando', default=False)],
    [sg.Checkbox('Music Rando', default=False)],
    [sg.Text("Patches ")],
    [sg.Checkbox('Stage clear weapon fire', default=False)],
    [sg.Checkbox('Mark stage with weakness', default=False)],
    [sg.Checkbox('Disables all quality of life changes.', default=False)],
    [sg.Checkbox('Disables all quality of life changes', default=False)],
    [sg.Checkbox('Disables ammo refill upon death', default=False)],
    [sg.Checkbox('Applies Roll-Chan graphics patch (Credit Zynk)', default=False)],
    [sg.Button("Generate!")]
]

# Create the window
window = sg.Window("Megaman Randomizer", layout)

# Create an event loop
while True:
    event, values = window.read()
    if values.has_key("In"):
        inStr = values[inKey]
        outStr = os.path.join(os.path.dirname(inStr), "generatedImage.nes")
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()
