from bs4 import BeautifulSoup
import requests, os, ast


# Código HTML
html = """
"""

soup = BeautifulSoup(html, 'html.parser')

client_list = []

# Encontra todas as tags "tr"
tr_tags = soup.find_all('tr')
for tr in tr_tags:
    # Encontra todas as tags "td" dentro das "tr"
    td_elements = tr.find_all('td')
    
    client_name = "N/A"

    # Encontra o nome do cliente
    if len(td_elements) >= 4:
        if len(td_elements) >= 5:
            client_name = td_elements[4].get_text(strip=True)
        else:
            client_name = td_elements[3].get_text(strip=True)

    # Adiciona na lista o nome do cliente
    if client_name != "N/A":
        client_list.append(client_name)

# Encontra todas as URLs dos pedidos
urls = soup.find_all('a', href=lambda href: href and '/pedidos/' in href)

# Cookies para autenticação
cookie = "{'Cookie':''}"
result = ast.literal_eval(cookie)
AuthCookies = result

# Diretorio onde serão salvos os PDFs
download_directory = ''

# Cria o diretorio por se não existe
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

c = 0

for url in urls:
    # Cria e formata a url
    href = url['href']
    href_replaced = href.replace("detalhar","pdf")
    full_url = f"https://app.mercos.com{href_replaced}"

    # Manda a request
    response = requests.get(full_url, headers=AuthCookies)

    # Define o nome do arquivo
    if response.status_code == 200 and response.headers.get('content-type') == 'application/pdf':
        filename = os.path.join(download_directory, os.path.basename(href_replaced))
 
    client_name = client_list[c]
    
    # Filtra o nome do cliente
    if "/" in client_name:
        client_name = client_name.replace("/","-")

    # Caso a extensão não seja pdf o nome é formatado
    if not filename.endswith(".pdf"):
        filename += f"{c+1}_{client_name}.pdf" 

    # Escreve e guarda os arquivos
    with open(filename, 'wb') as pdf_file:
        pdf_file.write(response.content)

    c += 1

print(f"Foram importados: {c} pedidos")