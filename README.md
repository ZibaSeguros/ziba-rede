# ziba-rede
Redes credenciadas dos estudos

## Rede da cotação (v2, até 3 planos lado a lado)
- `v2/e<numero>.json`: rede de cada cotação, lida pela página do site `zibaseguros.com.br/rede-credenciada/<numero>` (ou `?e=<numero>`).
- `cotacoes/<numero>.json`: planos, preços, região e plano atual da cotação. `python3 juntar_v2.py cotacoes/<numero>.json` gera o v2 a partir das redes já publicadas (e*.json).
- `logos/`: logos das operadoras usadas na página.
- `site/index.html`: arquivo de public_html/rede-credenciada no site (lê o snippet ziba_rede_dados e, se houver, v2/e<n>.json; chama ziba_rede_aviso).
