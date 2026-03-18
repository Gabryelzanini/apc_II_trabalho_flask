# Aqui ficara apenas os dicionarios

# deixando True aqui faz o jogo ficar no MODO DE TESTE
testando = False 

atributos = {
    "Vida": 10 if testando == False else 1,
    "Vida_Max" : 10,
    "Defesa": 0,
    "Ataque": 3,
    "Evasão": 0,
    "Chance_critico": 0,
    "Critico": 1.5,
    "Tenacidade": 0,
    "Sorte": 0,
    "Ouro": 10 if testando == False else 1000,
    "XP" : 0,
    "XP_Necessario": 50,
    "Ação" : 2,
    "Ação_Max" : 2
}


monstros = {
    "Slime": {
        "Abatidos": 0,
        "Dano": 3,
        "Defesa": 0,
        "Critico": 0,
        "Vida": 10 if testando == False else 1,
        "Vida_Max": 10,
        "Efeito negativo": [],
        "Ouro": 3,
        "XP": 25,
        "Drops": "Ferro"
    },
    "Lobo": {
        "Abatidos": 0,
        "Dano": 7,
        "Defesa": 3,
        "Critico": 5,
        "Vida": 45 if testando == False else 1,
        "Vida_Max": 45,
        "Efeito negativo": [],
        "Ouro": 6,
        "XP": 40,
        "Drops": "Espada Curta"
    },
    "Goblin": {
        "Abatidos": 0,
        "Dano": 12,
        "Defesa": 4,
        "Critico": 10,
        "Vida": 60 if testando == False else 1,
        "Vida_Max": 60,
        "Efeito negativo": [],
        "Ouro": 10,
        "XP": 75,
        "Drops": "Ouro"
    },
    "Cobra": {
        "Abatidos": 0,
        "Dano": 17,
        "Defesa": 5,
        "Critico": 15,
        "Vida": 75 if testando == False else 1,
        "Vida_Max": 75,
        "Efeito negativo": [],
        "Ouro": 15,
        "XP": 100,
        "Drops": "Adaga"
    },
    "Esqueleto": {
        "Abatidos": 0,
        "Dano": 20,
        "Defesa": 8,
        "Critico": 20,
        "Vida": 100 if testando == False else 1,
        "Vida_Max": 100,
        "Efeito negativo": [],
        "Ouro": 20,
        "XP": 150,
        "Drops": "Platina"
    }
}

encantamentos = {
    "Sangramento": {
        "DanoCausadoPorAtivaçao": 2,
        "Quantidade": 1,
        "ChanceAtivação": 50  # em porcentagem
    },
    "Gelo": {
        "DanoReduzidoPorAplicação": 2,
        "Quantidade": 1,
        "ChanceAtivação": 35,
        "Efeito": "Reduz Dano do inimigo"
    },
    "Envenenamento": {
        "DanoPorTurno": 2,
        "Quantidade": 1,
        "ChanceAtivação": 35
    },
    "Queimadura": {
        "DanoPorTurno": 2,
        "Quantidade": 1,
        "ChanceAtivação": 30
    },
    "Roubar Vida": {
        "PorcentagemRoubo": 50,  # % do dano causado é convertido em cura
        "ChanceAtivação": 40
    }
}

