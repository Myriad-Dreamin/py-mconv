
import pandas as pd
import json

class MJson(dict):
    def __init__(self, *kvs, **kwargs):
        super().__init__(*kvs, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = MJson(v)

    def update_key(self, key, value):
        if '.' in key:
            key, k1 = key.split('.', 2)
            obj = self.get(key, MJson())
            if not isinstance(obj, MJson):
                obj = MJson()
            obj.update_key(k1, value)
            value = obj
        self[key] = value

    def update_row(self, kkk, vvv):
        def _update_row(row):
            key = row[kkk]
            value = row[vvv]
            if key is not None:
                self.update_key(key, value)
            return row
        return _update_row

    def compress(self):
        ks, vs = [], []
        for k, v in self.items():
            if isinstance(v, MJson):
                sks, svs = v.compress()
                ks += [k + '.' + sk for sk in sks]
                vs += svs
            else:
                ks.append(k)
                vs.append(v)
        return ks, vs

class PyConv:
    def __init__(self):
        self.kvs = MJson()
    
    def from_csv(self, file_name, encoding='utf-8', key='key', value='value'):
        df = pd.read_csv(file_name, encoding=encoding)
        df = df.apply(self.kvs.update_row(key, value), axis=1)
        return self
    
    def from_json(self, file_name, encoding='utf-8'):
        with open(file_name, 'r', encoding=encoding) as f:
            self.kvs = MJson(json.load(f))
        return self

    def from_excel(self, file_name, sheet_name, key='key', value='value', header=0, encoding='utf-8'):
        df = pd.read_excel(file_name, sheet_name, header)
        df = df.apply(self.kvs.update_row(key, value), axis=1)
        return self

    def to_json(self, file_name, encoding='utf-8'):
        with open(file_name, 'w+', encoding=encoding) as f:
            json.dump(self.kvs, f, ensure_ascii=False)
        return self

    def to_js(self, file_name, encoding='utf-8'):
        with open(file_name, 'w+', encoding=encoding) as f:
            x = json.dumps(self.kvs, ensure_ascii=False)
            f.write("""
'use strict';
module.export=%s;
""" % x)
        return self
    
    def to_csv(self, file_name, encoding='utf-8'):
        ks, vs = self.kvs.compress()
        df = pd.DataFrame({'key': ks, 'value': vs})
        df.to_csv(file_name, encoding='utf-8',index=None)
        return self

    
    def to_excel(self, file_name, encoding='utf-8'):
        ks, vs = self.kvs.compress()
        df = pd.DataFrame({'key': ks, 'value': vs})
        df.to_excel(file_name, encoding='utf-8',index=None)
        return self

    def from_file(self, file_name, encoding='utf-8'):
        if file_name.endswith('.json'):
            self.from_json(file_name, encoding)
        elif file_name.endswith('.json'):
            self.from_json(file_name, encoding)
        elif file_name.endswith('.xlsx'):
            self.from_excel(file_name, encoding)
        elif file_name.endswith('.xls'):
            self.from_excel(file_name, encoding)
        elif file_name.endswith('.csv'):
            self.from_csv(file_name, encoding)
        else:
            self.from_json(file_name, encoding)
        return self
    
    def to_file(self, file_name, encoding='utf-8'):
        if file_name.endswith('.json'):
            self.to_json(file_name, encoding)
        elif file_name.endswith('.json'):
            self.to_json(file_name, encoding)
        elif file_name.endswith('.js'):
            self.to_js(file_name, encoding)
        elif file_name.endswith('.xlsx'):
            self.to_excel(file_name, encoding)
        elif file_name.endswith('.xls'):
            self.to_excel(file_name, encoding)
        elif file_name.endswith('.csv'):
            self.to_csv(file_name, encoding)
        else:
            self.to_json(file_name, encoding)
        return self

    
if __name__ == '__main__':
    PyConv().from_csv('x.csv', key='key', value='zh').to_json('x.json')
    PyConv().from_json('x.json').to_js('x.js')
    PyConv().from_json('x.json').to_csv('xx.csv')

    PyConv().from_excel('x.xls', 'Sheet1', key='key', value='zh').to_json('y.json')
    PyConv().from_json('y.json').to_js('y.js')
    PyConv().from_json('y.json').to_csv('y.csv')
    PyConv().from_json('y.json').to_excel('y.xls')
    
