# ziba-rede
Redes credenciadas dos estudos

## Rede da cotação (v2, até 3 planos lado a lado)
- `v2/e<numero>.json`: rede de cada cotação, lida pela página do site `zibaseguros.com.br/rede-credenciada/<numero>` (ou `?e=<numero>`).
- `cotacoes/<numero>.json`: planos, preços, região e plano atual da cotação. `python3 juntar_v2.py cotacoes/<numero>.json` gera o v2 a partir das redes já publicadas (e*.json).
- `logos/`: logos das operadoras usadas na página.
- `site/pagina-rede-credenciada.html`: widget HTML do Elementor da página (colado uma vez no site).
