#!/usr/bin/env python3
"""
Aplica a index.html los cambios de salida inmediata (berehalakoa) / diferida (geroratua).

Uso:   python3 aplicar_cambios.py index.html
Crea:  index_nuevo.html  (el original NO se modifica)

Seguridad: cada fragmento a sustituir debe aparecer exactamente UNA vez.
Si alguno no se encuentra (o aparece varias veces), el script se detiene
sin escribir nada.
"""
import sys

if len(sys.argv) != 2:
    sys.exit("Uso: python3 aplicar_cambios.py index.html")

src = sys.argv[1]
with open(src, encoding="utf-8", newline="") as f:
    html = f.read()

EDITS = []

# 1. Calculo (compute)
EDITS.append(("1. compute: inicio segun tipo de salida",
r'''else if(o.er!=null){o.start=o.er;o.startRule='ERANTZUNA'}''',
r'''else if(r.irteera==='geroratua'){const gd=P(r.irteeraGeroratua);
      if(gd!=null){o.start=gd;o.startRule='IRTEERA GERORATUA';o.deferred=true;if(gd<o.deia)o.warn.push({t:'Irteera geroratua DEIA baino lehenagokoa da'})}
      else if(o.er!=null){o.start=o.er;o.startRule='ERANTZUNA';o.warn.push({t:'Irteera geroratuaren ordua falta: ERANTZUNA erabili da'})}
      else{o.start=o.deia;o.startRule='DEIA';o.warn.push({t:'Irteera geroratuaren ordua falta: DEIA erabili da'})}}
    else if(o.er!=null){o.start=o.er;o.startRule='ERANTZUNA'}'''))

# 2. Formulario: selector de tipo de salida
EDITS.append(("2. intForm: selector Irteera mota",
r'''<div id="cutBox" style="margin-top:8px"></div></fieldset>''',
r'''<div id="cutBox" style="margin-top:8px"></div></fieldset>
  <fieldset><legend>Irteera mota</legend><div class="radios">
  <label class="chk"><input type="radio" name="irteera" value="berehala" ${r.irteera==='geroratua'?'':'checked'}> Berehalakoa</label>
  <label class="chk"><input type="radio" name="irteera" value="geroratua" ${r.irteera==='geroratua'?'checked':''}> Geroratua</label></div>
  <div class="grid" id="defBox" style="margin-top:10px">${dtF('irteeraGeroratua','Irteera geroratuaren ordua',r.irteeraGeroratua,ib,'erantzuna')}
  <p class="muted span2" style="font-size:13px;margin:0">Berehalakoan, itzaltzea ERANTZUNAtik kontatzen da. Geroratuan, erretenak adierazitako irteera-orduan hasten da. Deia zaintzan jaso bazuten, DEIAtik kontatzen da eta hau ez da erabiltzen.</p></div></fieldset>'''))

# 3. Mostrar/ocultar el campo
EDITS.append(("3. intForm onInput: mostrar/ocultar campo",
r'''document.getElementById('newFire').style.display=isNew?'':'none';''',
r'''document.getElementById('newFire').style.display=isNew?'':'none';
    document.getElementById('defBox').style.display=f.querySelector('input[name=irteera]:checked')?.value==='geroratua'?'':'none';'''))

# 4a. readInt: variable irt
EDITS.append(("4a. readInt: variable irt",
r'''const s=fv(f,'sutea');''',
r'''const s=fv(f,'sutea');
  const irt=f.querySelector('input[name=irteera]:checked')?.value==='geroratua'?'geroratua':'berehala';'''))

# 4b. readInt: campos nuevos
EDITS.append(("4b. readInt: campos nuevos",
r'''zaintzan:f.querySelector('input[name=zaintzan]:checked')?.value||'auto',oharrak:fv(f,'oharrak')};''',
r'''zaintzan:f.querySelector('input[name=zaintzan]:checked')?.value||'auto',irteera:irt,irteeraGeroratua:irt==='geroratua'?fv(f,'irteeraGeroratua'):'',oharrak:fv(f,'oharrak')};'''))

# 5. Validacion al guardar
EDITS.append(("5. save-int: validacion",
r'''{toast('Baliabidea eta deiaren ordua behar dira');break}''',
r'''{toast('Baliabidea eta deiaren ordua behar dira');break}
      if(rec.irteera==='geroratua'&&!rec.irteeraGeroratua){toast('Bete irteera geroratuaren ordua');break}'''))

# 6. Tabla de Suteak
EDITS.append(("6. timeCells: hora diferida en rojo",
r'''+c(r.erantzuna,!!r.erantzuna)+''',
r'''+c(r.erantzuna,!!r.erantzuna&&!o.deferred,o.deferred?`<div class="tused" style="font-size:12px">Geroratua: ${showMs(o.start)}</div>`:'')+'''))

# 7. Certificados bilingues
EDITS.append(("7. RULE_ES: salida diferida",
r"""'ERANTZUNA':'confirmación de salida',""",
r"""'ERANTZUNA':'confirmación de salida','IRTEERA GERORATUA':'salida diferida',"""))

# 8. Ayuda (Jarraibideak)
EDITS.append(("8a. Jarraibideak: Irteera mota",
r'''<li><b>Deia jaso zuenean zaintzan zegoen?</b>''',
r'''<li><b>Irteera mota</b>: <b>Berehalakoa</b> bada, itzaltze-orduak ERANTZUNAtik (irteera baieztatu zuten ordua) kontatzen dira. <b>Geroratua</b> bada (irteera baieztatu dute, baina ordu zehatz batean aterako dira, ordu batzuk geroago), sartu <b>Irteera geroratuaren ordua</b> eta hortik kontatuko dira. Zaintzan zeudela deia jaso bazuten, DEIAtik kontatzen da beti.</li>
  <li><b>Deia jaso zuenean zaintzan zegoen?</b>'''))

EDITS.append(("8b. Suteak atala: texto introductorio",
r'''Itzaltzea ERANTZUNAtik (irteera baieztatua) hasten da kontatzen.''',
r'''Itzaltzea ERANTZUNAtik (irteera baieztatua) hasten da kontatzen; irteera geroratua bada, geroratutako irteera-orduatik.'''))

# --- comprobar todo antes de escribir nada ---
errors = []
for name, old, new in EDITS:
    n = html.count(old)
    if n != 1:
        errors.append(f"  - {name}: encontrado {n} veces (debe ser 1)")
if errors:
    print("NO SE HA ESCRITO NADA. Estos fragmentos no coinciden:")
    print("\n".join(errors))
    print("\nProbablemente este index.html no es la misma version que se me envio.")
    sys.exit(1)

for name, old, new in EDITS:
    html = html.replace(old, new, 1)
    print("OK  ", name)

out = "index_nuevo.html"
with open(out, "w", encoding="utf-8", newline="") as f:
    f.write(html)
print(f"\nListo: {out} creado ({len(EDITS)} cambios aplicados). El original no se ha tocado.")
