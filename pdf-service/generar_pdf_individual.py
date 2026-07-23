import html
import subprocess
import sys
from parser_individual import parse_individual_text

ESFUERZO_COLOR = {'🟢': '#27AE60', '🟡': '#D4AC0D', '🔴': '#C0392B'}
ESFUERZO_LABEL = {'🟢': 'FÁCIL', '🟡': 'MODERADO', '🔴': 'EXIGENTE'}
DAY_COLORS = ['#C0392B', '#2980B9', '#27AE60', '#D4AC0D', '#8E44AD', '#16A085', '#E67E22']


def esc(text):
    return html.escape(text or '')


def render_portada(data):
    criterios_html = ''.join(f'<li>{esc(c)}</li>' for c in data['criterios_bloque'])
    reglas_html = ''.join(f'<li>{esc(r)}</li>' for r in data['reglas_operativas'])

    escala_html = ''
    for e in data['escala_esfuerzo']:
        parts = e.split(':', 1)
        emoji_label = parts[0].strip()
        desc = parts[1].strip() if len(parts) > 1 else ''
        emoji = emoji_label[0] if emoji_label else '🟡'
        label_text = emoji_label[1:].strip() if len(emoji_label) > 1 else emoji_label
        color = ESFUERZO_COLOR.get(emoji, '#888')
        escala_html += f'''
        <div class="escala-row">
          <span class="escala-dot" style="background:{color}"></span>
          <div>
            <div class="escala-label">{esc(label_text)}</div>
            <div class="escala-desc">{esc(desc)}</div>
          </div>
        </div>'''

    progresion_html = ''
    for p in data['progresion_mesociclo']:
        parts = p.split('|')
        titulo = parts[0].strip()
        desc = parts[1].strip() if len(parts) > 1 else ''
        progresion_html += f'''
        <div class="prog-row">
          <div class="prog-titulo">{esc(titulo)}</div>
          <div class="prog-desc">{esc(desc)}</div>
        </div>'''

    estructura_html = ''
    for idx, e in enumerate(data['estructura_semanal']):
        parts = e.split(':', 1)
        dia = parts[0].strip()
        resto = parts[1].strip() if len(parts) > 1 else ''
        sub = resto.split('|')
        bloque_nombre = sub[0].strip()
        foco = sub[1].strip() if len(sub) > 1 else ''
        accent = DAY_COLORS[idx % len(DAY_COLORS)]
        estructura_html += f'''
        <div class="map-row" style="border-left-color:{accent}">
          <div class="map-info">
            <div class="map-day-label" style="color:{accent}">{esc(dia)}</div>
            <div class="map-title">{esc(bloque_nombre)}</div>
            <div class="map-blocks">{esc(foco)}</div>
          </div>
        </div>'''

    return f'''
    <div class="page cover">
      <div class="page-body">
        <div class="okami-logo">OKAMI</div>
        <div class="brand-sub">Sistema Individual</div>
        <div class="cover-divider"></div>
        <div class="cover-meta">
          <div class="meta-item"><div class="meta-label">Persona</div><div class="meta-value">{esc(data['persona'])}</div></div>
          <div class="meta-item"><div class="meta-label">Duración</div><div class="meta-value">{esc(data['duracion'])}</div></div>
        </div>
        <div class="cover-meta" style="margin-top:10px;">
          <div class="meta-item"><div class="meta-label">Frecuencia</div><div class="meta-value-sm">{esc(data['frecuencia'])}</div></div>
          <div class="meta-item"><div class="meta-label">Sesión</div><div class="meta-value-sm">{esc(data['duracion_sesion'])}</div></div>
        </div>
        <div class="cover-intent">
          <div class="intent-label">Objetivo del mesociclo</div>
          <div class="intent-text">{esc(data['objetivo_mesociclo'])}</div>
        </div>
      </div>
      <div class="page-footer"><div class="footer-brand">OKAMI</div></div>
    </div>

    <div class="page">
      <div class="page-body">
        <div class="page-header-simple">LECTURA DEL CASO</div>
        <div class="lectura-caso-text">{esc(data['lectura_caso'])}</div>
        <div class="section-label">Criterios del bloque</div>
        <ul class="simple-list">{criterios_html}</ul>
        <div class="section-label">Reglas operativas</div>
        <ul class="simple-list">{reglas_html}</ul>
        <div class="section-label">Escala de esfuerzo</div>
        {escala_html}
      </div>
      <div class="page-footer"><div class="footer-brand">OKAMI</div></div>
    </div>

    <div class="page">
      <div class="page-body">
        <div class="page-header-simple">PROGRESIÓN DEL MESOCICLO</div>
        {progresion_html}
        <div class="section-label" style="margin-top:24px;">Estructura semanal fija</div>
        {estructura_html}
      </div>
      <div class="page-footer"><div class="footer-brand">OKAMI</div></div>
    </div>'''


