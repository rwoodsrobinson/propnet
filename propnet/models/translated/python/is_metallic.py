

def plug_in(self, symbol_values):
    return {'is_metallic': 1 if symbol_values['E_g'] <= 0 else 0}

config = {
    "name": "is_metallic",
    "connections": [
        {
            "inputs": [
                "E_g"
            ],
            "outputs": [
                "is_metallic"
            ]
        }
    ],
    "categories": [
        "classifier"
    ],
    "symbol_property_map": {
        "E_g": "band_gap",
        "is_metallic": "is_metallic"
    },
    "description": "\nThis model returns true if band gap is zero.\n",
    "references": [],
    "plug_in": plug_in
}