import flet as ft

COLORS = {
    "primary": ft.Colors.BLUE_700,
    "secondary": ft.Colors.TEAL_400,
    "success": ft.Colors.GREEN_700,
    "error": ft.Colors.RED_700,
    "warning": ft.Colors.ORANGE_700,
}

IMC_CLASSIFICATIONS = {
    "bajo_peso": {"range": (0, 18.5), "description": "Bajo peso", "color": ft.Colors.ERROR},
    "normal": {"range": (18.5, 25), "description": "Normal", "color": ft.Colors.GREEN},
    "sobrepeso": {"range": (25, 30), "description": "Sobrepeso", "color": ft.Colors.ORANGE},
    "obesidad_i": {"range": (30, 35), "description": "Obesidad I", "color": ft.Colors.ORANGE_ACCENT},
    "obesidad_ii": {"range": (35, 40), "description": "Obesidad II", "color": ft.Colors.DEEP_ORANGE},
    "obesidad_iii": {"range": (40, float('inf')), "description": "Obesidad III", "color": ft.Colors.RED_ACCENT},
}