import streamlit as st
import random

def escolher_dificuldade():
    st.subheader("Nível de Dificuldade do Bot")
    dificuldade = st.radio(
        "Escolha o nível:",
        options=["Fácil", "Médio", "Difícil"],
        index=1,
        horizontal=True
    )
    return ["Fácil", "Médio", "Difícil"].index(dificuldade) + 1

def jogada_bot(total_bolinhas, max_retirada, nome_bot, dificuldade):
    # Verifica se pode ganhar na jogada atual
    if total_bolinhas <= max_retirada + 1:
        jogada = total_bolinhas - 1 if total_bolinhas > 1 else 1
        st.write(f"**{nome_bot} retira {jogada} bolinhas.**")
        return jogada

    # Se não for jogada decisiva, segue a lógica normal
    alvo = 1
    while alvo <= total_bolinhas:
        alvo += max_retirada + 1
    jogada_otima = total_bolinhas - (alvo - (max_retirada + 1))

    jogada_otima_valida = (1 <= jogada_otima <= max_retirada)

    if jogada_otima_valida:
        if dificuldade == 1:  # Fácil
            usar_otima = random.random() < 0.3
        elif dificuldade == 2:  # Médio
            usar_otima = random.random() < 0.6
        else:  # Difícil
            usar_otima = True
    else:
        usar_otima = False

    if usar_otima:
        jogada = jogada_otima
    else:
        max_possivel = min(max_retirada, total_bolinhas)
        jogada = random.randint(1, max_possivel)

    st.write(f"**{nome_bot} retira {jogada} bolinhas.**")
    return jogada

