## Screen with Stats Button
screen gameUI:
    imagebutton:
        xalign 1.0
        yalign 0.0
        xoffset -30
        yoffset 30
        idle "UI/stats_idle.png"
        action ShowMenu("StatsUI")
        
## Stats UI
screen StatsUI:
    add "UI/bg peach.png"
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30

        hbox:
            spacing 40
            # Text Column
            vbox:
                spacing 10
                text "Knowledge" size 40
                text "Charm" size 40
                text "Guts" size 40
                text "Kindness" size 40
                text "Proficiency" size 40

            # Values Column     
            vbox:    
                spacing 10
                text "[knowledge]" size 40
                text "[charm]" size 40
                text "[guts]" size 40
                text "[kindness]" size 40
                text "[proficiency]" size 40
     
    ## Show a Return button
    imagebutton:
        xalign 1.0
        yalign 0.0
        xoffset -30
        yoffset 30
        auto "UI/return_%s.png"
        action Return()
