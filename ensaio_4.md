# Resumo

Nesta versão, o bot ganhou a capacidade de gerar texto. Para tanto, toda vez que o bot crawlear 100 novas URLS, ele
treinará, em um processo separado, uma LSTM para gerar textos. Assim, ao utilizar a função generate, será respondido um
frase, contendo 10 palavras, correlacionada a notícia. Os pontos mais críticos para o desenvolivimento foram a
implementação da rede neural, de treinamento, em paralelo ao código, juntamente a organização do mesmo. Para tanto, o
arquivo main.py foi reescrito assim como algumas outras mudanças foram realizadas.

As fontes consultadas foram:

- https://chat.openai.com/?model=gpt-4
    - Ajudou a refatorar o código
    - Ajudou na implementação via multiprocessamento da rede neural
- https://github.com/tiagoft/NLP/
