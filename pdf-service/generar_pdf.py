import html
import subprocess
import sys
from parser import parse_okami_text

DAY_COLORS = ['#C0392B', '#2980B9', '#27AE60', '#D4AC0D', '#8E44AD', '#16A085']

FORMAT_LABELS = {
    'ATLETA': 'Atleta',
    'CLASE': 'Clase',
    'HYBRID': 'Hybrid',
    'RECOMPOSICION': 'Recomposición',
}


def esc(text):
    return html.escape(text or '')


def render_cargas(rx, int_, scale):
    if not rx and not int_ and not scale:
        return ''
    parts = []
    if rx:
        parts.append(f'<span class="badge badge-rx">RX {esc(rx)}</span>')
    if int_:
        parts.append(f'<span class="badge badge-int">INT {esc(int_)}</span>')
    if scale:
        parts.append(f'<span class="badge badge-scale">SC {esc(scale)}</span>')
    return f'<div class="cargas-row">{"".join(parts)}</div>'


def render_bloque(bloque, accent):
    is_main = any(k in bloque['nombre'].upper() for k in ('MAIN EVENT', 'WOD', 'PRINCIPAL'))
    css_class = 'block block-wod' if is_main else 'block'

    items_html = ''
    for item in bloque['items']:
        formato_html = f'<span class="item-formato" style="color:{accent}">{esc(item["formato"])}</span>' if item['formato'] else ''
        buscamos_html = f'<div class="item-buscamos">Buscamos: {esc(item["buscamos"])}</div>' if item['buscamos'] else ''
        items_html += f'''
        <div class="item-row">
          <div class="item-main"><span>{esc(item["texto"])}</span>{formato_html}</div>
          {buscamos_html}
        </div>'''

    formato_wod_html = ''
    if bloque['formato_wod']:
        size_class = 'wod-format-main' if is_main else 'wod-format'
        formato_wod_html = f'<div class="{size_class}">{esc(bloque["formato_wod"])}</div>'

    nombre_limpio = bloque['nombre'].replace('_', ' ')

    return f'''
    <div class="{css_class}">
      <div class="block-label" style="color:{accent}">{esc(nombre_limpio)}</div>
      {formato_wod_html}
      {items_html}
      {render_cargas(bloque['rx'], bloque['int'], bloque['scale'])}
    </div>'''


def render_dia(dia, idx):
    accent = DAY_COLORS[idx % len(DAY_COLORS)]
    bloques_html = ''.join(render_bloque(b, accent) for b in dia['bloques'])

    tip_html = ''
    if dia['tip']:
        tip_html = f'''
        <div class="tip-box">
          <div class="tip-label">Tip entrenador</div>
          <div class="tip-text">{esc(dia['tip'])}</div>
        </div>'''

    objetivo_html = ''
    if dia['objetivo']:
        objetivo_html = f'<div class="dia-objetivo">{esc(dia["objetivo"])}</div>'

    tipo_dia_html = f' · {esc(dia["tipo_dia"])}' if dia['tipo_dia'] else ''
    titulo = dia['titulo'] or f"Día {dia['numero']}"

    return f'''
    <div class="page">
      <div class="page-body">
        <div class="page-header">
          <div class="page-day-number" style="color:{accent}">{str(dia['numero']).zfill(2)}</div>
          <div class="page-header-text">
            <div class="page-tag" style="color:{accent}">DÍA {esc(dia['numero'])}{tipo_dia_html}</div>
            <div class="page-title">{esc(titulo)}</div>
          </div>
        </div>
        <div class="dia-header">
          <div class="dia-accent-bar" style="background:{accent}"></div>
          {objetivo_html}
        </div>
        {bloques_html}
        {tip_html}
      </div>
      <div class="page-footer">
        <div class="footer-brand">OKAMI</div>
      </div>
    </div>'''


