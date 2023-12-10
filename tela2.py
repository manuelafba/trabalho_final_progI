import flet as ft
import control as c
import csv
import tela3

components = {
    'tabela': ft.Ref[ft.DataTable](),
    'tf_pesquisa': ft.Ref[ft.TextField](),
    # adicione todos os componentes da tela aqui
}

# Função para ler os dados do arquivo CSV
def ler_csv():
    with open('bd.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        # Adicionando a chave 'select' com o valor False para cada dicionário
        for cadastro in data:
            cadastro['selected'] = False
        return data

selected = []
cadastros = ler_csv()  # Carregar os dados do CSV
you_selected = ft.Column()

def view():
    
    return ft.View(
        "tela2",
        [
            ft.Column([ 
                    ft.Row([ft.Container( content=ft.Text("Área de Pesquisa de Cadastros", size=20))],alignment=ft.MainAxisAlignment.CENTER),
                    ft.TextField(ref=components['tf_pesquisa'], label='Pesquisar', on_change=pesquisar),
                    # ft.Row([fillNome, filltelefone, fillCPF, fillrg, fillendereco, fillnasciment, fillemail, fillacoes]),
                    ft.DataTable(
                    
                    columns=[
                        ft.DataColumn(ft.Text("Nome")),
                        ft.DataColumn(ft.Text("Telefone")),
                        ft.DataColumn(ft.Text("CPF")),
                        ft.DataColumn(ft.Text("RG")),
                        ft.DataColumn(ft.Text("Endereço")),
                        ft.DataColumn(ft.Text("Nascimento")),
                        ft.DataColumn(ft.Text("E-mail")),
                        ft.DataColumn(ft.Text("Actions")),
                        # ft.DataColumn(ft.Text("Upload de Foto")),
                    ],width=float('inf'),
                    ref=components['tabela'],
                ),
                ft.Row([
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Voltar para tela de cadastro",
                            on_click=navigate_to_tela1
                        )
                    ),
                    ft.Container(
                    content=ft.ElevatedButton(
                        text="Excluir selecionados",
                        on_click=removemultiple,
                    )
                ),
                ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],scroll=ft.ScrollMode.ALWAYS,
                        expand=True,),
        ],
        appbar=ft.AppBar(
            title=ft.Text("Sistema de cadastro",font_family="RobotoSlab",weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.colors.RED_900,
        ),
    )

def data_line(cadastro):
        return [
            ft.DataCell(ft.Text(cadastro['Nome'])),
            ft.DataCell(ft.Text(cadastro['Telefone'])),
            ft.DataCell(ft.Text(cadastro['CPF'])),
            ft.DataCell(ft.Text(cadastro['RG'])),
            ft.DataCell(ft.Text(cadastro['Endereco'])),
            ft.DataCell(ft.Text(cadastro['Nascimento'])),
            ft.DataCell(ft.Text(cadastro['E-mail'])),
            ft.DataCell(ft.Row([ft.Checkbox(value=cadastro['selected'],
                data=ft.Row([
                ft.Text(cadastro['Nome']),
                ft.Text(cadastro['Telefone']),
                ft.Text(cadastro['CPF']),
                ft.Text(cadastro['RG']),
                ft.Text(cadastro['Endereco']),
                ft.Text(cadastro['Nascimento']),
                ft.Text(cadastro['E-mail']),
                ]),
                on_change=this_seledted),
                ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_size=20,
        on_click=lambda e, cadastro=cadastro: atualizar(cadastro)
    )]))
]

def data_table():
    data_rows = [ft.DataRow(cells=data_line(cad)) for cad in cadastros]
    #print(data_rows)  # Adicionar este print para verificar as linhas de dados geradas
    return data_rows

def navigate_to_tela1(e):
    c.page.go('0')

def pesquisar(e):
    value = components['tf_pesquisa'].current.value.lower()
    filtered_rows = []

    for cad in cadastros:
        if value in cad['Nome'].lower() or value in cad['Telefone'] or value in cad['CPF'] or value in cad['RG'] or value in cad['Endereco'] or value in cad['Nascimento'] or value in cad['E-mail']:
            
            filtered_rows.append(data_line(cad))  

    components["tabela"].current.rows = [ft.DataRow(cells=row) for row in filtered_rows]
    c.page.update()

def this_seledted(e):
    select_name = ft.Text(e.control.data.controls[0].value)
    select_telefone = ft.Text(e.control.data.controls[1].value)
    select_cpf = ft.Text(e.control.data.controls[2].value)
    select_rg= ft.Text(e.control.data.controls[3].value)
    select_endereco = ft.Text(e.control.data.controls[4].value)
    select_nascimento = ft.Text(e.control.data.controls[5].value)
    select_email = ft.Text(e.control.data.controls[6].value)

    if e.control.value == True:
        you_selected.controls.append(ft.Row([select_name,select_telefone,select_cpf,select_rg,select_endereco,select_nascimento,select_email]))
    else:
        for c in you_selected.controls:
            if isinstance(c,ft.Row):
                if c.controls[0].value == select_name.value and c.controls[1].value == select_telefone.value:
                    you_selected.controls.remove(c)
                    break

def remove_selected_from_cadastros(selected_indices):
    global cadastros

    # Remover os itens selecionados da lista 'cadastros' pelos índices
    cadastros = [cad for idx, cad in enumerate(cadastros) if idx not in selected_indices]

def removemultiple(e):
    selected_indices = []

    # Coletar os índices dos itens selecionados em 'you_selected'
    for x in you_selected.controls:
        delete_name = x.controls[0].value
        delete_telefone = x.controls[1].value
        delete_cpf = x.controls[2].value
        delete_rg = x.controls[3].value
        delete_endereco = x.controls[4].value
        delete_nascimento = x.controls[5].value
        delete_email = x.controls[6].value

        for i in range(len(cadastros)):
            if (
                cadastros[i]['Nome'] == delete_name
                and cadastros[i]['Telefone'] == delete_telefone
                and cadastros[i]['CPF'] == delete_cpf
                and cadastros[i]['RG'] == delete_rg
                and cadastros[i]['Endereco'] == delete_endereco
                and cadastros[i]['Nascimento'] == delete_nascimento
                and cadastros[i]['E-mail'] == delete_email
            ):
                selected_indices.append(i)
                break

    # Remover os itens selecionados da lista 'cadastros'
    remove_selected_from_cadastros(selected_indices)

    # Atualizar a tabela com os dados restantes
    components["tabela"].current.rows = data_table()

    # Limpar you_selected após a exclusão
    you_selected.controls.clear()

    # Exibir um snackbar indicando sucesso na exclusão
    c.page.snack_bar = ft.SnackBar(
        ft.Text("Deletou com sucesso", size=20),
        duration=800,
        bgcolor="red"
    )

    c.page.snack_bar.open = True
    atualizar_csv(selected_indices)
    # Atualizar a página
    c.page.update()

import shutil

# Função para atualizar o arquivo CSV excluindo as linhas selecionadas
def atualizar_csv(selected_indices):
    with open('bd.csv', newline='') as csvfile, open('temp_bd.csv', 'w', newline='') as tempcsvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        writer = csv.DictWriter(tempcsvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Copiar as linhas, exceto as selecionadas, para o novo arquivo temporário
        for idx, row in enumerate(reader):
            if idx not in selected_indices:
                writer.writerow(row)

    # Substituir o arquivo original pelo novo arquivo temporário
    shutil.move('temp_bd.csv', 'bd.csv')
    global cadastros
    cadastros = ler_csv()  # Recarregar os dados do arquivo CSV após a exclusão

    # Atualizar a tabela com os dados recarregados
    components["tabela"].current.rows = data_table()
    c.page.update()

def atualizar(cadastro):
    # Utilize os dados do cadastro para atualização
    tela3.components['tf_nome'].current.value = cadastro['Nome']
    tela3.components['tf_telefone'].current.value = cadastro['Telefone']
    tela3.components['tf_cpf'].current.value = cadastro['CPF']
    tela3.components['tf_rg'].current.value = cadastro['RG']
    tela3.components['tf_endereço'].current.value = cadastro['Endereco']
    tela3.components['tf_nascimento'].current.value = cadastro['Nascimento']
    tela3.components['tf_e-mail'].current.value = cadastro['E-mail']
    tela3.selected_file_path = cadastro['Upload de Foto']
    tela3.uid = cadastro['id']

    # Navegue para a tela de edição (ou atualização)
    c.page.go('2')
