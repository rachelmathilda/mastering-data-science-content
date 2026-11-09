import json,subprocess,sys
for f in sys.argv[1:]:
    m=json.load(open(f,encoding='utf-8'))
    bad=0
    for l in m['lessons']:
        for p in l['parts']:
            for b in p['blocks']:
                if b['type']=='code_example':
                    r=subprocess.run(['python3','-I','-c',b['code']],capture_output=True,text=True,timeout=60)
                    exp=b['expected_output_note']
                    ok=r.stdout.split()==exp.split()
                    if not ok:
                        bad+=1
                        print('MISMATCH',f,b['filename']);print(r.stdout);print(r.stderr[-300:])
    print(f,'outputs ok' if not bad else '%d mismatches'%bad)
