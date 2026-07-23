import re


def parse_individual_text(raw: str) -> dict:
    lines = [l.strip() for l in raw.split('\n')]
    data = {
        'persona': '', 'duracion': '', 'frecuencia': '', 'duracion_sesion': '',
        'contexto': '', 'objetivo_mesociclo': '', 'lectura_caso': '',
        'criterios_bloque': [], 'reglas_operativas': [], 'escala_esfuerzo': [],
        'progresion_mesociclo': [], 'estructura_semanal': [],
        'sesiones': [], 'logica_progresion': [], 'criterios_exito': []
    }
    n = len(lines)
    i = 0
    current_sesion = None
    current_bloque = None

    def flush_bloque():
        nonlocal current_bloque
        if current_sesion is not None and current_bloque is not None:
            current_sesion['bloques'].append(current_bloque)
            current_bloque = None

    def flush_sesion():
        nonlocal current_sesion
        flush_bloque()
        if current_sesion is not None:
            data['sesiones'].append(current_sesion)
            current_sesion = None

    list_stop = re.compile(
        r'^(FORMATO|PERSONA|DURACION|FRECUENCIA|DURACION_SESION|CONTEXTO|'
        r'OBJETIVO_MESOCICLO|LECTURA_CASO|CRITERIOS_BLOQUE|REGLAS_OPERATIVAS|'
        r'ESCALA_ESFUERZO|PROGRESION_MESOCICLO|ESTRUCTURA_SEMANAL|SEMANA|'
        r'DIA_SEMANA|TITULO|OBJETIVO|ESFUERZO|BLOQUE|TIEMPO|LECTURA|'
        r'FEEDBACK_SESION|NOTAS_TECNICAS|LOGICA_PROGRESION|CRITERIOS_EXITO):'
    )

    def collect_list(start_idx):
        items = []
        j = start_idx
        while j < n and lines[j].startswith('- '):
            items.append(lines[j][2:].strip())
            j += 1
        return items, j

    def collect_paragraph(start_idx):
        text = ''
        j = start_idx
        while j < n and lines[j] and not list_stop.match(lines[j]):
            text += (' ' if text else '') + lines[j]
            j += 1
        return text.strip(), j

    while i < n:
        line = lines[i]
        if not line:
            i += 1
            continue
        if line.startswith('FORMATO:'):
            pass
        elif line.startswith('PERSONA:'):
            data['persona'] = line.replace('PERSONA:', '').strip()
        elif line.startswith('DURACION_SESION:'):
            data['duracion_sesion'] = line.replace('DURACION_SESION:', '').strip()
        elif line.startswith('DURACION:'):
            data['duracion'] = line.replace('DURACION:', '').strip()
        elif line.startswith('FRECUENCIA:'):
            data['frecuencia'] = line.replace('FRECUENCIA:', '').strip()
        elif line.startswith('CONTEXTO:'):
            data['contexto'] = line.replace('CONTEXTO:', '').strip()
        elif line.startswith('OBJETIVO_MESOCICLO:'):
            data['objetivo_mesociclo'] = line.replace('OBJETIVO_MESOCICLO:', '').strip()
        elif line.startswith('LECTURA_CASO:'):
            text, j = collect_paragraph(i + 1)
            data['lectura_caso'] = text
            i = j - 1
        elif line.startswith('CRITERIOS_BLOQUE:'):
            items, j = collect_list(i + 1)
            data['criterios_bloque'] = items
            i = j - 1
        elif line.startswith('REGLAS_OPERATIVAS:'):
            items, j = collect_list(i + 1)
            data['reglas_operativas'] = items
            i = j - 1
        elif line.startswith('ESCALA_ESFUERZO:'):
            items, j = collect_list(i + 1)
            data['escala_esfuerzo'] = items
            i = j - 1
        elif line.startswith('PROGRESION_MESOCICLO:') and current_sesion is None:
            items, j = collect_list(i + 1)
            data['progresion_mesociclo'] = items
            i = j - 1
        elif line.startswith('ESTRUCTURA_SEMANAL:'):
            items, j = collect_list(i + 1)
            data['estructura_semanal'] = items
            i = j - 1
        elif line.startswith('SEMANA:'):
            flush_sesion()
            current_sesion = {
                'semana': line.replace('SEMANA:', '').strip(),
                'dia_semana': '', 'titulo': '', 'objetivo': '', 'esfuerzo': '',
                'bloques': [], 'feedback': [], 'notas_tecnicas': []
            }
        elif line.startswith('DIA_SEMANA:'):
            if current_sesion is not None:
                current_sesion['dia_semana'] = line.replace('DIA_SEMANA:', '').strip()
        elif line.startswith('TITULO:'):
            if current_sesion is not None:
                current_sesion['titulo'] = line.replace('TITULO:', '').strip()
        elif line.startswith('OBJETIVO:'):
            text, j = collect_paragraph(i + 1)
            full = (line.replace('OBJETIVO:', '').strip() + ' ' + text).strip()
            if current_sesion is not None:
                current_sesion['objetivo'] = full
            i = j - 1
        elif line.startswith('ESFUERZO:'):
            if current_sesion is not None:
                current_sesion['esfuerzo'] = line.replace('ESFUERZO:', '').strip()
        elif line.startswith('BLOQUE:'):
            flush_bloque()
            current_bloque = {
                'nombre': line.replace('BLOQUE:', '').strip(),
                'tiempo': '', 'items': [], 'lectura': ''
            }
        elif line.startswith('TIEMPO:'):
            if current_bloque is not None:
                current_bloque['tiempo'] = line.replace('TIEMPO:', '').strip()
        elif line.startswith('LECTURA:'):
            text, j = collect_paragraph(i + 1)
            full = (line.replace('LECTURA:', '').strip() + ' ' + text).strip()
            if current_bloque is not None:
                current_bloque['lectura'] = full
            i = j - 1
        elif line.startswith('- ') and current_bloque is not None:
            current_bloque['items'].append(line[2:].strip())
        elif line.startswith('FEEDBACK_SESION:'):
            flush_bloque()
            items, j = collect_list(i + 1)
            if current_sesion is not None:
                current_sesion['feedback'] = items
            i = j - 1
        elif line.startswith('NOTAS_TECNICAS:'):
            items, j = collect_list(i + 1)
            if current_sesion is not None:
                current_sesion['notas_tecnicas'] = items
            i = j - 1
        elif line.startswith('LOGICA_PROGRESION:'):
            flush_sesion()
            items, j = collect_list(i + 1)
            data['logica_progresion'] = items
            i = j - 1
        elif line.startswith('CRITERIOS_EXITO:'):
            items, j = collect_list(i + 1)
            data['criterios_exito'] = items
            i = j - 1
        i += 1

    flush_sesion()
    return data
