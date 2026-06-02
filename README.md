# EVSimulator V3 – Simulador Automotivo Interativo

Aplicação em **Python + Streamlit** para treinamento técnico em diagnóstico automotivo e veículos eletrificados.

Esta versão V3 já foi ajustada com:

- **nova interface visual** em estilo dashboard/landing page com o veículo enviado pelo usuário;
- uso em **desktop e mobile**;
- **login com usuário e senha**;
- identificação de **nome** e **turma**;
- painel com **imagem do componente, alimentação, terra, sinal, pinos, forma de onda, sintomas e DTCs**.
- osciloscópio com **sinais em tempo real** (animação automática).
- **tela separada por perfil**: aluno e professor.
- **salvamento das respostas dos alunos em SQLite**.
- **painel do professor** com filtros e exportação CSV.
- **mapa interativo do veículo** para selecionar módulos como ECM, PCM, TCM, BCM, ABS, SRS, EPS e EPB.

---

## 1. Recursos incluídos

- Login por usuário e senha com hash SHA-256 em `data/users.json`.
- Perfis `professor` e `aluno`.
- Tela inicial com identidade visual tipo **EVSimulator**.
- Layout responsivo para desktop, tablet e celular.
- Modo de visualização: `Automático`, `Desktop` ou `Mobile`.
- Banco ampliado com sensores, atuadores e módulos automotivos.
- Simulação de sinais: analógico 0–5 V, NTC, Hall/frequência, lambda, piezo, PWM, motor DC, CAN, ultrassom e resistivo, com atualização em tempo real.
- Modos de falha: normal, circuito aberto, curto ao terra, curto ao positivo, intermitente e fora de faixa/plausibilidade.
- DTCs simulados com descrição técnica.
- Imagens vetoriais didáticas geradas internamente.
- Pasta de referências com imagens melhoradas para uso interno.


### Principais módulos incluídos

- ECM / ECU – Módulo de Controle do Motor
- PCM – Módulo de Controle do Trem de Força
- BCM – Módulo de Controle da Carroceria
- TCM – Módulo de Controle da Transmissão
- ABS – Módulo do Freio Antitravamento
- SRS – Módulo do Airbag
- EPS – Módulo da Direção Elétrica
- EPB – Módulo do Freio de Estacionamento Eletrônico

---

## 2. Novidades da V3

### Perfil aluno

- Acesso ao simulador.
- Visualização de sensores, atuadores e módulos.
- Seleção de falha simulada.
- Resposta guiada com causa provável e primeiro teste.
- Registro das respostas no banco local SQLite.

### Perfil professor

- Acesso ao roteiro/gabarito técnico.
- Painel de acompanhamento das respostas dos alunos.
- Filtro por turma e componente.
- Exportação das respostas em CSV.

### Mapa interativo do veículo

A tela **Mapa do veículo** permite selecionar os módulos principais e direcionar o estudo para o componente selecionado.

---

## 3. Instalação local

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

### Linux/Mac

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 4. Execução no desktop

### Windows

Execute:

```text
run_desktop.bat
```

ou:

```bash
streamlit run app.py
```

### Linux/Mac

```bash
chmod +x run_desktop.sh
./run_desktop.sh
```

---

## 5. Execução no celular pela mesma rede Wi-Fi

O aplicativo roda no computador e o celular acessa pelo navegador.

### Windows

1. Conecte computador e celular na mesma rede Wi-Fi.
2. Execute:

```text
run_mobile_lan.bat
```

3. Descubra o IP do computador:

```powershell
ipconfig
```

4. Procure o campo `Endereço IPv4`, por exemplo `192.168.0.25`.
5. No navegador do celular, abra:

```text
http://192.168.0.25:8501
```

6. Depois do login, selecione:

```text
Modo de visualização > Mobile
```

### Linux/Mac

```bash
chmod +x run_mobile_lan.sh
./run_mobile_lan.sh
```

Depois, acesse:

```text
http://IP_DO_COMPUTADOR:8501
```

---

## 6. Acesso inicial

| Perfil | Usuário | Senha |
|---|---|---|
| Professor | `professor` | `Senai@2026` |
| Aluno | `aluno` | `1234` |

> **Importante:** altere essas credenciais antes de publicar no GitHub ou colocar o sistema em uso real.

---

## 7. Criar novo usuário

```bash
python scripts/create_user.py
```

O script atualiza `data/users.json` com salt e hash da senha.

---

## 8. Estrutura do projeto

```text
simulador_automotivo_interativo/
├── app.py
├── requirements.txt
├── run_desktop.bat
├── run_desktop.sh
├── run_mobile_lan.bat
├── run_mobile_lan.sh
├── MOBILE_DESKTOP.md
├── data/
│   ├── componentes.json
│   ├── falhas.json
│   ├── users.json
│   └── media_index.csv
├── assets/
│   ├── componentes/
│   └── referencias/
├── scripts/
│   └── create_user.py
└── .streamlit/
    └── config.toml
```

---

## 9. Como adicionar sensores, atuadores ou módulos

1. Coloque a imagem em `assets/componentes/`.
2. Abra `data/componentes.json`.
3. Duplique um bloco existente.
4. Ajuste:
   - `id`
   - `nome`
   - `categoria`
   - `sistema`
   - `tipo_sinal`
   - alimentação
   - sinal
   - DTCs
   - roteiro de diagnóstico
5. Reinicie o Streamlit.

### Tipos de sinal aceitos

- `analogico`
- `digital_freq`
- `ntc`
- `lambda`
- `piezo`
- `pwm_current`
- `motor_dc`
- `can`
- `ultrasonic`
- `resistivo`

---

## 10. Como colocar no GitHub

### Passo 1 — criar o repositório no GitHub

1. Acesse [https://github.com](https://github.com)
2. Clique em **New repository**.
3. Dê um nome, por exemplo:

```text
EVSimulator
```

4. Escolha **Public** ou **Private**.
5. Clique em **Create repository**.

### Passo 2 — enviar o projeto

Abra o terminal dentro da pasta do projeto e execute:

```bash
git init
git add .
git commit -m "Primeira versao do EVSimulator"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/EVSimulator.git
git push -u origin main
```

Substitua `SEU-USUARIO` pelo seu usuário real do GitHub.

### Passo 3 — atualizar versões futuras

Quando você fizer novas alterações:

```bash
git add .
git commit -m "Atualizacao da interface e dos componentes"
git push
```

---

## 11. Como publicar online usando Streamlit Community Cloud

Se quiser abrir pelo navegador com link web:

1. Suba primeiro no GitHub.
2. Acesse: [https://share.streamlit.io](https://share.streamlit.io)
3. Faça login com GitHub.
4. Clique em **New app**.
5. Selecione o repositório `EVSimulator`.
6. Defina o arquivo principal:

```text
app.py
```

7. Clique em **Deploy**.

Pronto: o simulador ficará acessível por link web em desktop e celular.

---

## 12. Publicação segura

Antes de publicar:

1. Troque as senhas demonstrativas em `data/users.json`.
2. Revise os DTCs e descrições conforme manuais reais.
3. Use apenas imagens próprias ou com licença adequada.
4. Se quiser, mova credenciais para variáveis de ambiente em versões futuras.

---

## 13. Observação técnica

Os sinais e DTCs do sistema são **representações didáticas** para ensino e treinamento. Procedimentos reais devem seguir manual do fabricante, diagrama elétrico do veículo e normas de segurança aplicáveis.

---

## 14. Licença sugerida

Código: **MIT License**.

