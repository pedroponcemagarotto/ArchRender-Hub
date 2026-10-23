#!/usr/bin/env python3
"""ArchRender Hub V0.1 - private local-first architecture prompt library.

Python standard library only. Binds to localhost, persists recipes in SQLite,
and stores image uploads in a dedicated data folder.
"""
from __future__ import annotations

import argparse
import base64
import binascii
from datetime import datetime, timezone
from contextlib import contextmanager
import json
import mimetypes
import os
from pathlib import Path
import re
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, unquote
from uuid import uuid4
import webbrowser

VERSION = '0.1.0'
ROOT = Path(__file__).resolve().parent
STATIC = ROOT / 'static'
DATA = Path(os.environ.get('ARCHRENDER_DATA_DIR', ROOT / 'data')).expanduser().resolve()
IMAGES = DATA / 'uploads'
DB_FILE = DATA / 'archrender.sqlite3'
MAX_IMAGE = 8 * 1024 * 1024
MAX_REQUEST = 120 * 1024 * 1024
CATEGORIES = ['Fachadas', 'Interiores', 'Paisagismo', 'Plantas', 'Reformas', 'Materiais', 'Iluminacao', 'Pos-producao', 'Outros']
TOOLS = ['Universal', 'ChatGPT Images', 'Gemini', 'Midjourney', 'ComfyUI', 'Stable Diffusion', 'Veras', 'Outros']
FIELDS = ['title', 'summary', 'category', 'tool', 'input_type', 'style', 'lighting', 'camera',
          'materials', 'preserve', 'changes', 'prompt', 'negative_prompt', 'notes',
          'tags', 'before_image', 'after_image', 'favorite']
IMAGE_RE = re.compile(r'^/uploads/([0-9a-f]{32}\.(?:png|jpg|webp))$')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


