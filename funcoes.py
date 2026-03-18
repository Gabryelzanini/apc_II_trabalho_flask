#Aqui ficara apenas as funções
import dicionarios
import random
from time import *
import os
import time
import sys
import imagens
import math
    
# Faz texto dentro de quadrados
largura = 32
def imprimir_linha(texto):
    # Calcula espaço restante para completar a largura
    espacos = largura - len(texto) - 2  # 2 por causa das barras '|'
    print('|' + texto + ' ' * espacos + '|')

# Texto com delay

delay=0.005
def print_com_delay(texto):
    for ch in texto:
        sleep(delay)
        print(ch, end='', flush=True)
# Apaga a última linha
def apagar_ultima_linha(tempo):
    sleep(tempo)
    sys.stdout.write('\x1b[1A')  # Sobe o cursor uma linha
    sys.stdout.write('\x1b[2K')  # Apaga a linha

#para ampulheta
def mostrar_ampulheta(textos):
    for item in textos:
        os.system('cls')
        texto = item[0]  # pegar a string dentro da sublista
        print(texto)
        time.sleep(1)

#====================================================================================
#Hospital
def hospital():
    dicionarios.atributos["Vida"] = dicionarios.atributos["Vida_Max"]


#Estatísticas
def ver_estatisticas():
    os.system("cls")
    print("=== Atributos do Jogador ===")
    for chave, valor in dicionarios.atributos.items():
        imprimir_linha(f"{chave}: {valor}")
    
    print("\n=== Monstros Abatidos ===")
    for monstro, stats in monstros.items():
        imprimir_linha(f"{monstro}: {stats['Abatidos']} abatidos")
    a = input("SAIR: ")
    os.system("cls")    

# Equipar
CAMPOS_ARMADURA = {"Defesa", "Tenacidade", "Evasão", "Chance_critico", "Critico", "Ação"}

def aplicar_bonus_item(item_nome, categoria, atributos):
    if not item_nome:
        return
    item = dicionarios.equipamentos[categoria].get(item_nome)
    if not item:
        return
    for chave in CAMPOS_ARMADURA:
        if chave in item and chave in atributos:
            atributos[chave] += item[chave]

def remover_bonus_item(item_nome, categoria, atributos):
    if not item_nome:
        return
    item = dicionarios.equipamentos[categoria].get(item_nome)
    if not item:
        return
    for chave in CAMPOS_ARMADURA:
        if chave in item and chave in atributos:
            atributos[chave] -= item[chave]

def aplicar_bonus_set(bonus_set, atributos):
    for chave, valor in bonus_set.items():
        if chave != "Descrição" and chave in atributos:
            atributos[chave] += valor

def remover_bonus_set(atributos):
    for set_nome, dados in dicionarios.setcompleto.items():
        if dados["Ativo"]:
            for chave, valor in dados["Bonus"].items():
                if chave != "Descrição" and chave in atributos:
                    atributos[chave] -= valor
            dados["Ativo"] = False
            dados["Bonus"] = {}

def escolher_equipar_armaduras():
    categorias = {
        "Capacete": "Capacetes",
        "Peitoral": "Peitorais",
        "Calça": "Calças"
    }

    def tem_bonus_set(equipado):
        if None in equipado.values():
            return False, None
        sets = []
        for slot, nome_item in equipado.items():
            for categoria, itens in dicionarios.equipamentos.items():
                if categoria == "BonusSet":
                    continue
                if nome_item in itens:
                    sets.append(itens[nome_item]["Set"])
        if sets and all(s == sets[0] for s in sets):
            return True, sets[0]
        return False, None

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n=== Menu de Equipar Armaduras ===")

        tem_bonus, set_atual = tem_bonus_set(dicionarios.equipado)
        if tem_bonus:
            print(f"✅ Set completo equipado: {set_atual.upper()}")
            bonus = dicionarios.equipamentos["BonusSet"].get(set_atual, {})
            for chave, valor in bonus.items():
                if chave != "Descrição":
                    print(f"{chave}: {valor}")
            if "Descrição" in bonus:
                print(f"Descrição: {bonus['Descrição']}")
            print()
        else:
            print("❌ Set incompleto. Nenhum bônus ativo.\n")

        print("Escolha o que deseja equipar:")
        for i, slot in enumerate(dicionarios.equipado.keys(), 1):
            atual = dicionarios.equipado[slot] if dicionarios.equipado[slot] else "Nenhum"
            print(f"{i}. {slot} (Atual: {atual})")
        print(f"{len(dicionarios.equipado) + 1}. Finalizar")

        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite um número válido.")
            continue

        if escolha == len(dicionarios.equipado) + 1:
            break

        if 1 <= escolha <= len(dicionarios.equipado):
            slot = list(dicionarios.equipado.keys())[escolha - 1]
            categoria = categorias[slot]

            opcoes = []
            for armadura_dict in dicionarios.armaduras_adquiridas.values():
                for nome_item in armadura_dict:
                    if nome_item in dicionarios.equipamentos[categoria]:
                        opcoes.append(nome_item)
                        

            os.system("cls" if os.name == "nt" else "clear")
            if not opcoes:
                print(f"Você não possui nenhum item para o slot {slot}.")
                input("Pressione Enter para continuar...")
                continue

            print(f"\n--- {slot.upper()} ---")
            for i, item in enumerate(opcoes, 1):
                print(f"{i}. {item}")
            print(f"{len(opcoes) + 1}. Cancelar")

            while True:
                try:
                    escolha_item = int(input(f"Escolha um {slot.lower()} para equipar: "))
                except ValueError:
                    print("Digite um número válido.")
                    continue

                if escolha_item == len(opcoes) + 1:
                    print(f"Cancelado equipar {slot}.")
                    break
                elif 1 <= escolha_item <= len(opcoes):
                    novo_item = opcoes[escolha_item - 1]
                    item_antigo = dicionarios.equipado[slot]
                    categoria_equip = categorias[slot]
                    
                    # Remover bônus de set atual antes de trocar item
                    remover_bonus_set(dicionarios.atributos)

                    # Remover bônus do item antigo
                    remover_bonus_item(item_antigo, categoria_equip, dicionarios.atributos)

                    # Aplicar bônus do novo item
                    aplicar_bonus_item(novo_item, categoria_equip, dicionarios.atributos)

                    # Equipar novo item
                    dicionarios.equipado[slot] = novo_item

                    input(f"{slot} equipado com: {novo_item}. Pressione Enter para continuar...")
                    break
                else:
                    print("Opção inválida.")
        else:
            print("Opção inválida.")

    # Após finalizar, verificar e aplicar bônus de set se completo
    os.system("cls" if os.name == "nt" else "clear")
    tem_bonus, set_usado = tem_bonus_set(dicionarios.equipado)
    if tem_bonus:
        bonus = dicionarios.equipamentos["BonusSet"].get(set_usado)
        if bonus:
            print(f"\n=== BÔNUS DE SET ATIVADO: {set_usado.upper()} ===")
            for chave, valor in bonus.items():
                if chave != "Descrição":
                    print(f"{chave}: {valor}")
            print(f"Descrição: {bonus.get('Descrição', '')}")

            # Aplicar bônus do set nos atributos
            aplicar_bonus_set(bonus, dicionarios.atributos)

            # Atualizar dicionário de sets
            nome_dict_set = f"Set_{set_usado}"
            if nome_dict_set in dicionarios.setcompleto:
                dicionarios.setcompleto[nome_dict_set]["Ativo"] = True
                dicionarios.setcompleto[nome_dict_set]["Bonus"] = bonus
                print(f"\n[Dicionário '{nome_dict_set}' ativado em setcompleto!]")
            else:
                print(f"\n[AVISO] Dicionário '{nome_dict_set}' não encontrado.")
        else:
            print("\nSet completo, mas nenhum bônus encontrado.")
    else:
        print("\n⚠️ Você equipou armaduras de sets diferentes ou incompletos. Sem bônus de set.")

#Inventario
def ver_inventario(jogador_id=1):
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n====== INVENTÁRIO ======\n")

        opcoes = [
            "Armas",
            "Armaduras",
            "Materiais",
            "Poções",
            "Equipar Armadura",
            "Sair"
        ]

        for i, nome in enumerate(opcoes, start=1):
            print(f"{i}. {nome}")

        try:
            escolha = int(input("\nEscolha uma categoria para visualizar: "))
        except ValueError:
            print("Digite um número válido.")
            input("Pressione Enter...")
            continue

        if escolha == 1:  # Armas
            os.system("cls")
            if not armas_adquiridas:
                print("\n🔸 Nenhuma arma adquirida.")
            else:
                print("\n--- ARMAS ---")
                for jogador, armas in armas_adquiridas.items():
                    print(f"\n({jogador}) Arma:")
                    for nome_arma, atributos in armas.items():
                        print(f"  🗡️ {nome_arma}")
                        for atributo, valor in atributos.items():
                            print(f"    {atributo}: {valor}")
            input("\nPressione Enter para voltar...")

        elif escolha == 2:  # Armaduras
            os.system("cls")
            if not dicionarios.armaduras_adquiridas:
                print("\n🔸 Nenhuma armadura adquirida.")
            else:
                print("\n--- ARMADURAS ---")
                for i, atributos in dicionarios.armaduras_adquiridas.items():
                    print(f"\n🛡️  {i}:", end="")
                    for nome, atributo in atributos.items():
                        print(f" {nome}: {atributo}")
            input("\nPressione Enter para voltar...")

        elif escolha == 3:  # Materiais
            os.system("cls")
            materiais = dicionarios.materiais_adquiridos
            if not materiais:
                print("\n🔸 Nenhum material adquirido.")
            else:
                print("\n--- MATERIAIS ---")
                for nome, quantidade in materiais.items():
                    print(f"{nome}: {quantidade}")
            input("\nPressione Enter para voltar...")

        elif escolha == 4:  # Poções
            os.system("cls")
            pocoes = dicionarios.pocoes_adquiridas
            if not pocoes:
                print("\n🔸 Nenhuma poção adquirida.")
            else:
                print("\n--- POÇÕES ---")
                for tipo, niveis in pocoes.items():
                    print(f"\n🧪 {tipo}")
                    for nivel, quantidade in niveis.items():
                        print(f"  {nivel}: {quantidade}")
            input("\nPressione Enter para voltar...")

        elif escolha == 5:  # Equipar Armadura
            escolher_equipar_armaduras()

        elif escolha == 6:  # Sair
            print("Saindo do inventário...")
            break

        else:
            print("Opção inválida.")
            input("Pressione Enter...")                          

