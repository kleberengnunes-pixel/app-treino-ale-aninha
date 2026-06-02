# Execução em Mobile e Desktop

## Conceito correto

Este simulador é uma aplicação web em Python/Streamlit. Portanto:

- No desktop, ele pode rodar diretamente no computador.
- No celular, o app é acessado pelo navegador.
- O celular não precisa instalar Python.
- O computador, servidor ou serviço cloud é quem executa o Python.

## Desktop local

```bash
streamlit run app.py
```

URL padrão:

```text
http://localhost:8501
```

## Celular na mesma rede Wi-Fi

Execute no computador:

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

Depois acesse no celular:

```text
http://IP_DO_COMPUTADOR:8501
```

Exemplo:

```text
http://192.168.0.25:8501
```

## Ajuste visual no celular

Após login:

1. Abra o menu lateral.
2. Em `Modo de visualização`, selecione `Mobile`.
3. Use a caixa `Seção` para alternar entre os blocos:
   - Osciloscópio
   - Scanner e DTC
   - Descrição técnica
   - Teste guiado
   - Banco de imagens

## Desktop

No desktop, selecione `Desktop` ou mantenha `Automático`.

## Acesso fora da rede local

Para acesso externo, publique o projeto em um servidor ou plataforma compatível com Streamlit. O link gerado poderá ser aberto em qualquer desktop ou celular.
