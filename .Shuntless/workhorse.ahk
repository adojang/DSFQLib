#Persistent
Enabled := false

Menu, Tray, Tip, AutoHotkey Script
Menu, Tray, Icon, Shell32.dll, 44

SetTimer, ChangeTrayIcon, 500
return

ChangeTrayIcon:
if (Enabled) {
    Menu, Tray, Icon, Shell32.dll, 43
} else {
    Menu, Tray, Icon, Shell32.dll, 44
}
return

Numpad0::
if (Enabled) {
    SendInput josim -o ./testbench.csv ./testbench.cir -V 1{Enter}
    Sleep 250
    SendInput python josim-plot.py ./testbench.csv{Enter}
} else {
    SendInput 0
}
return

Numpad1::
if (Enabled) {
    SendInput josim -o ./testbench.csv ./testbench.cir -V 1{Enter}
    Sleep 250
    SendInput python josim-plot.py ./testbench.csv{Enter}
    Sleep 250
    SendInput josim-tools .\margins.toml{Enter}
} else {
    SendInput 1
}
return

Numpad2::
if (Enabled) {
    SendInput josim -o ./testbench.csv ./testbench.cir -V 1{Enter}
    Sleep 250
    SendInput python josim-plot.py ./testbench.csv{Enter}
    Sleep 250
    SendInput python sp_generator.py -t 0.70 -s 40E-12 -o testbench.sp -v testbench.csv{Enter}
    Sleep 250
    SendInput josim-tools .\verify.toml{Enter}
    Sleep 250
    SendInput josim-tools .\margins.toml{Enter}
} else {
    SendInput 2
}
return

Numpad3::
if (Enabled) {
    SendInput josim-tools .\optimize.toml{Enter}
} else {
    SendInput 3
}
return

$PgUp:: 
Enabled := !Enabled
If (Enabled) {
    Tooltip, Shortcut Enabled
} Else {
    Tooltip, Shortcut Disabled
}
SetTimer, RemoveToolTip, 1500
return

RemoveToolTip:
SetTimer, RemoveToolTip, Off
Tooltip
return
