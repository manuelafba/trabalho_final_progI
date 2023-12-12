import flet as ft
import control as c



def main(page: ft.Page):        
    c.init(page)
    page.title = "Sistema de cadastro"           
    page.on_route_change = c.route_change  
    page.theme_mode  = "light"
    page.go('0')
    page.theme = ft.Theme(color_scheme_seed='red')
    page.update()
    


ft.app(target=main)

