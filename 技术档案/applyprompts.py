# -*- coding: utf-8 -*-
"""
把两份提示词写入工作应用的草稿。
用法: python applyprompts.py <面试官提示词.txt> <分类器指令.txt>
生成 apply_iv.js / apply_cls.js，再由 bash 调 owb 执行。
"""
import base64, io, sys

TPL = """(async () => {
  const SRC='f2e4f2a5-8e96-4a15-972d-4c2d5af57669';
  const t=localStorage.getItem('console_token');
  const H={'Authorization':'Bearer '+t,'OperToken':t,'Content-Type':'application/json'};
  const dec=b=>new TextDecoder('utf-8').decode(Uint8Array.from(atob(b),c=>c.charCodeAt(0)));
  const s=await (await fetch('/console/api/apps/'+SRC+'/workflows/draft',{headers:H})).json();
  const log=[];
%s
  const r=await fetch('/console/api/apps/'+SRC+'/workflows/draft',{method:'POST',headers:H,
    body:JSON.stringify({graph:s.graph,features:s.features,environment_variables:s.environment_variables||{},
      conversation_variables:s.conversation_variables||[],hash:s.hash})});
  log.push('SAVE '+r.status+' '+(await r.text()).slice(0,140));
  return log.join(String.fromCharCode(10));
})()"""

IV_BODY = """  const iv=s.graph.nodes.find(n=>n.id==='1791552000021');
  const NEW=dec('%s');
  log.push('IV before='+iv.data.prompt_template[0].text.length);
  iv.data.prompt_template=[{new_level:true,role:'system',text:NEW}];
  log.push('IV after='+iv.data.prompt_template[0].text.length);"""

CLS_BODY = """  const cl=s.graph.nodes.find(n=>n.id==='1791544053269');
  const NEW=dec('%s');
  log.push('CLS before='+cl.data.instructions.length);
  cl.data.instructions=NEW;
  log.push('CLS after='+cl.data.instructions.length);"""


def b64(path):
    return base64.b64encode(io.open(path, encoding='utf-8').read().strip().encode('utf-8')).decode()


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    io.open('apply_iv.js', 'w', encoding='utf-8', newline='\n').write(TPL % (IV_BODY % b64(sys.argv[1])))
    io.open('apply_cls.js', 'w', encoding='utf-8', newline='\n').write(TPL % (CLS_BODY % b64(sys.argv[2])))
    print('generated apply_iv.js apply_cls.js')
    return 0


if __name__ == '__main__':
    sys.exit(main())
