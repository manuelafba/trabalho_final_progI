import flet as ft
import control as c



def main(page: ft.Page):        
    c.init(page)
    page.title = "Sistema de cadastro"           
    page.on_route_change = c.route_change  
    page.theme_mode  = "dark"
    page.go('0')
    


ft.app(target=main)