armas = {
    "Espada Curta": {
        "Ouro": 5,
        "Durabilidade": 5,
        "Dano": 2,
        "Chance Critico": 0,
        "Encantamento": "",
        "Qualidade": 0,
        "Ação": 1
    },
    "Machado de Guerra": {
        "Ouro": 10,
        "Durabilidade": 6,
        "Dano": 4,
        "Chance Critico": 0,
        "Encantamento": "",
        "Qualidade": 0,
        "Ação": 2
    },
    "Arco Longo": {
        "Ouro": 15,
        "Durabilidade": 7,
        "Dano": 3,
        "Chance Critico": 10,  # Crítico maior devido à natureza do arco
        "Encantamento": "",
        "Qualidade": 0,
        "Ação": 2
    },
    "Adaga": {
        "Ouro": 20,
        "Durabilidade": 4,
        "Dano": 2,
        "Chance Critico": 25,  # Muito crítico, pouco dano e pouca durabilidade
        "Encantamento": "",
        "Qualidade": 0,
        "Ação": 1
    },
    "Cajado Mágico": {
        "Ouro": 25,
        "Durabilidade": 8,
        "Dano": 5,
        "Chance Critico": 5,  # Menor crítico, mas dano mágico forte
        "Encantamento": "",
        "Qualidade": 0,
        "Ação": 2
    },
    "Lança": {
        "Ouro": 30,
        "Durabilidade": 9,
        "Dano": 6,
        "Chance Critico": 15,  # Alcance e penetração justificam o dano e crítico
        "Encantamento": "",
        "Qualidade": 0,
        "Ação": 3
    }
}

pocoes = {
    "cura_nivel_1": {
        "Ouro": 10,
        "Curar Vida": 2,
        "Ação": 0
    },
    "cura_nivel_2": {
        "Ouro": 25,
        "Curar Vida": 5,
        "Ação": 1
    },
    "cura_nivel_3": {
        "Ouro": 40,
        "Curar Vida": 10,
        "Ação": 2
    },
    "forca_nivel_1": {
        "Ouro": 10,
        "Ganhar Força": 1,
        "Ação": 0
    },
    "forca_nivel_2": {
        "Ouro": 25,
        "Ganhar Força": 3,
        "Ação": 1
    },
    "forca_nivel_3": {
        "Ouro": 40,
        "Ganhar Força": 7,
        "Ação": 2
    }}

equipamentos = {
    "Capacetes": {
        "Capacete de Couro": {
            "Ouro": 10,
            "Durabilidade": 80,
            "Defesa": 2,
            "Tenacidade": 5,
            "Qualidade": 0,
            "Set": "Couro"
        },
        "Capacete Imunidade": {
            "Ouro": 25,
            "Durabilidade": 70,
            "Defesa": 1,
            "Tenacidade": 10,
            "Qualidade": 0,
            "Set": "Imunidade"
        },
        "Capacete de Ferro": {
            "Ouro": 40,
            "Durabilidade": 100,
            "Defesa": 3,
            "Tenacidade": 2,
            "Qualidade": 0,
            "Set": "Ferro"
        }
    },
    "Peitorais": {
        "Peitoral de Couro": {
            "Ouro": 20,
            "Durabilidade": 120,
            "Defesa": 3,
            "Tenacidade": 10,
            "Qualidade": 0,
            "Set": "Couro"
        },
        "Peitoral Imunidade": {
            "Ouro": 45,
            "Durabilidade": 100,
            "Defesa": 2,
            "Tenacidade": 20,
            "Qualidade": 0,
            "Set": "Imunidade"
        },
        "Peitoral de Ferro": {
            "Ouro": 85,
            "Durabilidade": 150,
            "Defesa": 4,
            "Tenacidade": 5,
            "Qualidade": 0,
            "Set": "Ferro"
        }
    },
    "Calças": {
        "Calça de Couro": {
            "Ouro": 15,
            "Durabilidade": 100,
            "Defesa": 3,
            "Tenacidade": 7,
            "Qualidade": 0,
            "Set": "Couro"
        },
        "Calça Imunidade": {
            "Ouro": 35,
            "Durabilidade": 90,
            "Defesa": 2,
            "Tenacidade": 15,
            "Qualidade": 0,
            "Set": "Imunidade"
        },
        "Calça de Ferro": {
            "Ouro": 70,
            "Durabilidade": 120,
            "Defesa": 4,
            "Tenacidade": 4,
            "Qualidade": 0,
            "Set": "Ferro"
        }
    },
    "BonusSet": {
        "Couro": {
            "Bônus Agilidade": 10,
            "Bônus Evasão": 5,
            "Descrição": "Aumenta agilidade e evasão ao usar o set completo de Couro"
        },
        "Imunidade": {
            "Bônus Imunidade": True,
            "Descrição": "Concede imunidade a efeitos negativos ao usar o set completo de Imunidade"
        },
        "Ferro": {
            "Bônus Defesa": 10,
            "Bônus ação": 1,
            "Descrição": "Aumenta a defesa e tenacidade ao usar o set completo de Ferro"
        }
    }
}

