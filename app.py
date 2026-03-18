import funcoes
import dicionarios
import random
from funcoes import acao_atacar_maos
from funcoes import Jogador
from flask import Flask, render_template, request, redirect, url_for,flash
app = Flask(__name__)
app.secret_key = "alguma_senha_muito_muito_secreta_hihihi"

# Main
@app.route('/')
def index():
    return render_template('index.html')

# Aventura
@app.route('/aventura')
def aventura():
    monstros=dicionarios.monstros
    return render_template('aventura.html', monstros=monstros)

@app.route('/monstro/<monstro>')
def detalhes_monstro(monstro):
    dados = dicionarios.monstros.get(monstro)
    if not dados:
        return "Monstro não encontrado", 404
    return render_template("detalhes_monstro.html", nome=monstro, dados=dados)

# Batalha
import dicionarios
from funcoes import Jogador
import random
dicionarios.jogador = Jogador()

@app.route('/batalha/<monstro>', methods=['GET'])
def batalha(monstro):
    dados_monstro = dicionarios.monstros.get(monstro)
    if not dados_monstro:
        return "Monstro inexistente", 404

    if "batalha" not in dicionarios.__dict__ or dicionarios.batalha.get("monstro") != monstro:

        from funcoes import Monstro

        dicionarios.batalha = {
            "monstro": monstro,
            "dados_monstro": dados_monstro.copy(),
            "logs": ["A batalha começou!"],
            "objeto_monstro": Monstro(monstro),  # objeto real do monstro
            "acao_monstro": None
        }

    # Se não houver ação definida, sorteia uma
    if dicionarios.batalha.get("acao_monstro") is None:
        dicionarios.batalha["acao_monstro"] = random.choice(["Atacar", "Defender"])

    return render_template(
        "batalha.html",
        monstro=monstro,
        dados=dicionarios.batalha["dados_monstro"],
        jogador=dicionarios.jogador,
        logs=dicionarios.batalha["logs"],
        acao_monstro=dicionarios.batalha["acao_monstro"]
    )

@app.route('/batalha_acao/<monstro>', methods=['POST'])
def batalha_acao(monstro):
    from flask import redirect, url_for
    jogador = dicionarios.jogador
    acao = request.form.get("acao")
    resposta = None

    # Ataque com as mãos
    if acao == "atacar_maos":
        from funcoes import acao_atacar_maos
        resposta = acao_atacar_maos(monstro)

    # Ataque com arma
    elif acao.startswith("atacar_arma_"):
        id_arma = int(acao.replace("atacar_arma_", ""))
        from funcoes import acao_atacar_arma
        resposta = acao_atacar_arma(monstro, id_arma)

    # Defender
    elif acao == "defender":
        from funcoes import acao_defender
        resposta = acao_defender(monstro)

    # Usar poção
    elif acao.startswith("usar_pocao_"):
        from funcoes import acao_pocao
        resposta = acao_pocao(monstro)

    # Fugir
    elif acao == "fugir":
        from funcoes import acao_fugir
        resposta = acao_fugir(monstro)

    else:
        return redirect(url_for("batalha", monstro=monstro))

    if resposta:
        return resposta

    # Se o jogador zerou a ação, chama turno do monstro
    if jogador.acao <= 0:
        from funcoes import turno_do_monstro
        return turno_do_monstro(monstro)

    # Se ainda tiver ação, retorna para a batalha
    return redirect(url_for("batalha", monstro=monstro))

@app.route('/batalha/pocoes/<monstro>')
def escolher_pocoes(monstro):
    jogador = dicionarios.jogador
    pocoes = dicionarios.pocoes_adquiridas
    logs = dicionarios.batalha.get("logs", [])
    return render_template(
        'batalha_pocoes.html',
        monstro=monstro,
        pocoes=pocoes,
        logs=logs
    )

@app.route('/batalha/<monstro>/atacar')
def batalha_atacar(monstro):
    ouro = dicionarios.atributos["Ouro"]
    return render_template(
        'batalha_atacar.html', 
        ouro=ouro, 
        armas_adquiridas=dicionarios.armas_adquiridas,
        monstro=monstro
    )

# Mercado
@app.route('/mercado')
def mercado():
    ouro = dicionarios.atributos["Ouro"]
    return render_template('mercado.html', ouro=ouro)

@app.route('/mercado/comprar')
def mercado_comprar():
    ouro = dicionarios.atributos["Ouro"]
    return render_template('mercado_comprar.html', ouro=ouro)

@app.route('/mercado/comprar/armas')
def mercado_comprar_armas():
    ouro = dicionarios.atributos["Ouro"]
    return render_template('mercado_comprar_armas.html', ouro=ouro)