def main():
    st.title("🎮 Jogo do Nim - Último Perde")
    
    # Inicialização de variáveis de estado
    if 'total_bolinhas' not in st.session_state:
        st.session_state.total_bolinhas = 0
    if 'max_retirada' not in st.session_state:
        st.session_state.max_retirada = 0
    if 'jogador_atual' not in st.session_state:
        st.session_state.jogador_atual = 1
    if 'nome_jogador1' not in st.session_state:
        st.session_state.nome_jogador1 = ""
    if 'nome_jogador2' not in st.session_state:
        st.session_state.nome_jogador2 = ""
    if 'modo' not in st.session_state:
        st.session_state.modo = 0
    if 'dificuldade' not in st.session_state:
        st.session_state.dificuldade = 0
    if 'jogo_iniciado' not in st.session_state:
        st.session_state.jogo_iniciado = False
    if 'vez_bot' not in st.session_state:
        st.session_state.vez_bot = False
    
    # Tela inicial de configuração
    if not st.session_state.jogo_iniciado:
        st.header("Configuração do Jogo")
        
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.total_bolinhas = st.number_input(
                "Quantas bolinhas terá a pilha inicial?",
                min_value=2, max_value=100, value=15
            )
        with col2:
            st.session_state.max_retirada = st.number_input(
                "Máximo de bolinhas por jogada:",
                min_value=1, max_value=10, value=3
            )
        
        st.session_state.modo = st.radio(
            "Modo de Jogo:",
            options=["Um Jogador vs Bot", "Dois Jogadores"],
            index=0,
            horizontal=True
        )
        
        if st.session_state.modo == "Um Jogador vs Bot":
            st.session_state.nome_jogador1 = st.text_input("Digite seu nome:", "Jogador")
            st.session_state.nome_jogador2 = "Bot"
            st.session_state.dificuldade = escolher_dificuldade()
        else:
            st.session_state.nome_jogador1 = st.text_input("Nome do Jogador 1:", "Jogador 1")
            st.session_state.nome_jogador2 = st.text_input("Nome do Jogador 2:", "Jogador 2")
        
        if st.button("Iniciar Jogo"):
            st.session_state.jogo_iniciado = True
            st.session_state.vez_bot = False
            
            # Decidir quem começa no modo PvE
            if st.session_state.modo == "Um Jogador vs Bot":
                st.session_state.cara_ou_coroa = st.radio(
                    f"{st.session_state.nome_jogador1}, escolha cara ou coroa:",
                    options=["Cara", "Coroa"],
                    horizontal=True
                )
                st.session_state.resultado_sorteio = random.choice(["Cara", "Coroa"])
                
                if st.session_state.cara_ou_coroa == st.session_state.resultado_sorteio:
                    st.success(f"Resultado: {st.session_state.resultado_sorteio}! Você ganhou o sorteio!")
                    iniciante = st.radio(
                        "Quem deve começar?",
                        options=[st.session_state.nome_jogador1, st.session_state.nome_jogador2],
                        horizontal=True
                    )
                    st.session_state.jogador_atual = 1 if iniciante == st.session_state.nome_jogador1 else 2
                else:
                    st.warning(f"Resultado: {st.session_state.resultado_sorteio}! O Bot decide quem começa.")
                    
                    if (st.session_state.total_bolinhas - 1) % (st.session_state.max_retirada + 1) == 0:
                        st.info(f"O Bot escolhe que {st.session_state.nome_jogador1} começa.")
                        st.session_state.jogador_atual = 1
                    else:
                        st.info("O Bot escolhe começar!")
                        st.session_state.jogador_atual = 2
                
                if st.session_state.jogador_atual == 2:
                    st.session_state.vez_bot = True
            else:
                st.session_state.jogador_atual = 1
            
            st.experimental_rerun()
    
    # Tela principal do jogo
    else:
        st.header("Partida em Andamento")
        
        # Mostrar bolinhas restantes
        bolinhas_visual = '● ' * st.session_state.total_bolinhas
        st.subheader(f"Bolinhas restantes: {bolinhas_visual}({st.session_state.total_bolinhas})")
        
        # Verificar condições de término
        if st.session_state.total_bolinhas == 0:
            perdedor = st.session_state.nome_jogador2 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador1
            vencedor = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador2
            st.error(f"{perdedor} retirou a última bolinha e PERDEU!")
            st.success(f"🏆 {vencedor} venceu! Parabéns!")
            
            if st.button("Jogar Novamente"):
                st.session_state.jogo_iniciado = False
                st.experimental_rerun()
            return
        
        elif st.session_state.total_bolinhas == 1:
            perdedor = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador2
            vencedor = st.session_state.nome_jogador2 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador1
            st.error(f"{perdedor} é forçado a retirar a última bolinha e PERDE!")
            st.success(f"🏆 {vencedor} venceu! Parabéns!")
            
            if st.button("Jogar Novamente"):
                st.session_state.jogo_iniciado = False
                st.experimental_rerun()
            return
        
        # Vez do Bot
        if st.session_state.modo == "Um Jogador vs Bot" and st.session_state.jogador_atual == 2:
            if st.session_state.vez_bot:
                jogada = jogada_bot(
                    st.session_state.total_bolinhas,
                    st.session_state.max_retirada,
                    st.session_state.nome_jogador2,
                    st.session_state.dificuldade
                )
                st.session_state.total_bolinhas -= jogada
                st.session_state.jogador_atual = 1
                st.session_state.vez_bot = False
                st.experimental_rerun()
            else:
                st.session_state.vez_bot = True
                st.experimental_rerun()
        
        # Vez do Jogador
        else:
            jogador_atual_nome = st.session_state.nome_jogador1 if st.session_state.jogador_atual == 1 else st.session_state.nome_jogador2
            st.subheader(f"Vez de: {jogador_atual_nome}")
            
            max_permitido = min(st.session_state.max_retirada, st.session_state.total_bolinhas)
            jogada = st.number_input(
                f"{jogador_atual_nome}, quantas bolinhas deseja retirar (1-{max_permitido})?",
                min_value=1,
                max_value=max_permitido,
                value=1,
                step=1
            )
            
            if st.button("Realizar Jogada"):
                st.session_state.total_bolinhas -= jogada
                st.session_state.jogador_atual = 3 - st.session_state.jogador_atual
                st.experimental_rerun()
        
        if st.button("Reiniciar Jogo"):
            st.session_state.jogo_iniciado = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
