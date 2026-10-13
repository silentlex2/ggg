(async () => {
  const SRC='f2e4f2a5-8e96-4a15-972d-4c2d5af57669';
  const DST='d12ff679-81f2-4b55-a826-c8135638153a';
  const t=localStorage.getItem('console_token');
  const H={'Authorization':'Bearer '+t,'OperToken':t,'Content-Type':'application/json'};
  const c=await fetch('/console/api/apps/'+DST+'/copy',{method:'POST',headers:H,body:JSON.stringify({})});
  const cj=await c.json();
  if(c.status!==200&&c.status!==201) return 'COPY_FAIL '+c.status;
  const NEW=cj.id;
  const s=await (await fetch('/console/api/apps/'+SRC+'/workflows/draft',{headers:H})).json();
  const nd=await (await fetch('/console/api/apps/'+NEW+'/workflows/draft',{headers:H})).json();
  const r=await fetch('/console/api/apps/'+NEW+'/workflows/draft',{method:'POST',headers:H,
    body:JSON.stringify({graph:s.graph,features:s.features,environment_variables:s.environment_variables||{},
      conversation_variables:s.conversation_variables||[],hash:nd.hash})});
  if(r.status!==200) return 'SAVE_FAIL '+r.status;
  const p=await fetch('/console/api/apps/'+NEW+'/workflows/publish',{method:'POST',headers:H,body:'{}'});
  const pj=await p.json();
  const app=await (await fetch('/console/api/apps/'+NEW,{headers:H})).json();
  return 'NEW_ID='+NEW+'\nSITE_CODE='+app.site.code+'\nWF='+(pj.workflow_id||pj.id);
})()
