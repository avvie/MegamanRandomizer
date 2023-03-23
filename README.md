# Megaman Randomizer App
This repository contains the code for a very rudimentary Magaman randomizer app. The app was created by a small team of two developers.


![image](https://user-images.githubusercontent.com/10329405/215262462-b48717b5-d942-4d3e-b2e8-aa3b47de9bb8.png)

## Features

Randomizes the megaman pallete
Randomizes what each boss drops at the end of the level

## How to use
- Clone the repository to your local machine
- Navigate to the project directory/Randomizer
- You should add your megaman nes image into the directory/Randomizer. We support the (USA) or (U) release header.
If it wont load, open an issue :)
- Run the app using `python3 MMRando.py`

### Rando current options

| Command | Description |
| --- | --- |
| -h | Displays the help menu in the app |
| -w | Disables randomization of weapons. Enabled by default |
| -p | Disables randomization of megaman pallete. Enabled by default |
| +weakness | Randomizes damage delt to main 6 bosses. Disabled by default |
| +damagetoboss | Randomizes damage dealt to main 6 Robots excluding weaknesses: Default Off|
| +music | Shuffles stage music. Disabled by default |
| Game Patches | --- |
| +stageclear | Mega Man now fires his newly obtained weapon upon clearing a stage. Default: Off|
| +weaknessviz | Marks levels on stage select based on if you have that bosses weakness. Default: Off|
| +weaknessviz | Red for not having it, Green for having it, Black for level completed|
| +roll | Applies Roll-Chan graphics patch (Credit Zynk). Disabled by default |
| -qol | Disables all quality of life changes. |
| -a | Disables ammo refil upon death |
| -b | Disables buff on bomb timer |
| --- | --- |
| -o | Sets the output file path | 
| -i | Sets the input file path | 

### Quality of life Patches bundle
By default we are applying some patches to the randomized image. These include 
- Buffing the bomb timer 
- Refilling ammo on death

## Requirements
Python 3.11.*

## Contributions
We welcome contributions to the project. 
If you would like to contribute, please fork the repository and submit a pull request.

## Attributions
We are using Zynk Oxhyde's art in our test ips file. You can see their romhacking.net profile [here](https://www.romhacking.net/community/2041/)

Here are some resources if you are interested in contributing. [Disassembly](https://bisqwit.iki.fi/jutut/megamansource/)
ZeroSoft for ips file [format specification}(https://zerosoft.zophar.net/ips.php)

## Authors
- [JoJoCrusade](https://github.com/JoJoCrusade) - with whom this would not exist <3

- [avvie](https://github.com/avvie)
## License
This project is licensed under the [CCC3](LICENSE.md).

## Disclaimer
This is a very basic app and is in no way affiliated with the official Magaman franchise.
Please note that the code is not production-ready and is intended for educational purposes only.
