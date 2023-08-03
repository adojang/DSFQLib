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

!0::
if (Enabled) {
    SendInput josim -o ./testbench.csv ./testbench.cir -V 1{Enter}
    Sleep 250
    SendInput python josim-plot.py ./testbench.csv{Enter}
} else {
    SendInput 0
}
return

!1::
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

!2::
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

!3::
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

!p::
Run, cmd.exe /c cd /d "C:\JoSim\.LAYOUTS\2023_Layouts\DSFQ_AND" & python param.py & exit
return

!o::
Run, cmd.exe /k cd /d "C:\JoSim\.LAYOUTS\2023_Layouts\DSFQ_OR" & inductex or.GDS -n or.cir -l mitll_sfq5ee_res.ldf -th & pause

return


::drcx::C:/JoSim/.LAYOUTS/Design Rules/KLayout_DRC_MITLL_SFQ5ee_1_3_v211117_1444 (1)/KLayout_DRC_MITLL_SFQ5ee_1_3.drc