import glob
import json
import os

cands = glob.glob('cdt_open_prs.json') + glob.glob(os.path.join('.cron_tmp','cdt_open_prs.json'))
print('candidate paths:', cands)
p = cands[0]
data = json.load(open(p))
print('total open PRs:', len(data))
rows = []
for pr in data:
    repo = pr['repository']['nameWithOwner']
    if any(x in repo.lower() for x in ['hermes','openclaw','openhuman']) or '.github.io' in repo.lower():
        continue
    rows.append((repo, pr['number'], pr['updatedAt'], pr['createdAt']))
print('in-scope open PRs:', len(rows))
for r in sorted(rows, key=lambda x: x[2], reverse=True):
    print(r)
