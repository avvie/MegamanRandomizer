#Instances of loading Mega Man's classic blue palette
Megaman_Default_Offsets = [0xCB1, 0xCE1, 0xDDD, 0x4CB1, 0x4CE1, 0X4D9B, 0x8CB1, 0x8CE1, 0xCCB1, 0xCCE1, 
0x10CB1, 0x10ce1, 0x14cb1, 0x1D485, 0x1D493, 0x14CE1]

Megaman_WeaponPal_Offset = 0x1D487 # 2 bytes for each color with 7 weapon colors C I B F E G M

WeaponReward = 0x1C148 #Table for rewarding weapons
BossDefeated_Offset = 0x1BFCC  #Table for bosses deafeted

Gutsman_ClearPatch = 0x1B69E # Fixes a cmp call for checking if we beat gutsman

Megaman_Bossroom_PalPatch = [0x1C29B, 0x1C2A0] # Patches hard coded palette values
                                                # First address is 2c, the second is 11

#please name this more concretely
Megaman_Default = [0x2c, 0x11]
