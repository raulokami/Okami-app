import re


def parse_okami_text(raw: str) -> dict:
    """
    Parser unificado OKAMI. Cubre todos los formatos de texto con marcadores:
    - CLASE (SUBFORMATO: METCON / ENDURANCE)
    - ATLETA
    - HYBRID (usa TIPO_DIA para distinguir días Box/Run/etc.)
    - RECOMPOSICION
    - HYBRID INDIVIDUAL (mismo marcador que Atleta/Hybrid + TIPO_DIA)

    Campos de salida:
      formato, subformato, semana, intencion, dias_totales, dias, cierre
      Cada día: numero, titulo, objetivo, tipo_dia, bloques, tip
      Cada bloque: nombre, formato_wod, items, rx, int, scale
      Cada item: texto, formato, buscamos
    """
    lines = [l.strip() for l in raw.split('\n')]
    data = {
        'formato': '', 'semana': '', 'intencion': '', 'dias_totales': '',
        'dias': [], 'cierre': []
    }

    i = 0
    current_dia = None
    current_bloque = None

    def flush_bloque():
        nonlocal current_bloque
        if current_dia is not None and current_bloque is not None:
            current_dia['bloques'].append(current_bloque)
            current_bloque = None

    def flush_dia():
        nonlocal current_dia
        flush_bloque()
        if current_dia is not None:
            data['dias'].append(current_dia)
            current_dia = None

    stop_markers_intencion = re.compile(r'^(DIA|FORMATO|SEMANA|DIAS_TOTALES|CIERRE_SEMANA):')
    stop_markers_objetivo = re.compile(r'^(BLOQUE|DIA|TIP|CIERRE_SEMANA):')
    stop_markers_tip = re.compile(r'^(DIA|CIERRE_SEMANA):')

    n = len(lines)
    while i < n:
        line = lines[i]
        if not line:
            i += 1
            continue

        if line.startswith('FORMATO:'):
            data['formato'] = line.replace('FORMATO:', '').strip()
        elif line.startswith('SEMANA:'):
            data['semana'] = line.replace('SEMANA:', '').strip()
        elif line.startswith('DIAS_TOTALES:'):
            data['dias_totales'] = line.replace('DIAS_TOTALES:', '').strip()
        elif line.startswith('INTENCION:'):
            text = line.replace('INTENCION:', '').strip()
            j = i + 1
            while j < n and lines[j] and not stop_markers_intencion.match(lines[j]):
                text += ' ' + lines[j]
                j += 1
            data['intencion'] = text.strip()
            i = j - 1
        elif line.startswith('DIA:'):
            flush_dia()
            current_dia = {
                'numero': line.replace('DIA:', '').strip(),
                'titulo': '', 'objetivo': '', 'tipo_dia': '',
                'bloques': [], 'tip': ''
            }
        elif line.startswith('TIPO_DIA:'):
            if current_dia is not None:
                current_dia['tipo_dia'] = line.replace('TIPO_DIA:', '').strip()
        elif line.startswith('TITULO:'):
            if current_dia is not None:
                current_dia['titulo'] = line.replace('TITULO:', '').strip()
        elif line.startswith('OBJETIVO:'):
            text = line.replace('OBJETIVO:', '').strip()
            j = i + 1
            while j < n and lines[j] and not stop_markers_objetivo.match(lines[j]):
                text += ' ' + lines[j]
                j += 1
            if current_dia is not None:
                current_dia['objetivo'] = text.strip()
            i = j - 1
        elif line.startswith('BLOQUE:'):
            flush_bloque()
            current_bloque = {
                'nombre': line.replace('BLOQUE:', '').strip(),
                'formato_wod': '', 'items': [], 'rx': '', 'int': '', 'scale': ''
            }
        elif line.startswith('FORMATO_WOD:'):
            if current_bloque is not None:
                current_bloque['formato_wod'] = line.replace('FORMATO_WOD:', '').strip()
        elif line.startswith('- ') and current_bloque is not None:
            item_text = line[2:].strip()
            if '|' in item_text:
                parts = [p.strip() for p in item_text.split('|')]
                ejercicio = parts[0]
                formato_part = next((p for p in parts if p.startswith('FORMATO:')), None)
                buscamos_part = next((p for p in parts if p.startswith('BUSCAMOS:')), None)
                current_bloque['items'].append({
                    'texto': ejercicio,
                    'formato': formato_part.replace('FORMATO:', '').strip() if formato_part else '',
                    'buscamos': buscamos_part.replace('BUSCAMOS:', '').strip() if buscamos_part else ''
                })
            else:
                current_bloque['items'].append({'texto': item_text, 'formato': '', 'buscamos': ''})
        elif line.startswith('RX:'):
            if current_bloque is not None:
                current_bloque['rx'] = line.replace('RX:', '').strip()
        elif line.startswith('INT:'):
            if current_bloque is not None:
                current_bloque['int'] = line.replace('INT:', '').strip()
        elif line.startswith('SCALE:'):
            if current_bloque is not None:
                current_bloque['scale'] = line.replace('SCALE:', '').strip()
        elif line.startswith('TIP:'):
            flush_bloque()
            text = line.replace('TIP:', '').strip()
            j = i + 1
            while j < n and lines[j] and not stop_markers_tip.match(lines[j]):
                text += ' ' + lines[j]
                j += 1
            if current_dia is not None:
                current_dia['tip'] = text.strip()
            i = j - 1
        elif line.startswith('CIERRE_SEMANA:'):
            flush_dia()
        elif line.startswith('- ') and current_dia is None and len(data['dias']) > 0:
            data['cierre'].append(line[2:].strip())

        i += 1

    flush_dia()
    return data


if __name__ == '__main__':
    with open('/home/claude/okami-app/semana_4.44_atleta.txt', encoding='utf-8') as f:
        raw = f.read()
    result = parse_okami_text(raw)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False)[:2000])
    print(f"\nTotal dias: {len(result['dias'])}")
