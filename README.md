## 📝 Documentação – Extração de Perfis da Web Summit

### 📌 Objetivo

Este script automatiza a extração de informações públicas de startups listadas na Web Summit, acessando suas páginas individuais e coletando:

* Nome da startup
* Descrição
* País
* Segmento
* Link para Instagram
* Link para LinkedIn
* Website oficial

Os dados são extraídos usando `Selenium` + `BeautifulSoup` e salvos em um arquivo `.xlsx`.

---

### 📂 Entrada

Um arquivo CSV chamado `startup_urls.csv` com a seguinte estrutura:

```csv
url
https://websummit.com/appearances/lis24/xxxxxx/startup-name
https://websummit.com/appearances/lis24/yyyyyy/startup-name-2
...
```

A coluna `url` deve conter os links diretos das startups no site da Web Summit.

---

### 📦 Requisitos

Instale os pacotes necessários:

```bash
pip install selenium beautifulsoup4 pandas chromedriver-autoinstaller openpyxl
```

---

### 🧠 Como Funciona

1. **Lê as URLs do arquivo `startup_urls.csv`**
2. **Abre cada página usando Selenium (com Chrome)**
3. **Aguarda até que os dados estejam carregados**
4. **Usa BeautifulSoup para fazer parsing do HTML**
5. **Extrai os dados usando seletores CSS**
6. **Filtra os links do Instagram e LinkedIn**
7. **Coleta o link do website (posição 2 entre os botões)**
8. **Armazena todos os dados em uma planilha Excel (`.xlsx`)**

---

### 📤 Saída

* `perfis_extraidos.xlsx`: Planilha com os dados extraídos
* `erros_de_extracao.xlsx` (opcional): URLs que apresentaram falha na coleta

---

### 🧾 Estrutura do Código

#### Bibliotecas e configuração do WebDriver:

* Usa `chromedriver_autoinstaller` para garantir compatibilidade com o navegador.
* `Selenium` é usado para renderizar a página e esperar o conteúdo carregar.

#### Leitura de URLs:

```python
df_urls = pd.read_csv('startup_urls.csv')
```

#### Extração de informações com `BeautifulSoup`:

```python
soup.select('[class^="headlines__H1"]')  # Nome
soup.select('[class^="ProfileDetails__ProfileDetailsContent"] > div')  # Descrição
soup.select('[class^="ContentTagList__ContentTagListItem"]')  # País e Segmento
soup.select('[class^="DetailsLayout__SocialMediaWrapper"]')  # Redes sociais
soup.select('[class^="Button__StyledButton"]')  # Botões (Website)
```

#### Filtro de links:

* Instagram: se `'instagram.com' in href`
* LinkedIn: se `'linkedin.com' in href`
* Website: botão na posição 2 (índice 2) da lista de botões com `href`

---

### 📌 Exemplo de saída:

| name     | description    | country | segment | instagram                                           | linkedin                                          | web\_site                                  |
| -------- | -------------- | ------- | ------- | --------------------------------------------------- | ------------------------------------------------- | ------------------------------------------ |
| Schoolux | Edtech startup | Brazil  | EdTech  | [https://instagram.com/](https://instagram.com/)... | [https://linkedin.com/](https://linkedin.com/)... | [https://schoolux.ai](https://schoolux.ai) |

---

### 🛠 Possíveis melhorias (futuras)

* Adicionar `time.sleep()` aleatório entre requisições para evitar bloqueios.
* Permitir salvar dados parcialmente mesmo se interrompido.
* Usar `tqdm` para barra de progresso.
* Modularizar em funções ou classes para reaproveitamento.

---

### 👨‍💻 Autor

Willian Phaiffer Cardoso.

---
