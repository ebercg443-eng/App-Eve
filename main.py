import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import flet as ft

def main(page: ft.Page):
    # Configuración general de la ventana y tema
    page.title = "Simulador Industrial de Capacidad y Costos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- CAMPOS DE ENTRADA ---
    txt_cap_instalada = ft.TextField(
        label="Capacidad Instalada (Piezas/Hora)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        filled=True
    )
    txt_cap_efectiva = ft.TextField(
        label="Capacidad Efectiva (Piezas/Hora)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        filled=True
    )
    txt_prod_real = ft.TextField(
        label="Producción Real (Piezas/Hora)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        filled=True
    )
    txt_costo_fijo = ft.TextField(
        label="Costos Fijos Totales ($)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        filled=True
    )
    txt_costo_var = ft.TextField(
        label="Costo Variable Unitario Base ($)",
        keyboard_type=ft.KeyboardType.NUMBER,
        border_radius=10,
        filled=True
    )

    # --- COMPONENTES DE RESULTADOS ---
    txt_utilizacion = ft.Text(value="--", size=18, weight=ft.FontWeight.BOLD, color="blue")
    txt_eficiencia = ft.Text(value="--", size=18, weight=ft.FontWeight.BOLD, color="indigo")
    txt_brecha = ft.Text(value="--", size=18, weight=ft.FontWeight.BOLD, color="orange")
    txt_costo_total = ft.Text(value="--", size=18, weight=ft.FontWeight.BOLD, color="teal")
    txt_costo_unitario = ft.Text(value="--", size=18, weight=ft.FontWeight.BOLD, color="green")
    txt_economia = ft.Text(value="Ingrese los datos para calcular las economías de escala.", size=14, italic=True, color="grey")

    # Tarjeta de Resultados
    card_resultados = ft.Card(
        elevation=4,
        content=ft.Container(
            padding=20,
            width=420,
            content=ft.Column([
                ft.Text("Resultados del Análisis Industrial", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row([ft.Text("• Utilización (%):"), txt_utilizacion], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("• Eficiencia (%):"), txt_eficiencia], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("• Brecha de Capacidad (Pz/h):"), txt_brecha], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("• Costo Total de Producción:"), txt_costo_total], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("• Costo Unitario Real (Escala):"), txt_costo_unitario], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                txt_economia
            ])
        )
    )

    # --- FUNCIÓN DE CÁLCULO ---
    def calcular_click(e):
        try:
            # Obtener y validar valores numéricos
            cap_inst = float(txt_cap_instalada.value)
            cap_efec = float(txt_cap_efectiva.value)
            prod_real = float(txt_prod_real.value)
            cf = float(txt_costo_fijo.value)
            cv_base = float(txt_costo_var.value)

            if cap_inst <= 0 or cap_efec <= 0:
                raise ValueError("Las capacidades deben ser mayores a cero.")

            # 1. Cálculos basados estrictamente en el documento del proyecto
            utilizacion = (prod_real / cap_inst) * 100
            eficiencia = (prod_real / cap_efec) * 100
            brecha = cap_efec - prod_real

            # 2. Cálculo de Costos y Economía de Escala
            factor_escala = max(0.75, 1.0 - (0.05 * (prod_real / cap_inst))) 
            cv_ajustado = cv_base * factor_escala

            costo_total = cf + (cv_ajustado * prod_real)
            costo_unitario = costo_total / prod_real if prod_real > 0 else 0

            # Actualizar textos en la interfaz
            txt_utilizacion.value = f"{utilizacion:.2f}%"
            txt_eficiencia.value = f"{eficiencia:.2f}%"
            txt_brecha.value = f"{brecha:,.2f} Pz/h"
            txt_costo_total.value = f"${costo_total:,.2f}"
            txt_costo_unitario.value = f"${costo_unitario:,.2f} /u"
            
            if factor_escala < 1.0:
                txt_economia.value = f"¡Economía de escala aplicada! Reducción en costos variables: {(1-factor_escala)*100:.1f}% debido al volumen de producción real."
            else:
                txt_economia.value = "Producción baja: No se aprecian ventajas significativas por economías de escala aún."

            page.snack_bar = ft.SnackBar(ft.Text("¡Cálculos industriales realizados con éxito!"), bgcolor="green")
            page.snack_bar.open = True

        except ValueError as ex:
            page.snack_bar = ft.SnackBar(ft.Text("Error: Verifique que todos los campos tengan números válidos."), bgcolor="red")
            page.snack_bar.open = True
        
        page.update()

    # Botón Principal con Container Interactivo
    btn_calcular = ft.Container(
        content=ft.Text("Calcular Métricas y Costos", color="white", weight=ft.FontWeight.BOLD, size=15),
        alignment=ft.Alignment(0, 0),
        bgcolor="blue",
        padding=15,
        border_radius=8,
        width=300,
        ink=True,
        on_click=calcular_click
    )

    # --- DISEÑO DE LA PANTALLA ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Simulador de Capacidad y Costos", size=22, weight=ft.FontWeight.BOLD, color="blue"),
                ft.Text("Basado en métricas de Ingeniería Industrial (Piezas/Hora)", size=13, color="grey", italic=True),
                ft.Divider(height=20),
                
                ft.Container(
                    content=ft.Column([
                        txt_cap_instalada,
                        txt_cap_efectiva,
                        txt_prod_real,
                        txt_costo_fijo,
                        txt_costo_var,
                    ], spacing=15),
                    width=400
                ),
                
                ft.Container(height=10),
                btn_calcular,
                ft.Container(height=10),
                
                card_resultados
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            alignment=ft.Alignment(0, 0)
        )
    )

ft.run(main)