@app.route('/mercado/comprar/pocoes')
def mercado_comprar_pocoes():
    ouro = dicionarios.atributos["Ouro"]
    return render_template('mercado_comprar_pocoes.html', ouro=ouro)

@app.route('/mercado/comprar/material')
def mercado_comprar_material():
    materiais = dicionarios.materiais_adquiridos
    ouro = dicionarios.atributos["Ouro"]
    return render_template('mercado_comprar_material.html', ouro=ouro, materiais=materiais)

@app.route('/mercado/vender')
def mercado_vender():
    ouro = dicionarios.atributos["Ouro"]
    return render_template('mercado_vender.html', ouro=ouro)

@app.route('/mercado/vender/armas')
def mercado_vender_armas():
    ouro = dicionarios.atributos["Ouro"]
    return render_template("mercado_vender_armas.html",
                           ouro=ouro,
                           armas_adquiridas=dicionarios.armas_adquiridas)

@app.route('/mercado/vender/pocoes')
def mercado_vender_pocoes():
    ouro = dicionarios.atributos["Ouro"]
    return render_template('mercado_vender_pocoes.html', ouro=ouro)

@app.route('/mercado/vender/material')
def mercado_vender_material():
    materiais = dicionarios.materiais_adquiridos
    ouro = dicionarios.atributos["Ouro"]
    return render_template('mercado_vender_material.html', ouro=ouro, materiais = materiais)

@app.route('/mercado_comprar_confirmar')
def mercado_comprar_confirmar():
    item = request.args.get("item")
    ouro = dicionarios.atributos["Ouro"]
    return render_template("mercado_comprar_confirmar.html", item=item, ouro=ouro)

@app.route('/mercado_vender_confirmar/<int:item_id>')
def mercado_vender_confirmar(item_id):
    arma = dicionarios.armas_adquiridas.get(item_id)
    if not arma:
        return "Arma não encontrada", 404

    nome_arma = list(arma.keys())[0]

    return render_template(
        "mercado_vender_confirmar.html",
        tipo_item="arma",
        id=item_id,
        nome_arma=nome_arma,
        ouro=dicionarios.atributos["Ouro"]
    )

@app.route('/mercado_vender_confirmar_item/<item>')
def mercado_vender_confirmar_item(item):
    return render_template(
        "mercado_vender_confirmar.html",
        tipo_item="consumivel",
        item=item,
        ouro=dicionarios.atributos["Ouro"]
    )

@app.route('/comprar')
def comprar():
    item = request.args.get("item")
    quantidade = int(request.args.get("quantidade", 1))

    if not item:
        return "Item não informado", 400

    funcoes.comprar_aprovada(item, quantidade)
    flash(f"Você comprou {quantidade}x {item}!")
    return redirect(url_for('mercado_comprar'))

@app.route('/vender')
def vender():
    item = request.args.get("item")
    quantidade = request.args.get("quantidade", 1)

    # Tenta converter para int se for id de arma
    try:
        item_id = int(item)

        arma = dicionarios.armas_adquiridas.get(item_id)
        if arma:
            nome_arma = list(arma.keys())[0]
        else:
            nome_arma = "NA"

        funcoes.venda_aprovada(item_id)

        flash(f"Você vendeu a arma {nome_arma}!")

    except ValueError:
        quantidade = int(quantidade)
        antes = dicionarios.atributos["Ouro"]

        funcoes.venda_aprovada(item, quantidade)

        depois = dicionarios.atributos["Ouro"]

        if depois > antes:
            flash(f"Você vendeu {quantidade}x {item.replace('_', ' ').title()}!") # .replace para tirar o _ do nome da poção
        else:
            flash("Você não tem materiais/poções suficientes!")

    return redirect(url_for('mercado_vender'))

# Hospital
@app.route('/hospital')
def curar():
    return render_template('hospital.html')

@app.route('/curado')
def curado():
    funcoes.hospital()
    flash("Sua vida foi totalmente restaurada!")
    return redirect(url_for('index'))

# Ferreiro
@app.route('/ferreiro')
def ferreiro():
    return render_template('ferreiro.html')

# Ferreiro melhorar
@app.route('/ferreiro_melhorar')
def ferreiro_melhorar():
    materiais = dicionarios.materiais_adquiridos
    armas = dicionarios.armas_adquiridas
    return render_template('ferreiro_melhorar.html', materiais=materiais, armas_dic=armas)

@app.route('/melhorar_arma', methods=['POST'])
def melhorar_arma():
    id_arma = request.form.get('id_arma')
    id_arma = int(id_arma)
    arma = dicionarios.armas_adquiridas[id_arma]
    nome = next(iter(arma))
    atributos = arma[nome]

    return render_template(
        "confirmar_melhoria.html",
        id_arma=id_arma,
        nome=nome,
        atributos=atributos,
        materiais=dicionarios.materiais_adquiridos,
        req=dicionarios.req_melhoria,
        melhoria_por_nivel=dicionarios.melhoria_por_nivel,
        dur_base=dicionarios.armas[nome]["Durabilidade"]
    )

