# Resumo

Nesta versão, o bot ganhou a capacidade de filtrar conteúdo considerado negativo. Para tanto, basta, ao realizar uma busca, por meio de !search ou !wn_search, utilizar o parâmetro th=y, onde y é um float. Vale notar que est parâmetro é opcional, mas se for utilizado, deve receber um float (ex: 1.0)

O maior desafio dessa implementação foi relacionada ao ambiente e coleta dos dados. Ao utilizar o tensorflow com o keras, muitas bibliotecas ficaram incopátiveis. O segundo ponto foi quanto encontrar uma base de dados para realizar o treinamento, que no final acabou sendo uma do Twitter mais uma do IMDB.

As fontes consultadas foram:

- https://github.com/tiagoft/NLP/
- https://www.kaggle.com/datasets/abhi8923shriv/sentiment-analysis-dataset?resource=download&select=train.csv
