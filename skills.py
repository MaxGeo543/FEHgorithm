# Phase means: 'permanent; at start of turn (turn); before combat (bef-combat); during combat (dur-combat); after combat (aft-combat)'


def effect(unit, phase):
    
    ### WEAPONS ###
    
#    if unit.wpn == "":
#        if phase == "permanent":
#            
#        if phase == "turn":
#            
#        if phase == "bef-combat":
#            
#        if phase == "dur-combat":
#            
#        if phase == "aft-combat":
#            

    if unit.weapon == "Blazing Durandal":
        if phase == "permanent":
            unit.base_atk += 19

    if unit.weapon == "Dark Aura":
        if phase == "permanent":
            unit.base_atk += 14

    if unit.weapon == "Dark Excalibur":
        if phase == "permanent":
            unit.base_atk += 14

    if unit.weapon == "Dire Thunder":
        if phase == "permanent":
            unit.base_atk += 9
            unit.base_spd -= 5

    if unit.weapon == "Divine Naga":
        if phase == "permanent":
            unit.base_atk += 14

    if unit.weapon == "Divine Tyrfing":
        if phase == "permanent":
            unit.base_atk += 16
            unit.base_res += 3

    if unit.weapon == "Dragoon Axe":
        if phase == "permanent":
            unit.base_atk += 16

    if unit.weapon == "Mirage Falchion":
       if phase == "permanent":
        unit.base_atk += 16
        unit.base_def += 3

    if unit.weapon == "Spendthrift Bow+ (+Res)":
        if phase == "permanent":
            unit.base_atk += 12
            unit.max_hp += 2
            unit.base_res += 3
    
    
    
    ### A-SKILLS ###
    
    if unit.a_skill == "Dragoon Shield":
        if phase == "permanent":
            unit.base_atk += 3
            unit.base_spd += 3
            unit.base_def += 3

    if unit.a_skill == "HP +5":
        if phase == "permanent":
            unit.max_hp += 5



    if unit.a_skill == "Resistance +3":
        if phase == "permanent":
            unit.base_res += 3

    if unit.a_skill == "Speed +3":
        if phase == "permanent":
            unit.base_spd += 3



    
    
    
    ### B-SKILLS ###
    
    if unit.b_skill == "Pass 3":
        if phase == "turn":
            if unit.current_hp >= unit.max_hp*25/100:
                unit.pass_status = True
        if phase == "aft-combat":
            if unit.current_hp < unit.max_hp*25/100:
                unit.pass_status = False