@app.route('/confirmar_melhoria', methods=['POST'])
def confirmar_melhoria():
    id_arma = int(request.form.get('id_arma'))
    arma = dicionarios.armas_adquiridas[id_arma]
    nome = next(iter(arma))
    atributos = arma[nome]

    proximo_level = atributos["Qualidade"] + 1
    requisitos = dicionarios.req_melhoria[proximo_level]

    for material, qtd_necessaria in requisitos.items():
        if dicionarios.materiais_adquiridos.get(material, 0) < qtd_necessaria:
            flash("Você não possui materiais suficientes!")
            return redirect(url_for('ferreiro_melhorar'))

    for material, qtd_necessaria in requisitos.items():
        dicionarios.materiais_adquiridos[material] -= qtd_necessaria

    atributos["Durabilidade"] += dicionarios.melhoria_por_nivel["Durabilidade"]
    atributos["Dano"] += dicionarios.melhoria_por_nivel["Dano"]
    atributos["Chance Critico"] += dicionarios.melhoria_por_nivel["Chance Critico"]
    atributos["Qualidade"] += 1

    flash(f"Sua {nome} foi melhorada para a qualidade {proximo_level}!")
    return redirect(url_for('ferreiro_melhorar'))

# Ferreiro reparar
@app.route('/ferreiro_reparar')
def ferreiro_reparar():
    materiais = dicionarios.materiais_adquiridos
    armas = dicionarios.armas_adquiridas
    armas_base = dicionarios.armas
    return render_template(
        'ferreiro_reparar.html', 
        materiais=materiais, 
        armas_dic=armas,
        armas_base=armas_base,
        melhoria_por_nivel=dicionarios.melhoria_por_nivel)

@app.route('/reparar_arma', methods=['POST'])
def reparar_arma():
    id_arma = int(request.form.get('id_arma'))
    arma = dicionarios.armas_adquiridas[id_arma]
    nome = next(iter(arma))
    atributos = arma[nome]
    return render_template(
        'confirmar_reparo.html',
        id_arma=id_arma,
        nome=nome,
        atributos=atributos,
        materiais=dicionarios.materiais_adquiridos,
        melhoria_por_nivel=dicionarios.melhoria_por_nivel,
        dur_base=dicionarios.armas[nome]["Durabilidade"])

@app.route('/confirmar_reparo', methods=['POST'])
def confirmar_reparo():
    id_arma = int(request.form.get('id_arma'))
    custo_total = int(request.form.get('custo_total'))
    dur_max = int(request.form.get('dur_max'))
    arma = dicionarios.armas_adquiridas[id_arma]
    nome = next(iter(arma))
    atributos = arma[nome]
    materiais = dicionarios.materiais_adquiridos

    if materiais["Ferro"] >= custo_total:
        materiais["Ferro"] -= custo_total
        atributos["Durabilidade"] = dur_max
    else:
        flash("Você não possui materiais suficientes!")
        return redirect(url_for('ferreiro_reparar'))

    flash(f"Sua {nome} foi reparada para a durabilidade máxima!")
    flash(f"Você agora possui {materiais['Ferro']} Ferros.")
    return redirect(url_for('ferreiro_reparar'))

# Encantar
@app.route('/encantar')
def encantar():
    return render_template('encantar.html')

@app.route('/encantar_encantar')
def encantar_encantar():
    return render_template('encantar_encantar.html')

@app.route('/encantar_desencantar')
def encantar_desencantar():
    return render_template('encantar_desencantar.html')

# Inventário
@app.route('/inventario')
def inventario():
    return render_template('inventario.html')

@app.route('/inventario/armas')
def inventario_armas():
    armas = dicionarios.armas_adquiridas
    return render_template('inventario_armas.html', armas_dic=armas)

@app.route('/inventario/materiais')
def inventario_materiais():
    materiais = dicionarios.materiais_adquiridos
    return render_template('inventario_materiais.html', materiais = materiais)

@app.route('/inventario/pocoes')
def inventario_pocoes():
    pocoes = dicionarios.pocoes_adquiridas
    return render_template('inventario_pocoes.html', pocoes=pocoes)

# Estatísticas
@app.route('/estatisticas')
def estatisticas():
    atributos = dicionarios.atributos
    monstros = dicionarios.monstros
    return render_template('estatisticas.html', atributos=atributos, monstros=monstros)

# Rodar só se for diretamente (main)
if __name__ == '__main__':
    app.run(debug=True)