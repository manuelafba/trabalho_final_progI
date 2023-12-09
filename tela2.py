import flet as ft
import control as c
import csv

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
        return data


cadastros = ler_csv()  # Carregar os dados do CSV
def view():
    return ft.View(
        "tela2",
        [
            ft.Column([
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
                        # ft.DataColumn(ft.Text("Upload de Foto")),
                        ft.DataColumn(ft.Text("Ações")),
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
                ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],scroll=ft.ScrollMode.ALWAYS,
                        expand=True,),
        ],
        appbar=ft.AppBar(
            title=ft.Text("Sistema de cadastro"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
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
        # ft.DataCell(ft.Text(cadastro['Upload de Foto'])),
        ft.DataCell(
            ft.Row([
                ft.IconButton(
                    icon=ft.icons.EDIT,
                    icon_color="blue",
                    icon_size=20,
                    tooltip="Atualizar",
                    key=cadastro['CPF'],  # Corrigido para usar a chave correta 'CPF'
                    on_click=None
                ),
                ft.IconButton(
                    icon=ft.icons.REMOVE_CIRCLE,
                    icon_color="red",
                    icon_size=20,
                    tooltip="Remover",
                    key=cadastro['CPF'],  # Corrigido para usar a chave correta 'CPF'
                    on_click=None
                ),
            ])
        )
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

