import flet as ft

def create_calculadoras_module():
    peso_field = ft.TextField(
        label="Peso (kg)",
        width=130,
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.InputBorder.OUTLINE
    )
    
    dosis_field = ft.TextField(
        label="Dosis (mg/kg/día)",
        width=130,
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.InputBorder.OUTLINE
    )
    
    conc_field = ft.TextField(
        label="Concentración (mg/ml)",
        width=130,
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.InputBorder.OUTLINE
    )
    
    freq_field = ft.TextField(
        label="Dosis/día",
        width=130,
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.InputBorder.OUTLINE
    )
    
    vol_field = ft.TextField(
        label="Volumen (ml)",
        width=130,
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.InputBorder.OUTLINE
    )
    
    time_field = ft.TextField(
        label="Tiempo (horas)",
        width=130,
        keyboard_type=ft.KeyboardType.NUMBER,
        border=ft.InputBorder.OUTLINE
    )
    
    dosis_result = ft.Text("", size=16)
    goteo_result = ft.Text("", size=16)
    
    dosis_container = ft.Container(
        content=dosis_result,
        padding=12,
        bgcolor=ft.Colors.GREY_100,
        border_radius=8,
        visible=False
    )
    
    goteo_container = ft.Container(
        content=goteo_result,
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
    
    def calc_dosis(e):
        try:
            if not all([peso_field.value, dosis_field.value, conc_field.value, freq_field.value]):
                show_error(e.page, "Completa todos los campos")
                return
            
            peso = float(peso_field.value)
            dosis = float(dosis_field.value)
            conc = float(conc_field.value)
            freq = int(freq_field.value)
            
            if any([peso <= 0, dosis <= 0, conc <= 0, freq <= 0]):
                show_error(e.page, "Todos los valores deben ser > 0")
                return
            
            resultado = (peso * dosis) / (conc * freq)
            dosis_result.value = f"Dosis por toma: {resultado:.2f} ml"
            dosis_result.color = ft.Colors.GREY_900
            dosis_container.visible = True
            e.page.update()
            
        except ValueError:
            show_error(e.page, "Ingresa valores numéricos válidos")
        except Exception as ex:
            show_error(e.page, f"Error: {str(ex)}")
    
    def calc_goteo(e):
        try:
            if not vol_field.value or not time_field.value:
                show_error(e.page, "Completa ambos campos")
                return
            
            vol = float(vol_field.value)
            tiempo = float(time_field.value)
            
            if vol <= 0 or tiempo <= 0:
                show_error(e.page, "Los valores deben ser > 0")
                return
            
            gotas = vol / (3 * tiempo)
            goteo_result.value = f"Goteo: {gotas:.1f} gotas/minuto"
            goteo_result.color = ft.Colors.GREY_900
            goteo_container.visible = True
            e.page.update()
            
        except ValueError:
            show_error(e.page, "Ingresa valores numéricos válidos")
        except Exception as ex:
            show_error(e.page, f"Error: {str(ex)}")
    
    dosis_section = ft.Container(
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.MEDICATION, color=ft.Colors.PRIMARY),
                        ft.Text("Dosis Pediátrica", size=16, weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Row(controls=[peso_field, dosis_field], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[conc_field, freq_field], alignment=ft.MainAxisAlignment.CENTER),
                ft.ElevatedButton(
                    text="Calcular Dosis",
                    on_click=calc_dosis,
                    bgcolor=ft.Colors.PRIMARY,
                    color=ft.Colors.WHITE
                ),
                dosis_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=16,
        bgcolor=ft.Colors.GREY_50,
        border_radius=12
    )
    
    goteo_section = ft.Container(
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.WATER_DROP, color=ft.Colors.PRIMARY),
                        ft.Text("Goteo de Infusión", size=16, weight=ft.FontWeight.BOLD)
                    ]
                ),
                ft.Row(controls=[vol_field, time_field], alignment=ft.MainAxisAlignment.CENTER),
                ft.ElevatedButton(
                    text="Calcular Goteo",
                    on_click=calc_goteo,
                    bgcolor=ft.Colors.PRIMARY,
                    color=ft.Colors.WHITE
                ),
                goteo_container
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
            controls=[dosis_section, goteo_section]
        ),
        padding=8,
        expand=True,
        bgcolor=ft.Colors.WHITE
    )