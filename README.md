# 0mhz_dosbox

basic convertor for the 0mhz collection to dosbox-x, requires dosbox-x atm for vhd geometry support and dosbox reported version must be at least 7.0

dosbox didn't like device indexes for cdroms so the below is true
`index`
- 0 is `a:`
- 1 is `b:`
- 2 is `c:`
- 4 is `e:`
- 5 is `f:`
- 6 is `g:`

assumptions are made about the devices
- `vhd` is `hdd`
- `chd` is `iso`
- `img` is `floppy`

example run for conversion
```
python3 0mhz_dosbox.py --mgls "/mnt/retrodump/retronas/mister/_DOS Games" --dosbox-base "/mnt/retrodump/retronas/mister/games/AO486"
```

will ignore invalid xml, e.g.
```
Invalid XML: Command & Conquer Red Alert.mgl
Invalid XML: Joe & Mac - Caveman Ninja.mgl
Invalid XML: Command & Conquer.mgl
Invalid XML: Warcraft - Orcs and Humans.mgl
```

will report on games with and `index` < 2, if the game works fine you can ignore this. e.g. Wizardry requires a scenario disk in `A:` but still boots from the VHD on `C:`
```
Game Wizardry IV.mgl has a floppy type image at index 0 if you have trouble booting this may be why
Game Wizardry V.mgl has a floppy type image at index 0 if you have trouble booting this may be why
Game Wizardry III.mgl has a floppy type image at index 0 if you have trouble booting this may be why
Game Wizardry I.mgl has a floppy type image at index 0 if you have trouble booting this may be why
Game Wizardry II.mgl has a floppy type image at index 0 if you have trouble booting this may be why
```

output will be a barebones dosbox config file per game you can load with `-conf`
```
$ cat 0mhz_dosbox/Discworld.conf 
[dos]
ver = 7.0

[autoexec]

imgmount c "/mnt/retrodump/retronas/mister/games/AO486/media/discworld/discworld.vhd" -t hdd
imgmount d "/mnt/retrodump/retronas/mister/games/AO486/media/discworld/discworld.chd" -t iso
boot -l c 
```

Original MisTer `.mgl` contents
```
$ cat Discworld.mgl 
<mistergamedescription>
    <rbf>_computer/ao486</rbf>
    <file delay="0" type="s" index="2" path="media/discworld/discworld.vhd"/>
    <file delay="0" type="s" index="4" path="media/discworld/discworld.chd"/>
    <reset delay="1"/>
</mistergamedescription>
```

load in DosBox-X flatpak instance
```
flatpak run com.dosbox_x.DOSBox-X -conf 'Wizardry II.conf'
```