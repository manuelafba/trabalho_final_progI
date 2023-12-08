import flet as ft
import control as c
import re
import base64

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

# image_holder = ft.Image(visible=False, fit=ft.ImageFit.CONTAIN)

# def handle_loaded_file(e: ft.FilePickerResultEvent):
#     print(e.files)
#     if e.files and len(e.files):
#         with open(e.files[0].path, 'rb') as r:
#             image_holder.src_base64 = base64.b64enconde(r.read()).decode('utf-8')
#             image_holder.visible = True
#             c.page.uptade()
#     #[{name, path, size}]
# file_picker = ft.FilePicker(on_result=handle_loaded_file)
# ft.page.overlay.append(file_picker)

def changetheme(e):
    c.page.theme_mode = "light" if c.page.theme_mode =="dark" else "dark"
    c.page.update()
 
    c.time.sleep(0.5)
 
    toggledarklight.selected = not toggledarklight.selected
 
    c.page.splash.visible = False
    c.page.update()

toggledarklight = ft.IconButton(
    on_click=changetheme,
    icon="dark_mode",
    selected_icon="light_mode",
    style=ft.ButtonStyle(
    color={"":ft.colors.BLACK,"selected":ft.colors.WHITE}))

def view():     
    return ft.View(
                "tela1",
                [                           
                    ft.Column(
                        [
                            ft.Row([ft.Container( content=ft.Text("Cadastro", size=20))],alignment=ft.MainAxisAlignment.CENTER),
                            ft.Column([ft.Row([
                                # image_holder,
                                ft.Container(content= 
                                ft.ElevatedButton(
                                text="Escolher foto", icon="image", on_click= None
                                # lambda _:file_picker.pick_files(allow_multiple=False, allowed_extensions=['jpg', 'jpeg', 'png'])
                                ))
                                ],alignment=ft.MainAxisAlignment.CENTER)#Container,
                                ]),
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
                                                        text="Cadastrar", 
                                                        icon="save", 
                                                        on_click= cadastrar
                                                    )#ElevatedButton   
                                    ),#Container
                                    ft.Container(
                                            content= ft.ElevatedButton(
                                                        text="Pesquisar", 
                                                        icon="search"
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
                    actions=[toggledarklight]                   
                ),    
            )
    
def cadastrar(e):

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
    c.page.update()

    # Se todos os campos forem válidos, escreva no arquivo CSV
    if validar_nome(nome) and validar_telefone(telefone) and validar_cpf(cpf) and validar_rg(rg) and validar_email(email) and validar_nascimento(nascimento) and validar_endereco(endereco):
        dados = [
            [nome, telefone, cpf, rg, endereco, nascimento, email, 'path']]

        # Abre o arquivo em modo de escrita
        with open('bd.csv', 'a') as arquivo:
            # arquivo.write('Nome,Telefone,CPF,RG,Endereco,Nascimento,E-mail,Upload de Foto\n')
            for linha in dados:
                arquivo.write(','.join(linha) + '\n')

        #Zera os TextFields
        components['tf_nome'].current.value = ''    
        components['tf_cpf'].current.value = ''
        components['tf_rg'].current.value = ''
        components['tf_telefone'].current.value = ''
        components['tf_endereço'].current.value = ''
        components['tf_nascimento'].current.value = ''
        components['tf_e-mail'].current.value = ''
        c.page.update()

def validar_nome(nome):
    # Verifica se o nome não contém números
    nome_pattern = re.compile(r'^[^\d]+$')
    return bool(nome_pattern.match(nome))

def validar_telefone(telefone):
    # Verifica se o telefone possui o formato (xx)xxxxx-xxxx ou (xx) xxxxx-xxxx
    telefone_pattern = re.compile(r'^\(\d{2}\) ?\d{5}-\d{4}$')
    return bool(telefone_pattern.match(telefone))

def validar_cpf(cpf):
    # Verifica se o CPF possui o formato 111.111.111-11
    cpf_pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$')
    return bool(cpf_pattern.match(cpf))

def validar_rg(rg):
    # Verifica se o RG possui exatamente 9 dígitos
    rg_pattern = re.compile(r'^\d{7}$')
    return bool(rg_pattern.match(rg))

def validar_email(email):
    email_pattern = re.compile(r'^\S+@\S+\.(com|com\.br)$')
    return bool(email_pattern.match(email))

def validar_nascimento(data):
    # Considerando o formato DD/MM/AAAA
    nascimento_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')
    return bool(nascimento_pattern.match(data))

def validar_endereco(endereco):
    # Validação simples de endereço
    return len(endereco) >= 5  # Exemplo: endereço deve ter pelo menos 5 caracteres

def error_message(data):
    try:
        if data == 'nome':
            # Validação do nome
            if not validar_nome(components['tf_nome'].current.value) and components['tf_nome'].current.value:
                raise ValueError("O nome não deve conter números")
            elif not components['tf_nome'].current.value:
                raise ValueError("Por favor preencha o seu nome.")
        elif data == 'telefone':
            # Validação do telefone
            if not validar_telefone(components['tf_telefone'].current.value) and components['tf_telefone'].current.value:
                raise ValueError("O telefonde deve ser no formato: (xx) xxxxx-xxxx")
            elif not components['tf_telefone'].current.value:
                raise ValueError("Por favor preencha o telefone.")
        elif data == 'cpf':
            # Validação do CPF
            if not validar_cpf(components['tf_cpf'].current.value) and components['tf_cpf'].current.value:
                raise ValueError("O CPF deve ser no formato: xxx.xxx.xxx-xx")
            elif not components['tf_cpf'].current.value:
                raise ValueError("Por favor preencha o seu CPF.")
        elif data == 'rg':
            # Validação do RG
            if not validar_rg(components['tf_rg'].current.value) and components['tf_rg'].current.value:
                raise ValueError("RG inválido(O RG possui deve exatamente 7 dígitos e não conter letras)")
            elif not components['tf_rg'].current.value:
                raise ValueError("Por favor preencha o seu RG.")
        elif data == 'email':
            # Validação do E-mail
            if not validar_email(components['tf_e-mail'].current.value) and components['tf_e-mail'].current.value:
                raise ValueError("E-mail inválido(formato correto: name@example.com ou name@example.com.br)")
            elif not components['tf_e-mail'].current.value:
                raise ValueError("Por favor preencha o seu email.")
        elif data == 'nascimento':
            # Validação da data de nascimento
            if not validar_nascimento(components['tf_nascimento'].current.value) and components['tf_nascimento'].current.value:
                raise ValueError("Data de nascimento inválida(formato: DD/MM/AAAA)")
            elif not components['tf_nascimento'].current.value:
                raise ValueError("Por favor preencha a sua data de nascimento.")
        elif data == 'endereco':
            if not validar_endereco(components['tf_endereço'].current.value) and components['tf_endereço'].current.value:
                raise ValueError("Endereço inválido")
            elif not components['tf_endereço'].current.value:
                raise ValueError("Por favor preencha o seu endereço.")
        else:
            raise ValueError("Data inválida")
    except ValueError as e:
        return str(e)
    else:
        return ''