def render_portada(week):
    formato_label = FORMAT_LABELS.get(week['formato'], week['formato'])
    intencion_html = ''
    if week['intencion']:
        intencion_html = f'''
        <div class="cover-intent">
          <div class="intent-label">Intención del bloque</div>
          <div class="intent-text">{esc(week['intencion'])}</div>
        </div>'''

    map_rows = ''
    for idx, dia in enumerate(week['dias']):
        accent = DAY_COLORS[idx % len(DAY_COLORS)]
        bloques_nombres = ' · '.join(b['nombre'].replace('_', ' ') for b in dia['bloques'])
        titulo = dia['titulo'] or f"Día {dia['numero']}"
        tipo = f' · {esc(dia["tipo_dia"])}' if dia['tipo_dia'] else ''
        map_rows += f'''
        <div class="map-row" style="border-left-color:{accent}">
          <div class="map-info">
            <div class="map-day-label" style="color:{accent}">DÍA {str(dia['numero'])}</div>
            <div class="map-title">{esc(titulo)}{tipo}</div>
            <div class="map-blocks">{esc(bloques_nombres)}</div>
          </div>
        </div>'''

    return f'''
    <div class="page cover">
      <div class="page-body">
        <div class="cover-top">
          <div class="okami-logo">OKAMI</div>
          <div class="brand-sub">Sistema de Entrenamiento</div>
          <div class="cover-divider"></div>
          <div class="cover-meta">
            <div class="meta-item">
              <div class="meta-label">Semana</div>
              <div class="meta-value">{esc(week['semana'])}</div>
            </div>
            <div class="meta-item">
              <div class="meta-label">Formato</div>
              <div class="meta-value">{esc(formato_label)}</div>
            </div>
          </div>
          {intencion_html}
        </div>
        <div class="map-section">
          <div class="map-section-label">Mapa de la semana</div>
          {map_rows}
        </div>
      </div>
      <div class="page-footer">
        <div class="footer-brand">OKAMI</div>
      </div>
    </div>'''


def render_cierre(week):
    if not week['cierre']:
        return ''
    items_html = ''.join(f'<div class="cierre-item">→ {esc(c)}</div>' for c in week['cierre'])
    return f'''
    <div class="page">
      <div class="page-body">
        <div class="page-header">
          <div class="page-tag" style="color:#C0392B">CIERRE DE SEMANA</div>
          <div class="page-title">Notas y observaciones</div>
        </div>
        <div class="cierre-box">
          {items_html}
        </div>
      </div>
      <div class="page-footer">
        <div class="footer-brand">OKAMI</div>
      </div>
    </div>'''


