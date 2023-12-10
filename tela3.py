import flet as ft
import control as c
import tela2, tela1

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

image_holder = ft.Image(visible=False, fit=ft.ImageFit.CONTAIN, width=100,
        height=100)

global selected_file_path, uid

import base64
def handle_loaded_file(e: ft.FilePickerResultEvent):
    global selected_file_path
    print(e.files)
    if e.files and len(e.files):
        selected_file_path = e.files[0].path
        with open(e.files[0].path, 'rb') as r:
            image_holder.src_base64 = base64.b64encode(r.read()).decode('utf-8')
            image_holder.visible = True
            c.page.update()

def view():
    file_picker = ft.FilePicker(on_result=handle_loaded_file)
    c.page.overlay.append(file_picker)
    def button_clicked(e):
        file_picker.pick_files(allow_multiple=False, allowed_extensions=['jpg', 'jpeg', 'png']) 
        c.page.update()
    return ft.View(
        "tela3",        
                [                           
                    ft.Column(
                        [
                            ft.Row([ft.Container( content=ft.Text("Edição", size=20))],alignment=ft.MainAxisAlignment.CENTER),
                            ft.Column([
                                ft.Row([image_holder],alignment=ft.MainAxisAlignment.CENTER),
                                ft.Row([
                                # Botão de upload da foto
                                ft.Container(content= 
                                ft.ElevatedButton(
                                text="Escolher foto", icon="image", on_click=
                                button_clicked
                                ))
                                ],alignment=ft.MainAxisAlignment.CENTER)#Container,
                                ]),
                            ft.TextField(ref=components['tf_nome'], label="Nome", autofocus=True,prefix_icon=ft.icons.PERSON, helper_text="Apenas letras"),
                            ft.TextField(ref=components['tf_cpf'], label="CPF", prefix_icon=ft.icons.DOCUMENT_SCANNER, helper_text="xxx.xxx.xxx-xx"),
                            ft.TextField(ref=components['tf_rg'], label="RG", prefix_icon=ft.icons.DOCUMENT_SCANNER, helper_text="Deve conter 7 digitos"),
                            ft.TextField(ref=components['tf_telefone'], label="Telefone", prefix_icon=ft.icons.PHONE, helper_text="(xx) xxxxx-xxxx"),
                            ft.TextField(ref=components['tf_endereço'], label="Endereço",prefix_icon=ft.icons.HOME, helper_text="Deve conter no máximo 20 caracteres"),
                            ft.TextField(ref=components['tf_nascimento'], label="Nascimento",prefix_icon=ft.icons.STAR, helper_text="DD/MM/AAAA"),
                            ft.TextField(ref=components['tf_e-mail'], label="E-mail",prefix_icon=ft.icons.EMAIL,helper_text="name@example.com ou name@example.com.br"),
                            ft.Row(
                                [
                                    ft.Container(
                                        #Botao de cadastrar
                                            content= ft.ElevatedButton(
                                                        text="Atualizar", 
                                                        icon="edit", 
                                                        on_click= lambda e: atualizar(e, selected_file_path)
                                                    )#ElevatedButton   
                                    ),#Container                                 
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),#Row
                        ],
                        scroll=ft.ScrollMode.ALWAYS,
                        expand=True,
                    ),                    
                ],
                # navigation_bar= c.barra_navegacao(),
                appbar= ft.AppBar(            
                    title=ft.Text("Sistema de cadastro"),
                    center_title=False,
                    bgcolor=ft.colors.SURFACE_VARIANT,                
                ),    
            )


def atualizar(e, selected_file_path = None):
    print(selected_file_path)

    nome = components['tf_nome'].current.value
    cpf = components['tf_cpf'].current.value
    rg = components['tf_rg'].current.value
    telefone = components['tf_telefone'].current.value
    endereco = components['tf_endereço'].current.value
    nascimento = components['tf_nascimento'].current.value
    email = components['tf_e-mail'].current.value

    components['tf_nome'].current.error_text = error_message('nome')
    components['tf_cpf'].current.error_text = error_message('cpf')
    components['tf_rg'].current.error_text = error_message('rg')
    components['tf_telefone'].current.error_text = error_message('telefone')
    components['tf_endereço'].current.error_text = error_message('endereco')
    components['tf_nascimento'].current.error_text = error_message('nascimento')
    components['tf_e-mail'].current.error_text = error_message('email')
    # exibir_snackbar_imagem_salva(selected_file_path)
    c.page.update()
    import csv
    # Se todos os campos forem válidos, escreva no arquivo CSV
    if tela1.validar_nome(nome) and tela1.validar_telefone(telefone) and tela1.validar_cpf(cpf) and tela1.validar_rg(rg) and tela1.validar_email(email) and tela1.validar_nascimento(nascimento) and tela1.validar_endereco(endereco) and selected_file_path is not None:
      dados = [
          [nome, telefone, cpf, rg, endereco, nascimento, email, selected_file_path]]
        # Ler o arquivo CSV
      with open('bd.csv', newline='', encoding='utf-8') as csvfile:
          reader = csv.reader(csvfile)
          data = list(reader)
      global uid
      # Encontrar a linha correspondente ao UID
      for row in data:
          if row and row[-1] == uid:
              # Atualizar os dados na linha encontrada
              row[:-1] = [nome, telefone, cpf, rg, endereco, nascimento, email, selected_file_path]
              break  # Parar após encontrar a linha

      # Escrever os dados atualizados de volta ao arquivo CSV
      with open('bd.csv', 'w', newline='', encoding='utf-8') as csvfile:
          writer = csv.writer(csvfile)
          writer.writerows(data)
      #Zera os TextFields
      components['tf_nome'].current.value = ''    
      components['tf_cpf'].current.value = ''
      components['tf_rg'].current.value = ''
      components['tf_telefone'].current.value = ''
      components['tf_endereço'].current.value = ''
      components['tf_nascimento'].current.value = ''
      components['tf_e-mail'].current.value = ''
      selected_file_path = None
      image_holder.visible = False
      uid = ''
      c.page.snack_bar = ft.SnackBar(
      ft.Text("Cadastro editado com sucesso!", size=20),
      duration=2000,
      bgcolor="green"
      )
      c.page.snack_bar.open = True
      tela2.atualizar_csv([])
      c.page.update() 
      c.page.go('1')

def error_message(data):
    try:
        if data == 'nome':
            # Validação do nome
            if not tela1.validar_nome(components['tf_nome'].current.value) and components['tf_nome'].current.value:
                raise ValueError("O nome não deve conter números")
            elif not components['tf_nome'].current.value:
                raise ValueError("Por favor preencha o seu nome.")
        elif data == 'telefone':
            # Validação do telefone
            if not tela1.validar_telefone(components['tf_telefone'].current.value) and components['tf_telefone'].current.value:
                raise ValueError("O telefonde deve ser no formato: (xx) xxxxx-xxxx")
            elif not components['tf_telefone'].current.value:
                raise ValueError("Por favor preencha o telefone.")
        elif data == 'cpf':
            # Validação do CPF
            if not tela1.validar_cpf(components['tf_cpf'].current.value) and components['tf_cpf'].current.value:
                raise ValueError("O CPF deve ser no formato: xxx.xxx.xxx-xx")
            elif not components['tf_cpf'].current.value:
                raise ValueError("Por favor preencha o seu CPF.")
        elif data == 'rg':
            # Validação do RG
            if not tela1.validar_rg(components['tf_rg'].current.value) and components['tf_rg'].current.value:
                raise ValueError("RG inválido(O RG possui deve exatamente 7 dígitos e não conter letras)")
            elif not components['tf_rg'].current.value:
                raise ValueError("Por favor preencha o seu RG.")
        elif data == 'email':
            # Validação do E-mail
            if not tela1.validar_email(components['tf_e-mail'].current.value) and components['tf_e-mail'].current.value:
                raise ValueError("E-mail inválido(formato correto: name@example.com ou name@example.com.br)")
            elif not components['tf_e-mail'].current.value:
                raise ValueError("Por favor preencha o seu email.")
        elif data == 'nascimento':
            # Validação da data de nascimento
            if not tela1.validar_nascimento(components['tf_nascimento'].current.value) and components['tf_nascimento'].current.value:
                raise ValueError("Data de nascimento inválida(formato: DD/MM/AAAA)")
            elif not components['tf_nascimento'].current.value:
                raise ValueError("Por favor preencha a sua data de nascimento.")
        elif data == 'endereco':
            if not tela1.validar_endereco(components['tf_endereço'].current.value) and components['tf_endereço'].current.value:
                raise ValueError("Endereço inválido")
            elif not components['tf_endereço'].current.value:
                raise ValueError("Por favor preencha o seu endereço.")
        else:
            raise ValueError("Data inválida")
    except ValueError as e:
        return str(e)
    else:
        return ''
    