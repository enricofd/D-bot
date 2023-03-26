# Resumo

Nesta versão, o bot ganhou a capacidade de baixar dados da internet, por meio do crawling. Além disso, para realizar busca nesse conteúdo, está sendo utilizado duas estratégia, uma de índice invertido e outra de similidaridade. Ou seja, busca-se no banco de dados as palavras de maior similaridade com as pesquisadas, e a partir delas, utiliza-se a estratégia de ídice invertido.

O maior desafio dessa implementação foi o crawling. Muitas vezes o processo era demasiadamente demorado, então, balancear essa demora com um bom resultado não foi um tarefa fácil. No fim dia, utilizando a profundidade de busca de 1, acabou se mostrando suficiente. Muitas vezes, ao passar uma URL, são retornados mais de 50 valores, o que já acrescenta, e muito, ao banco de dados.

As fontes consultadas foram:

- https://github.com/tiagoft/NLP/
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