CSS = '''
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: #1F1F1F;
  font-family: 'Inter', Helvetica, Arial, sans-serif;
  color: #fff;
}
.page {
  width: 210mm;
  min-height: 297mm;
  background: #1F1F1F;
  padding: 20mm 18mm;
  position: relative;
  page-break-after: always;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}
.page:last-child { page-break-after: auto; }
.page-body { flex: 1; }

/* Portada */
.cover { display: flex; flex-direction: column; justify-content: space-between; }
.okami-logo {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 900; font-size: 47.6px; letter-spacing: 10px; color: #fff; line-height: 1;
}
.brand-sub {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 600; font-size: 14.4px; letter-spacing: 4px; color: #C0392B;
  text-transform: uppercase; margin-top: 14px;
}
.cover-divider { width: 50px; height: 4px; background: #C0392B; margin: 30px 0; }
.cover-meta { display: flex; gap: 0; border: 1px solid rgba(255,255,255,0.1); }
.meta-item { flex: 1; padding: 20px 20px; border-right: 1px solid rgba(255,255,255,0.1); }
.meta-item:last-child { border-right: none; }
.meta-label {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 600; font-size: 12.8px; letter-spacing: 2px; text-transform: uppercase;
  color: #C0392B; margin-bottom: 8px;
}
.meta-value {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 700; font-size: 22.1px; color: #fff;
}
.cover-intent {
  margin-top: 28px; padding: 22px 22px; border-left: 4px solid #C0392B;
  background: rgba(192,57,43,0.1);
}
.intent-label {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 600; font-size: 12.8px; letter-spacing: 2px; text-transform: uppercase;
  color: #C0392B; margin-bottom: 10px;
}
.intent-text { font-size: 17.8px; line-height: 1.5; color: rgba(255,255,255,0.9); }

.map-section { margin-top: 30px; }
.map-section-label {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 600; font-size: 13.6px; letter-spacing: 2px; text-transform: uppercase;
  color: rgba(255,255,255,0.4); margin-bottom: 14px;
}
.map-row {
  display: flex; align-items: flex-start; gap: 0;
  background: #262626; border-left: 5px solid #C0392B;
  padding: 16px 18px; margin-bottom: 10px;
}
.map-info { flex: 1; min-width: 0; }
.map-day-label {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 700; font-size: 11.9px; letter-spacing: 1px; text-transform: uppercase;
  color: rgba(255,255,255,0.4); margin-bottom: 4px;
}
.map-title {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 700; font-size: 17.8px; color: #fff;
}
.map-blocks { font-size: 13.6px; color: rgba(255,255,255,0.5); margin-top: 4px; }

/* Página de día */
.page-header { border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 14px; margin-bottom: 18px; display: flex; align-items: center; gap: 14px; }
.page-day-number {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 900; font-size: 51px; line-height: 1;
}
.page-header-text { flex: 1; }
.page-tag {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 600; font-size: 12.8px; letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 8px;
}
.page-title {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 800; font-size: 27.2px; color: #fff; line-height: 1.15;
}
.dia-header { display: flex; gap: 12px; margin-bottom: 16px; align-items: flex-start; }
.dia-accent-bar { width: 5px; min-height: 36px; flex-shrink: 0; }
.dia-objetivo { font-size: 16.1px; color: rgba(255,255,255,0.85); line-height: 1.5; }

.block {
  background: #262626; border: 1px solid rgba(255,255,255,0.08);
  padding: 14px 16px; margin-bottom: 10px;
  page-break-inside: avoid;
}
.block-wod { background: #1A1A1A; border: 1px solid rgba(192,57,43,0.3); }
.block-label {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 600; font-size: 11.9px; letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 10px;
}
.wod-format {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 700; font-size: 20.4px; color: #fff; margin-bottom: 10px;
}
.wod-format-main {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 800; font-size: 23.8px; color: #fff; margin-bottom: 12px;
}
.item-row { margin-bottom: 6px; }
.item-main { font-size: 16.1px; color: rgba(255,255,255,0.92); display: flex; justify-content: space-between; gap: 10px; flex-wrap: wrap; }
.item-formato {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 700; font-size: 15.3px; white-space: nowrap;
}
.item-buscamos { font-size: 13.6px; color: rgba(255,255,255,0.5); margin-top: 3px; }

.cargas-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.badge {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 700; font-size: 12.8px; letter-spacing: 0.3px; text-transform: uppercase;
  padding: 6px 12px; border: 1px solid;
}
.badge-rx { border-color: #C0392B; color: #C0392B; }
.badge-int { border-color: rgba(255,255,255,0.2); color: rgba(255,255,255,0.75); }
.badge-scale { border-color: rgba(255,255,255,0.1); color: rgba(255,255,255,0.5); }

.tip-box { background: #262626; border-left: 4px solid #C0392B; padding: 18px 20px; margin-top: 12px; page-break-inside: avoid; }
.tip-label {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 600; font-size: 11.9px; letter-spacing: 2px; text-transform: uppercase;
  color: #C0392B; margin-bottom: 8px;
}
.tip-text { font-size: 15.3px; color: rgba(255,255,255,0.85); line-height: 1.5; }

.cierre-box { background: #262626; border: 1px solid rgba(255,255,255,0.08); padding: 20px; page-break-inside: avoid; }
.cierre-item { font-size: 16.1px; color: rgba(255,255,255,0.8); line-height: 1.6; margin-bottom: 10px; }

.page-footer {
  border-top: 1px solid rgba(255,255,255,0.08); padding-top: 10px; margin-top: 18px;
}
.footer-brand {
  font-family: 'Montserrat', Helvetica, Arial, sans-serif;
  font-weight: 800; font-size: 11.9px; letter-spacing: 2px; color: rgba(255,255,255,0.3);
  text-transform: uppercase;
}
'''


def generar_html(week):
    portada = render_portada(week)
    dias_html = ''.join(render_dia(d, idx) for idx, d in enumerate(week['dias']))
    cierre_html = render_cierre(week)

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>{CSS}</style>
</head>
<body>
{portada}
{dias_html}
{cierre_html}
</body>
</html>'''


def generar_pdf(texto_semana, output_path):
    week = parse_okami_text(texto_semana)
    if not week['dias']:
        raise ValueError('No se ha podido leer ningún día del texto proporcionado.')

    html_path = output_path.replace('.pdf', '.html')
    html_content = generar_html(week)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    subprocess.run([
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--encoding', 'utf-8',
        '--disable-smart-shrinking',
        '--print-media-type',
        html_path, output_path
    ], check=True)

    return week


if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/okami-app/semana_4.44_atleta.txt'
    output_file = sys.argv[2] if len(sys.argv) > 2 else '/home/claude/okami-pdf/output.pdf'

    with open(input_file, encoding='utf-8') as f:
        texto = f.read()

    week = generar_pdf(texto, output_file)
    print(f"PDF generado: {output_file}")
    print(f"Formato: {week['formato']} · Semana {week['semana']} · {len(week['dias'])} días")
