"""End-to-end API regression tests using a temporary database and HTTP server."""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+L0x0AAAAASUVORK5CYII=')


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='archrender_tests_')
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            cls.port = s.getsockname()[1]
        cls.base = f'http://127.0.0.1:{cls.port}'
        env = dict(os.environ, ARCHRENDER_DATA_DIR=cls.tmp.name)
        cls.server = subprocess.Popen([sys.executable, str(ROOT/'app.py'), '--no-browser', '--port', str(cls.port)], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env)
        for _ in range(70):
            try:
                with urlopen(cls.base+'/api/status',timeout=.2) as res:
                    if res.status == 200:
                        break
            except Exception:
                time.sleep(.1)
        else:
            raise RuntimeError('Server failed to start: '+str(cls.server.poll()))

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        try: cls.server.wait(timeout=4)
        except subprocess.TimeoutExpired: cls.server.kill()
        cls.tmp.cleanup()

    def request(self, path, method='GET', data=None, content_type='application/json', origin=None):
        headers = {'Content-Type':content_type}
        if origin:headers['Origin']=origin
        if data is not None:
            body=json.dumps(data,ensure_ascii=False).encode('utf-8')
        else:
            body=b'' if method in ('DELETE','PATCH','POST') else None
        req=Request(self.base+path,method=method,data=body,headers=headers)
        try:
            with urlopen(req,timeout=10) as res:
                raw=res.read()
                return res.status, json.loads(raw) if raw and res.headers.get_content_type()=='application/json' else raw
        except HTTPError as ex:
            return ex.code,json.loads(ex.read())

    def test_01_initial_seed_and_static(self):
        code,meta=self.request('/api/status')
        self.assertEqual(200,code)
        self.assertEqual('0.1.0',meta['version'])
        self.assertGreaterEqual(meta['recipes'],10)
        code,html=self.request('/')
        self.assertEqual(200,code)
        self.assertIn(b'ArchRender Hub',html)
        code,records=self.request('/api/recipes')
        self.assertEqual(200,code)
        self.assertEqual(meta['recipes'],len(records['items']))

    def test_02_crud_copy_favorite_and_xss_input_roundtrip(self):
        payload={'title':'Teste <script>alert(1)</script>', 'summary':'<img src=x onerror=alert(1)>',
            'category':'Interiores','tool':'Universal','prompt':'Preservar janela e cobertura.',
            'tags':['teste','interiores'],'favorite':False}
        status,recipe=self.request('/api/recipes',method='POST',data=payload)
        self.assertEqual(201,status)
        rid=recipe['id']
        self.assertRegex(rid,r'^[0-9a-f]{32}$')
        self.assertEqual(payload['title'],recipe['title'])
        status,fav=self.request('/api/recipes/'+rid+'/favorite','PATCH')
        self.assertEqual(200,status)
        self.assertTrue(fav['favorite'])
        status,updated=self.request('/api/recipes/'+rid,'PUT',data={'title':'Atualizado','tags':['agora']})
        self.assertEqual(200,status)
        self.assertTrue(updated['favorite'])
        self.assertEqual(['agora'],updated['tags'])
        status,copied=self.request('/api/recipes/'+rid+'/duplicate','POST')
        self.assertEqual(201,status)
        self.assertNotEqual(rid,copied['id'])
        self.assertIn('(copia)',copied['title'])
        for to_delete in [rid,copied['id']]:
            self.assertEqual(200,self.request('/api/recipes/'+to_delete,'DELETE')[0])
        self.assertEqual(404,self.request('/api/recipes/'+rid)[0])

    def test_03_bad_json_category_and_origin(self):
        bad={'title':'titulo','prompt':'teste','category':'inexistente'}
        status,data=self.request('/api/recipes','POST',bad)
        self.assertEqual(400,status)
        self.assertIn('Categoria',data['error'])
        status,_=self.request('/api/recipes','POST',{'title':'x','prompt':'x','category':'Fachadas'},origin='http://bad.test')
        self.assertEqual(403,status)
        status,_=self.request('/api/recipes','POST',{'title':'x','prompt':'x','category':'Fachadas'},content_type='text/plain')
        self.assertEqual(415,status)

    def test_04_image_upload_and_header(self):
        status,data=self.request('/api/images','POST',{'data':'data:image/png;base64,'+base64.b64encode(PNG).decode('ascii')})
        self.assertEqual(201,status)
        self.assertRegex(data['url'],r'^/uploads/[0-9a-f]{32}\.png$')
        code,img=self.request(data['url'])
        self.assertEqual(200,code)
        self.assertEqual(PNG,img)
        self.assertEqual(400,self.request('/api/images','POST',{'data':base64.b64encode(b'not image').decode()})[0])
        self.assertEqual(404,self.request('/uploads/../../app.py')[0])

    def test_05_backup_and_restore(self):
        status,im=self.request('/api/images','POST',{'data':base64.b64encode(PNG).decode('ascii')})
        self.assertEqual(201,status)
        status,rc=self.request('/api/recipes','POST',{'title':'Preservar dados','prompt':'Fachada fiel','category':'Fachadas','tool':'Gemini','after_image':im['url']})
        self.assertEqual(201,status)
        status,bkp=self.request('/api/backup')
        self.assertEqual(200,status)
        backup=bkp
        self.assertEqual('archrender-hub-v1',backup['format'])
        self.assertTrue(backup['images'])
        status,restored=self.request('/api/restore','POST',backup)
        self.assertEqual(200,status)
        self.assertGreater(restored['restored'],0)
        status,latest=self.request('/api/recipes/'+rc['id'])
        self.assertEqual(200,status)
        self.assertNotEqual(im['url'],latest['after_image'])
        self.assertEqual(200,self.request(latest['after_image'])[0])
        self.assertEqual(400,self.request('/api/restore','POST',{'format':'other'})[0])

    def test_06_no_external_assets(self):
        _,html=self.request('/')
        self.assertNotIn(b'https://',html)
        _,css=self.request('/style.css')
        self.assertIn(b'.recipe-grid',css)
        self.assertNotIn(b'@import',css)
        _,script=self.request('/app.js')
        self.assertIn(b'buildPrompt',script)
        self.assertNotIn(b'import(',script)

if __name__ == '__main__':
    unittest.main(verbosity=2)
