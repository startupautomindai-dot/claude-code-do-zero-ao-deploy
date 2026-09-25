#!/usr/bin/env python3
"""Verificação visual de uma página: prints em 3 larguras + auditoria automática.

Uso:
    python3 verificar-visual.py <url> [pasta-de-saida]

Precisa de: pip install playwright && playwright install chromium

Aponta: estouro de largura (scroll horizontal), erros de console, imagens
quebradas, texto com contraste abaixo de WCAG AA, emoji usado como ícone,
e os sinais de "cara de IA" como ATENÇÃO (cantos muito arredondados, sombra
pesada, gradiente decorativo, excesso de fontes/pesos).

Sai com código 1 se houver FALHA (útil em CI).
"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

LARGURAS = [("celular", 390), ("tablet", 768), ("desktop", 1280)]

AUDITORIA_JS = r"""
() => {
  const vis = el => {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0';
  };
  const desc = el => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
    (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const W = document.documentElement.clientWidth;
  const todos = [...document.querySelectorAll('body *')].filter(vis);

  // 1. estouro de largura
  const estouro = todos.filter(el => el.getBoundingClientRect().right > W + 1)
    .filter(el => !el.closest('pre, code, table, [style*="overflow"]'))
    .slice(0, 8).map(el => desc(el) + ' (até ' + Math.round(el.getBoundingClientRect().right) + 'px)');

  // 2. contraste (texto direto no elemento)
  const rgb = c => { const m = c.match(/[\d.]+/g); return m ? m.map(Number) : null; };
  const lum = ([r, g, b]) => { const f = v => (v /= 255) <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const fundo = el => { for (let e = el; e; e = e.parentElement) { const c = rgb(getComputedStyle(e).backgroundColor); if (c && (c.length < 4 || c[3] > 0.5)) return c; if (getComputedStyle(e).backgroundImage !== 'none') return null; } return [255, 255, 255]; };
  const contraste = [];
  for (const el of todos) {
    const txt = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ');
    if (!txt) continue;
    const s = getComputedStyle(el), fg = rgb(s.color), bg = fundo(el);
    if (!fg || !bg) continue;
    const L1 = lum(fg), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    const grande = parseFloat(s.fontSize) >= 24 || (parseFloat(s.fontSize) >= 18.66 && +s.fontWeight >= 700);
    if (ratio < (grande ? 3 : 4.5)) contraste.push(desc(el) + ' "' + txt.slice(0, 30) + '" ' + ratio.toFixed(2) + ':1');
  }

  // 3. emoji como ícone em elementos de interface
  const EMOJI = /\p{Emoji_Presentation}|\p{Extended_Pictographic}\uFE0F/u;
  const emoji = todos.filter(el => el.matches('button, a, nav *, [role=button], h1, h2, h3, h4, label, .icon, [class*=icon]'))
    .filter(el => [...el.childNodes].some(n => n.nodeType === 3 && EMOJI.test(n.textContent)))
    .slice(0, 8).map(el => desc(el) + ' "' + el.textContent.trim().slice(0, 25) + '"');

  // 4. imagens quebradas / sem alt
  const imgs = [...document.images];
  const quebradas = imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.src.slice(-60));
  const semAlt = imgs.filter(i => !i.hasAttribute('alt')).length;

  // 5. sinais de "cara de IA" nos blocos (cards, botões, seções)
  const blocos = todos.filter(el => { const r = el.getBoundingClientRect(); return r.width >= 60 && r.height >= 28; });
  const raios = {}, pesos = {}, fontes = {};
  let sombraPesada = 0, gradiente = 0;
  for (const el of blocos) {
    const s = getComputedStyle(el);
    const r = parseFloat(s.borderTopLeftRadius);
    if (r > 0 && r < 999) raios[r] = (raios[r] || 0) + 1;
    const sh = s.boxShadow;
    if (sh !== 'none') { const blur = (sh.match(/(-?[\d.]+)px/g) || []).map(parseFloat)[2] || 0; if (blur >= 20) sombraPesada++; }
    if (/gradient/.test(s.backgroundImage)) gradiente++;
  }
  for (const el of todos) {
    const txt = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!txt) continue;
    const s = getComputedStyle(el);
    pesos[s.fontWeight] = (pesos[s.fontWeight] || 0) + 1;
    const f = s.fontFamily.split(',')[0].replace(/["']/g, '').trim();
    fontes[f] = (fontes[f] || 0) + 1;
  }
  const raiosGrandes = Object.entries(raios).filter(([r]) => +r >= 16).reduce((a, [, n]) => a + n, 0);
  const totalRaios = Object.values(raios).reduce((a, n) => a + n, 0);

  return {
    largura: W, scrollWidth: document.documentElement.scrollWidth,
    estouro, contraste: contraste.slice(0, 10), totalContraste: contraste.length,
    emoji, quebradas, semAlt, totalImgs: imgs.length,
    raios, raiosGrandesPct: totalRaios ? Math.round(100 * raiosGrandes / totalRaios) : 0,
    sombraPesada, gradiente, pesos, fontes,
  };
}
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    url = sys.argv[1]
    saida = sys.argv[2] if len(sys.argv) > 2 else "verificacao-visual"
    os.makedirs(saida, exist_ok=True)
    problemas = 0
    avisos = 0

    with sync_playwright() as p:
        exe = os.environ.get("CHROMIUM_PATH")
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        for nome, largura in LARGURAS:
            page = browser.new_page(viewport={"width": largura, "height": 900})
            erros = []
            page.on("console", lambda m, e=erros: e.append(m.text[:150]) if m.type == "error" else None)
            page.on("pageerror", lambda ex, e=erros: e.append(str(ex)[:150]))
            falhas = []
            page.on("requestfailed", lambda r, f=falhas: f.append(r.url[-80:]))
            page.goto(url, wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(600)
            arquivo = os.path.join(saida, f"{nome}-{largura}.png")
            page.screenshot(path=arquivo, full_page=True)
            a = page.evaluate(AUDITORIA_JS)
            page.close()

            print(f"\n=== {nome} ({largura}px) → {arquivo}")
            def item(ok, texto, detalhes=(), estilo=False):
                nonlocal problemas, avisos
                if not ok:
                    if estilo:
                        avisos += 1
                    else:
                        problemas += 1
                print(("  OK      " if ok else "  ATENÇÃO " if estilo else "  FALHA   ") + texto)
                for d in list(detalhes)[:8]:
                    print("         - " + d)

            item(a["scrollWidth"] <= a["largura"], f"largura: página {a['scrollWidth']}px na tela de {a['largura']}px", a["estouro"])
            item(not erros, f"console: {len(erros)} erro(s)", erros)
            item(not falhas, f"requisições falhando: {len(falhas)}", falhas)
            item(not a["quebradas"], f"imagens quebradas: {len(a['quebradas'])}", a["quebradas"])
            item(a["semAlt"] == 0, f"imagens sem alt: {a['semAlt']} de {a['totalImgs']}")
            item(a["totalContraste"] == 0, f"contraste abaixo de WCAG AA: {a['totalContraste']}", a["contraste"])
            item(not a["emoji"], f"emoji usado como ícone: {len(a['emoji'])}", a["emoji"])
            if nome == "desktop":
                raios = ", ".join(f"{k}px×{v}" for k, v in sorted(a["raios"].items(), key=lambda kv: -kv[1])[:5])
                item(a["raiosGrandesPct"] <= 30, f"cantos ≥16px: {a['raiosGrandesPct']}% dos blocos arredondados (mais usados: {raios or 'nenhum'})", estilo=True)
                item(a["sombraPesada"] <= 3, f"sombras pesadas (blur ≥20px): {a['sombraPesada']}", estilo=True)
                item(a["gradiente"] <= 2, f"blocos com gradiente: {a['gradiente']}", estilo=True)
                item(len(a["fontes"]) <= 3, f"famílias de fonte: {len(a['fontes'])} ({', '.join(a['fontes'])})", estilo=True)
                item(len(a["pesos"]) <= 4, f"pesos de fonte diferentes: {len(a['pesos'])} ({json.dumps(a['pesos'])})", estilo=True)
        browser.close()

    print(f"\nFALHAS: {problemas} (corrigir antes de entregar) · ATENÇÃO: {avisos} (padrão de 'cara de IA' — justificar ou ajustar)")
    print(f"Prints em {saida}/ — abra e confira a olho: o script não substitui olhar.")
    sys.exit(1 if problemas else 0)


if __name__ == "__main__":
    main()