@contextmanager
def db_connect():
    con = sqlite3.connect(DB_FILE, timeout=20)
    try:
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA foreign_keys=ON')
        con.execute('PRAGMA busy_timeout=5000')
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def seed_data():
    return [
        {'title': 'Fachada contemporânea brasileira', 'summary': 'Criação conceitual de fachada residencial com materiais naturais.', 'category': 'Fachadas', 'tool': 'Universal', 'input_type': 'Descrição textual', 'style': 'Contemporaneo brasileiro', 'lighting': 'Manha suave', 'camera': 'Vista ao nível dos olhos', 'materials': 'Reboco mineral claro, madeira natural e pedra bege', 'preserve': '', 'changes': 'Conceito livre', 'tags': ['conceito', 'residencial', 'fachada'], 'prompt': 'Crie uma visualização conceitual de uma residência brasileira contemporânea, com entrada sombreada, volumes proporcionais, esquadrias discretas, fachada em reboco mineral claro, painéis de madeira natural e base em pedra bege. Inclua paisagismo tropical de escala compativel com a residência. Enquadramento fotografico a altura dos olhos, verticais alinhadas, luz suave da manha, materiais realistas e atmosfera acolhedora. Não inclua textos ou marcas d agua.'},
        {'title': 'SketchUp para render realista', 'summary': 'Transforme uma captura de modelo 3D sem redesenhar a arquitetura.', 'category': 'Fachadas', 'tool': 'Universal', 'input_type': 'Captura de modelo 3D', 'style': 'Fotorrealismo', 'lighting': 'Luz natural difusa', 'camera': 'Mesma câmera da imagem de entrada', 'materials': 'Definir conforme o projeto', 'preserve': 'Volumetria, cobertura, aberturas, pilares, níveis e perspectiva', 'changes': 'Materiais, iluminação, vegetacao autorizada', 'tags': ['sketchup', 'revit', 'fidelidade'], 'prompt': 'Use a imagem de modelo 3D fornecida como base obrigatoria. Preserve a volumetria, as proporções, o alinhamento de pilares, a cobertura, os vãos de portas e janelas, os níveis e a perspectiva da câmera. Converta a apresentação em um render arquitetônico fotorrealista. Aplique materiais compativeis com o projeto: [DESCREVER MATERIAIS E POSICOES]. Utilize luz natural difusa, sombras fisicamente plausiveis e paisagismo apenas nas áreas autorizadas. Não acrescente ou elimine elementos arquitetônicos. Confira o resultado contra o modelo original.'},
        {'title': 'Sala de estar com materiais naturais', 'summary': 'Composicao de interior contemporâneo com luz equilibrada.', 'category': 'Interiores', 'tool': 'Universal', 'input_type': 'Descrição textual', 'style': 'Natural contemporâneo', 'lighting': 'Luz lateral de janela', 'camera': 'Fotografia interior de angulo amplo moderado', 'materials': 'Carvalho claro, pedra bege, tecidos de linho', 'preserve': '', 'changes': 'Conceito livre', 'tags': ['sala', 'interiores', 'marcenaria'], 'prompt': 'Crie uma imagem conceitual de sala de estar contemporânea e acolhedora, com marcenaria em madeira clara, revestimentos minerais bege, tecidos de linho, poucos objetos decorativos e mobiliario de proporções realistas. Luz natural lateral difusa, sombras de contato suaves, reflexos discretos, perspectiva com verticais alinhadas e fotografia de interiores de aspecto editorial. Evite excesso de brilho, decoração artificial ou objetos deformados.'},
        {'title': 'Troca controlada de revestimento', 'summary': 'Substitua um unico material mantendo todo o restante da imagem.', 'category': 'Materiais', 'tool': 'Universal', 'input_type': 'Imagem de render existente', 'style': 'Edicao localizada', 'lighting': 'Preservar a original', 'camera': 'Preservar a original', 'materials': '[MATERIAL ALVO]', 'preserve': 'Geometria, demais materiais, objetos e câmera', 'changes': 'Somente o revestimento indicado', 'tags': ['material', 'edição', 'precisao'], 'prompt': 'Edite apenas a area indicada na imagem. Substitua [REVESTIMENTO ATUAL] por [NOVO REVESTIMENTO E ACABAMENTO], mantendo juntas, bordas, dimensoes e posição do elemento. Preserve toda a arquitetura, mobiliario, paisagismo, câmera e outros materiais. Ajuste somente os reflexos e sombras estritamente necessarios para integrar o material a cena. Prefira mascara de selecao quando o editor disponibilizar esse recurso.'},
        {'title': 'Render ao entardecer', 'summary': 'Conversao controlada da iluminação mantendo o projeto.', 'category': 'Iluminacao', 'tool': 'Universal', 'input_type': 'Imagem de render existente', 'style': 'Blue hour', 'lighting': 'Entardecer com luz artificial quente', 'camera': 'Preservar a original', 'materials': 'Preservar os originais', 'preserve': 'Edificacao, câmera, paisagismo, elementos e materiais', 'changes': 'Horario e iluminação', 'tags': ['noturno', 'entardecer', 'fachada'], 'prompt': 'Transforme esta vista arquitetônica em uma imagem no inicio do entardecer, mantendo o mesmo edificio, enquadramento, vegetacao e acabamentos. Utilize céu azul suave, contraste moderado e iluminação interna quente visivel pelas janelas existentes. Acenda apenas as luminárias representadas no projeto; não invente aberturas nem novos pontos de luz. Preserve a leitura dos materiais e revise as sombras para que sejam coerentes com a nova iluminação.'},
        {'title': 'Paisagismo de jardim residencial', 'summary': 'Estudo de vegetacao para uma area externa existente.', 'category': 'Paisagismo', 'tool': 'Universal', 'input_type': 'Fotografia do local', 'style': 'Tropical contemporâneo', 'lighting': 'Dia claro, luz suave', 'camera': 'Preservar a fotografia', 'materials': 'Pedra drenante, vegetacao tropical', 'preserve': 'Muros, caminhos, edificacoes e limites do terreno', 'changes': 'Vegetacao apenas nas áreas indicadas', 'tags': ['jardim', 'vegetacao', 'exterior'], 'prompt': 'Use a fotografia como base do jardim. Preserve muros, caminhos, acesso, edificação, perspectiva e limites existentes. Planeje vegetacao tropical contemporânea somente nas áreas autorizadas: [AREAS]. Priorize espécies com portes coerentes e composição em camadas, com textura vegetal natural e sombras realistas. Mantenha as circulacoes desimpedidas. A imagem e conceitual e a escolha de espécies deve ser validada para o clima e a manutencao local.'},
        {'title': 'Planta baixa humanizada', 'summary': 'Colorizacao visual de planta técnica sem alterar a organizacao espacial.', 'category': 'Plantas', 'tool': 'Universal', 'input_type': 'Planta baixa', 'style': 'Humanizacao discreta', 'lighting': 'Sombras leves', 'camera': 'Ortografica superior', 'materials': 'Pisos diferenciados por ambiente', 'preserve': 'Paredes, vãos, circulacao, mobiliario desenhado', 'changes': 'Cores, materiais e sombras', 'tags': ['planta', 'humanizada', 'cad'], 'prompt': 'Humanize a planta aprovada mantendo vista superior ortográfica. Preserve paredes, portas, janelas, circulacoes, mobiliario desenhado e relacoes espaciais. Aplique pisos em cores naturais, texturas discretas e sombras leves para facilitar a leitura dos ambientes. Não acrescente, elimine ou reposicione elementos. Mantenha cotas e textos técnicos em camada original separada, quando possivel, e verifique a humanização por sobreposicao.'},
        {'title': 'Reforma visual de fachada fotografada', 'summary': 'Estudo de pintura e acabamentos sobre uma foto real.', 'category': 'Reformas', 'tool': 'Universal', 'input_type': 'Fotografia do local', 'style': 'Atualizacao contemporânea', 'lighting': 'Luz do registro original', 'camera': 'Preservar a fotografia', 'materials': 'Pintura fosca e revestimento de destaque', 'preserve': 'Pavimentos, portao, cobertura, aberturas, perspectiva e vizinhos', 'changes': 'Acabamentos especificados', 'tags': ['fachada', 'reforma', 'fotografia'], 'prompt': 'Utilize a fotografia fornecida para elaborar um estudo de reforma da fachada. Preserve numero de pavimentos, cobertura, dimensoes aparentes, localizacao de portas, janelas, portao, calcada, construcoes vizinhas e perspectiva. Altere exclusivamente [DESCREVER ACABAMENTOS E AREAS], utilizando a paleta [CORES]. Produza visualização realista, sem criar ou remover elementos arquitetônicos fora do escopo.'},
        {'title': 'Vista axonométrica de arquitetura', 'summary': 'Apresentacao tridimensional de leitura técnica a partir de uma base.', 'category': 'Pos-producao', 'tool': 'Universal', 'input_type': 'Modelo ou planta', 'style': 'Axonometrico editorial', 'lighting': 'Sombra técnica suave', 'camera': 'Vista axonométrica', 'materials': 'Superficies neutras e destaques pontuais', 'preserve': 'Distribuicao espacial e elementos documentados', 'changes': 'Linguagem grafica', 'tags': ['axonometria', 'apresentação', 'analise'], 'prompt': 'Crie uma vista axonométrica editorial a partir do desenho fornecido. Preserve a distribuicao espacial, os elementos documentados, os acessos e as relacoes de proporcao. Represente volumes com materiais neutros, linhas limpas, poucas cores de destaque, fundo claro e sombras suaves. Não invente escadas, circulacoes nem ambientes. Quando faltar informacao de altura ou espessura, sinalize a incerteza em vez de tratar a forma reconstruida como medida precisa.'},
        {'title': 'Melhoria de render existente', 'summary': 'Aprimore luz e acabamento sem alterar a arquitetura aprovada.', 'category': 'Pos-producao', 'tool': 'Universal', 'input_type': 'Render existente', 'style': 'Fotografia editorial', 'lighting': 'Corrigir contraste e exposição', 'camera': 'Preservar a original', 'materials': 'Melhorar textura sem substituicao', 'preserve': 'Geometria, materiais, quantidade de objetos e enquadramento', 'changes': 'Exposicao, textura e pos-produção', 'tags': ['upscale', 'acabamento', 'qualidade'], 'prompt': 'Melhore a qualidade visual deste render arquitetônico ja aprovado. Preserve exatamente a arquitetura representada, a câmera, a vegetacao, o mobiliario e os materiais selecionados. Corrija excesso de brilho, textura artificial, ruído, contraste desequilibrado e reflexos incoerentes. Aprimore microtexturas e sombras de contato sem alterar distribuicao, dimensoes ou numero de objetos. Compare as duas imagens antes de aceitar o resultado.'},
    ]