#====================================================================================
# Mercado 
def mercado():
    while True:
        os.system("cls")
        print(f"Gold: {dicionarios.atributos["Ouro"]}")
        print_com_delay("Olá caro minion, desejas comprar algo com seu gold suado? \n(1) Comprar\n(2) Vender\n(3) Sair")
        
        try:
            _escolha = int(input("\nEu quero: "))

        except ValueError:
            print("Informe um número dentro das opções viáveis.")
        #Comprar
        if _escolha == 1:
            while True:
                os.system("cls")
                print_com_delay("O que deseja comprar?\n(1) Armas\n(2) Equipamentos\n(3) Poções\n(4) Materiais\n(5) Voltar\n")
                
                try:
                    _escolha = int(input("Eu quero: "))
            
                except ValueError:
                    print("Informe um número dentro das opções viáveis.")

                if _escolha == 1:  # Armas
                    while True:
                        os.system("cls")
                        print(f"Gold: {dicionarios.atributos['Ouro']}")
                        print_com_delay("=== Armas ===\n")

                        lista_armas = list(dicionarios.armas.keys())

                        for i, arma in enumerate(lista_armas, start=1):
                            print(f"({i}) {arma}")
                        print("(0) Voltar")

                        try:
                            _escolha = int(input("Eu quero: "))
                        except ValueError:
                            print("Informe um número dentro das opções viáveis.")
                            input()
                            continue

                        if _escolha == 0:
                            break

                        if 1 <= _escolha <= len(lista_armas):
                            os.system("cls")
                            item_escolhido = lista_armas[_escolha - 1]
                            atributos = dicionarios.armas[item_escolhido]
                            
                            print(f"\n=== {item_escolhido} ===")
                            for chave, valor in atributos.items():
                                print(f"{chave}: {valor}")

                            preco = atributos.get("Ouro", 0)
                            print(f"(1) Comprar ({preco} gold)")
                            print("(2) Voltar")

                            try:
                                comprar = int(input("Ação: "))
                            except ValueError:
                                print("Informe um número dentro das opções viáveis.")
                                input()
                                continue

                            if comprar == 2:
                                continue

                            elif comprar == 1:
                                try:
                                    quantidade = int(input("Quantidade: "))
                                    if quantidade <= 0:
                                        raise ValueError
                                except ValueError:
                                    print("Informe um número válido e maior que 0.")
                                    input()
                                    continue

                                custo_total = preco * quantidade
                                if dicionarios.atributos["Ouro"] >= custo_total:
                                    dicionarios.atributos["Ouro"] -= custo_total
                                    proximo_id = max(dicionarios.armas_adquiridas.keys(), default=0) + 1
                                    for i in range(quantidade):
                                        dicionarios.armas_adquiridas[proximo_id + i] = {
                                            item_escolhido: atributos.copy()   # .copy pra copiar sem referência compartilhada
                                        }
                                    print_com_delay(f"Você comprou {quantidade}x {item_escolhido}.")
                                else:
                                    print_com_delay("Gold insuficiente!")
                                input()

                        else:
                            print("Escolha inválida.")
                            input("Pressione Enter para continuar.") 
                # Equipamentos
                elif _escolha == 2:  
                    while True:
                        os.system("cls")
                        print(f"Gold: {dicionarios.atributos['Ouro']}")
                        print_com_delay("=== Equipamentos ===\n")

                        categorias = ["Capacetes", "Peitorais", "Calças"]

                        for i, categoria in enumerate(categorias, start=1):
                            print(f"({i}) {categoria}")
                        print("(0) Voltar")

                        try:
                            cat_escolhida = int(input("Escolha uma categoria: "))
                        except ValueError:
                            print("Informe um número dentro das opções viáveis.")
                            input()
                            continue

                        if cat_escolhida == 0:
                            break

                        if 1 <= cat_escolhida <= len(categorias):
                            categoria = categorias[cat_escolhida - 1]
                            equipamentos_disponiveis = list(dicionarios.equipamentos[categoria].keys())

                            while True:
                                os.system("cls")
                                print(f"Gold: {dicionarios.atributos['Ouro']}")
                                print(f"=== {categoria} ===\n")

                                for i, item in enumerate(equipamentos_disponiveis, start=1):
                                    print(f"({i}) {item}")
                                print("(0) Voltar")

                                try:
                                    eq_escolhido = int(input("Escolha um equipamento: "))
                                except ValueError:
                                    print("Informe um número dentro das opções viáveis.")
                                    input()
                                    continue

                                if eq_escolhido == 0:
                                    break

                                if 1 <= eq_escolhido <= len(equipamentos_disponiveis):
                                    os.system("cls")
                                    nome_item = equipamentos_disponiveis[eq_escolhido - 1]
                                    atributos = dicionarios.equipamentos[categoria][nome_item]

                                    print(f"\n=== {nome_item} ===")
                                    for chave, valor in atributos.items():
                                        print(f"{chave}: {valor}")

                                    preco = atributos.get("Ouro", 0)
                                    print(f"\n(1) Comprar ({preco} gold)")
                                    print("(2) Voltar")

                                    try:
                                        acao = int(input("Ação: "))
                                    except ValueError:
                                        print("Informe um número dentro das opções viáveis.")
                                        input()
                                        continue

                                    if acao == 2:
                                        continue

                                    elif acao == 1:
                                        try:
                                            quantidade = int(input("Quantidade: "))
                                            if quantidade <= 0:
                                                raise ValueError
                                        except ValueError:
                                            print("Informe um número válido e maior que 0.")
                                            input()
                                            continue

                                        custo_total = preco * quantidade
                                        if dicionarios.atributos["Ouro"] >= custo_total:
                                            dicionarios.atributos["Ouro"] -= custo_total
                                            proximo_id = max(dicionarios.armaduras_adquiridas.keys(), default=0) + 1
                                            for i in range(quantidade):
                                                dicionarios.armaduras_adquiridas[proximo_id + i] = {
                                                    nome_item: atributos.copy() # .copy aqui também para copiar sem referência compartilhada
                                                }
                                            print_com_delay(f"Você comprou {quantidade}x {nome_item}.")
                                        else:
                                            print_com_delay("Gold insuficiente!")
                                        input()

                                else:
                                    print("Escolha inválida.")
                                    input("Pressione Enter para continuar.")
                        else:
                            print("Categoria inválida.")
                            input("Pressione Enter para continuar.")
                # Poções
                elif _escolha == 3:
                    while True:
                        os.system("cls")
                        print(f"Gold: {dicionarios.atributos['Ouro']}")
                        print_com_delay("=== Poções ===\n")

                        tipos_pocao = {
                            1: "Cura",
                            2: "Força",}

                        for i, nome in tipos_pocao.items():
                            print(f"({i}) {nome}")
                        print("(0) Voltar")

                        try:
                            tipo_escolhido = int(input("Escolha um tipo de poção: "))
                        except ValueError:
                            print("Informe um número dentro das opções viáveis.")
                            input()
                            continue

                        if tipo_escolhido == 0:
                            break

                        if tipo_escolhido in tipos_pocao:
                            tipo_nome = tipos_pocao[tipo_escolhido]

                            while True:
                                os.system("cls")
                                print(f"Gold: {dicionarios.atributos['Ouro']}")
                                print_com_delay(f"=== Poções de {tipo_nome} ===\n")

                                niveis = {
                                    1: "Level 1",
                                    2: "Level 2",
                                    3: "Level 3"
                                }

                                for i, nivel_nome in niveis.items():
                                    print(f"({i}) {nivel_nome}")
                                print("(0) Voltar")

                                try:
                                    nivel_escolhido = int(input("Escolha o nível da poção: "))
                                except ValueError:
                                    print("Informe um número válido.")
                                    input()
                                    continue

                                if nivel_escolhido == 0:
                                    break

                                if nivel_escolhido in niveis:
                                    nivel_nome = niveis[nivel_escolhido]
                                    mapa_chaves = {
                                        "Cura": "cura_nivel_",
                                        "Força": "forca_nivel_",
                                        "RemoverEfeito": "remocao_de_efeito_nivel_"
                                    }

                                    chave_base = mapa_chaves.get(tipo_nome)
                                    chave_pocao = f"{chave_base}{nivel_escolhido}"


                                    if chave_pocao in dicionarios.pocoes:
                                        atributos = dicionarios.pocoes[chave_pocao]
                                        preco = atributos.get("Ouro", 0)

                                        os.system("cls")
                                        print(f"\n=== Poção: {tipo_nome} {nivel_nome} ===")
                                        for chave, valor in atributos.items():
                                            print(f"{chave}: {valor}")
                                        print(f"\n(1) Comprar ({preco} gold)")
                                        print("(2) Voltar")

                                        try:
                                            acao = int(input("Ação: "))
                                        except ValueError:
                                            print("Informe um número válido.")
                                            input()
                                            continue

                                        if acao == 2:
                                            continue
                                        elif acao == 1:
                                            try:
                                                quantidade = int(input("Quantidade: "))
                                                if quantidade <= 0:
                                                    raise ValueError
                                            except ValueError:
                                                print("Informe uma quantidade válida (maior que 0).")
                                                input()
                                                continue

                                            custo_total = preco * quantidade
                                            if dicionarios.atributos["Ouro"] >= custo_total:
                                                dicionarios.atributos["Ouro"] -= custo_total
                                                dicionarios.pocoes_adquiridas[tipo_nome][nivel_nome] += quantidade
                                                print_com_delay(f"Você comprou {quantidade}x Poção {tipo_nome} {nivel_nome}.")
                                            else:
                                                print_com_delay("Gold insuficiente!")
                                            input()
                                    else:
                                        print("Poção não encontrada.")
                                        input()
                                else:
                                    print("Nível inválido.")
                                    input()
                        else:
                            print("Tipo de poção inválido.")
                            input()
                 # Materiais
                elif _escolha == 4: 
                    while True:
                        os.system("cls")
                        print(f"Gold: {dicionarios.atributos['Ouro']}")
                        print_com_delay("=== Materiais ===\n")

                        lista_materiais = list(dicionarios.materiais.keys())

                        for i, material in enumerate(lista_materiais, start=1):
                            preco = dicionarios.materiais[material]["Preço"]
                            print(f"({i}) {material} - {preco} gold")
                        print("(0) Voltar")

                        try:
                            mat_escolhido = int(input("Escolha um material: "))
                        except ValueError:
                            print("Informe um número dentro das opções viáveis.")
                            input()
                            continue

                        if mat_escolhido == 0:
                            break

                        if 1 <= mat_escolhido <= len(lista_materiais):
                            material_nome = lista_materiais[mat_escolhido - 1]
                            preco = dicionarios.materiais[material_nome]["Preço"]

                            try:
                                quantidade = int(input(f"Quantidade de {material_nome} que deseja comprar: "))
                                if quantidade <= 0:
                                    raise ValueError
                            except ValueError:
                                print("Informe uma quantidade válida (maior que 0).")
                                input()
                                continue

                            custo_total = preco * quantidade
                            if dicionarios.atributos["Ouro"] >= custo_total:
                                dicionarios.atributos["Ouro"] -= custo_total
                                dicionarios.materiais_adquiridos[material_nome] += quantidade
                                print_com_delay(f"Você comprou {quantidade}x {material_nome}.")
                            else:
                                print_com_delay("Gold insuficiente!")
                            input()

                        else:
                            print("Escolha inválida.")
                            input("Pressione Enter para continuar.")
                elif _escolha == 5: # Voltar
                    break
        #Venda
        elif _escolha == 2:
            while True:
                os.system("cls")
                print(f"Gold: {dicionarios.atributos['Ouro']}")
                print_com_delay("=== Venda de Itens ===\n")
                print("(1) Armas")
                print("(2) Armaduras")
                print("(3) Materiais")
                print("(4) Poções")
                print("(0) Voltar")

                try:
                    categoria = int(input("O que deseja vender? "))
                except ValueError:
                    print("Informe uma opção válida.")
                    input()
                    continue

                if categoria == 0:
                    break

                elif categoria == 1:  # Vender Armas
                    if not dicionarios.armas_adquiridas:
                        print("Você não possui armas para vender.")
                        input()
                        continue

                    while True:
                        os.system("cls")
                        print("=== Armas Disponíveis ===")
                        for id_item, arma in dicionarios.armas_adquiridas.items():
                            nome = list(arma.keys())[0]
                            print(f"ID: {id_item} | {nome} | Valor de venda: {arma[nome]['Ouro'] // 2} gold")
                        print("(0) Voltar")

                        try:
                            id_venda = int(input("Digite o ID da arma que deseja vender: "))
                        except ValueError:
                            print("ID inválido.")
                            input()
                            continue

                        if id_venda == 0:
                            break

                        if id_venda in dicionarios.armas_adquiridas:
                            nome_arma = list(dicionarios.armas_adquiridas[id_venda].keys())[0]
                            valor = dicionarios.armas_adquiridas[id_venda][nome_arma]["Ouro"] // 2
                            dicionarios.atributos["Ouro"] += valor
                            del dicionarios.armas_adquiridas[id_venda]
                            print_com_delay(f"Você vendeu {nome_arma} por {valor} gold.")
                            input()
                        else:
                            print("ID não encontrado.")
                            input()

                elif categoria == 2:  # Vender Armaduras
                    if not dicionarios.armaduras_adquiridas:
                        print("Você não possui armaduras para vender.")
                        input()
                        continue

                    while True:
                        os.system("cls")
                        print("=== Armaduras Disponíveis ===")
                        for id_item, armadura in dicionarios.armaduras_adquiridas.items():
                            nome = list(armadura.keys())[0]
                            print(f"ID: {id_item} | {nome} | Valor de venda: {armadura[nome]['Ouro'] // 2} gold")
                        print("(0) Voltar")

                        try:
                            id_venda = int(input("Digite o ID da armadura que deseja vender: "))
                        except ValueError:
                            print("ID inválido.")
                            input()
                            continue

                        if id_venda == 0:
                            break

                        if id_venda in dicionarios.armaduras_adquiridas:
                            nome_item = list(dicionarios.armaduras_adquiridas[id_venda].keys())[0]
                            valor = dicionarios.armaduras_adquiridas[id_venda][nome_item]["Ouro"] // 2
                            dicionarios.atributos["Ouro"] += valor
                            del dicionarios.armaduras_adquiridas[id_venda]
                            print_com_delay(f"Você vendeu {nome_item} por {valor} gold.")
                            input()
                        else:
                            print("ID não encontrado.")
                            input()

                elif categoria == 3:  # Vender Materiais
                    while True:
                        os.system("cls")
                        print("=== Materiais ===")
                        lista_materiais = list(dicionarios.materiais_adquiridos.keys())
                        for i, nome in enumerate(lista_materiais, start=1):
                            quantidade = dicionarios.materiais_adquiridos[nome]
                            preco = dicionarios.materiais[nome]["Preço"] // 2
                            print(f"({i}) {nome} | Quantidade: {quantidade} | Venda: {preco} gold cada")
                        print("(0) Voltar")

                        try:
                            escolha = int(input("Escolha um material para vender: "))
                        except ValueError:
                            print("Escolha inválida.")
                            input()
                            continue

                        if escolha == 0:
                            break

                        if 1 <= escolha <= len(lista_materiais):
                            nome_mat = lista_materiais[escolha - 1]
                            try:
                                quantidade = int(input(f"Quantidade de {nome_mat} para vender: "))
                                if quantidade <= 0 or quantidade > dicionarios.materiais_adquiridos[nome_mat]:
                                    raise ValueError
                            except ValueError:
                                print("Quantidade inválida.")
                                input()
                                continue

                            valor = (dicionarios.materiais[nome_mat]["Preço"] // 2) * quantidade
                            dicionarios.atributos["Ouro"] += valor
                            dicionarios.materiais_adquiridos[nome_mat] -= quantidade
                            print_com_delay(f"Você vendeu {quantidade}x {nome_mat} por {valor} gold.")
                            input()
                        else:
                            print("Escolha inválida.")
                            input()

                elif categoria == 4:  # Vender Poções
                    while True:
                        os.system("cls")
                        print("=== Poções ===")
                        tipos = {
                            "Cura": "cura_nivel_",
                            "Força": "forca_nivel_",
                            "RemoverEfeito": "remocao_de_efeito_nivel_"}

                        index_map = {}
                        idx = 1
                        for tipo, base in tipos.items():
                            for lvl in range(1, 4):
                                nome = f"{tipo} - Level {lvl}"
                                quantidade = dicionarios.pocoes_adquiridas[tipo][f"Level {lvl}"]
                                preco = dicionarios.pocoes[f"{base}{lvl}"]["Ouro"] // 2
                                print(f"({idx}) {nome} | Quantidade: {quantidade} | Venda: {preco} gold cada")
                                index_map[idx] = (tipo, lvl)
                                idx += 1
                        print("(0) Voltar")

                        try:
                            escolha = int(input("Escolha a poção para vender: "))
                        except ValueError:
                            print("Escolha inválida.")
                            input()
                            continue

                        if escolha == 0:
                            break

                        if escolha in index_map:
                            tipo, lvl = index_map[escolha]
                            chave = f"Level {lvl}"
                            base = tipos[tipo]
                            if dicionarios.pocoes_adquiridas[tipo][chave] == 0:
                                print("Você não possui essa poção.")
                                input()
                                continue

                            try:
                                quantidade = int(input(f"Quantidade de {tipo} {chave} para vender: "))
                                if quantidade <= 0 or quantidade > dicionarios.pocoes_adquiridas[tipo][chave]:
                                    raise ValueError
                            except ValueError:
                                print("Quantidade inválida.")
                                input()
                                continue

                            valor = (dicionarios.pocoes[f"{base}{lvl}"]["Ouro"] // 2) * quantidade
                            dicionarios.atributos["Ouro"] += valor
                            dicionarios.pocoes_adquiridas[tipo][chave] -= quantidade
                            print_com_delay(f"Você vendeu {quantidade}x Poção {tipo} {chave} por {valor} gold.")
                            input()
                        else:
                            print("Escolha inválida.")
                            input()

        elif _escolha == 3: # Sair
            return
        
        else:
            print("Escolha inválida!")
            input()

#====================================================================================
#encantamento
class EncantadorDeArmas:
    def __init__(self, id_arma):
        self.id = id_arma
        self.armas = dicionarios.armas_adquiridas
        self.encantamentos_disponiveis = dicionarios.encantamentos
        self.atributos = dicionarios.atributos

        if id_arma not in self.armas:
            raise ValueError(f"Arma com ID {id_arma} não encontrada.")

        # Pega o nome da arma (ex: "Espada Curta")
        self.nome_arma = next(iter(self.armas[self.id]))

    def encantar(self, nome_encantamento):
        arma = self.armas[self.id][self.nome_arma]

        if nome_encantamento not in self.encantamentos_disponiveis:
            print(f"Encantamento '{nome_encantamento}' não é válido.")
            sleep(2)
            return

        if arma["Encantamento"]:
            print(f"A arma '{self.nome_arma}' já está encantada com '{arma['Encantamento']}'. Não é possível substituir o encantamento.")
            sleep(2)
            return

        if self.atributos["Ouro"] < 10:
            print("Você não tem ouro suficiente para encantar a arma. (Custa 10 de ouro)")
            sleep(2)
            return

        # Desconta o ouro
        self.atributos["Ouro"] -= 10
        arma["Encantamento"] = nome_encantamento
        print(f"A arma '{self.nome_arma}' foi encantada com '{nome_encantamento}'. (-10 de ouro)")
        print(f"Ouro restante: {self.atributos['Ouro']}")
        sleep(2)

    def desencantar(self):
        arma = self.armas[self.id][self.nome_arma]

        if not arma["Encantamento"]:
            print(f"A arma '{self.nome_arma}' não possui encantamento para remover.")
            sleep(2)
            return

        if self.atributos["Ouro"] < 5:
            print("Você não tem ouro suficiente para remover o encantamento. (Custa 5 de ouro)")
            sleep(2)
            return

        # Desconta o ouro
        self.atributos["Ouro"] -= 5
        arma["Encantamento"] = ""
        print(f"Encantamento removido da arma '{self.nome_arma}'. (-5 de ouro)")
        print(f"Ouro restante: {self.atributos['Ouro']}")
        sleep(2)

    def mostrar_encantamento(self):
        arma = self.armas[self.id][self.nome_arma]
        encantamento = arma["Encantamento"]
        if encantamento:
            print(f"A arma '{self.nome_arma}' está encantada com '{encantamento}'.")
            sleep(2)
        else:
            print(f"A arma '{self.nome_arma}' não possui encantamento.")
            sleep(2)

def listar_armas():
    armas = dicionarios.armas_adquiridas
    nomes = []
    for id_arma, conteudo in armas.items():
        nome_arma = next(iter(conteudo))
        nomes.append((id_arma, nome_arma))
    return nomes

def listar_encantamentos():
    return list(dicionarios.encantamentos.keys())

def menu_magia():
    while True:
        os.system("cls")
        print("\nBem-vindo à Sala de Encantamentos!")
        print(f"Ouro atual: {dicionarios.atributos['Ouro']}")
        print("(1) Encantar arma, Custará 10 de ouro")
        print("(2) Desencantar arma, Custará 5 de ouro")
        print("(3) Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            armas_disponiveis = listar_armas()
            os.system("cls")
            print("\nEscolha uma arma para encantar:")
            for i, (id_arma, nome) in enumerate(armas_disponiveis, start=1):
                dados_arma = dicionarios.armas_adquiridas[id_arma][nome]
                encantamento = dados_arma["Encantamento"]
                status = f"Encantada com '{encantamento}'" if encantamento else "Sem encantamento"
                print(f"({i}) {nome} - {status}")
            print("(0) Voltar")


            opcao = input("Opção: ")

            if opcao == '0':
                continue

            try:
                indice = int(opcao) - 1
                id_arma = armas_disponiveis[indice][0]
                encantador = EncantadorDeArmas(id_arma)
            except (ValueError, IndexError):
                print("Opção inválida.")
                continue

            encantamentos = listar_encantamentos()

            os.system("cls")
            print("\nEscolha um encantamento:")
            for i, nome in enumerate(encantamentos, start=1):
                print(f"({i}) {nome}")
            print("(0) Voltar")

            opcao_enc = input("Opção: ")

            if opcao_enc == '0':
                continue

            try:
                indice_enc = int(opcao_enc) - 1
                nome_encantamento = encantamentos[indice_enc]
                encantador.encantar(nome_encantamento)
                # encantador.mostrar_encantamento()
            except (ValueError, IndexError):
                print("Encantamento inválido.")

        elif escolha == '2':
            armas_disponiveis = listar_armas()
            os.system("cls")
            print("\nEscolha uma arma para desencantar:")
            for i, (id_arma, nome) in enumerate(armas_disponiveis, start=1):
                dados_arma = dicionarios.armas_adquiridas[id_arma][nome]
                encantamento = dados_arma["Encantamento"]
                status = f"Encantada com '{encantamento}'" if encantamento else "Sem encantamento"
                print(f"({i}) {nome} - {status}")
            print("(0) Voltar")


            opcao = input("Opção: ")

            if opcao == '0':
                continue

            try:
                indice = int(opcao) - 1
                id_arma = armas_disponiveis[indice][0]
                encantador = EncantadorDeArmas(id_arma)
                encantador.desencantar()
                # encantador.mostrar_encantamento()
            except (ValueError, IndexError):
                print("Opção inválida.")

        elif escolha == '3':
            print("Saindo... Até a próxima!")
            sleep(2)
            break
        else:
            print("Opção inválida. Tente novamente.")
            sleep(2)

#====================================================================================
# Forja
def forja():
    while True:
        os.system("cls")
        print_com_delay("Bom dia meu bom cliente, o que precisa hoje?")
        print("\n(1) Melhorar"
            "\n(2) Reparar"
            "\n(3) Sair")

        try:
            _escolha = int(input("Eu quero: "))
        except ValueError:
            print("Informe um número dentro das opções viáveis.")
            continue

        if _escolha == 1: # Melhorar
            while True:
                os.system("cls")
                print_com_delay("=== Melhorar ===\n")
                for material, quantidade in dicionarios.materiais_adquiridos.items():
                    print(f"{material}: {quantidade}")

                for id_item, arma in dicionarios.armas_adquiridas.items():
                    nome = next(iter(arma))
                    print(f"({id_item}) | {nome} | Qualidade: {arma[nome]['Qualidade']}")
                print("(0) Voltar")

                try:
                    _escolha = int(input("Eu quero: "))
                except ValueError:
                    print("Informe um número dentro das opções viáveis.")
                    continue

                if _escolha in dicionarios.armas_adquiridas:
                    id_arma = _escolha
                    arma = dicionarios.armas_adquiridas[_escolha]
                    nome = next(iter(arma))
                    atributos = arma[nome]

                    os.system("cls")

                    if atributos["Qualidade"] == dicionarios.melhoria_por_nivel["Melhoria Máxima"]:
                        print_com_delay("Sua arma já está na qualidade máxima!")
                        input()
                        continue
                    
                    dur_max = dicionarios.armas[nome]["Durabilidade"] + atributos["Qualidade"] * dicionarios.melhoria_por_nivel["Durabilidade"]
                    print_com_delay(f"=== {nome} ===\n")
                    print(f"Durabilidade = {atributos["Durabilidade"]}/{dur_max} --> {dur_max + dicionarios.melhoria_por_nivel["Durabilidade"]}",
                        f"\nDano = {atributos["Dano"]} --> {atributos["Dano"] + dicionarios.melhoria_por_nivel["Dano"]}",
                        f"\nChance Critico = {atributos["Chance Critico"]} --> {atributos["Chance Critico"] + dicionarios.melhoria_por_nivel["Chance Critico"]}",
                        f"\nEncantamento = {atributos["Encantamento"] if atributos["Encantamento"] else "Nenhum"}",
                        f"\nQualidade = {atributos["Qualidade"]} --> {atributos["Qualidade"] + 1}",
                        f"\nAção = {atributos["Ação"]}"
                        f"\n\n=== Requisitos ===")
                    for level, requisitos in dicionarios.req_melhoria.items():
                        if atributos["Qualidade"] + 1 == level:
                            for material, quantidade in requisitos.items():
                                if quantidade > 0:
                                    print(f"{material}: {quantidade}")
                    
                    print("\n(1) Melhorar\n(2) Voltar")

                    try:
                        _escolha = int(input("Eu quero: "))
                    except ValueError:
                        print("Informe um número dentro das opções viáveis.")
                        continue

                    if _escolha == 1: 
                        proximo_level = atributos["Qualidade"] + 1
                        requisitos = dicionarios.req_melhoria[proximo_level]
                        pode_upar = True

                        os.system("cls")
                        for material, quantidade_necessaria in requisitos.items():
                            if dicionarios.materiais_adquiridos.get(material, 0) < quantidade_necessaria:
                                print_com_delay(f"Faltam {quantidade_necessaria - dicionarios.materiais_adquiridos.get(material, 0)} de {material}\n")
                                pode_upar = False
                             
                        if pode_upar == False:
                            input()
                            continue
                        
                        for material in requisitos:
                            dicionarios.materiais_adquiridos[material] -= requisitos[material]
                        

                        dicionarios.armas_adquiridas[id_arma][nome]["Durabilidade"] += dicionarios.melhoria_por_nivel["Durabilidade"]
                        dicionarios.armas_adquiridas[id_arma][nome]["Dano"] += dicionarios.melhoria_por_nivel["Dano"]
                        dicionarios.armas_adquiridas[id_arma][nome]["Chance Critico"] += dicionarios.melhoria_por_nivel["Chance Critico"]
                        dicionarios.armas_adquiridas[id_arma][nome]["Qualidade"] += 1

                        print_com_delay(f"Parabéns por upar {nome} para a Qualidade {proximo_level}!")
                        input()
               

                    elif _escolha == 2:
                        continue

                elif _escolha == 0:
                    break

        elif _escolha == 2: # Reparar
            while True:
                os.system("cls")
                print_com_delay("=== Reparar ===\n")
                for id_item, arma in dicionarios.armas_adquiridas.items():
                    nome = next(iter(arma))
                    atributos = arma[nome]
                    dur_max = dicionarios.armas[nome]["Durabilidade"] + atributos["Qualidade"] * dicionarios.melhoria_por_nivel["Durabilidade"]
                    print(f"({id_item}) | {nome} | Durabilidade: {atributos['Durabilidade']}/{dur_max}")
                print("(0) Voltar")

                try:
                    _escolha = int(input("Qual arma deseja reparar? "))
                except ValueError:
                    print("Informe um número dentro das opções viáveis.")
                    continue

                if _escolha == 0:
                    break

                if _escolha in dicionarios.armas_adquiridas:
                    id_arma = _escolha
                    arma = dicionarios.armas_adquiridas[id_arma]
                    nome = next(iter(arma))
                    atributos = arma[nome]

                    dur_max = dicionarios.armas[nome]["Durabilidade"] + atributos["Qualidade"] * dicionarios.melhoria_por_nivel["Durabilidade"]
                    dur_atual = atributos["Durabilidade"]

                    if dur_atual >= dur_max:
                        print_com_delay("A arma já está com durabilidade máxima!")
                        input()
                        continue

                    custo_por_ponto = 2  # ferro por ponto de durabilidade
                    dur_necessaria = dur_max - dur_atual
                    custo_total = dur_necessaria * custo_por_ponto

                    print(f"\nDeseja reparar a arma {nome} de {dur_atual}/{dur_max} por {custo_total} de ferro?")
                    print(f"Ferro disponível: {dicionarios.materiais_adquiridos["Ferro"]}")
                    print("\n(1) Reparar")
                    print("(2) Voltar")

                    try:
                        escolha = int(input("Eu quero: "))
                    except ValueError:
                        print("Informe uma opção válida.")
                        continue

                    if escolha == 1:
                        if dicionarios.materiais_adquiridos["Ferro"] >= custo_total:
                            dicionarios.materiais_adquiridos["Ferro"] -= custo_total
                            dicionarios.armas_adquiridas[id_arma][nome]["Durabilidade"] = dur_max
                            print_com_delay(f"{nome} foi completamente reparada!")
                        else:
                            print_com_delay("Você não tem ferro suficiente.")
                        input()

                    elif escolha == 2:
                        continue
                    
        elif _escolha == 3: # Sair
            break
    
    
#==============================================================================================
#Batalha

import random
from dicionarios import armas_adquiridas, atributos
from dicionarios import monstros, armas, armas_adquiridas, materiais_adquiridos
from dicionarios import monstros
from dicionarios import armas_adquiridas, atributos, encantamentos, pocoes_adquiridas, pocoes
class Arma:
    def __init__(self, nome_arma: str):
        self.nome = nome_arma
        self.id_arma, self.dados = self._buscar_dados_arma(nome_arma)
        if self.dados is None:
            raise ValueError(f"Arma '{nome_arma}' não encontrada.")

        self._durabilidade = self.dados["Durabilidade"]

    def _buscar_dados_arma(self, nome_arma: str):
        for id_arma, arma_info in armas_adquiridas.items():
            if nome_arma in arma_info:
                return id_arma, arma_info[nome_arma]
        return None, None

    @property
    def encantamento(self):
        return self.dados["Encantamento"]

    @property
    def chance_critico(self):
        return self.dados["Chance Critico"] + atributos.get("Chance_critico", 0)

    @property
    def critico_multiplicador(self):
        return atributos.get("Critico", 1.5)

    @property
    def acao(self):
        return self.dados["Ação"]

    @property
    def durabilidade(self):
        return self._durabilidade
    
    def calcular_dano(self, inimigo=None, jogador=None):
        if self._durabilidade <= 0:
            print(f"A arma '{self.nome}' está quebrada e será removida.")
            self.remover_do_inventario()
            return 0

        base_dano = self.dados["Dano"]
        ataque = jogador.ataque_total() if jogador else atributos.get("Ataque", 0)
        dano_total = base_dano + ataque

        critico = random.randint(1, 100) <= self.chance_critico
        dano_final = round(dano_total * self.critico_multiplicador, 2) if critico else dano_total

        # Reduz durabilidade
        self._durabilidade -= 1
        self._atualizar_durabilidade_no_dicionario()

        # Verifica quebra
        if self._durabilidade == 0:
            print(f"A arma '{self.nome}' quebrou e foi removida do inventário.")
            self.remover_do_inventario()

        # Tenta aplicar encantamento
        self._tentar_aplicar_encantamento(inimigo, dano_final, jogador)

        return dano_final
    
    def _tentar_aplicar_encantamento(self, inimigo, dano_final, jogador):
        nome_encantamento = self.dados.get("Encantamento")
        if not nome_encantamento:
            return  # Sem encantamento

        encantamento = encantamentos.get(nome_encantamento)
        if not encantamento:
            return  # Encantamento inválido

        chance = encantamento.get("ChanceAtivação", 0)
        if random.randint(1, 100) > chance:
            return  # Não ativou

        print(f"Encantamento '{nome_encantamento}' ativado!")

        # Se for Roubar Vida, aplica direto no jogador (cura), não no inimigo
        if nome_encantamento == "Roubar Vida" and jogador:
            porcentagem = encantamento.get("PorcentagemRoubo", 50)
            vida_roubada = int(dano_final * (porcentagem / 100))
            jogador.vida = min(jogador.vida + vida_roubada, jogador.vida_max)
            print(f"Você roubou {vida_roubada} de vida!")
            return  # Não aplica efeito no inimigo

        # Aplica o efeito no inimigo
        if inimigo:
            # Garante que "Efeito negativo" seja um dicionário
            if "Efeito negativo" not in inimigo.dados or not isinstance(inimigo.dados["Efeito negativo"], dict):
                inimigo.dados["Efeito negativo"] = {}

            efeitos = inimigo.dados["Efeito negativo"]

            # Se o efeito já existe, aumenta a carga
            if nome_encantamento in efeitos:
                efeitos[nome_encantamento] += 1
                print(f"{nome_encantamento} agora tem {efeitos[nome_encantamento]} carga(s).")
            else:
                efeitos[nome_encantamento] = 1
                print(f"{nome_encantamento} foi aplicado com 1 carga.")
    
    def _atualizar_durabilidade_no_dicionario(self):
        """Atualiza o valor da durabilidade no dicionário original."""
        try:
            armas_adquiridas[self.id_arma][self.nome]["Durabilidade"] = self._durabilidade
        except KeyError:
            pass  # Já foi removida ou não existe mais

    def remover_do_inventario(self):
        # Remove a arma do dicionário original
        if self.id_arma in armas_adquiridas:
            if self.nome in armas_adquiridas[self.id_arma]:
                del armas_adquiridas[self.id_arma][self.nome]
                # Se não restar nenhuma arma nesse ID, remove o ID também
                if not armas_adquiridas[self.id_arma]:
                    del armas_adquiridas[self.id_arma]
            print(f"Arma '{self.nome}' removida com sucesso do inventário.")

    def __str__(self):
        return (
            f"Arma: {self.nome}\n"
            f"  Durabilidade: {self.durabilidade}\n"
            f"  Chance Crítico Total: {self.chance_critico}%\n"
            f"  Encantamento: {self.encantamento or 'Nenhum'}\n"
            f"  Ação: {self.acao}"
        )





import random
from dicionarios import monstros, materiais_adquiridos, armas_adquiridas, armas, encantamentos


class Monstro:
    def __init__(self, nome: str):
        self.nome = nome
        self.dados = monstros.get(nome)
        if not self.dados:
            raise ValueError(f"Monstro '{nome}' não encontrado.")
        # Garante que o campo "Efeito negativo" seja um dicionário
        if "Efeito negativo" not in self.dados or not isinstance(self.dados["Efeito negativo"], dict):
            self.dados["Efeito negativo"] = {}

    @property
    def vida(self):
        return self.dados["Vida"]

    @property
    def defesa(self):
        return self.dados["Defesa"]

    def defender(self):
        return self.defesa * 5

    def receber_dano(self, dano: int):
        defesa = self.defesa() if callable(self.defesa) else self.defesa
        dano_real = max(dano - defesa, 0)
        self.dados["Vida"] = max(self.dados["Vida"] - dano_real, 0)
        print(f"{self.nome} recebeu {dano_real} de dano (reduzido pela defesa). Vida restante: {self.dados['Vida']}")

    @property
    def critico(self):
        return self.dados["Critico"]

    @property
    def ouro(self):
        return self.dados["Ouro"]

    @property
    def xp(self):
        return self.dados["XP"]

    @property
    def drops(self):
        return self.dados["Drops"]

    @property
    def abatidos(self):
        return self.dados["Abatidos"]

    @property
    def efeitos_negativos(self):
        return self.dados.get("Efeito negativo", {})

    def dano(self):
        critico_ativo = random.randint(1, 100) <= self.critico
        dano_base = self.dados["Dano"]
        dano_final = dano_base * 2 if critico_ativo else dano_base
        print(f"{'Dano CRÍTICO!' if critico_ativo else 'Dano normal.'} ({dano_final})")
        return dano_final

    def modificar_dano_com_efeitos(self, dano):
        if "Gelo" in self.efeitos_negativos:
            qtd = self.efeitos_negativos["Gelo"]
            reducao = encantamentos["Gelo"]["DanoReduzidoPorAplicação"] * qtd
            dano = max(0, dano - reducao)
            print(f"{self.nome} teve seu dano reduzido em {reducao} por Gelo.")
            self.efeitos_negativos["Gelo"] -= 1
            if self.efeitos_negativos["Gelo"] <= 0:
                self.remover_efeito_negativo("Gelo")
                print("O efeito de Gelo se dissipou.")
        return dano

    def aplicar_efeitos_apos_ataque(self):
        if "Envenenamento" in self.efeitos_negativos:
            qtd = self.efeitos_negativos["Envenenamento"]
            dano_base = encantamentos["Envenenamento"]["DanoPorTurno"]
            dano = dano_base * qtd
            self.dados["Vida"] = max(0, self.dados["Vida"] - dano)
            print(f"{self.nome} sofre {dano} de dano por Envenenamento! Vida: {self.dados['Vida']}")
            
            # Reduz 1 carga local
            self.efeitos_negativos["Envenenamento"] -= 1
            if self.efeitos_negativos["Envenenamento"] <= 0:
                self.remover_efeito_negativo("Envenenamento")
                print("O efeito de Envenenamento se dissipou.")


        if "Queimadura" in self.efeitos_negativos:
            qtd = self.efeitos_negativos["Queimadura"]
            dano_base = encantamentos["Queimadura"]["DanoPorTurno"]
            dano = dano_base * qtd
            self.dados["Vida"] = max(0, self.dados["Vida"] - dano)
            print(f"{self.nome} sofre {dano} de dano por Queimadura! Vida: {self.dados['Vida']}")

            # 🔥 Queimadura não reduz carga!


    def aplicar_efeitos_ao_receber_dano(self):
        if "Sangramento" in self.efeitos_negativos:
            qtd = self.efeitos_negativos["Sangramento"]
            dano_base = encantamentos["Sangramento"]["DanoCausadoPorAtivaçao"]
            dano = dano_base * qtd
            self.dados["Vida"] = max(0, self.dados["Vida"] - dano)
            print(f"{self.nome} sofre {dano} de dano por Sangramento! Vida: {self.dados['Vida']}")


    def adicionar_efeito_negativo(self, efeito: str):
        if efeito not in self.efeitos_negativos:
            self.efeitos_negativos[efeito] = 1
        else:
            self.efeitos_negativos[efeito] += 1
        print(f"{self.nome} agora tem {self.efeitos_negativos[efeito]} carga(s) de {efeito}.")

    def remover_efeito_negativo(self, efeito: str):
        if efeito in self.efeitos_negativos:
            del self.efeitos_negativos[efeito]

    def limpar_efeitos_negativos(self):
        self.efeitos_negativos.clear()

    def morrer(self, jogador):
        print(f"O monstro '{self.nome}' foi derrotado!")
        jogador.ganhar_xp(self.dados["XP"])
        jogador.ganhar_ouro(self.dados["Ouro"])
        self.dados["Abatidos"] += 1
        self.dados["Vida"] = self.dados["Vida_Max"]
        self.dados["Efeito negativo"] = ['']
        jogador.dados["Ação"] = jogador.dados["Ação_Max"]

        drop = self.dados["Drops"]
        if drop in materiais_adquiridos:
            materiais_adquiridos[drop] += 1
            print(f"Você obteve o material: {drop}.")
        elif drop in armas:
            novo_id = max(armas_adquiridas.keys(), default=0) + 1
            armas_adquiridas[novo_id] = {
                drop: armas[drop].copy()
            }
            print(f"Você obteve a arma: {drop}.")
        else:
            print(f"Nenhum drop válido foi encontrado: {drop}")
        

    def __str__(self):
        efeitos = (
            ", ".join(f"{k} ({v})" for k, v in self.efeitos_negativos.items())
            if self.efeitos_negativos else "Nenhum"
        )
        return (
            f"Monstro: {self.nome}\n"
            f"  Vida: {self.vida}\n"
            f"  Dano: {self.dados['Dano']}\n"
            f"  Defesa: {self.defesa}\n"
            f"  Crítico: {self.critico}%\n"
            f"  Ouro: {self.ouro}\n"
            f"  XP: {self.xp}\n"
            f"  Drops: {self.drops}\n"
            f"  Efeitos Negativos: {efeitos}\n"
            f"  Abatidos: {self.abatidos}"
        )






class Jogador:
    def __init__(self):
        self.dados = atributos
        self.buffs_ativos = {
    "forca": {"quantidade": 0, "turnos": 0},
    "defesa": {"quantidade": 0, "turnos": 0}}

    @property
    def vida(self):
        return self.dados["Vida"]

    @vida.setter
    def vida(self, valor):
        if valor < 0:
            valor = 0
        elif valor > self.dados["Vida_Max"]:
            valor = self.dados["Vida_Max"]
        self.dados["Vida"] = valor

    @property
    def vida_max(self):
        return self.dados["Vida_Max"]

    @property
    def defesa(self):
        return self.dados["Defesa"]

    @property
    def defesa_total(self):
        buff_defesa = self.buffs_ativos.get("defesa", {"quantidade": 0})["quantidade"]
        return self.defesa + buff_defesa

    @property
    def ataque(self):
        return self.dados["Ataque"]

    @property
    def evasao(self):
        return self.dados["Evasão"]

    @property
    def chance_critico(self):
        return self.dados["Chance_critico"]

    @property
    def critico(self):
        return self.dados["Critico"]

    @property
    def sorte(self):
        return self.dados["Sorte"]

    @property
    def ouro(self):
        return self.dados["Ouro"]

    @property
    def xp(self):
        return self.dados["XP"]

    @property
    def xp_necessario(self):
        return self.dados["XP_Necessario"]

    @property
    def acao(self):
        return self.dados.get("Ação", 0)

    @acao.setter
    def acao(self, valor):
        self.dados["Ação"] = valor

    @property
    def acao_max(self):
        return self.dados.get("Ação_Max", 0)



    def usar_pocao(self, tipo: str, nivel: int):
        nome_nivel = f"Level {nivel}"
        tipo_capitalizado = tipo.capitalize()
        
        if tipo_capitalizado not in pocoes_adquiridas or pocoes_adquiridas[tipo_capitalizado].get(nome_nivel, 0) <= 0:
            print(f"Você não possui a poção {tipo_capitalizado} nível {nivel}.")
            return

        # Formata o nome da poção
        tipo_formatado = tipo.lower().replace("ç", "c").replace("á", "a").replace("ã", "a")
        nome_pocao = f"{tipo_formatado}_nivel_{nivel}"
        dados_pocao = pocoes.get(nome_pocao)

        if not dados_pocao:
            print(f"Poção {nome_pocao} não existe.")
            return

        # ⚡ Aplica efeito da poção
        if tipo_formatado == "cura":
            cura = dados_pocao.get("Curar Vida", 0)
            self.curar(cura)
            print(f"Você usou uma poção de cura nível {nivel} e recuperou {cura} de vida.")

        elif tipo_formatado == "forca":
            ganho = dados_pocao.get("Ganhar Força", 0)
            acoes = 1  # duração sempre 1 turno
            self.buffs_ativos["forca"]["quantidade"] += ganho
            self.buffs_ativos["forca"]["turnos"] = max(self.buffs_ativos["forca"]["turnos"], acoes)
            print(f"Você usou uma poção de força nível {nivel}: +{ganho} ataque por {acoes} turno(s).")

        else:
            print(f"Tipo de poção desconhecido: {tipo}")
            return

        # ⚡ Diminui poção do inventário
        pocoes_adquiridas[tipo_capitalizado][nome_nivel] -= 1

        # ⚡ Gasta 1 ação
        self.acao -= 1


    def ataque_total(self):
        """Retorna o ataque total com buffs."""
        return self.ataque + self.buffs_ativos.get("forca", {}).get("quantidade", 0)

    def aplicar_buffs(self):
        """Diminui turnos de buffs ativos."""
        # Buff de força
        if self.buffs_ativos["forca"]["turnos"] > 0:
            self.buffs_ativos["forca"]["turnos"] -= 1
            if self.buffs_ativos["forca"]["turnos"] == 0:
                print("O efeito da Poção de Força acabou.")
                self.buffs_ativos["forca"]["quantidade"] = 0

        # Buff de defesa
        if self.buffs_ativos["defesa"]["turnos"] > 0:
            self.buffs_ativos["defesa"]["turnos"] -= 1
            if self.buffs_ativos["defesa"]["turnos"] == 0:
                print("O efeito de Defesa acabou.")
                self.buffs_ativos["defesa"]["quantidade"] = 0



    # Métodos de manipulação
    def receber_dano(self, dano: int):
        dano_real = max(dano - self.defesa_total, 0)
        self.vida -= dano_real
        print(f"Você recebeu {dano_real} de dano.")
        return dano_real

    def curar(self, quantidade: int):
        vida_atual = self.dados.get("Vida", 0)
        vida_max = self.dados.get("Vida_Max", 0)
        self.dados["Vida"] = min(vida_atual + quantidade, vida_max)

    def ganhar_ouro(self, quantidade: int):
        self.dados["Ouro"] += quantidade

    def ganhar_xp(self, quantidade: int):
        self.dados["XP"] += quantidade
        print(f"Você ganhou {quantidade} de XP.")
        while self.dados["XP"] >= self.dados["XP_Necessario"]:
            self.upar()
    @property
    def nivel(self):
        # Por exemplo: XP_Necessario = 100 + 50*(nível - 1)
        # Inverso da fórmula:
        return ((self.dados["XP_Necessario"] - 100) // 50) + 1


    def upar(self):
        print("Você subiu de nível!")

        # Aumenta os atributos
        self.dados["Vida_Max"] += 5
        self.dados["Vida"] += 5  # Recupera vida ao subir de nível
        self.dados["Defesa"] += 1
        self.dados["Ataque"] += 1
        self.dados["Chance_critico"] += 5
        self.dados["Critico"] += 0.1
        self.dados["Ação"] += 1
        self.dados["Ação_Max"] += 1

        # Reseta XP e aumenta XP necessário para próximo nível
        self.dados["XP"] = 0
        self.dados["XP_Necessario"] += 50

    def modificar_atributo(self, nome: str, valor: int | float):
        if nome in self.dados:
            self.dados[nome] = valor
        else:
            raise ValueError(f"Atributo '{nome}' não encontrado.")

    def __str__(self):
        buff_info = ""
        if self.buffs_ativos["forca"]["quantidade"] > 0:
            buff_info = f"  Buff de Força: +{self.buffs_ativos['forca']['quantidade']} ATQ por {self.buffs_ativos['forca']['turnos']} turno(s)\n"

        return (
            f"Jogador:\n"
            f"  Nível: {self.nivel}\n"
            f"  Vida: {self.vida}/{self.vida_max}\n"
            f"  Ataque: {self.ataque_total()}\n"
            f"  Defesa: {self.defesa_total}\n"
            f"  Evasão: {self.evasao}%\n"
            f"  Chance Crítico: {self.chance_critico}%\n"
            f"  Crítico: x{round(self.critico, 2)}\n"
            f"  Sorte: {self.sorte}\n"
            f"  Ouro: {self.ouro}\n"
            f"  XP: {self.xp}/{self.xp_necessario}\n"
            f"  Ação: {self.acao}\n"
            f"{buff_info}"
        )


#=======================================================================================================================
# Batalha
import random

def batalha(jogador, nome_monstro):
    monstro = Monstro(nome_monstro)
    acao_jogador = jogador.acao
    acao_monstro = None
    monstro_derrotado = False

    def atacar_com_arma(jogador, monstro):
        print("\nEscolha como deseja atacar:")
        print("(1) Soco com as Mãos (dano base, custo: 1 ação)")

        id_para_item = {}
        idx = 2

        for id_arma, arma_info in armas_adquiridas.items():
            for nome_arma, dados in arma_info.items():
                encantamento = dados.get("Encantamento") or "Nenhum"
                durabilidade = dados.get("Durabilidade", "∞")
                print(f"({idx}) {nome_arma} | Dano: {dados['Dano']} | Encantamento: {encantamento} | Ação: {dados['Ação']} | Durabilidade: {durabilidade}")
                id_para_item[idx] = (id_arma, nome_arma)
                idx += 1

        print("(0) Voltar")

        escolha = input(">>> ")

        if not escolha.isdigit():
            print("Entrada inválida.")
            return False

        escolha = int(escolha)

        if escolha == 0:
            return False

        elif escolha == 1:
            if jogador.acao < 1:
                print("Você não tem ação suficiente para atacar com as mãos.")
                return False
            dano = jogador.ataque_total()
            print(f"\nVocê ataca com os punhos e causa {dano} de dano!")
            jogador.dados["Ação"] -= 1
            monstro.receber_dano(dano)
            monstro.aplicar_efeitos_ao_receber_dano()
            return True

        elif escolha in id_para_item:
            id_escolhido, nome_escolhido = id_para_item[escolha]

            arma = Arma(nome_escolhido)
           
            arma.id_arma = id_escolhido
            arma.dados = armas_adquiridas[id_escolhido][nome_escolhido]
            if hasattr(arma, "_durabilidade"): 
                arma._durabilidade = arma.dados.get("Durabilidade", arma._durabilidade)

            if jogador.acao < arma.acao:
                print(f"Você não tem ação suficiente para usar essa arma (precisa de {arma.acao}, tem {jogador.acao}).")
                return False

            dano = arma.calcular_dano(monstro, jogador)
            print(f"\nVocê atacou com '{arma.nome}' e causou {dano} de dano!")

            jogador.dados["Ação"] -= arma.acao
            monstro.receber_dano(dano)
            monstro.aplicar_efeitos_ao_receber_dano()
            return True

        else:
            print("Opção inválida.")
            return False


    print("\n--- BATALHA INICIADA ---\n")

    while jogador.vida > 0 and monstro.vida > 0:
        os.system("cls")
        # Exibe status do monstro
        print(f"Monstro: {monstro.nome}")
        print(monstro.efeitos_negativos)
        print(f"  Vida: {monstro.vida}")
        print(f"  Dano: {monstro.dados['Dano']}")
        # Se não há ação escolhida para o monstro, escolha uma
        if acao_monstro is None:
            acao_monstro = random.choice(["Atacar", "Defender"])
            print(f"  Ação do monstro: {acao_monstro}\n")
        else:
            print(f"  Ação do monstro: {acao_monstro}\n")


        # Status do jogador
        print("Jogador:")
        print(f"  Vida: {jogador.vida}/{jogador.vida_max}")
        print(f"  Ataque: {jogador.ataque_total()}")
        print(f"  Defesa: {jogador.defesa_total}")
        print(f"  Ação restante: {jogador.acao}")
        # Opções do jogador
        print("\nEscolha uma ação:")
        print("(1) Atacar")
        print("(2) Defender")
        print("(3) Usar poção")
        print("(4) Sair da batalha")

        escolha = input(">>> ")
        #ataque
        if escolha == "1":
            atacar_com_arma(jogador, monstro)
        #defesa
        elif escolha == "2":
            print("Você escolheu DEFENDER.")
            if "defesa" not in jogador.buffs_ativos:
                jogador.buffs_ativos["defesa"] = {"quantidade": 0, "turnos": 0}
            jogador.buffs_ativos["defesa"]["quantidade"] += 5
            jogador.buffs_ativos["defesa"]["turnos"] = 1  # dura até o fim do turno inimigo
            jogador.acao -= 1
        #poção
        elif escolha == "3":
            if jogador.acao <= 0:
                print("Você não tem ação suficiente para usar uma poção.")
                continue

            # Lista todas as poções disponíveis
            todas_pocoes = []
            idx = 1

            print("\n--- POÇÕES DISPONÍVEIS ---")
            for tipo, niveis in pocoes_adquiridas.items():
                for nivel, qtd in niveis.items():
                    if qtd > 0:
                        print(f"({idx}) {tipo} {nivel} - Quantidade: {qtd}")
                        todas_pocoes.append((tipo, int(nivel.split()[-1])))  # ex: ("Cura", 1)
                        idx += 1

            if not todas_pocoes:
                print("Você não possui nenhuma poção.")
                continue

            print("(0) Voltar\n")

            escolha_pocao = input("Escolha uma poção para usar: ")

            if not escolha_pocao.isdigit():
                print("Entrada inválida.")
                continue

            escolha_pocao = int(escolha_pocao)

            if escolha_pocao == 0:
                continue

            if 1 <= escolha_pocao <= len(todas_pocoes):
                tipo, nivel = todas_pocoes[escolha_pocao - 1]
                jogador.usar_pocao(tipo, nivel)
                jogador.acao -= 1
            else:
                print("Opção inválida.")

        elif escolha == "4":
            chance_fuga = random.randint(1, 100)
            if chance_fuga <= 33:
                print("Você tentou fugir... mas o monstro te impediu!\n")
                jogador.dados["Ação"] -= 1
            else:
                print("Você conseguiu escapar da batalha!\n")
                jogador.dados["Ação"] = jogador.dados["Ação_Max"]
                dicionarios.monstros[monstro.nome]["Efeito negativo"] = ['']
                dicionarios.monstros[monstro.nome]["Vida"] = dicionarios.monstros[monstro.nome]["Vida_Max"]
                break

        else:
            print("Opção inválida. Tente novamente.\n")
            continue

        # Verifica se acabou as ações do jogador
        if jogador.acao <= 0:
            print("\n--- Turno do monstro ---")

            # Aplica efeitos negativos
            monstro.aplicar_efeitos_apos_ataque()

            # Verifica se o monstro morreu pelos efeitos
            if monstro.vida <= 0 and not monstro_derrotado:
                monstro.morrer(jogador)
                monstro_derrotado = True
                break


            # Executa a ação decidida anteriormente
            if acao_monstro == "Atacar":
                dano = monstro.dano()
                dano_modificado = monstro.modificar_dano_com_efeitos(dano)
                jogador.receber_dano(dano_modificado)
                print(f"O monstro atacou e causou {dano_modificado} de dano!")
            elif acao_monstro == "Defender":
                defesa_ativa = monstro.defender()
                print("O monstro está se defendendo!")

            # Reseta ação do monstro para que escolha nova no próximo turno
            acao_monstro = None

            jogador.aplicar_buffs()  # Aplica/atualiza buffs
            jogador.dados["Ação"] = jogador.dados["Ação_Max"]  # Restaura ação
            print("\nSua ação foi restaurada!\n")
            if "defesa" in jogador.buffs_ativos:
                jogador.buffs_ativos["defesa"]["turnos"] -= 1
                if jogador.buffs_ativos["defesa"]["turnos"] <= 0:
                    jogador.buffs_ativos["defesa"]["quantidade"] = 0
                    print("O efeito de Defesa acabou.")
            # Verifica se o buff de força acabou
            if jogador.buffs_ativos["forca"]["turnos"] > 0:
                jogador.buffs_ativos["forca"]["turnos"] -= 1
                if jogador.buffs_ativos["forca"]["turnos"] <= 0:
                    jogador.buffs_ativos["forca"]["quantidade"] = 0
                    print("O efeito da Poção de Força acabou.")
        print("-" * 40)
        input()

    if jogador.vida <= 0:
        print("Você foi derrotado...\n")
        print("-" * 40)
        return
    elif monstro.vida <= 0 and not monstro_derrotado:
        jogador.dados["Ação"] = jogador.dados["Ação_Max"]
        monstro.morrer(jogador)

#====================================================================================
# Aventura

def aventura():
    x = random.randint(1,4)
    print_com_delay("Ao escolher se aventurar, você ouve alguém falando à você...\n")
    sleep(1)
    print("NPC: ", end="")
    print_com_delay("Tome cuidado com os monstros!\n") if x == 1 else print_com_delay("Cuidado com a floresta, lá habitam seres horríveis...\n") if x == 2 else print_com_delay("Vai pela sombra meu amigo!\n") if x == 3 else print_com_delay("Boa viagem, senhor aventureiro!\n")
    input("Manterei isso em mente!") if x == 1 else input("Terei cuidado...") if x == 2 else input("Hoje e sempre!") if x == 3 else input("Muito obrigado!")
    while dicionarios.atributos["Vida"] > 0:
        os.system("cls")
        print_com_delay("Chegando na floresta, você se depara com um desafio!"
                        " O que você vai fazer?")
        sleep(1)
        print_com_delay("\nVocê avista: \n")
        
        print("(1) Slime")
        if monstros["Slime"]["Abatidos"] >= 1:
            print("(2) Lobo")
        if monstros["Lobo"]["Abatidos"] >= 1:
            print("(3) Goblin")
        if monstros["Goblin"]["Abatidos"] >= 1:
            print("(4) Cobra")
        if monstros["Cobra"]["Abatidos"] >= 1:  
            print("(5) Esqueleto")
        print("(6) Voltar")
        
        try:
            decisao = int(input("O que eu faço:\n"))
        except ValueError:
            print("Digite um número válido.")
            input()
            continue

        if decisao == 1:
            Jogador1 = Jogador()
            batalha(Jogador1, "Slime")
            input()
        elif decisao == 2 and monstros["Slime"]["Abatidos"] >= 1:
            Jogador1 = Jogador()
            batalha(Jogador1, "Lobo")
            input()
        elif decisao == 3 and monstros["Lobo"]["Abatidos"] >= 1:
            Jogador1 = Jogador()
            batalha(Jogador1, "Goblin")
            input()
        elif decisao == 4 and monstros["Goblin"]["Abatidos"] >= 1:
            Jogador1 = Jogador()
            batalha(Jogador1, "Cobra")
            input()
        elif decisao == 5 and monstros["Cobra"]["Abatidos"] >= 1:
            Jogador1 = Jogador()
            batalha(Jogador1, "Esqueleto")
            input()

            if monstros["Esqueleto"]["Abatidos"] == 1:
                print_com_delay("Parabéns por derrotar todos os monstros! A próxima vila está agora ao seu alcance! *Coming Soon*")
                input("Pressione enter para continuar...")

        elif decisao == 6:
            return
    return



#====================================================================================
#Hospital
def hospital():
    dicionarios.atributos["Vida"] = dicionarios.atributos["Vida_Max"]

#====================================================================================
#venda
def venda_aprovada(item_escolhido, quantidade=1):
    """
    Vende um item do inventário:
    - Armas: pelo ID
    - Poções e Materiais: pelo nome
    """
    # Armas (vendidas pelo ID)
    if isinstance(item_escolhido, int) and item_escolhido in dicionarios.armas_adquiridas:
        nome_arma = list(dicionarios.armas_adquiridas[item_escolhido].keys())[0]
        preco = dicionarios.armas[nome_arma]["Ouro"] // 2
        dicionarios.atributos["Ouro"] += preco
        del dicionarios.armas_adquiridas[item_escolhido]
        print_com_delay(f"Você vendeu {nome_arma} por {preco} ouro.")
        return

    # Poções
    for categoria in ["Cura", "Força"]:
        for level, qtd in dicionarios.pocoes_adquiridas[categoria].items():
            nome_item = f"{categoria.lower()}_nivel_{level[-1]}"
            if item_escolhido == nome_item:
                if qtd < quantidade:
                    print_com_delay("Você não tem poções suficientes para vender.")
                    return
                preco = dicionarios.pocoes[nome_item]["Ouro"] // 2
                total = preco * quantidade
                dicionarios.atributos["Ouro"] += total
                dicionarios.pocoes_adquiridas[categoria][level] -= quantidade
                print_com_delay(f"Você vendeu {quantidade}x {nome_item.replace('_', ' ').title()} por {total} ouro.")
                return

    # Materiais
    if item_escolhido in dicionarios.materiais_adquiridos:
        if dicionarios.materiais_adquiridos[item_escolhido] < quantidade:
            print_com_delay("Você não tem materiais suficientes para vender.")
            return
        preco = dicionarios.materiais[item_escolhido]["Preço"] // 2
        total = preco * quantidade
        dicionarios.atributos["Ouro"] += total
        dicionarios.materiais_adquiridos[item_escolhido] -= quantidade
        print_com_delay(f"Você vendeu {quantidade}x {item_escolhido} por {total} ouro.")
        return

    # Item não encontrado
    print_com_delay("Item inválido.")

#====================================================================================
#compra
def comprar_aprovada(item_escolhido, quantidade):

    #  é arma?
    if item_escolhido in dicionarios.armas:
        atributos = dicionarios.armas[item_escolhido]
        preco = atributos["Ouro"]
        custo_total = preco * quantidade

        if dicionarios.atributos["Ouro"] >= custo_total:
            dicionarios.atributos["Ouro"] -= custo_total

            proximo_id = max(dicionarios.armas_adquiridas.keys(), default=0) + 1
            for i in range(quantidade):
                dicionarios.armas_adquiridas[proximo_id + i] = {
                    item_escolhido: atributos.copy()
                }

            print_com_delay(f"Você comprou {quantidade}x {item_escolhido}.")
        else:
            print_com_delay("Gold insuficiente!")
        return


    # é poção?
    if item_escolhido in dicionarios.pocoes:
        atributos = dicionarios.pocoes[item_escolhido]
        preco = atributos["Ouro"]
        custo_total = preco * quantidade

        if dicionarios.atributos["Ouro"] >= custo_total:
            dicionarios.atributos["Ouro"] -= custo_total

            # Atualiza o inventário de poções
            if "cura" in item_escolhido:
                nivel = item_escolhido[-1]  # pega 1, 2 ou 3
                dicionarios.pocoes_adquiridas["Cura"][f"Level {nivel}"] += quantidade

            elif "forca" in item_escolhido:
                nivel = item_escolhido[-1]
                dicionarios.pocoes_adquiridas["Força"][f"Level {nivel}"] += quantidade

            print_com_delay(f"Você comprou {quantidade}x {item_escolhido.replace('_', ' ').title()}.")
        else:
            print_com_delay("Gold insuficiente!")
        return


    # é material?
    if item_escolhido in dicionarios.materiais:
        preco = dicionarios.materiais[item_escolhido]["Preço"]
        custo_total = preco * quantidade

        if dicionarios.atributos["Ouro"] >= custo_total:
            dicionarios.atributos["Ouro"] -= custo_total

            dicionarios.materiais_adquiridos[item_escolhido] += quantidade

            print_com_delay(f"Você comprou {quantidade}x {item_escolhido}.")
        else:
            print_com_delay("Gold insuficiente!")
        return

    print_com_delay("Item inválido.")

#------------------------------------
from flask import redirect, url_for, request, flash
import dicionarios

def acao_defender(monstro_nome):
    # Pega o jogador real
    jogador = dicionarios.jogador
    logs = dicionarios.batalha.get("logs", [])

    # Verifica se jogador tem ação suficiente
    if jogador.acao < 1:
        logs.append("Você não tem ação suficiente para se defender!")
        dicionarios.batalha["logs"] = logs
        return redirect(url_for("batalha", monstro=monstro_nome))

    # Aplica o buff de defesa
    if "defesa" not in jogador.buffs_ativos:
        jogador.buffs_ativos["defesa"] = {"quantidade": 0, "turnos": 0}

    jogador.buffs_ativos["defesa"]["quantidade"] += 5
    jogador.buffs_ativos["defesa"]["turnos"] = 1  # dura até o fim do turno inimigo

    # Deduz ação
    jogador.acao -= 1

    logs.append("Você escolheu DEFENDER e ganhou +5 de defesa até o próximo turno do inimigo!")
    
    # Atualiza logs e ação no dicionário global
    dicionarios.batalha["logs"] = logs
    dicionarios.atributos["Ação"] = jogador.acao

    # Se o jogador ficar sem ação, passa o turno para o monstro
    if jogador.acao <= 0:
        return turno_do_monstro(monstro_nome)

    return redirect(url_for("batalha", monstro=monstro_nome))


# funcoes.py
import dicionarios

def acao_pocao(monstro):
    jogador = dicionarios.jogador
    logs = dicionarios.batalha.get("logs", [])

    if jogador.acao <= 0:
        logs.append("Você não tem ação suficiente para usar uma poção!")
        dicionarios.batalha["logs"] = logs
        return redirect(url_for("batalha", monstro=monstro))

    # ⚡ Aqui precisa do 'request'
    acao = request.form.get("acao")  # ex: "usar_pocao_Cura_Level 1"
    partes = acao.split("_")
    tipo = partes[2]          # "Cura" ou "Força"
    nivel_str = partes[3]     # "Level 1"
    nivel = int(nivel_str.split()[-1])

    if dicionarios.pocoes_adquiridas[tipo][f"Level {nivel}"] <= 0:
        logs.append(f"Você não possui poção {tipo} Level {nivel}.")
        dicionarios.batalha["logs"] = logs
        return redirect(url_for("batalha", monstro=monstro))

    # Aplica poção e gasta ação
    jogador.usar_pocao(tipo, nivel)
    logs.append(f"Você usou uma poção {tipo} Level {nivel}!")

    dicionarios.atributos["Ação"] = jogador.acao
    dicionarios.batalha["logs"] = logs

    if jogador.acao <= 0:
        from funcoes import turno_do_monstro
        return turno_do_monstro(monstro)

    return redirect(url_for("batalha", monstro=monstro))



def acao_fugir(monstro):
    jogador = dicionarios.jogador
    logs = dicionarios.batalha.get("logs", [])

    # Chance de fuga: 33%
    chance_fuga = random.randint(1, 100)
    if chance_fuga <= 33:
        # Falhou em fugir
        jogador.acao -= 1
        logs.append("Você tentou fugir... mas o monstro te impediu!")
        flash("Você falhou em fugir da batalha...")
        destino = url_for("batalha", monstro=monstro)  # continua na batalha
    else:
        # Fugiu com sucesso
        jogador.acao = jogador.acao_max
        # Reseta vida e efeitos negativos do monstro
        if monstro in dicionarios.monstros:
            dicionarios.monstros[monstro]["Vida"] = dicionarios.monstros[monstro]["Vida_Max"]
            dicionarios.monstros[monstro]["Efeito negativo"] = []
        logs.append("Você conseguiu escapar da batalha!")
        flash("Você conseguiu fugir da batalha!")

        # Remove a batalha atual
        if hasattr(dicionarios, "batalha"):
            del dicionarios.batalha

        destino = url_for("aventura")  # volta para a aventura principal

    # Atualiza logs (mesmo que a batalha seja removida, não há problema)
    # Só para o caso de falhar a fuga e continuar a batalha
    if hasattr(dicionarios, "batalha"):
        dicionarios.batalha["logs"] = logs

    # Redireciona para o destino correto
    return redirect(destino)




import dicionarios

import random



def finalizar_batalha(monstro_nome):
    jogador = dicionarios.jogador
    monstro_obj = dicionarios.batalha["objeto_monstro"]

    logs = dicionarios.batalha.get("logs", [])

    # Jogador morreu
    if jogador.vida <= 0:
        jogador.vida = 1
        logs.append("Você foi derrotado e voltou para a aventura!")
        dicionarios.batalha["logs"] = logs
        return redirect(url_for("index"))

    # Monstro morreu
    elif monstro_obj.vida <= 0:
        jogador.acao = jogador.acao_max
        monstro_obj.morrer(jogador)
        logs.append(f"Você derrotou o {monstro_nome}!")
        dicionarios.batalha["logs"] = logs
        if hasattr(dicionarios, "batalha"):
            del dicionarios.batalha
        
        flash(f"Parabéns, você derrotou {monstro_nome}!")
        return redirect(url_for('aventura'))
    else:
        # Ninguém morreu ainda
        dicionarios.batalha["logs"] = logs
        return redirect(url_for("batalha", monstro=monstro_nome))


# Função para checar morte
def checar_morte(jogador, monstro, monstro_nome):
    # Jogador morreu
    if jogador.vida <= 0:
        jogador.vida = 1  # Restaura para 1
        return redirect(url_for('index'))  # Envia para index

    # Monstro morreu
    if monstro.vida <= 0:
        jogador.acao = jogador.acao_max
        monstro.morrer(jogador)
        return finalizar_batalha(monstro_nome)

    # Se ninguém morreu, continua a batalha
    return None


# Ataque com as mãos
def acao_atacar_maos(monstro_nome):
    jogador_obj = dicionarios.jogador
    monstro_obj = dicionarios.batalha["objeto_monstro"]

    logs = dicionarios.batalha.get("logs", [])

    if jogador_obj.acao < 1:
        logs.append("Você não tem ação suficiente para atacar com as mãos!")
        dicionarios.batalha["logs"] = logs
        return redirect(url_for("batalha", monstro=monstro_nome))

    dano = jogador_obj.ataque_total()

    # Aplica redução de 50% se monstro estiver defendendo
    acao_monstro = dicionarios.batalha.get("acao_monstro")
    if acao_monstro == "Defender":
        dano = int(dano * 0.5)

    logs.append(f"Você ataca com os punhos e causa {dano} de dano!")
    jogador_obj.acao -= 1

    monstro_obj.receber_dano(dano)
    monstro_obj.aplicar_efeitos_ao_receber_dano()

    dicionarios.batalha["dados_monstro"]["Vida"] = monstro_obj.vida
    dicionarios.batalha["dados_monstro"]["Efeito negativo"] = monstro_obj.efeitos_negativos
    dicionarios.atributos["Ação"] = jogador_obj.acao
    dicionarios.batalha["logs"] = logs

    # Monstro morreu?
    if monstro_obj.vida <= 0:
        return finalizar_batalha(monstro_nome)

    # Jogador sem ação?
    if jogador_obj.acao <= 0:
        return turno_do_monstro(monstro_nome)

    return redirect(url_for("batalha", monstro=monstro_nome))



# Ataque com arma
def acao_atacar_arma(monstro_nome, id_arma):
    jogador_obj = dicionarios.jogador
    monstro_obj = dicionarios.batalha["objeto_monstro"]

    logs = dicionarios.batalha.get("logs", [])

    if id_arma not in dicionarios.armas_adquiridas:
        logs.append("Arma inexistente!")
        dicionarios.batalha["logs"] = logs
        return redirect(url_for("batalha", monstro=monstro_nome))

    arma_info = dicionarios.armas_adquiridas[id_arma]
    nome_arma = list(arma_info.keys())[0]
    dados_arma = arma_info[nome_arma]
    arma_obj = Arma(nome_arma)
    arma_obj._durabilidade = dados_arma.get("Durabilidade", arma_obj._durabilidade)

    if jogador_obj.acao < arma_obj.acao:
        logs.append(f"Você não tem ação suficiente para usar {nome_arma}.")
        dicionarios.batalha["logs"] = logs
        return redirect(url_for("batalha", monstro=monstro_nome))

    dano = arma_obj.calcular_dano(inimigo=monstro_obj, jogador=jogador_obj)

    # Reduz 50% se monstro estiver defendendo
    acao_monstro = dicionarios.batalha.get("acao_monstro")
    if acao_monstro == "Defender":
        dano = int(dano * 0.5)

    monstro_obj.receber_dano(dano)
    logs.append(f"Você atacou com '{nome_arma}' e causou {dano} de dano!")

    jogador_obj.acao -= arma_obj.acao
    monstro_obj.aplicar_efeitos_ao_receber_dano()

    dicionarios.batalha["dados_monstro"]["Vida"] = monstro_obj.vida
    dicionarios.batalha["dados_monstro"]["Efeito negativo"] = monstro_obj.efeitos_negativos
    dicionarios.atributos["Ação"] = jogador_obj.acao

    if monstro_obj.vida <= 0:
        return finalizar_batalha(monstro_nome)

    if jogador_obj.acao <= 0:
        return turno_do_monstro(monstro_nome)

    dicionarios.batalha["logs"] = logs
    return redirect(url_for("batalha", monstro=monstro_nome))



# Turno do monstro
def turno_do_monstro(monstro_nome):
    jogador = dicionarios.jogador
    monstro_obj = dicionarios.batalha["objeto_monstro"]
    dados_monstro = dicionarios.batalha["dados_monstro"]
    logs = dicionarios.batalha.get("logs", [])

    if "acao_monstro" not in dicionarios.batalha or dicionarios.batalha["acao_monstro"] is None:
        dicionarios.batalha["acao_monstro"] = random.choice(["Atacar", "Defender"])

    acao_monstro = dicionarios.batalha["acao_monstro"]
    logs.append(f"O monstro parece que vai: {acao_monstro}!")

    if acao_monstro == "Atacar":
        dano = dados_monstro["Dano"]
        jogador.receber_dano(dano)
        logs.append(f"O monstro atacou e causou {dano} de dano!")

        resultado = checar_morte(jogador, monstro_obj, monstro_nome)
        if resultado:
            return resultado

    elif acao_monstro == "Defender":
        logs.append("O monstro está se defendendo!")

    dicionarios.batalha["acao_monstro"] = None

    jogador.aplicar_buffs()
    jogador.acao = jogador.acao_max

    dicionarios.batalha["logs"] = logs
    return redirect(url_for("batalha", monstro=monstro_nome))