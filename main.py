import flet as ft
from modules.cie10 import create_cie10_module
from modules.antropometria import create_antropometria_module
from modules.ginecologia import create_ginecologia_module
from modules.calculadoras import create_calculadoras_module

COLOR_PRIMARY = ft.Colors.BLUE_700

def main(page: ft.Page):
    page.title = "Rancas Prueba"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=COLOR_PRIMARY)
    page.dark_theme = ft.Theme(color_scheme_seed=COLOR_PRIMARY)
    page.padding = 0
    page.window_min_width = 360
    page.window_max_width = 600
    
    content_container = ft.Container(
        expand=True,
        padding=16,
        bgcolor=ft.Colors.WHITE
    )
    
    modules = {
        0: create_cie10_module(),
        1: create_antropometria_module(),
        2: create_ginecologia_module(),
        3: create_calculadoras_module()
    }
    
    def on_nav_change(e):
        index = e.control.selected_index
        content_container.content = modules[index]
        content_container.update()
    
    nav_bar = ft.NavigationBar(
        selected_index=0,
        label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
        indicator_color=COLOR_PRIMARY,
        bgcolor=ft.Colors.GREY_100,
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.SEARCH, label="CIE-10"),
            ft.NavigationBarDestination(icon=ft.icons.MONITOR_HEART, label="Antropometría"),
            ft.NavigationBarDestination(icon=ft.icons.PREGNANT_WOMAN, label="Ginecología"),
            ft.NavigationBarDestination(icon=ft.icons.CALCULATE, label="Calculadoras"),
        ],
        on_change=on_nav_change
    )
    
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.icons.MEDICAL_SERVICES, color=COLOR_PRIMARY, size=28),
                ft.Text("Rancas Prueba", size=22, weight=ft.FontWeight.BOLD, color=COLOR_PRIMARY)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=12,
        bgcolor=ft.Colors.GREY_100
    )
    
    page.add(
        ft.Column(
            spacing=0,
            expand=True,
            controls=[
                header,
                ft.Column(expand=True, controls=[content_container]),
                nav_bar
            ]
        )
    )
    
    content_container.content = modules[0]
    page.update()

if __name__ == "__main__":
    ft.app(target=main)