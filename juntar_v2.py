"""Monta a rede de uma cotação (formato v2: até 3 planos lado a lado) a partir das redes já publicadas.
Uso: python3 juntar_v2.py cotacao.json   ->  grava v2/e<numero>.json
cotacao.json: {"numero": "10404", "nome": "Elon Engenharia", "data": "2026-10-10",
  "atual": "4.100,00", "quem": "a empresa paga",
  "prioridade": {"rotulo": "Hospitais na Barra da Tijuca", "curto": "Na Barra da Tijuca", "tipo": "h",
                 "termos": ["barra"], "cidade": "Rio de Janeiro", "regiao": "Zona Oeste"},
  "planos": [{"fonte": "e10202", "plano": "Especial 100", "nome": "Especial 100", "op": "SulAmérica",
              "sub": "Apartamento · com coparticipação", "preco": "3.548,45", "logo": "op_sulamerica"}, ...]}"""
import json, sys, re, unicodedata
C = json.load(open(sys.argv[1]))
def chave(n):
    n = unicodedata.normalize("NFKD", n).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", n).strip()
idx, N = {}, len(C["planos"])
for k, p in enumerate(C["planos"]):
    d = json.load(open(p["fonte"] + ".json"))
    j = [q["nome"] for q in d["planos"]].index(p["plano"])   # coluna do plano na rede publicada
    for t, nome, uf, cid, bai, serv, *flags in d["items"]:
        if not flags[j]: continue
        it = idx.setdefault((t, chave(nome), cid), [t, nome, uf, cid, bai, [None] * N])
        it[5][k] = serv if t == "h" else ([] if t == "l" else ["Centro médico"])
planos = [dict(id=f"o{k+1}", nome=p["nome"], op=p["op"], sub=p["sub"], preco=p.get("preco"), logo=p.get("logo")) for k, p in enumerate(C["planos"])]
out = {"v": 2, "id": "e" + C["numero"], "nome": C["nome"], "data": C["data"], "planos": planos,
       "prioridade": C.get("prioridade"), "items": sorted(idx.values(), key=lambda i: (i[0], i[1]))}
for c in ("atual", "quem"):
    if C.get(c): out[c] = C[c]
json.dump(out, open(f"v2/e{C['numero']}.json", "w"), ensure_ascii=False, separators=(",", ":"))
from collections import Counter
print(out["id"], len(out["items"]), [dict(Counter(i[0] for i in out["items"] if i[5][k] is not None)) for k in range(N)])