materiais = {
    "Ferro": {
        "Preço": 5
    },
    "Ouro": {
        "Preço": 10
    },
    "Platina": {
        "Preço": 15
    },
}

armas_adquiridas = {
    1: {
        "Espada Curta": {
            "Ouro": 5,
            "Durabilidade": 5,
            "Dano": 2,
            "Chance Critico": 0,
            "Encantamento": "",
            "Qualidade": 0,
            "Ação": 1
        }
    },
    2: {
        "Adaga": {
            "Ouro": 20,
            "Durabilidade": 4,
            "Dano": 2,
            "Chance Critico": 25,
            "Encantamento": "",
            "Qualidade": 1,
            "Ação": 1
            }
    },
    3: {
        "Cajado Mágico": {
            "Ouro": 25,
            "Durabilidade": 8,
            "Dano": 5,
            "Chance Critico": 5,
            "Encantamento": "Frio (bota frio nisso)",
            "Qualidade": 2,
            "Ação": 2
            }
    },
    4: {
        "Lança": {
            "Ouro": 30,
            "Durabilidade": 9,
            "Dano": 6,
            "Chance Critico": 15,
            "Encantamento": "",
            "Qualidade": 3,
            "Ação": 3
            }
    },
    5: {
        "Lança": {
            "Ouro": 30,
            "Durabilidade": 9,
            "Dano": 6,
            "Chance Critico": 15,
            "Encantamento": "",
            "Qualidade": 4,
            "Ação": 3
            }
    },
    6: {
        "Espada Curta": {
            "Ouro": 5,
            "Durabilidade": 5,
            "Dano": 2,
            "Chance Critico": 0,
            "Encantamento": "",
            "Qualidade": 5,
            "Ação": 1
        }
    },
}   

armaduras_adquiridas = {} 

materiais_adquiridos = { 
    "Ferro": 100 if testando == False else 1000, 
    "Ouro": 0 if testando == False else 1000, 
    "Platina": 0 if testando == False else 1000} 

pocoes_adquiridas = {
    "Cura": { 
        "Level 1": 2,
        "Level 2": 1,
        "Level 3": 0 },
    "Força": { 
        "Level 1": 1, 
        "Level 2": 0, 
        "Level 3": 0 }}

equipado = {
    "Capacete": None,
    "Peitoral": None,
    "Calça": None
}

setcompleto = {
    "Set_Ferro": {
        "Ativo": False,
        "Bonus": {}
    },
    "Set_Couro": {
        "Ativo": False,
        "Bonus": {}
    },
    "Set_Imunidade": {
        "Ativo": False,
        "Bonus": {}
    }
}

melhoria_por_nivel = {
    "Melhoria Máxima": 5,
    "Durabilidade": 5,
    "Dano": 2,
    "Chance Critico": 5
}

req_melhoria = {
    1: {"Ferro": 5, "Ouro": 0, "Platina": 0},    # Requisitos para upar do level 0 ao 1
    2: {"Ferro": 10, "Ouro": 5, "Platina": 0},   # do 1 ao 2
    3: {"Ferro": 15, "Ouro": 10, "Platina": 5},  # e por aí vai
    4: {"Ferro": 30, "Ouro": 20, "Platina": 10},
    5: {"Ferro": 50, "Ouro": 35, "Platina": 25}
}

batalha = {
    "monstro": None,
    "dados_monstro": None,
    "logs": []
}