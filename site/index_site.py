"""index.html novo de public_html/rede-credenciada (o .htaccess manda /rede-credenciada/<nº> para ele).
Dados: snippet do site (admin-ajax ziba_rede_dados: cadastro, validade e rede do GitHub); se existir v2/e<nº>.json
no ziba-rede, usa a versão com os planos lado a lado. Ao abrir, chama ziba_rede_aviso (e-mail para a Ziba)."""
import base64, json, sys
G = "/tmp/claude-0/-home-claude/bc014e19-48e5-5297-a166-9e4a1ca73583/scratchpad/gen/img/"
b64 = lambda p, m: f"data:{m};base64," + base64.b64encode(open(G + p, "rb").read()).decode()
AJAX = sys.argv[2] if len(sys.argv) > 2 else "/wp-admin/admin-ajax.php"
RAW = sys.argv[3] if len(sys.argv) > 3 else "https://raw.githubusercontent.com/ZibaSeguros/ziba-rede/main/"
t = open("../rede/rede_B.html").read()
t = (t.replace("__FONT__", b64("inter-latin-wght-normal.woff2", "font/woff2"))
      .replace("__LOGO__", b64("logo_branco.png", "image/png"))
      .replace('<img class="z" src="__Z__" alt="">', "")
      .replace("<title>Rede Credenciada Ziba B</title>", ""))
i = t.index("<script>"); j = t.index("</script>", i)
corpo, app = t[:i], t[i + 8:j].replace("const D = __DATA__;", "const D = window.ZD;")
boot = r'''<script>
(function(){
var AJAX=__AJAX__, RAW=__RAW__;
var m=location.pathname.match(/(\d{3,})\/?$/), q=new URLSearchParams(location.search).get("e"), n=((q||"")||(m?m[1]:"")).replace(/\D/g,"");
function aviso(t,s){document.body.insertAdjacentHTML("afterbegin",'<div style="max-width:640px;margin:0 auto;padding:64px 16px;font:400 17px/1.5 Switzer,Inter,system-ui,sans-serif;color:#08214F"><b style="display:block;font-size:24px;font-weight:500;color:#001E62;margin-bottom:6px">'+t+'</b>'+s+'</div>');document.querySelectorAll("body > :not(div):not(script)").forEach(function(e){e.style.display="none"});}
function pega(u){return fetch(u,{cache:"no-cache"}).then(function(r){if(!r.ok)throw 0;return r.json();});}
function v1(P){var N=P.planos.length;return {v:2,id:P.id,data:P.data,planos:P.planos.map(function(p,k){return {id:"o"+(k+1),nome:p.nome,op:"",sub:p.sub};}),
  items:P.items.map(function(i){var c=[];for(var k=0;k<N;k++)c.push(i[6+k]?(i[0]=="h"?i[5]:(i[0]=="l"?[]:["Centro médico"])):null);return [i[0],i[1],i[2],i[3],i[4],c];})};}
if(!n){aviso("Rede credenciada","Abra esta página pelo link da sua cotação.");return;}
pega(AJAX+"?action=ziba_rede_dados&e="+n).then(function(j){
  if(!j||!j.produto)throw 0;
  return pega(RAW+"v2/e"+n+".json").catch(function(){return null;}).then(function(D2){
    var D=(D2&&D2.v==2)?D2:(j.produto.v==2?j.produto:v1(j.produto));
    if(j.c)D.nome=j.c;
    D.planos.forEach(function(p){if(p.logo&&!/^(data:|https?:)/.test(p.logo))p.logo=RAW+"logos/"+p.logo+".png";});
    window.ZD=D;
    var s=document.createElement("script");s.textContent=document.getElementById("zr-app").textContent;document.body.appendChild(s);
    /* aviso para a Ziba de que o cliente abriu a rede */
    try{fetch(AJAX+"?action=ziba_rede_aviso&e="+n+"&p="+encodeURIComponent(D.planos.map(function(p){return p.nome;}).join(" / ")),{cache:"no-cache"});}catch(e){}
  });
}).catch(function(){aviso("Rede credenciada","Não encontramos a rede desta cotação. Fale com o corretor responsável pela sua cotação.");});
})();
</script>'''.replace("__AJAX__", json.dumps(AJAX)).replace("__RAW__", json.dumps(RAW))
doc = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
       '<meta name="robots" content="noindex,nofollow"><meta name="description" content="Rede credenciada · Ziba Seguros">'
       '<title>Rede Credenciada Ziba</title>'
       '<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=switzer@400,500,600,700&display=swap"></head><body>'
       + corpo + '<script type="text/plain" id="zr-app">' + app + '</script>' + boot + '</body></html>')
open(sys.argv[1], "w").write(doc)
print(len(doc) // 1024, "KB")