def initialize():
    DATA.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)
    with db_connect() as con:
        con.execute('PRAGMA journal_mode=WAL')
        con.execute('''CREATE TABLE IF NOT EXISTS recipes (
          id TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          summary TEXT NOT NULL DEFAULT '',
          category TEXT NOT NULL,
          tool TEXT NOT NULL,
          input_type TEXT NOT NULL DEFAULT '',
          style TEXT NOT NULL DEFAULT '',
          lighting TEXT NOT NULL DEFAULT '',
          camera TEXT NOT NULL DEFAULT '',
          materials TEXT NOT NULL DEFAULT '',
          preserve TEXT NOT NULL DEFAULT '',
          changes TEXT NOT NULL DEFAULT '',
          prompt TEXT NOT NULL,
          negative_prompt TEXT NOT NULL DEFAULT '',
          notes TEXT NOT NULL DEFAULT '',
          tags TEXT NOT NULL DEFAULT '[]',
          before_image TEXT NOT NULL DEFAULT '',
          after_image TEXT NOT NULL DEFAULT '',
          favorite INTEGER NOT NULL DEFAULT 0,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        )''')
        con.execute('CREATE TABLE IF NOT EXISTS app_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        seeded = con.execute("SELECT value FROM app_settings WHERE key='seeded'").fetchone()
        if not seeded:
            if con.execute('SELECT count(*) FROM recipes').fetchone()[0] == 0:
                for recipe in seed_data():
                    normalized = normalize_recipe(recipe)
                    insert_recipe(con, normalized)
            con.execute("INSERT INTO app_settings (key,value) VALUES ('seeded','1')")


def normalize_recipe(input_data, previous=None):
    if not isinstance(input_data, dict):
        raise ValueError('Receita deve ser um objeto JSON.')
    values = {}
    for field in FIELDS:
        value = input_data.get(field, (previous or {}).get(field, '' if field != 'tags' else []))
        if field == 'tags':
            if isinstance(value, str):
                value = [p.strip() for p in value.split(',') if p.strip()]
            if not isinstance(value, list) or len(value) > 20:
                raise ValueError('Use no máximo 20 etiquetas.')
            value = list(dict.fromkeys([str(x).strip()[:45] for x in value if str(x).strip()]))
        elif field == 'favorite':
            value = int(bool(value))
        else:
            if not isinstance(value, str):
                raise ValueError(f'Campo {field} deve ser texto.')
            max_len = 12000 if field in ('prompt', 'negative_prompt') else 3000 if field in ('notes', 'preserve', 'changes') else 600
            if len(value) > max_len:
                raise ValueError(f'Campo {field} excede o limite de caracteres.')
            value = value.strip()
        values[field] = value
    if not values['title'] or not values['prompt']:
        raise ValueError('Título e prompt são obrigatórios.')
    if values['category'] not in CATEGORIES:
        raise ValueError('Categoria inválida.')
    if not values['tool']:
        values['tool'] = 'Universal'
    for name in ('before_image', 'after_image'):
        if values[name] and not IMAGE_RE.fullmatch(values[name]):
            raise ValueError(f'Imagem invalida em {name}.')
    return values


def row_recipe(row):
    d = dict(row)
    try:
        d['tags'] = json.loads(d['tags'])
    except (json.JSONDecodeError, TypeError):
        d['tags'] = []
    d['favorite'] = bool(d['favorite'])
    return d


def insert_recipe(con, d, recipe_id=None, created_at=None):
    item_id = recipe_id or uuid4().hex
    created = created_at or now()
    columns = ['id', *FIELDS, 'created_at', 'updated_at']
    payload = [item_id, *[(json.dumps(d[f], ensure_ascii=False) if f == 'tags' else d[f]) for f in FIELDS], created, now()]
    con.execute('INSERT INTO recipes (' + ','.join(columns) + ') VALUES (' + ','.join('?' for _ in columns) + ')', payload)
    return item_id


def detect_image(content: bytes):
    if content.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png', 'image/png'
    if content.startswith(b'\xff\xd8\xff') and content.endswith(b'\xff\xd9'):
        return 'jpg', 'image/jpeg'
    if content[:4] == b'RIFF' and content[8:12] == b'WEBP':
        return 'webp', 'image/webp'
    raise ValueError('Use arquivos PNG, JPEG ou WebP validos.')


def decode_image(raw: str):
    if not isinstance(raw, str) or len(raw) > MAX_IMAGE * 1.38 + 100:
        raise ValueError('Imagem muito grande (limite de 8 MB).')
    if raw.startswith('data:'):
        raw = raw.split(',', 1)[-1]
    try:
        data = base64.b64decode(raw, validate=True)
    except (ValueError, binascii.Error):
        raise ValueError('Imagem em base64 invalida.')
    if not data or len(data) > MAX_IMAGE:
        raise ValueError('Imagem vazia ou superior a 8 MB.')
    return data, detect_image(data)


class ApiError(Exception):
    def __init__(self, message, status=400):
        self.message = message
        self.status = status


class AppHandler(BaseHTTPRequestHandler):
    server_version = f'ArchRenderHub/{VERSION}'

    def log_message(self, fmt, *args):
        print(f'[{self.log_date_time_string()}] {self.address_string()} {fmt % args}', flush=True)

    def headers_common(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'self'; img-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; script-src 'self'; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")

    def output(self, raw, status=200, content_type='application/json; charset=utf-8', download=None):
        self.send_response(status)
        self.headers_common()
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(raw)))
        if download:
            self.send_header('Content-Disposition', f'attachment; filename="{download}"')
        self.end_headers()
        self.wfile.write(raw)

    def send_json(self, payload, status=200):
        raw = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        self.output(raw, status)

    def json_body(self):
        size = self.headers.get('Content-Length')
        if size is None:
            raise ApiError('Corpo da requisicao obrigatorio.', 411)
        try:
            size = int(size)
        except ValueError:
            raise ApiError('Tamanho da requisicao invalido.', 400)
        if size <= 0 or size > MAX_REQUEST:
            raise ApiError('Requisição vazia ou muito grande.', 413)
        try:
            return json.loads(self.rfile.read(size).decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ApiError('JSON inválido.', 400)

    def check_write_origin(self):
        origin = self.headers.get('Origin')
        if origin:
            target = urlsplit(origin)
            valid = target.scheme == 'http' and target.hostname in ('localhost', '127.0.0.1') and target.port in (self.server.server_port, 5173)
            if not valid or (target.port == 5173 and os.environ.get('ARCHRENDER_DEV') != '1'):
                raise ApiError('Origem da requisicao nao autorizada.', 403)
        if self.headers.get('Content-Type', '').split(';')[0].strip().lower() != 'application/json':
            raise ApiError('Utilize Content-Type: application/json.', 415)

    def route(self, method):
        pathname = unquote(urlsplit(self.path).path)
        if method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            self.check_write_origin()
        if method == 'GET' and pathname == '/api/status':
            with db_connect() as con:
                count = con.execute('SELECT COUNT(*) FROM recipes').fetchone()[0]
                fav = con.execute('SELECT COUNT(*) FROM recipes WHERE favorite=1').fetchone()[0]
            return self.send_json({'ok': True, 'version': VERSION, 'recipes': count, 'favorites': fav, 'categories': CATEGORIES, 'tools': TOOLS})
        if method == 'GET' and pathname == '/api/recipes':
            with db_connect() as con:
                rows = con.execute('SELECT * FROM recipes ORDER BY updated_at DESC, id DESC LIMIT 2000').fetchall()
            return self.send_json({'items': [row_recipe(x) for x in rows], 'limit': 2000})
        if method == 'POST' and pathname == '/api/recipes':
            d = normalize_recipe(self.json_body())
            with db_connect() as con:
                recipe_id = insert_recipe(con, d)
                row = con.execute('SELECT * FROM recipes WHERE id=?', (recipe_id,)).fetchone()
                con.commit()
            return self.send_json(row_recipe(row), 201)
        m = re.fullmatch(r'/api/recipes/([0-9a-f]{32})(?:/(duplicate|favorite))?', pathname)
        if m:
            recipe_id, action = m.groups()
            with db_connect() as con:
                row = con.execute('SELECT * FROM recipes WHERE id=?', (recipe_id,)).fetchone()
                if not row:
                    raise ApiError('Receita não encontrada.', 404)
                previous = row_recipe(row)
                if method == 'GET' and action is None:
                    return self.send_json(previous)
                if method == 'POST' and action == 'duplicate':
                    d = normalize_recipe({**previous, 'title': f"{previous['title']} (copia)", 'favorite': False})
                    new_id = insert_recipe(con, d)
                    new_row = row_recipe(con.execute('SELECT * FROM recipes WHERE id=?', (new_id,)).fetchone())
                    con.commit()
                    return self.send_json(new_row, 201)
                if method == 'PATCH' and action == 'favorite':
                    con.execute('UPDATE recipes SET favorite=?,updated_at=? WHERE id=?', (int(not previous['favorite']), now(), recipe_id))
                    con.commit()
                    return self.send_json({'favorite': not previous['favorite']})
                if method == 'PUT' and action is None:
                    d = normalize_recipe(self.json_body(), previous)
                    assigns = ','.join(f'{f}=?' for f in FIELDS)
                    values = [(json.dumps(d[f], ensure_ascii=False) if f == 'tags' else d[f]) for f in FIELDS]
                    con.execute(f'UPDATE recipes SET {assigns}, updated_at=? WHERE id=?', [*values, now(), recipe_id])
                    updated = row_recipe(con.execute('SELECT * FROM recipes WHERE id=?', (recipe_id,)).fetchone())
                    con.commit()
                    return self.send_json(updated)
                if method == 'DELETE' and action is None:
                    con.execute('DELETE FROM recipes WHERE id=?', (recipe_id,))
                    con.commit()
                    return self.send_json({'deleted': True})
            raise ApiError('Operação não permitida.', 405)
        if method == 'POST' and pathname == '/api/images':
            body = self.json_body()
            if not isinstance(body, dict):
                raise ApiError('Imagem inválida.')
            try:
                data, (ext, _) = decode_image(body.get('data', ''))
            except ValueError as exc:
                raise ApiError(str(exc))
            filename = uuid4().hex + '.' + ext
            target = IMAGES / filename
            # create atomically and never overwrite an existing upload
            with target.open('xb') as file:
                file.write(data)
            return self.send_json({'url': '/uploads/' + filename, 'bytes': len(data)}, 201)
        if method == 'GET' and pathname == '/api/backup':
            with db_connect() as con:
                rows = [row_recipe(x) for x in con.execute('SELECT * FROM recipes ORDER BY id').fetchall()]
            used = set()
            for row in rows:
                for f in ('before_image', 'after_image'):
                    m = IMAGE_RE.fullmatch(row.get(f) or '')
                    if m:
                        used.add(m.group(1))
            image_data = {}
            total_size = 0
            for filename in sorted(used):
                f = IMAGES / filename
                if f.exists():
                    total_size += f.stat().st_size
                    if total_size > 90 * 1024 * 1024:
                        raise ApiError('Backup maior que 90 MB. Reduza as imagens antes de exportar.', 413)
                    image_data[filename] = base64.b64encode(f.read_bytes()).decode('ascii')
            archive = {'format': 'archrender-hub-v1', 'version': VERSION, 'exported_at': now(), 'recipes': rows, 'images': image_data}
            raw = json.dumps(archive, ensure_ascii=False).encode('utf-8')
            return self.output(raw, 200, 'application/json; charset=utf-8', 'archrender-hub-backup.json')
        if method == 'POST' and pathname == '/api/restore':
            data = self.json_body()
            if not isinstance(data, dict) or data.get('format') != 'archrender-hub-v1':
                raise ApiError('Backup não compatível.')
            recipes = data.get('recipes')
            images = data.get('images')
            if not isinstance(recipes, list) or not isinstance(images, dict) or len(recipes) > 2000:
                raise ApiError('Formato de backup invalido.')
            staged = []
            images_map = {}
            try:
                for key, blob in images.items():
                    if not re.fullmatch(r'[0-9a-f]{32}\.(?:png|jpg|webp)', key):
                        raise ApiError('Nome de imagem invalido no backup.')
                    try:
                        content, (ext, _) = decode_image(blob)
                    except ValueError as exc:
                        raise ApiError(str(exc))
                    new_name = uuid4().hex + '.' + ext
                    staged.append((IMAGES / new_name, content))
                    images_map['/uploads/' + key] = '/uploads/' + new_name
                normalized = []
                for row in recipes:
                    if not isinstance(row, dict):
                        raise ApiError('Receita invalida no backup.')
                    mapped = dict(row)
                    for f in ('before_image', 'after_image'):
                        if mapped.get(f):
                            if mapped[f] not in images_map:
                                raise ApiError('Backup incompleto: imagem não encontrada.')
                            mapped[f] = images_map[mapped[f]]
                    d = normalize_recipe(mapped)
                    if not re.fullmatch(r'[0-9a-f]{32}', str(row.get('id', ''))):
                        raise ApiError('Identificador de receita inválido.')
                    normalized.append((row['id'], d, str(row.get('created_at') or now())[:64]))
                for path, raw in staged:
                    with path.open('xb') as f:
                        f.write(raw)
                with db_connect() as con:
                    for rid, d, created in normalized:
                        con.execute('DELETE FROM recipes WHERE id=?', (rid,))
                        insert_recipe(con, d, rid, created)
                return self.send_json({'restored': len(normalized), 'images': len(images_map)})
            except Exception:
                for path, _ in staged:
                    path.unlink(missing_ok=True)
                raise
        if method == 'GET':
            if pathname == '/':
                return self.file_response(STATIC / 'index.html', 'text/html; charset=utf-8')
            m = IMAGE_RE.fullmatch(pathname)
            if m:
                path = IMAGES / m.group(1)
                if not path.is_file():
                    raise ApiError('Imagem não encontrada.', 404)
                mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
                return self.file_response(path, mime)
            if pathname in ('/style.css', '/app.js', '/favicon.svg'):
                file = STATIC / pathname[1:]
                if not file.is_file():
                    raise ApiError('Arquivo não encontrado.', 404)
                return self.file_response(file, mimetypes.guess_type(str(file))[0] or 'application/octet-stream')
        raise ApiError('Rota nao encontrada.', 404)

    def file_response(self, file, mime):
        return self.output(file.read_bytes(), 200, mime)

    def handle_method(self, method):
        try:
            return self.route(method)
        except ApiError as exc:
            self.send_json({'error': exc.message}, exc.status)
        except (ValueError, sqlite3.Error) as exc:
            self.send_json({'error': str(exc)}, 400)
        except Exception as exc:
            print(f'Erro inesperado: {type(exc).__name__}: {exc}', flush=True)
            self.send_json({'error': 'Erro interno. Consulte o terminal do servidor.'}, 500)

    def do_GET(self): self.handle_method('GET')
    def do_POST(self): self.handle_method('POST')
    def do_PUT(self): self.handle_method('PUT')
    def do_PATCH(self): self.handle_method('PATCH')
    def do_DELETE(self): self.handle_method('DELETE')


def run():
    parser = argparse.ArgumentParser(description='ArchRender Hub - biblioteca local de prompts')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    if not (1024 <= args.port <= 65535):
        parser.error('Use porta entre 1024 e 65535.')
    initialize()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), AppHandler)
    url = f'http://127.0.0.1:{args.port}'
    print(f'ArchRender Hub V{VERSION} em {url}', flush=True)
    print(f'Dados locais: {DATA}', flush=True)
    print('Para encerrar: pressione Ctrl+C', flush=True)
    if not args.no_browser:
        import threading
        threading.Timer(0.9, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor encerrado.', flush=True)
    finally:
        server.server_close()


if __name__ == '__main__':
    run()
