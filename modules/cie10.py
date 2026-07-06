import flet as ft
from database.db_manager import DatabaseManager

def create_cie10_module():
    db = DatabaseManager()
    
    search_field = ft.TextField(
        hint_text="Buscar por código o descripción",
        prefix_icon=ft.icons.SEARCH,
        border=ft.InputBorder.OUTLINE,
        border_color=ft.Colors.PRIMARY,
        focused_border_color=ft.Colors.PRIMARY,
        autofocus=True,
        expand=True
    )
    
    results = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO, expand=True)
    stats = ft.Text("Ingresa al menos 2 caracteres", size=14, color=ft.Colors.GREY_600)
    
    def on_search(e):
        query = search_field.value
        results.controls.clear()
        
        if not query or len(query.strip()) < 2:
            stats.value = "Ingresa al menos 2 caracteres"
            stats.color = ft.Colors.GREY_600
            e.page.update()
            return
        
        data = db.search_cie10(query)
        
        if not data:
            stats.value = "No se encontraron resultados"
            stats.color = ft.Colors.RED
            e.page.update()
            return
        
        stats.value = f"Se encontraron {len(data)} resultados"
        stats.color = ft.Colors.GREY_600
        
        for r in data:
            card = create_result_card(r["codigo"], r["descripcion"], e.page)
            results.controls.append(card)
        
        e.page.update()
    
    def create_result_card(codigo, descripcion, page):
        def copy_code(e):
            page.set_clipboard(codigo)
            page.snack_bar = ft.SnackBar(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                        ft.Text(f"Código {codigo} copiado")
                    ]
                ),
                bgcolor=ft.Colors.BLUE_100,
                duration=2000
            )
            page.snack_bar.open = True
            page.update()
        
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            spacing=4,
                            expand=True,
                            controls=[
                                ft.Text(codigo, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                                ft.Text(descripcion, size=14)
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.icons.COPY,
                            icon_color=ft.Colors.PRIMARY,
                            tooltip="Copiar código",
                            on_click=copy_code
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=12
            ),
            elevation=2,
            margin=ft.margin.only(bottom=4)
        )
    
    search_field.on_change = on_search
    
    return ft.Container(
        content=ft.Column(
            spacing=16,
            expand=True,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.LOCAL_HOSPITAL, color=ft.Colors.PRIMARY),
                        ft.Text("Clasificación CIE-10", size=20, weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Divider(),
                search_field,
                stats,
                results
            ]
        ),
        padding=8,
        expand=True,
        bgcolor=ft.Colors.WHITE
    )