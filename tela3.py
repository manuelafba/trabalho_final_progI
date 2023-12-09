import flet as ft
import control as c
import tela2

components = {
        'tf_nome': ft.Ref[ft.TextField](),
        'tf_cpf': ft.Ref[ft.TextField](),
        'tf_rg':ft.Ref[ft.TextField](),
        'tf_telefone': ft.Ref[ft.TextField](),
        'tf_endereço': ft.Ref[ft.TextField](),
        'tf_nascimento': ft.Ref[ft.TextField](),
        'tf_e-mail': ft.Ref[ft.TextField](),
        #add todos os compontens da tela aqui
    }

def view():
    return ft.View(
        "tela3",        
        [                           
            ft.Column(
                [
                    ft.Container( content=ft.Text("Editar", size=20)),
                    ft.TextField(ref=components['tf_nome'], label="Nome", autofocus=True,prefix_icon=ft.icons.PERSON, helper_text="Apenas letras"),
                    ft.TextField(ref=components['tf_cpf'], label="CPF", prefix_icon=ft.icons.DOCUMENT_SCANNER, helper_text="xxx.xxx.xxx-xx"),
                    ft.TextField(ref=components['tf_rg'], label="RG", prefix_icon=ft.icons.DOCUMENT_SCANNER, helper_text="xxxxxxx"),
                    ft.TextField(ref=components['tf_telefone'], label="Telefone", prefix_icon=ft.icons.PHONE, helper_text="(xx) xxxxx-xxxx"),
                    ft.TextField(ref=components['tf_endereço'], label="Endereço",prefix_icon=ft.icons.HOME),
                    ft.TextField(ref=components['tf_nascimento'], label="Nascimento",prefix_icon=ft.icons.STAR, helper_text="DD/MM/AAAA"),
                    ft.TextField(ref=components['tf_e-mail'], label="E-mail",prefix_icon=ft.icons.EMAIL,helper_text="name@example.com ou name@example.com.br"),
                    ft.Row(
                        [
                            ft.Container(
                                    content= ft.ElevatedButton(
                                                text="Atualizar", 
                                                icon="edit", 
                                                on_click= atualizar
                                            )#ElevatedButton   
                            ),#Container                                    
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),#Row
                ]
            ),                    
        ],
        appbar= ft.AppBar(
                    leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: c.page.go('1')),
                    leading_width=40,
                    title=ft.Text("Sistema de cadastro"),
                    center_title=False,
                    bgcolor=ft.colors.SURFACE_VARIANT,                    
                ),
    )


def atualizar(e):
     nome = components['tf_nome'].current.value
     cpf = components['tf_cpf'].current.value
     rg = components['tf_rg'].current.value
     telefone = components['tf_telefone'].current.value
     endereco = components['tf_endereço'].current.value
     nascimento = components['tf_nascimento'].current.value
     email = components['tf_e-mail'].current.value
     cadastro = [cad for cad in c.cadastros if cpf == cad['cpf']][0]
     idx = c.cadastros.index(cadastro)
     c.cadastros[idx] = {'nome':nome, 'cpf':cpf, 'rg': rg, 'telefone': telefone, 'endereço': endereco, 'nascimento': nascimento, 'e-mail': email}     
     tela2.components["tabela"].current.rows = tela2.data_table()
     c.page.go('1')
     