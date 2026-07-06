import flet as ft
from datetime import datetime, timedelta, date

def create_ginecologia_module():
    fur_field = ft.TextField(
        label="Fecha Última Regla (DD/MM/AAAA)",
        border=ft.InputBorder.OUTLINE,
        width=250
    )
    
    result_text1 = ft.Text("", size=16)
    result_text2 = ft.Text("", size=16)
    
    result_container = ft.Container(
        content=ft.Column(
            controls=[
                result_text1,
                ft.Divider(),
                result_text2
            ],
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=12,
        bgcolor=ft.Colors.GREY_100,
        border_radius=8,
        visible=False
    )
    
    def show_error(page, msg):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor=ft.Colors.RED_100,
            duration=3000
        )
        page.snack_bar.open = True
        page.update()
    
    def calculate(e):
        try:
            if not fur_field.value:
                show_error(e.page, "Ingresa la FUR")
                return
            
            fur = datetime.strptime(fur_field.value, "%d/%m/%Y").date()
            
            if fur > date.today():
                show_error(e.page, "La FUR no puede ser futura")
                return
            
            days = (date.today() - fur).days
            
            if days < 0:
                show_error(e.page, "La FUR debe ser anterior a hoy")
                return
            
            weeks = days // 7
            days_rest = days % 7
            fpp = fur + timedelta(days=280)
            
            result_text1.value = f"Edad gestacional: {weeks} semanas y {days_rest} días"
            result_text1.color = ft.Colors.GREY_900
            result_text2.value = f"FPP: {fpp.strftime('%d/%m/%Y')}"
            result_text2.color = ft.Colors.PRIMARY
            
            result_container.visible = True
            e.page.update()
            
        except ValueError:
            show_error(e.page, "Formato inválido. Usa DD/MM/AAAA")
        except Exception as ex:
            show_error(e.page, f"Error: {str(ex)}")
    
    return ft.Container(
        content=ft.Column(
            spacing=16,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.PREGNANT_WOMAN, color=ft.Colors.PRIMARY),
                        ft.Text("Edad Gestacional", size=18, weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Text("Regla de Naegele: FPP = FUR + 280 días", size=12, color=ft.Colors.GREY_600),
                fur_field,
                ft.ElevatedButton(
                    text="Calcular",
                    icon=ft.icons.CALCULATE,
                    on_click=calculate,
                    bgcolor=ft.Colors.PRIMARY,
                    color=ft.Colors.WHITE
                ),
                result_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=16,
        expand=True,
        bgcolor=ft.Colors.WHITE
    )