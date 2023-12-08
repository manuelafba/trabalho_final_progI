import flet as ft
import control as c

components = {
        'tabela': ft.Ref[ft.DataTable](),   
        'tf_pesquisa': ft.Ref[ft.TextField](),     
        #add todos os compontens da tela aqui
    }

def view():            
    return ft.View(
                    "tela2",
                    [
                        ft.TextField(ref=components['tf_pesquisa'], label='Pesquisar', on_change=pesquisar),
                        ft.DataTable(
                            width=float('inf'),
                            ref=components['tabela'],                                                    
                            columns=[
                                ft.DataColumn(ft.Text("Nome")),
                                ft.DataColumn(ft.Text("CPF")),                                
                                ft.DataColumn(ft.Text("Ações")),                                
                            ],
                            #rows=[] são carregadas dinamicamente quando clica no menu de navegação
                         ),               
                    ],
                    navigation_bar=c.barra_navegacao(),
                    appbar= ft.AppBar(            
                    title=ft.Text("Sistema de cadastro"),
                    center_title=False,
                    bgcolor=ft.colors.SURFACE_VARIANT,                    
                ),                                                      
                )


def pesquisar(e):
    value = components['tf_pesquisa'].current.value
    components["tabela"].current.rows = [ft.DataRow(cells=data_line(cad)) for cad in c.cadastros if value in cad['nome']]    
    c.page.update()


def remover(e):
    value = e.control.key
    c.cadastros = [cad for cad in c.cadastros if value != cad['cpf']]
    components["tabela"].current.rows = data_table()
    c.page.update()


def atualizar(e):
    value = e.control.key
    cadastro = [cad for cad in c.cadastros if value == cad['cpf']][0]
   # tela3.components['tf_nome'].current.value = cadastro['nome']
   # tela3.components['tf_cpf'].current.value = cadastro['cpf']
    c.page.go('2')


def data_line(cadastro):
    return [
                ft.DataCell(ft.Text(cadastro['nome'])),
                ft.DataCell(ft.Text(cadastro['cpf'])),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color="blue",
                                icon_size=35,
                                tooltip="Atualizar",
                                key=cadastro['cpf'],
                                on_click=atualizar
                            ),
                            ft.IconButton(
                                icon=ft.icons.REMOVE_CIRCLE,
                                icon_color="red",
                                icon_size=35,
                                tooltip="Remover",
                                key=cadastro['cpf'],
                                on_click=remover
                            ),
                        ]
                    )                    
                ),
            
        ]


def data_table():    
    return [ft.DataRow(cells=data_line(cad)) for cad in c.cadastros]    