def render_sesion(sesion, idx):
    accent = DAY_COLORS[idx % len(DAY_COLORS)]
    esfuerzo = sesion['esfuerzo']
    esf_color = ESFUERZO_COLOR.get(esfuerzo, accent)
    esf_label = ESFUERZO_LABEL.get(esfuerzo, '')

    bloques_html = ''
    for b in sesion['bloques']:
        items_html = ''.join(f'<li>{esc(it)}</li>' for it in b['items'])
        lectura_html = f'<div class="bloque-lectura">{esc(b["lectura"])}</div>' if b['lectura'] else ''
        bloques_html += f'''
        <div class="ind-block">
          <div class="ind-block-header">
            <span class="ind-block-label">{esc(b["nombre"].replace("_", " "))}</span>
            <span class="ind-block-tiempo">{esc(b["tiempo"])}</span>
          </div>
          <ul class="ind-items">{items_html}</ul>
          {lectura_html}
        </div>'''

    feedback_html = ''.join(f'<li>{esc(q)}</li>' for q in sesion['feedback'])
    notas_html = ''
    for n in sesion['notas_tecnicas']:
        if ':' in n:
            nombre, desc = n.split(':', 1)
            notas_html += f'<div class="nota-item"><span class="nota-nombre">{esc(nombre.strip())}:</span> {esc(desc.strip())}</div>'
        else:
            notas_html += f'<div class="nota-item">{esc(n)}</div>'

    return f'''
    <div class="page">
      <div class="page-body">
        <div class="page-header">
          <div class="page-header-text">
            <div class="page-tag" style="color:{accent}">SEMANA {esc(sesion["semana"])} · {esc(sesion["dia_semana"])}</div>
            <div class="page-title">{esc(sesion["titulo"])}</div>
          </div>
          <div class="esfuerzo-badge" style="border-color:{esf_color};color:{esf_color}">{esf_label}</div>
        </div>
        <div class="dia-header">
          <div class="dia-accent-bar" style="background:{accent}"></div>
          <div class="dia-objetivo">{esc(sesion["objetivo"])}</div>
        </div>
        {bloques_html}
        <div class="feedback-box">
          <div class="feedback-label">Feedback de sesión</div>
          <ul class="feedback-list">{feedback_html}</ul>
        </div>
        <div class="notas-box">
          <div class="notas-label">Notas técnicas</div>
          {notas_html}
        </div>
      </div>
      <div class="page-footer"><div class="footer-brand">OKAMI</div></div>
    </div>'''


def render_cierre(data):
    logica_html = ''.join(f'<div class="cierre-item">→ {esc(c)}</div>' for c in data['logica_progresion'])
    criterios_html = ''.join(f'<div class="cierre-item">→ {esc(c)}</div>' for c in data['criterios_exito'])
    return f'''
    <div class="page">
      <div class="page-body">
        <div class="page-header-simple">LÓGICA DE PROGRESIÓN</div>
        <div class="cierre-box">{logica_html}</div>
        <div class="section-label" style="margin-top:24px;">Criterios de éxito</div>
        <div class="cierre-box">{criterios_html}</div>
      </div>
      <div class="page-footer"><div class="footer-brand">OKAMI</div></div>
    </div>'''


