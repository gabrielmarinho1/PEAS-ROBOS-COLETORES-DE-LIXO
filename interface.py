import tkinter as tk
from tkinter import ttk
import random
import time

import agentes

class InterfaceAgentes:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Agentes - Coleta de Lixo")
        self.root.geometry("1100x750")

        self.tamanho = agentes.TAMANHO
        self.animando = False
        self.posicao_agente = agentes.POSICAO_INICIAL
        self.carga_agente = None
        self.lixos = {}

        self._configurar_interface()
        self.resetar_ambiente()

    def _configurar_interface(self):
        # Painel Lateral (Controles e Estatísticas)
        painel_esquerdo = ttk.Frame(self.root, padding=10)
        painel_esquerdo.pack(side=tk.LEFT, fill=tk.Y)

        # Seleção de Agente
        ttk.Label(painel_esquerdo, text="Selecione o Agente:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=5)
        self.combo_agentes = ttk.Combobox(
            painel_esquerdo, 
            values=["Reativo Simples", "Baseado em Modelos", "Baseado em Objetivos", "Baseado em Utilidades"],
            state="readonly",
            font=("Arial", 10)
        )
        self.combo_agentes.current(0)
        self.combo_agentes.pack(fill=tk.X, pady=5)

        # Controle de Velocidade
        ttk.Label(painel_esquerdo, text="Velocidade da Animação (ms):", font=("Arial", 10)).pack(anchor=tk.W, pady=(15, 5))
        self.scale_velocidade = tk.Scale(painel_esquerdo, from_=10, to=500, orient=tk.HORIZONTAL)
        self.scale_velocidade.set(50)
        self.scale_velocidade.pack(fill=tk.X)

        # Botões de Ação
        self.btn_iniciar = ttk.Button(painel_esquerdo, text="Iniciar Simulação", command=self.iniciar_simulacao)
        self.btn_iniciar.pack(fill=tk.X, pady=(20, 5))

        self.btn_reset = ttk.Button(painel_esquerdo, text="Resetar Grid", command=self.resetar_ambiente)
        self.btn_reset.pack(fill=tk.X, pady=5)

        # Quadro de Métricas
        frame_metricas = ttk.LabelFrame(painel_esquerdo, text=" Métricas em Tempo Real ", padding=10)
        frame_metricas.pack(fill=tk.X, pady=20)

        self.lbl_passos = ttk.Label(frame_metricas, text="Passos: 0", font=("Arial", 10))
        self.lbl_passos.pack(anchor=tk.W, pady=2)

        self.lbl_pontos = ttk.Label(frame_metricas, text="Pontuação: 0", font=("Arial", 10))
        self.lbl_pontos.pack(anchor=tk.W, pady=2)

        self.lbl_coletados = ttk.Label(frame_metricas, text="Lixos Coletados: 0 / 15", font=("Arial", 10))
        self.lbl_coletados.pack(anchor=tk.W, pady=2)

        self.lbl_carga = ttk.Label(frame_metricas, text="Carga Atual: Livre", font=("Arial", 10))
        self.lbl_carga.pack(anchor=tk.W, pady=2)

        # Legenda
        frame_legenda = ttk.LabelFrame(painel_esquerdo, text=" Legenda ", padding=10)
        frame_legenda.pack(fill=tk.X, pady=10)

        legendas = [
            ("🤖 Robô (Agente)", "#3498db"),
            ("🗑️ Lixeira (20,20)", "#e74c3c"),
            ("🍂 Lixo Orgânico", "#2ecc71"),
            ("🍾 Lixo Reciclável", "#f1c40f"),
        ]
        for texto, cor in legendas:
            lbl = tk.Label(frame_legenda, text=texto, bg=cor, fg="white", font=("Arial", 9, "bold"), pady=2)
            lbl.pack(fill=tk.X, pady=2)

        # Grid Canvas
        self.canvas_size = 600
        self.cell_size = self.canvas_size // self.tamanho
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="#f0f0f0")
        self.canvas.pack(side=tk.RIGHT, padx=20, pady=20)

    def resetar_ambiente(self):
        self.animando = False
        self.lixos = agentes.criar_ambiente()
        self.posicao_agente = agentes.POSICAO_INICIAL
        self.carga_agente = None
        self.atualizar_metricas(0, 0, 0, None)
        self.desenhar_grid()

    def atualizar_metricas(self, passos, pontos, coletados, carga):
        self.lbl_passos.config(text=f"Passos: {passos}")
        self.lbl_pontos.config(text=f"Pontuação: {pontos}")
        total = agentes.QUANTIDADE_ORGANICO + agentes.QUANTIDADE_RECICLAVEL
        self.lbl_coletados.config(text=f"Lixos Coletados: {coletados} / {total}")
        
        texto_carga = "Livre" if carga is None else ("Orgânico (O)" if carga == "O" else "Reciclável (R)")
        self.lbl_carga.config(text=f"Carga Atual: {texto_carga}")

    def desenhar_grid(self):
        self.canvas.delete("all")

        for r in range(1, self.tamanho + 1):
            for c in range(1, self.tamanho + 1):
                x1 = (c - 1) * self.cell_size
                y1 = (r - 1) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                pos = (r, c)
                cor_fundo = "#ffffff"
                texto = ""

                # Definindo cores e ícones por elemento
                if pos == self.posicao_agente:
                    cor_fundo = "#3498db"
                    texto = "🤖"
                elif pos == agentes.POSICAO_LIXEIRA:
                    cor_fundo = "#e74c3c"
                    texto = "🗑️"
                elif pos in self.lixos:
                    tipo = self.lixos[pos]
                    if tipo == "O":
                        cor_fundo = "#2ecc71"
                        texto = "🍂"
                    else:
                        cor_fundo = "#f1c40f"
                        texto = "🍾"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cor_fundo, outline="#dcdde1")
                if texto:
                    self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, text=texto, font=("Arial", 12))

    def iniciar_simulacao(self):
        if self.animando:
            return
        
        self.resetar_ambiente()
        self.animando = True

        agente_selecionado = self.combo_agentes.get()
        
        # Gerador passo a passo conforme a escolha na interface
        if agente_selecionado == "Reativo Simples":
            passos_generator = self._passo_a_passo_simples()
        elif agente_selecionado == "Baseado em Modelos":
            passos_generator = self._passo_a_passo_modelos()
        elif agente_selecionado == "Baseado em Objetivos":
            passos_generator = self._passo_a_passo_objetivos()
        else:
            passos_generator = self._passo_a_passo_utilidades()

        self._executar_passo(passos_generator)

    def _executar_passo(self, generator):
        if not self.animando:
            return

        try:
            estado = next(generator)
            self.posicao_agente = estado["posicao"]
            self.carga_agente = estado["carga"]
            self.lixos = estado["lixos"]
            
            self.atualizar_metricas(
                estado["passos"], 
                estado["pontuacao"], 
                estado["coletados"], 
                estado["carga"]
            )
            self.desenhar_grid()

            atraso = self.scale_velocidade.get()
            self.root.after(atraso, lambda: self._executar_passo(generator))

        except StopIteration:
            self.animando = False

    # --- GERADORES adaptados mantendo a lógica exata dos seus agentes ---

    def _passo_a_passo_simples(self):
        lixos = dict(agentes.criar_ambiente())
        pos = agentes.POSICAO_INICIAL
        carga = None
        pontos = 0
        coletados = 0
        passos = 0

        while lixos or carga is not None:
            if passos >= 20000: break

            if pos in lixos and carga is None:
                carga = lixos.pop(pos)
            elif carga is not None and pos == agentes.POSICAO_LIXEIRA:
                valor = agentes.VALOR_RECICLAVEL if carga == "R" else agentes.VALOR_ORGANICO
                pontos += valor
                coletados += 1
                carga = None
            elif carga is None:
                vizinho = agentes.escolher_vizinho_com_lixo(pos, lixos)
                if vizinho:
                    pos = agentes.passo_em_direcao(pos, vizinho)
                else:
                    pos = random.choice(agentes.obter_vizinhos(pos))
                passos += 1
            else:
                pos = agentes.passo_em_direcao(pos, agentes.POSICAO_LIXEIRA)
                passos += 1

            yield {"posicao": pos, "carga": carga, "lixos": lixos, "passos": passos, "pontuacao": pontos, "coletados": coletados}

    def _passo_a_passo_modelos(self):
        lixos = dict(agentes.criar_ambiente())
        pos = agentes.POSICAO_INICIAL
        carga = None
        V = [[0] * (agentes.TAMANHO + 1) for _ in range(agentes.TAMANHO + 1)]
        V[pos[0]][pos[1]] = 1
        pontos = 0
        coletados = 0
        passos = 0

        while lixos or carga is not None:
            if passos >= 20000: break

            if pos in lixos and carga is None:
                carga = lixos.pop(pos)
            elif carga is not None and pos == agentes.POSICAO_LIXEIRA:
                valor = agentes.VALOR_RECICLAVEL if carga == "R" else agentes.VALOR_ORGANICO
                pontos += valor
                coletados += 1
                carga = None
            elif carga is not None:
                pos = agentes.passo_em_direcao(pos, agentes.POSICAO_LIXEIRA)
                passos += 1
                V[pos[0]][pos[1]] += 1
            elif carga is None:
                vizinho = agentes.escolher_vizinho_com_lixo(pos, lixos)
                if vizinho:
                    pos = agentes.passo_em_direcao(pos, vizinho)
                    passos += 1
                    V[pos[0]][pos[1]] += 1
                else:
                    vizinhos = agentes.obter_vizinhos(pos)
                    menor = min(V[v[0]][v[1]] for v in vizinhos)
                    candidatos = [v for v in vizinhos if V[v[0]][v[1]] == menor]
                    pos = random.choice(candidatos)
                    passos += 1
                    V[pos[0]][pos[1]] += 1

            yield {"posicao": pos, "carga": carga, "lixos": lixos, "passos": passos, "pontuacao": pontos, "coletados": coletados}

    def _passo_a_passo_objetivos(self):
        lixos = dict(agentes.criar_ambiente())
        crencas = {
            "posicao": agentes.POSICAO_INICIAL,
            "carga": None,
            "V": [[0] * (agentes.TAMANHO + 1) for _ in range(agentes.TAMANHO + 1)],
            "lixos_conhecidos": {}
        }
        crencas["V"][agentes.POSICAO_INICIAL[0]][agentes.POSICAO_INICIAL[1]] = 1

        def perc():
            p = crencas["posicao"]
            if p in lixos: crencas["lixos_conhecidos"][p] = lixos[p]
            elif p in crencas["lixos_conhecidos"]: del crencas["lixos_conhecidos"][p]
            for v in agentes.obter_vizinhos(p):
                if v in lixos: crencas["lixos_conhecidos"][v] = lixos[v]
                elif v in crencas["lixos_conhecidos"]: del crencas["lixos_conhecidos"][v]

        perc()
        pontos = 0
        coletados = 0
        passos = 0

        while lixos or crencas["carga"] is not None:
            if passos >= 20000: break
            pos = crencas["posicao"]
            carga = crencas["carga"]
            rec = [p for p, t in crencas["lixos_conhecidos"].items() if t == "R"]

            if pos in lixos and carga is None and (lixos[pos] == "R" or not rec):
                carga = lixos.pop(pos)
                crencas["carga"] = carga
                crencas["lixos_conhecidos"].pop(pos, None)
            elif carga is not None and pos == agentes.POSICAO_LIXEIRA:
                pontos += agentes.VALOR_RECICLAVEL if carga == "R" else agentes.VALOR_ORGANICO
                coletados += 1
                crencas["carga"] = None
            elif carga is not None:
                pos = agentes.passo_em_direcao(pos, agentes.POSICAO_LIXEIRA)
                passos += 1
                crencas["posicao"] = pos
                crencas["V"][pos[0]][pos[1]] += 1
                perc()
            else:
                org = [p for p, t in crencas["lixos_conhecidos"].items() if t == "O"]
                if rec:
                    meta = min(rec, key=lambda p: agentes.distancia_manhattan(pos, p))
                elif org:
                    meta = min(org, key=lambda p: agentes.distancia_manhattan(pos, p))
                else:
                    nao_vis = [(l, c) for l in range(1, agentes.TAMANHO + 1) for c in range(1, agentes.TAMANHO + 1) if crencas["V"][l][c] == 0]
                    if nao_vis:
                        meta = min(nao_vis, key=lambda p: (agentes.distancia_manhattan(pos, p), p[0], p[1]))
                    else:
                        menor = min(crencas["V"][l][c] for l in range(1, agentes.TAMANHO + 1) for c in range(1, agentes.TAMANHO + 1))
                        cand = [(l, c) for l in range(1, agentes.TAMANHO + 1) for c in range(1, agentes.TAMANHO + 1) if crencas["V"][l][c] == menor]
                        meta = min(cand, key=lambda p: (agentes.distancia_manhattan(pos, p), p[0], p[1]))

                pos = agentes.passo_em_direcao(pos, meta)
                passos += 1
                crencas["posicao"] = pos
                crencas["V"][pos[0]][pos[1]] += 1
                perc()

            yield {"posicao": crencas["posicao"], "carga": crencas["carga"], "lixos": lixos, "passos": passos, "pontuacao": pontos, "coletados": coletados}

    def _passo_a_passo_utilidades(self):
        lixos = dict(agentes.criar_ambiente())
        crencas = {
            "posicao": agentes.POSICAO_INICIAL,
            "carga": None,
            "V": [[0] * (agentes.TAMANHO + 1) for _ in range(agentes.TAMANHO + 1)],
            "lixos_conhecidos": {}
        }
        crencas["V"][agentes.POSICAO_INICIAL[0]][agentes.POSICAO_INICIAL[1]] = 1

        def perc():
            p = crencas["posicao"]
            if p in lixos: crencas["lixos_conhecidos"][p] = lixos[p]
            elif p in crencas["lixos_conhecidos"]: del crencas["lixos_conhecidos"][p]
            for v in agentes.obter_vizinhos(p):
                if v in lixos: crencas["lixos_conhecidos"][v] = lixos[v]
                elif v in crencas["lixos_conhecidos"]: del crencas["lixos_conhecidos"][v]

        perc()
        pontos = 0
        coletados = 0
        passos = 0

        while lixos or crencas["carga"] is not None:
            if passos >= 20000: break
            pos = crencas["posicao"]
            carga = crencas["carga"]

            if pos in lixos and carga is None:
                carga = lixos.pop(pos)
                crencas["carga"] = carga
                crencas["lixos_conhecidos"].pop(pos, None)
            elif carga is not None and pos == agentes.POSICAO_LIXEIRA:
                pontos += agentes.VALOR_RECICLAVEL if carga == "R" else agentes.VALOR_ORGANICO
                coletados += 1
                crencas["carga"] = None
            elif carga is not None:
                pos = agentes.passo_em_direcao(pos, agentes.POSICAO_LIXEIRA)
                passos += 1
                crencas["posicao"] = pos
                crencas["V"][pos[0]][pos[1]] += 1
                perc()
            else:
                if crencas["lixos_conhecidos"]:
                    melhor = None
                    maior_u = -float('inf')
                    for p_lixo, t_lixo in crencas["lixos_conhecidos"].items():
                        v = agentes.VALOR_RECICLAVEL if t_lixo == "R" else agentes.VALOR_ORGANICO
                        d1 = agentes.distancia_manhattan(pos, p_lixo)
                        d2 = agentes.distancia_manhattan(p_lixo, agentes.POSICAO_LIXEIRA)
                        u = v - d1 - d2
                        if u > maior_u:
                            maior_u = u
                            melhor = p_lixo
                    meta = melhor
                else:
                    nao_vis = [(l, c) for l in range(1, agentes.TAMANHO + 1) for c in range(1, agentes.TAMANHO + 1) if crencas["V"][l][c] == 0]
                    if nao_vis:
                        meta = min(nao_vis, key=lambda p: (agentes.distancia_manhattan(pos, p), p[0], p[1]))
                    else:
                        menor = min(crencas["V"][l][c] for l in range(1, agentes.TAMANHO + 1) for c in range(1, agentes.TAMANHO + 1))
                        cand = [(l, c) for l in range(1, agentes.TAMANHO + 1) for c in range(1, agentes.TAMANHO + 1) if crencas["V"][l][c] == menor]
                        meta = min(cand, key=lambda p: (agentes.distancia_manhattan(pos, p), p[0], p[1]))

                pos = agentes.passo_em_direcao(pos, meta)
                passos += 1
                crencas["posicao"] = pos
                crencas["V"][pos[0]][pos[1]] += 1
                perc()

            yield {"posicao": crencas["posicao"], "carga": crencas["carga"], "lixos": lixos, "passos": passos, "pontuacao": pontos, "coletados": coletados}

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceAgentes(root)
    root.mainloop()