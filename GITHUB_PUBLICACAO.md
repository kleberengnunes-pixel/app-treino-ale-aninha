# Como publicar o EVSimulator no GitHub

## Opção mais simples

1. Extraia o `.zip` em uma pasta no computador.
2. Abra essa pasta no **VS Code**.
3. Abra o terminal dentro da pasta.
4. Execute:

```bash
git init
git add .
git commit -m "Primeira versao do EVSimulator"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/EVSimulator.git
git push -u origin main
```

## Se o Git pedir login

Hoje o GitHub normalmente usa:

- login da conta GitHub;
- ou token pessoal (Personal Access Token), no lugar da senha.

## Se quiser publicar online

Após subir no GitHub, você pode usar:

- **Streamlit Community Cloud**
- **Render**
- **Railway**
- servidor próprio/VPS

## Arquivo principal para deploy

```text
app.py
```

## Dependências

O deploy vai instalar automaticamente o que está em:

```text
requirements.txt
```

