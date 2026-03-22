## things used everywhere

TYPES = {
    1: "Grass",
    2: "Fire",
    3: "Water",
    4: "Lightning",
    5: "Psychic",
    6: "Fighting",
    7: "Darkness",
    8: "Metal",
    9: "Dragon",
    10: "Colorless",
}

TYPE_IDS = {v: k for k, v in TYPES.items()}

ENERGY_SYMBOLS = {
    "{G}": "Grass",
    "{R}": "Fire",
    "{W}": "Water",
    "{L}": "Lightning",
    "{P}": "Psychic",
    "{F}": "Fighting",
    "{D}": "Darkness",
    "{M}": "Metal",
    "{N}": "Dragon",
    "{C}": "Colorless",
}

STAGES = {
    0: "Basic",
    1: "Stage1",
    2: "Stage2",
}

STAGE_IDS = {v: k for k, v in STAGES.items()}

ENERGY_SYMBOLS = {
    "{G}": "Grass",
    "{R}": "Fire",
    "{W}": "Water",
    "{L}": "Lightning",
    "{P}": "Psychic",
    "{F}": "Fighting",
    "{D}": "Darkness",
    "{M}": "Metal",
    "{N}": "Dragon",
    "{C}": "Colorless",
}

ENERGY_NAMES_TO_SYMBOLS = {v: k for k, v in ENERGY_SYMBOLS.items()}

# --- Rarities ---
RARITIES = [
    "One Diamond",
    "Two Diamond",
    "Three Diamond",
    "Four Diamond",
    "One Star",
    "Two Star",
    "Three Star",
    "Crown",
]

SETS = [
    "A1",   # Genetic Apex
    "A1a",  # Mythical Island
    "A2",   # Space-Time Smackdown
    "A2a",  # Triumphant Light
    "A2b",  # Shining Revelry
    "A3",   # Extradimensional Crisis
    "A3a",  # Eevee Grove
    "A4",   # Celestial Guardians
    "A4a",  # Secluded Springs
    "B1",
    "B2",
    "P-A",  # Promos-A
]