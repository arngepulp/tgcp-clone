# engine/game/effects.py

def resolve_effects(state, effect_data, source):
    if not effect_data:
        return None
    
    effect_id = effect_data.get("type")
    if effect_data.get("amount"):
        amount = effect_data.get("amount")
    else:
        amount = None
        
    target_id = effect_data.get("target")
    
    if target_id == "SELF_ALL":
        targets = [b for b in state.current_player.bench if b is not None] + [state.current_player.active] 
    
    if effect_id == "HEAL":
        for t in targets:
            if t and t.current_hp < t.hp:
                t.current_hp = min(t.hp, t.current_hp + amount)
                print(f"Heal has occurred! {t.name} healed for {amount} HP.")
    