CSS = '''
@page { size: A4; margin: 0; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: #1F1F1F; font-family: 'Inter', Helvetica, Arial, sans-serif; color: #fff; }
.page { width: 210mm; min-height: 297mm; background: #1F1F1F; padding: 18mm 16mm; position: relative; page-break-after: always; box-sizing: border-box; display: flex; flex-direction: column; }
.page:last-child { page-break-after: auto; }
.page-body { flex: 1; }
.okami-logo { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 900; font-size: 47.6px; letter-spacing: 8.5px; color: #fff; line-height: 1; }
.brand-sub { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 14.5px; letter-spacing: 3.4px; color: #C0392B; text-transform: uppercase; margin-top: 12px; }
.cover-divider { width: 42.5px; height: 3.4px; background: #C0392B; margin: 25px 0; }
.cover-meta { display: flex; gap: 0; border: 1px solid rgba(255,255,255,0.1); }
.meta-item { flex: 1; padding: 17px 17px; border-right: 1px solid rgba(255,255,255,0.1); }
.meta-item:last-child { border-right: none; }
.meta-label { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 12.75px; letter-spacing: 1.7px; text-transform: uppercase; color: #C0392B; margin-bottom: 7px; }
.meta-value { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 22.1px; color: #fff; }
.meta-value-sm { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 15.3px; color: #fff; }
.cover-intent { margin-top: 24px; padding: 19px; border-left: 3.4px solid #C0392B; background: rgba(192,57,43,0.1); }
.intent-label { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 12.75px; letter-spacing: 1.7px; text-transform: uppercase; color: #C0392B; margin-bottom: 8px; }
.intent-text { font-size: 17.85px; line-height: 1.5; color: rgba(255,255,255,0.9); }
.page-header-simple { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 800; font-size: 22px; color: #fff; letter-spacing: 1px; margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.lectura-caso-text { font-size: 17px; line-height: 1.6; color: rgba(255,255,255,0.88); margin-bottom: 24px; }
.section-label { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 13.6px; letter-spacing: 1.7px; text-transform: uppercase; color: rgba(255,255,255,0.4); margin-bottom: 10px; }
.simple-list { list-style: none; margin-bottom: 20px; }
.simple-list li { font-size: 15.3px; color: rgba(255,255,255,0.85); line-height: 1.6; padding-left: 16px; position: relative; margin-bottom: 6px; }
.simple-list li::before { content: "–"; position: absolute; left: 0; color: #C0392B; }
.escala-row { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px; }
.escala-dot { width: 14px; height: 14px; border-radius: 50%; flex-shrink: 0; margin-top: 4px; }
.escala-label { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 15.3px; color: #fff; }
.escala-desc { font-size: 14.45px; color: rgba(255,255,255,0.6); margin-top: 2px; }
.prog-row { background: #262626; border: 1px solid rgba(255,255,255,0.08); padding: 14px 16px; margin-bottom: 8px; }
.prog-titulo { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 15.3px; color: #fff; margin-bottom: 4px; }
.prog-desc { font-size: 13.6px; color: rgba(255,255,255,0.6); }
.map-row { display: flex; align-items: flex-start; gap: 0; background: #262626; border-left: 4.25px solid #C0392B; padding: 13.6px 13.6px; margin-bottom: 8.5px; }
.map-info { flex: 1; min-width: 0; }
.map-day-label { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 11.9px; letter-spacing: 0.85px; text-transform: uppercase; margin-bottom: 3px; }
.map-title { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 17.85px; color: #fff; }
.map-blocks { font-size: 13.6px; color: rgba(255,255,255,0.5); margin-top: 3px; }
.page-header { border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 14px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.page-header-text { flex: 1; }
.page-tag { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 12.75px; letter-spacing: 1.7px; text-transform: uppercase; margin-bottom: 7px; }
.page-title { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 800; font-size: 24px; color: #fff; line-height: 1.15; }
.esfuerzo-badge { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 11px; letter-spacing: 1px; padding: 7px 12px; border: 1.5px solid; white-space: nowrap; }
.dia-header { display: flex; gap: 12px; margin-bottom: 16px; align-items: flex-start; }
.dia-accent-bar { width: 4.25px; min-height: 30px; flex-shrink: 0; }
.dia-objetivo { font-size: 15.3px; color: rgba(255,255,255,0.85); line-height: 1.5; }
.ind-block { background: #262626; border: 1px solid rgba(255,255,255,0.08); padding: 13px 14px; margin-bottom: 9px; page-break-inside: avoid; }
.ind-block-header { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px; }
.ind-block-label { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 11.9px; letter-spacing: 1.7px; text-transform: uppercase; color: #C0392B; }
.ind-block-tiempo { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 700; font-size: 12.75px; color: rgba(255,255,255,0.5); }
.ind-items { list-style: none; margin-bottom: 6px; }
.ind-items li { font-size: 14.45px; color: rgba(255,255,255,0.92); line-height: 1.45; margin-bottom: 4px; padding-left: 14px; position: relative; }
.ind-items li::before { content: "–"; position: absolute; left: 0; color: rgba(255,255,255,0.3); }
.bloque-lectura { font-size: 13px; color: rgba(255,255,255,0.5); font-style: italic; }
.feedback-box { background: rgba(192,57,43,0.08); border-left: 3.4px solid #C0392B; padding: 14px 16px; margin-top: 10px; page-break-inside: avoid; }
.feedback-label { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 11.9px; letter-spacing: 1.7px; text-transform: uppercase; color: #C0392B; margin-bottom: 8px; }
.feedback-list { list-style: none; }
.feedback-list li { font-size: 13.6px; color: rgba(255,255,255,0.85); line-height: 1.5; margin-bottom: 4px; padding-left: 14px; position: relative; }
.feedback-list li::before { content: "?"; position: absolute; left: 0; color: #C0392B; font-weight: 700; }
.notas-box { background: #262626; border: 1px solid rgba(255,255,255,0.08); padding: 14px 16px; margin-top: 10px; page-break-inside: avoid; }
.notas-label { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 600; font-size: 11.9px; letter-spacing: 1.7px; text-transform: uppercase; color: rgba(255,255,255,0.4); margin-bottom: 8px; }
.nota-item { font-size: 12.75px; color: rgba(255,255,255,0.7); line-height: 1.5; margin-bottom: 5px; }
.nota-nombre { font-weight: 700; color: rgba(255,255,255,0.9); }
.cierre-box { background: #262626; border: 1px solid rgba(255,255,255,0.08); padding: 18px; }
.cierre-item { font-size: 16.15px; color: rgba(255,255,255,0.8); line-height: 1.6; margin-bottom: 8px; }
.page-footer { border-top: 1px solid rgba(255,255,255,0.08); padding-top: 9px; margin-top: 15px; }
.footer-brand { font-family: 'Montserrat', Helvetica, Arial, sans-serif; font-weight: 800; font-size: 11.9px; letter-spacing: 1.7px; color: rgba(255,255,255,0.3); text-transform: uppercase; }
'''


def generar_html(data):
    portada = render_portada(data)
    sesiones_html = ''.join(render_sesion(s, idx) for idx, s in enumerate(data['sesiones']))
    cierre = render_cierre(data)
    return f'''<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><style>{CSS}</style></head>
<body>{portada}{sesiones_html}{cierre}</body></html>'''


def generar_pdf_individual(texto_mesociclo, output_path):
    data = parse_individual_text(texto_mesociclo)
    if not data['sesiones']:
        raise ValueError('No se ha podido leer ninguna sesión del texto proporcionado.')
    html_path = output_path.replace('.pdf', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(generar_html(data))
    subprocess.run([
        'wkhtmltopdf', '--enable-local-file-access', '--encoding', 'utf-8',
        '--disable-smart-shrinking', '--print-media-type',
        html_path, output_path
    ], check=True)
    return data


if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'mesociclo.txt'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output_individual.pdf'
    with open(input_file, encoding='utf-8') as f:
        texto = f.read()
    data = generar_pdf_individual(texto, output_file)
    print(f"PDF generado: {output_file}")
    print(f"Persona: {data['persona']} · {len(data['sesiones'])} sesiones")
