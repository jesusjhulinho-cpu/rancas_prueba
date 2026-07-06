import flet as ft
from datetime import datetime, date, timedelta

def create_antropometria_module():
    weight_field = ft.TextField(
        label="Peso (kg)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.InputBorder.OUTLINE,
        width=150
    )
    
    height_field = ft.TextField(
        label="Talla (cm)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.InputBorder.OUTLINE,
        width=150
    )
    
    birth_field = ft.TextField(
        label="Fecha Nacimiento (DD/MM/AAAA)",
        border=ft.InputBorder.OUTLINE,
        width=200
    )
    
    imc_result = ft.Text("", size=16)
    imc_class = ft.Text("", size=18, weight=ft.FontWeight.BOLD)
    age_result = ft.Text("", size=16)
    
    imc_container = ft.Container(
        content=ft.Column(
            controls=[imc_result, imc_class],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=12,
        bgcolor=ft.Colors.GREY_100,
        border_radius=8,
        visible=False
    )
    
    age_container = ft.Container(
        content=age_result,
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
    
    def calc_imc(e):
        try:
            if not weight_field.value or not height_field.value:
                show_error(e.page, "Completa ambos campos")
                return
            
            peso = float(weight_field.value)
            talla = float(height_field.value)
            
            if peso <= 0 or talla <= 0:
                show_error(e.page, "Los valores deben ser > 0")
                return
            
            talla_m = talla / 100
            imc = peso / (talla_m * talla_m)
            
            if imc < 18.5:
                clasif = "Bajo peso"
                color = ft.Colors.RED
            elif imc < 25:
                clasif = "Normal"
                color = ft.Colors.GREEN
            elif imc < 30:
                clasif = "Sobrepeso"
                color = ft.Colors.ORANGE
            elif imc < 35:
                clasif = "Obesidad I"
                color = ft.Colors.ORANGE_ACCENT
            elif imc < 40:
                clasif = "Obesidad II"
                color = ft.Colors.DEEP_ORANGE
            else:
                clasif = "Obesidad III"
                color = ft.Colors.RED_ACCENT
            
            imc_result.value = f"IMC: {imc:.2f}"
            imc_result.color = ft.Colors.GREY_900
            imc_class.value = f"Clasificación: {clasif}"
            imc_class.color = color
            imc_container.visible = True
            e.page.update()
            
        except ValueError:
            show_error(e.page, "Ingresa valores numéricos válidos")
        except Exception as ex:
            show_error(e.page, f"Error: {str(ex)}")
    
    def calc_age(e):
        try:
            if not birth_field.value:
                show_error(e.page, "Ingresa una fecha")
                return
            
            birth = datetime.strptime(birth_field.value, "%d/%m/%Y").date()
            
            if birth > date.today():
                show_error(e.page, "La fecha no puede ser futura")
                return
            
            today = date.today()
            years = today.year - birth.year
            months = today.month - birth.month
            days = today.day - birth.day
            
            if days < 0:
                months -= 1
                prev = today.replace(day=1) - timedelta(days=1)
                days += prev.day
            
            if months < 0:
                years -= 1
                months += 12
            
            age_result.value = f"Edad: {years} años, {months} meses, {days} días"
            age_result.color = ft.Colors.GREY_900
            age_container.visible = True
            e.page.update()
            
        except ValueError:
            show_error(e.page, "Formato inválido. Usa DD/MM/AAAA")
        except Exception as ex:
            show_error(e.page, f"Error: {str(ex)}")
    
    imc_section = ft.Container(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.HEALTH_AND_SAFETY, color=ft.Colors.PRIMARY),
                        ft.Text("Calculadora IMC", size=18, weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Row(
                    controls=[weight_field, height_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                ),
                ft.ElevatedButton(
                    text="Calcular IMC",
                    icon=ft.icons.CALCULATE,
                    on_click=calc_imc,
                    bgcolor=ft.Colors.PRIMARY,
                    color=ft.Colors.WHITE
                ),
                imc_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=16,
        bgcolor=ft.Colors.GREY_50,
        border_radius=12
    )
    
    age_section = ft.Container(
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.CAKE, color=ft.Colors.PRIMARY),
                        ft.Text("Calculadora de Edad", size=18, weight=ft.FontWeight.BOLD)
                    ]
                ),
                birth_field,
                ft.ElevatedButton(
                    text="Calcular Edad",
                    icon=ft.icons.CALCULATE,
                    on_click=calc_age,
                    bgcolor=ft.Colors.PRIMARY,
                    color=ft.Colors.WHITE
                ),
                age_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=16,
        bgcolor=ft.Colors.GREY_50,
        border_radius=12,
        margin=ft.margin.only(top=16)
    )
    
    return ft.Container(
        content=ft.Column(
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[imc_section, age_section]
        ),
        padding=8,
        expand=True,
        bgcolor=ft.Colors.WHITE
    )