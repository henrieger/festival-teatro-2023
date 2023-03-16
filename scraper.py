#!/usr/bin/python

import requests

def main():
    response = make_request('https://nucleo.jor.br')
    print(response.text)

def make_request(url: str, wait_time=10, max_wait_time=160, panic_counter=0, max_panic_counter=10) -> requests.Response:
    response = requests.get(url)
    status_code = response.status_code

    if(status_code >= 400):
        print(f"Request para {url} com erro {status_code}.", endl=' ')
        if panic_counter >= max_panic_counter:
            printf("PANICO!!! Abortando scraper...")
            quit()
        wt = min(wait_time, max_wait_time)
        print(f"Aguardando {wt} segundos...")
        time.sleep(wt)
        response = make_request(url, wait_time*2)
    return response

if __name__ == '__main__':
    main()
