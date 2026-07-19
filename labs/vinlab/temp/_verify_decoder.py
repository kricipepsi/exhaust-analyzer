import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open('vinlab/decoder.py').read()
assert 'db_dict.get("has_maf")' in src or "db_dict.get('has_maf')" in src, "decoder does not read has_maf"
assert 'db_dict.get("has_map")' in src or "db_dict.get('has_map')" in src, "decoder does not read has_map"
print('OK: decoder reads has_maf/has_map from db_dict')
