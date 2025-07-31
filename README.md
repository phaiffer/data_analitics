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

## 📧 Documentação – Coletor de E-mails de Sites

### 📌 Objetivo

Este script automatiza a extração de endereços de e-mail de sites informados em um arquivo `.csv`. Ele navega nas páginas iniciais e também em páginas relacionadas a contato, utilizando `Selenium` e `re` (expressões regulares).

---

### 📂 Entrada

Um arquivo CSV chamado `links.csv` com uma coluna `url`:

```csv
url
https://empresa1.com
https://empresa2.org
...
```

---

### 📤 Saída

* `emails_encontrados.csv`: Contém os sites e os e-mails encontrados.
* `sem_email.csv`: Lista os sites onde nenhum e-mail foi encontrado.

---

### 📦 Requisitos

```bash
pip install selenium pandas chromedriver-autoinstaller
```

---

### 🧠 Como Funciona

1. Lê os sites a partir de `links.csv`.
2. Usa `Selenium` (em modo headless) para visitar os sites.
3. Extrai os e-mails da página inicial.
4. Se necessário, acessa páginas de contato (usando palavras-chave como “contato”, “contact”, etc.).
5. Extrai e valida os e-mails usando expressões regulares.
6. Salva os resultados em dois arquivos CSV.

---

### 🔍 Palavras-chave para identificar páginas de contato

```python
KEYWORDS = ['contato', 'fale conosco', 'about', 'about us', 'contact', 'contact us', 'contáctanos']
```

---

### 📁 Principais Funções

#### `get_domain_from_url(url)`

Extrai e padroniza o domínio a partir da URL.

#### `create_email_pattern(domain)`

Gera um padrão regex específico para e-mails daquele domínio.

#### `setup_driver(headless)`

Configura o navegador Chrome para automação.

#### `find_emails_on_page(driver, pattern)`

Busca e-mails na página atual com base no padrão regex.

#### `find_contact_links(driver)`

Procura links na página atual que levem a páginas de contato.

#### `scrape_emails_from_site(url)`

Função principal que executa o processo de scraping em um único site.

#### `save_results(...)`

Salva os e-mails encontrados e os sites sem e-mail nos arquivos finais.

---

### 🛠 Sugestões de melhorias

* Adicionar suporte a múltiplos domínios por página.
* Tornar o tempo de `sleep` aleatório para evitar bloqueios.
* Adicionar tratamento para redirecionamentos.
* Incluir barra de progresso com `tqdm`.

---

### 👨‍💻 Autor

Willian Phaiffer Cardoso.

---
