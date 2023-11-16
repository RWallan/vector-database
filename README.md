# Repositório de aprendizado de Vector Database

Repositório que introduz o conceito básico de vector-databases e exemplos utilizando banco de dados locais com o ChromaDB.

## O que é Vector Database

O Vector Database - que será chamado como VecDB nesse repositório - consiste em um banco de dados especializado para armazenar e manipular dados vetoriais altamente dimensionados de forma eficiente.

Hoje em dia é extremamente necessário utilizar esse tipo de banco de dados pois 80% das informações disponíveis estão de maneira não estruturadas ([Onna](https://onna.com/maximizing-value-of-unstructured-data)). Armazenar e fazer queries de maneira eficiente ainda podem ser problemas mesmo nos bancos de dados não relacionais.

### O fluxograma do VecDB

De maneira geral, o fluxograma para construir os vetores seguem como na imagem abaixo:

![VecDB Fluxograma](/public/vecdb_fluxogram.png)

Com isso, é possível calcular a similaridade entre os vetores a partir de cálculos vetoriais, tais como:

* Distância euclidiana
* Cosseno
* Manhattan

![VecDB Similaridade](/public/vecdb_similarity.png)

## O que irá encontrar nesse repositório

* Uma breve introdução aos conceito de Vector Database;
* Exemplos simples mostrando como funciona o armazenamento em um banco de dados relacional e em um banco de dados vetorial;
* Como fazer queries para buscar os documentos;
* Pipelines para tratar dados

Os exemplos se basearão no banco de dados **Medium Post Titles** disponível no [Kaggle](https://www.kaggle.com/datasets/nulldata/medium-post-titles). Também estará uma no repositório a partir de um arquivo `.csv` no diretório `data/0_raw`.

# Referências

* [Master Vector Database with Python for AI & LLM Use Cases](https://www.udemy.com/course/vector-db/)

* [Onna](https://onna.com/maximizing-value-of-unstructured-data)

# Requisitos

Python 3.11.

Este repositório conta com as principais bibliotecas:

* [ChromaDB](https://www.trychroma.com/)
* [Pandas](https://pandas.pydata.org/docs/)

E o [Poetry]() como gerenciados de bibliotecas.

# Como instalar

Para instalar o projeto, primeiramente clone-o do github

```bash
git clone https://github.com/RWallan/vector-database.git
cd vector-database
```

E instale as dependências

```bash
poetry install
```

# Licença

Esse projeto está sob os termos da licença MIT.

