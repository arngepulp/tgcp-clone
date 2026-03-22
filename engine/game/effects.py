# engine/game/effects.py

def resolve_effects(state, effect_data, source,damage_dealt=0,):
    if not effect_data:
        return None
    effect_id = effect_data.get("type")
    amount = effect_data.get("amount")
    targets = resolve_targets(state, effect_data, source)
    
    if effect_id == "HEAL":
        heal(targets, amount)
    elif effect_id == "HEAL_DRAIN":
        heal_drain(state, source, damage_dealt)
    elif effect_id == "POISON":
        apply_status(targets, "poisoned")
    elif effect_id == "SLEEP":
        apply_status(targets, "asleep")
    elif effect_id == "PARALYSIS":
        apply_status(targets, "paralyzed")
    elif effect_id == "DAMAGE_BONUS_FLAT":
        damage_bonus_flat(state, amount)
    elif effect_id == "DAMAGE_BONUS_CONDITIONAL":
        damage_bonus_conditional(state, source, effect_data)
    elif effect_id == "DAMAGE_BONUS_PER_BENCH":
        damage_bonus_per_bench(state, source, amount, effect_data)
    elif effect_id == "DAMAGE_BONUS_PER_ENERGY":
        damage_bonus_per_energy(state, amount)
    elif effect_id == "DAMAGE_SELF":
        damage_self(source, amount)
    elif effect_id == "DAMAGE_BENCH_SELF":
        damage_bench_self(state, amount, effect_data)
    elif effect_id == "DAMAGE_BENCH_OPP":
        damage_bench_opp(state, amount, effect_data)
    elif effect_id == "DAMAGE_RANDOM_OPP":
        damage_random_opp(state, amount, effect_data)
    elif effect_id == "COIN_FLIP":
        coin_flip(state, effect_data, source)
    elif effect_id == "DISCARD_ENERGY_SELF":
        discard_energy_self(source, amount)
    elif effect_id == "DISCARD_ENERGY_OPP":
        discard_energy_opp(state, amount)
    elif effect_id == "ATTACH_ENERGY":
        attach_energy_effect(state, effect_data)
    elif effect_id == "DRAW":
        draw(state, amount)
    elif effect_id == "SEARCH_DECK":
        search_deck(state, effect_data)
    elif effect_id == "FORCE_SWITCH_OPP":
        force_switch_opp(state)
    elif effect_id == "SWITCH_SELF":
        switch_self(state, effect_data)
    elif effect_id == "BLOCK_SUPPORTER":
        block_supporter(state)
    elif effect_id == "BLOCK_ATTACK":
        block_attack(state)
    elif effect_id == "BLOCK_RETREAT":
        block_retreat(state)
    elif effect_id == "DAMAGE_REDUCTION_SELF":
        damage_reduction_self(source, amount)
    elif effect_id == "SHUFFLE_INTO_DECK":
        shuffle_into_deck(state)
    else:
        print(f"Unknown effect: {effect_id}")


def resolve_targets(state, effect_data, source):
    target_id = effect_data.get("target")
    if target_id == "SELF_ALL":
        return [state.current_player.active] + [b for b in state.current_player.bench if b]
    elif target_id == "SELF":
        return [source]
    elif target_id == "OPPONENT_ACTIVE":
        return [state.opponent.active]
    elif target_id == "OPPONENT_BENCH":
        return [b for b in state.opponent.bench if b]
    elif target_id == "OPPONENT_ALL":
        return [state.opponent.active] + [b for b in state.opponent.bench if b]
    elif target_id == "ALL":
        return [state.current_player.active] + [b for b in state.current_player.bench if b] + \
               [state.opponent.active] + [b for b in state.opponent.bench if b]
    elif target_id == "OPPONENT_BENCH_1":
        index = effect_data.get("index", 0)
        return [state.opponent.bench[index]] if state.opponent.bench[index] else []
    return []


# --- Healing ---
def heal(targets, amount):
    for t in targets:
        if t and t.current_hp < t.hp:
            t.current_hp = min(t.hp, t.current_hp + amount)
            print(f"{t.name} healed for {amount} HP.")

def heal_drain(source, damage_dealt):
    source.current_hp = min(source.hp, source.current_hp + damage_dealt)
    print(f"{source.name} healed {damage_dealt} HP.")


# --- Status Conditions ---
def apply_status(targets, status):
    for t in targets:
        if t:
            t.status = status
            print(f"{t.name} is now {status}.")


# --- Damage Modifiers ---
def damage_bonus_flat(state, targets, amount):
    # adds flat damage to current attack
    pass

def damage_bonus_conditional(state, source, effect_data):
    # does more damage if X extra energy attached
    # effect_data needs: energy_type, extra_energy_count, bonus_damage
    pass  # TODO

def damage_bonus_per_bench(state, source, amount, effect_data):
    # does X damage for each benched pokemon
    # effect_data needs: bench_type (filter by type or None for all)
    pass  # TODO

def damage_bonus_per_energy(state, amount):
    # does X more damage for each energy attached to opponent's active
    pass  # TODO

def damage_self(source, amount):
    source.current_hp -= amount
    print(f"{source.name} took {amount} damage to itself.")

def damage_bench_self(state, amount, effect_data):
    # does X damage to one of your own benched pokemon
    # effect_data needs: index or random
    pass  # TODO

def damage_bench_opp(state, amount, effect_data):
    # does X damage to one of opponent's benched pokemon
    # effect_data needs: index or random
    pass  # TODO

def damage_random_opp(state, amount, effect_data):
    # chosen at random X times, do Y damage each
    # effect_data needs: times, damage_per_hit
    pass  # TODO


# --- Coin Flips ---
def coin_flip(state, effect_data, source):
    # wraps another effect conditionally on coin flip
    # effect_data needs: coins, heads_effect, tails_effect
    import random
    pass  # TODO


# --- Energy ---
def discard_energy_self(source, amount):
    for _ in range(amount):
        if source.attached_energy:
            source.attached_energy.pop()
    print(f"{source.name} discarded {amount} energy.")

def discard_energy_opp(state, amount):
    # discard random energy from opponent's active
    import random
    pass  # TODO

def attach_energy_effect(state, effect_data):
    # take from energy zone and attach
    # effect_data needs: energy_type, target
    pass  # TODO


# --- Drawing ---
def draw(state, amount):
    for _ in range(amount):
        state.current_player.draw_card()
    print(f"Drew {amount} card(s).")

def search_deck(state, effect_data):
    # put random X pokemon of type Y from deck into hand
    # effect_data needs: pokemon_type, count
    pass  # TODO


# --- Control ---
def force_switch_opp(state):
    # switch opponent's active to bench, they choose new active
    # needs UI interaction
    pass  # TODO

def switch_self(state, effect_data):
    # switch this pokemon with a benched pokemon
    # needs UI interaction
    pass  # TODO

def block_supporter(state):
    # opponent can't use supporter cards next turn
    # needs a flag on game state
    pass  # TODO

def block_attack(state):
    # defending pokemon can't attack next turn
    # needs a flag on opponent's active
    pass  # TODO

def block_retreat(state):
    # defending pokemon can't retreat next turn
    # needs a flag on opponent's active
    pass  # TODO

def damage_reduction_self(source, amount):
    # this pokemon takes -X damage from attacks
    # needs to be checked in take_damage
    pass  # TODO

def shuffle_into_deck(state):
    # shuffle opponent's active into their deck
    pass  # TODO