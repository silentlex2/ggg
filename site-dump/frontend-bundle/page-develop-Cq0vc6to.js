import{a as h,j as e,r as A,u as v,a4 as R}from"./framework-BEpUYYOL.js";import{ad as b,ae as C,af as M,ag as f,ah as k,t as B,j as E,ai as U,a as z,aj as L}from"./index-xH1_rf.js";import"./vendor-B9l90QxW.js";import{a as w,s as x,S as I}from"./button-Dg0PWVPl.js";import{P as O,a as G,J as u}from"./index-6S1gRNBn.js";import{t as H,a as N}from"./third-party-template-data-zh-B_QGdLXU.js";import"./agora-rtc-sdk-ng-BBXtXa5O.js";import"./echarts-BnmgLYUC.js";import"./katex-Cuu8o0Tm.js";import"./highlight-D7dQlGy7.js";const D=({template:t,mcpBaseUrl:a})=>{const{t:o}=h(),s=i=>{if(!i)return i;if(/\n-\s/.test(i)){const r=[],c=i.split(`
`);let p=[],_=!1;for(const m of c)m.trim().startsWith("- ")?(_||(p.length>0&&(r.push({type:"text",content:p.join(`
`)}),p=[]),_=!0),p.push(m.trim().substring(2))):(_&&(p.length>0&&(r.push({type:"list",content:p}),p=[]),_=!1),p.push(m));return p.length>0&&r.push(_?{type:"list",content:p}:{type:"text",content:p.join(`
`)}),e.jsx("span",{children:r.map((m,q)=>{if(m.type==="list"&&Array.isArray(m.content))return e.jsx("ul",{style:{marginTop:"6px",marginBottom:"6px",paddingLeft:"20px",listStyle:"disc"},children:m.content.map((j,P)=>{const S=j.replace(/`([^`]+)`/g,'<code class="inline-code">$1</code>').replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/\*([^*]+)\*/g,"<em>$1</em>").replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">$1</a>');return e.jsx("li",{dangerouslySetInnerHTML:{__html:S}},P)})},q);const T=(typeof m.content=="string"?m.content:m.content.join(`
`)).replace(/\n/g,"<br/>").replace(/`([^`]+)`/g,'<code class="inline-code">$1</code>').replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/\*([^*]+)\*/g,"<em>$1</em>").replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">$1</a>');return e.jsx("span",{dangerouslySetInnerHTML:{__html:T}},q)})})}const n=i.replace(/\n/g,"<br/>").replace(/`([^`]+)`/g,'<code class="inline-code">$1</code>').replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/\*([^*]+)\*/g,"<em>$1</em>").replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline">$1</a>');return e.jsx("span",{dangerouslySetInnerHTML:{__html:n}})},d=(i,n=0)=>e.jsx("ul",{style:{marginLeft:`${n*20}px`,marginTop:n===0?"6px":"4px",marginBottom:"0",paddingLeft:"20px",listStyle:"disc"},children:i.map((r,c)=>e.jsxs("li",{style:{marginBottom:"4px"},children:[e.jsx("code",{className:"inline-code",children:r.name})," (",r.type,")"," ",s(r.description),r.default&&e.jsxs("span",{children:[" ",t.labels.default,":"," ",e.jsx("code",{className:"inline-code",children:r.default})]}),r.children&&d(r.children,n+1)]},c))}),l=i=>i.map((n,r)=>e.jsxs(G,{name:n.name,type:n.type,required:n.required||!1,anchor:!1,children:[s(n.description),n.default&&e.jsxs("div",{children:[t.labels.default," ",e.jsx("code",{className:"inline-code",children:n.default})]}),n.options&&e.jsxs("div",{children:[t.labels.options,"：",n.options.map((c,p)=>e.jsxs("span",{children:[e.jsx("code",{className:"inline-code",children:c}),p<n.options.length-1?", ":""]},p))]}),n.children&&e.jsx("div",{style:{marginTop:"8px"},children:d(n.children,0)})]},r)),g=i=>!i||i.length===0?null:e.jsx(e.Fragment,{children:i.map((n,r)=>e.jsxs("div",{style:{marginBottom:r<i.length-1?"20px":"0"},children:[e.jsx("h3",{children:n.title}),e.jsx(b,{title:n.language.toUpperCase(),targetCode:n.code,children:e.jsx("pre",{children:e.jsx("code",{children:n.code})})})]},r))}),y=({endpoint:i})=>{const[n,r]=A.useState(!1);return e.jsxs("div",{children:[e.jsx("h2",{className:"mt-2 scroll-mt-32",children:i.title}),e.jsx("div",{children:s(i.description)}),i.requestBody&&i.requestBody.length>0&&e.jsxs(e.Fragment,{children:[e.jsx("h3",{children:t.labels.requestBody}),e.jsx(O,{anchor:!1,children:l(i.requestBody)})]}),i.codeExamples&&i.codeExamples.length>0&&e.jsx("div",{style:{marginTop:"16px"},children:g(i.codeExamples)}),i.documentation&&e.jsxs("div",{style:{marginTop:"20px"},children:[e.jsxs("div",{onClick:()=>r(!n),style:{cursor:"pointer",display:"flex",alignItems:"center",padding:"12px 16px",background:"#f5f5f5",borderRadius:"4px",border:"1px solid #d9d9d9",transition:"all 0.3s"},onMouseEnter:c=>{c.currentTarget.style.borderColor="#40a9ff",c.currentTarget.style.boxShadow="0 0 0 2px rgba(24, 144, 255, 0.2)"},onMouseLeave:c=>{c.currentTarget.style.borderColor="#d9d9d9",c.currentTarget.style.boxShadow="none"},children:[e.jsx("span",{style:{marginRight:"8px",fontSize:"12px",transition:"transform 0.2s",transform:n?"rotate(90deg)":"rotate(0deg)"},children:e.jsx(C,{})}),e.jsx("h3",{style:{margin:0,fontSize:"16px",fontWeight:500},children:i.documentationTitle||o("ui.apiDocRerender.title")})]}),n&&e.jsx("div",{style:{padding:"16px",background:"#ffffff",borderRadius:"0 0 4px 4px",border:"1px solid #d9d9d9",marginTop:"-1px"},children:e.jsx(M,{content:i.documentation})})]}),e.jsx("hr",{})]},i.id)};return e.jsxs("div",{className:"api-doc-container",children:[e.jsx("style",{children:`
        .api-doc-container .inline-code {
          background-color: rgba(175, 184, 193, 0.2);
          padding: 0.125rem 0.25rem;
          border-radius: 0.25rem;
          font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
          font-size: 0.875em;
          color: black;
        }
        .api-doc-container a {
          color: #10b981 !important;
          text-decoration: none;
        }
        .api-doc-container a:hover {
          color: #059669 !important;
          text-decoration: underline;
        }
      `}),e.jsx("h1",{children:t.title}),t.description&&e.jsx("div",{children:s(t.description)}),(a||t.baseUrl)&&e.jsxs("div",{children:[e.jsx("h3",{children:t.labels.baseUrl}),e.jsx(b,{title:"URL",targetCode:a||t.baseUrl,children:e.jsx("pre",{children:e.jsx("code",{children:a||t.baseUrl})})})]}),e.jsxs("div",{children:[e.jsx("h3",{children:t.labels.authentication}),e.jsx("div",{children:s(t.authentication.description)}),e.jsx(b,{title:"Code",children:e.jsx("pre",{children:e.jsx("code",{children:t.authentication.example})})})]}),e.jsx("hr",{}),t.endpoints.map((i,n)=>e.jsx(y,{endpoint:i},i.id??n)),t.errorTable&&t.errorTable.length>0&&e.jsxs(e.Fragment,{children:[e.jsxs("table",{className:"max-w-auto border-collapse border border-slate-400",style:{maxWidth:"none",width:"auto"},children:[e.jsx("thead",{style:{background:"#f9fafc"},children:e.jsxs("tr",{children:[e.jsx("th",{className:"p-2 border border-slate-300",children:t.labels.errorTableCode}),t.labels.errorTableStatus&&e.jsx("th",{className:"p-2 border border-slate-300",children:t.labels.errorTableStatus}),e.jsx("th",{className:"p-2 border border-slate-300",children:t.labels.errorTableMessage})]})}),e.jsx("tbody",{children:t.errorTable.map((i,n)=>e.jsxs("tr",{children:[e.jsx("td",{className:"p-2 border border-slate-300",children:i.code}),t.labels.errorTableStatus&&e.jsx("td",{className:"p-2 border border-slate-300",children:i.status}),e.jsx("td",{className:"p-2 border border-slate-300",children:i.message})]},n))})]}),e.jsx("div",{className:"pb-4"})]})]})},W={title:"工作流编排对话型应用 API",description:"对话应用支持会话持久化，可将之前的聊天记录作为上下进行回答，可适用于聊天/客服 AI 等。",baseUrl:"{{appDetail.api_base_url}}",authentication:{type:"Bearer Token",description:"Service API 使用 `API-Key` 进行鉴权。**強烈建议开发者把 `API-Key` 放在后端存储，而非分享或者放在客户端存储，以免 `API-Key` 泄露，导致财产损失。** 所有 API 请求都应在 **`Authorization`** HTTP Header 中包含您的 `API-Key`，如下所示：",example:"Authorization: Bearer {API_KEY}"},labels:{baseUrl:"基础 URL",authentication:"鉴权",pathParams:"Path Params",queryParams:"Query",requestBody:"Request Body",response:"Response",errors:"Errors",requestExample:"Request Example",default:"默认",options:"可选值",streamingStructureDiffers:"流式块中根据 event 不同，结构也不同：",errorInformation:"错误信息",errorCodeReturned:"返回的错误代码",errorStatusReturned:"返回的错误状态",errorMessageReturned:"返回的错误消息",errorTableCode:"code",errorTableStatus:"status",errorTableMessage:"message",interfaceDefinition:"接口定义",path:"Path",method:"Method",contentType:"Content-Type",authorization:"Authorization",basicInfo:"基础信息"},endpoints:[{id:"Create-Chat-Message",url:"/chat-messages",method:"POST",title:"发送对话消息",description:"创建会话消息。",requestBody:[{name:"query",type:"string",required:!0,description:"用户输入/提问内容。"},{name:"input_data",type:"object",required:!1,description:"允許传入 App 定义的各变量值。input_data 参数包含了多组键值对（Key/Value pairs），每组的键对应一个特定变量，每组的值则是该变量的具体值。默认 `{}`"},{name:"mode",type:"string",required:!0,description:"- `streaming` 流式模式（推荐）。基于 SSE（**[Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)**）实现类似打字机输出方式的流式返回。\n- `blocking` 阻塞模式，等待执行完毕后返回结果。（请求若流程较长可能会被中断）。\n*由于 Cloudflare 限制，请求会在 100 秒超时无返回后中断。*"},{name:"user",type:"string",required:!0,description:"用户标识，用于定义终端用户的身份，方便检索、统计。由开发者定义规则，需保证用户标识在应用内唯一。"},{name:"conversation_id",type:"string",required:!1,description:"（选填）会话 ID，需要基于之前的聊天记录继续对话，必须传之前消息的 conversation_id。"},{name:"files",type:"array[object]",required:!1,description:"文件列表，适用于传入文件结合文本理解并回答问题，仅当模型支持 Vision 能力时可用。",children:[{name:"type",type:"string",description:"支持类型：",children:[{name:"document",type:"string",description:"具体类型包含：'TXT', 'MD', 'MARKDOWN', 'PDF', 'XLSX', 'XLS', 'DOC', 'DOCX', 'WPS', 'WPT', 'ET', 'ETT', 'CSV', 'EML', 'MSG', 'PPTX', 'PPT', 'XML', 'EPUB'"},{name:"image",type:"string",description:"具体类型包含：'JPG', 'JPEG', 'PNG', 'GIF', 'WEBP', 'SVG'"},{name:"audio",type:"string",description:"具体类型包含：'MP3', 'M4A', 'WAV'"},{name:"video",type:"string",description:"具体类型包含：'MP4', 'WEBM'"}]},{name:"transfer_method",type:"string",description:"传递方式:",children:[{name:"remote_url",type:"string",description:"图片地址。"},{name:"local_file",type:"string",description:"上传文件。"}]},{name:"url",type:"string",required:!1,description:"图片地址。（仅当传递方式为 `remote_url` 时）。"},{name:"upload_file_id",type:"string",required:!1,description:"上传文件 ID。（仅当传递方式为 `local_file` 时）。"}]},{name:"is_name_auto",type:"bool",required:!1,description:"（选填）自动生成标题，默认 `true`。若设置为 `false`，则可通通过调用会话重命名接口并设置 `auto_generate` 为 `true` 实现异步生成标题。"}],responseSection:{generalDescription:"当 `response_mode` 为 `blocking` 时，返回 ChatCompletionResponse object。当 `response_mode` 为 `streaming`时，返回 ChunkChatCompletionResponse object 流式序列。",responseTypes:[{title:"ChatCompletionResponse",description:"返回完整的 App 结果，`Content-Type` 为 `application/json`。",fields:[{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"mode",type:"string",description:"App 模式，固定为 chat"},{name:"answer",type:"string",description:"完整回复内容"},{name:"metadata",type:"object",description:"元数据",children:[{name:"usage",type:"Usage",description:"模型用量信息"},{name:"retriever_resources",type:"array[RetrieverResource]",description:"引用和归属分段列表"}]},{name:"created_at",type:"int",description:"消息创建时间戳，如：1705395332"}]},{title:"ChunkChatCompletionResponse",description:"返回 App 输出的流式块，`Content-Type` 为 `text/event-stream`。每个流式块均为 data: 开头，块之间以 \\n\\n 即两个换行符分隔，如下所示：",events:[{name:"event: message",description:"LLM 返回文本块事件，即：完整的文本以分块的方式输出。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"answer",type:"string",description:"LLM 返回文本块内容"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: message_file",description:"文件事件，表示有新文件需要展示",fields:[{name:"id",type:"string",description:"文件唯一ID"},{name:"type",type:"string",description:"文件类型，目前仅为image"},{name:"belongs_to",type:"string",description:"文件归属，user或assistant，该接口返回仅为 `assistant`"},{name:"url",type:"string",description:"文件访问地址"},{name:"conversation_id",type:"string",description:"会话ID"}]},{name:"event: message_end",description:"消息结束事件，收到此事件则代表流式返回结束。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"metadata",type:"object",description:"元数据",children:[{name:"usage",type:"Usage",description:"模型用量信息"},{name:"retriever_resources",type:"array[RetrieverResource]",description:"引用和归属分段列表"}]}]},{name:"event: tts_message",description:"TTS 音频流事件，即：语音合成输出。内容是Mp3格式的音频块，使用 base64 编码后的字符串，播放的时候直接解码即可。(开启自动播放才有此消息)",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"audio",type:"string",description:"语音合成之后的音频块使用 Base64 编码之后的文本内容，播放的时候直接 base64 解码送入播放器即可"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: tts_message_end",description:"TTS 音频流结束事件，收到这个事件表示音频流返回结束。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"audio",type:"string",description:"结束事件是没有音频的，所以这里是空字符串"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: message_replace",description:"消息内容替换事件。开启内容审查和审查输出内容时，若命中了审查条件，则会通过此事件替换消息内容为预设回复。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"answer",type:"string",description:"替换内容（直接替换 LLM 所有回复文本）"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: workflow_started",description:"workflow 开始执行",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"event",type:"string",description:"固定为 `workflow_started`"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"workflow 执行 ID"},{name:"workflow_id",type:"string",description:"关联 Workflow ID"},{name:"sequence_number",type:"int",description:"自增序号，App 内自增，从 1 开始"},{name:"created_at",type:"timestamp",description:"开始时间"}]}]},{name:"event: node_started",description:"node 开始执行",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"event",type:"string",description:"固定为 `node_started`"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"workflow 执行 ID"},{name:"node_id",type:"string",description:"节点 ID"},{name:"node_type",type:"string",description:"节点类型"},{name:"title",type:"string",description:"节点名称"},{name:"index",type:"int",description:"执行序号，用于展示 Tracing Node 顺序"},{name:"predecessor_node_id",type:"string",description:"前置节点 ID，用于画布展示执行路径"},{name:"inputs",type:"array[object]",description:"节点中所有使用到的前置节点变量内容"},{name:"created_at",type:"timestamp",description:"开始时间"}]}]},{name:"event: node_finished",description:"node 执行结束，成功失败同一事件中不同状态",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"event",type:"string",description:"固定为 `node_finished`"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"node 执行 ID"},{name:"node_id",type:"string",description:"节点 ID"},{name:"index",type:"int",description:"执行序号，用于展示 Tracing Node 顺序"},{name:"predecessor_node_id",type:"string",description:"optional 前置节点 ID，用于画布展示执行路径"},{name:"inputs",type:"array[object]",description:"节点中所有使用到的前置节点变量内容"},{name:"process_data",type:"json",description:"Optional 节点过程数据"},{name:"outputs",type:"json",description:"Optional 输出内容"},{name:"status",type:"string",description:"执行状态 `running` / `succeeded` / `failed` / `stopped`"},{name:"error",type:"string",description:"Optional 错误原因"},{name:"elapsed_time",type:"float",description:"Optional 耗时(s)"},{name:"execution_metadata",type:"json",description:"元数据",children:[{name:"total_tokens",type:"int",description:"optional 总使用 tokens"},{name:"total_price",type:"decimal",description:"optional 总费用"},{name:"currency",type:"string",description:"optional 货币，如 `USD` / `RMB`"}]},{name:"created_at",type:"timestamp",description:"开始时间"}]}]},{name:"event: workflow_finished",description:"workflow 执行结束，成功失败同一事件中不同状态",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"event",type:"string",description:"固定为 `workflow_finished`"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"workflow 执行 ID"},{name:"workflow_id",type:"string",description:"关联 Workflow ID"},{name:"status",type:"string",description:"执行状态 `running` / `succeeded` / `failed` / `stopped`"},{name:"outputs",type:"json",description:"Optional 输出内容"},{name:"error",type:"string",description:"Optional 错误原因"},{name:"elapsed_time",type:"float",description:"Optional 耗时(s)"},{name:"total_tokens",type:"int",description:"Optional 总使用 tokens"},{name:"total_steps",type:"int",description:"总步数（冗余），默认 0"},{name:"created_at",type:"timestamp",description:"开始时间"},{name:"finished_at",type:"timestamp",description:"结束时间"}]}]},{name:"event: error",description:"流式输出过程中出现的异常会以 stream event 形式输出，收到异常事件后即结束。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"status",type:"int",description:"HTTP 状态码"},{name:"code",type:"string",description:"错误码"},{name:"message",type:"string",description:"错误消息"}]},{name:"event: ping",description:"每 10s 一次的 ping 事件，保持连接存活。",fields:[]}]}],streamingExample:{language:"streaming",title:"Response",code:'data: {"event": "message", "task_id": "aa321d77-dd8a-469b-a176-7791e44dfa1e", "id": "403f4621-5332-4fb2-85a1-a36ecac331cf", "answer": "你好", "created_at": 1705398420}\\n\\n'}},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/chat-messages' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "input_data": {{inputs}},
    "query": "请介绍下华为手机",
    "conversation_id": "",
    "mode": "streaming",
    "user": "admin",
    "files": [
      {
        "type": "image",
        "transfer_method": "remote_url",
        "url": "http://cloud.itbg2.ffcs.cn:20361/logo/logo-site.png"
      }
    ]
}'`},{language:"json",title:"阻塞模式",code:`{
    "event": "message",
    "message_id": "26b1a6b9-f297-4c21-9135-c8606d982a10",
    "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2",
    "mode": "chat",
    "answer": "华为手机的规格参数如下...",
    "metadata": {
        "usage": {
            "prompt_tokens": 1233,
            "prompt_unit_price": "0.001",
            "prompt_price_unit": "0.001",
            "prompt_price": "0.0010330",
            "completion_tokens": 124,
            "completion_unit_price": "0.002",
            "completion_price_unit": "0.001",
            "completion_price": "0.0002560",
            "total_tokens": 1161,
            "total_price": "0.0012890",
            "currency": "USD",
            "latency": 0.7682376249867957
        },
        "retriever_resources": [
            {
                "position": 1,
                "dataset_id": "7f7f7e1a-802e-4d52-9088-c8e9eeb5da0d",
                "dataset_name": "iPhone",
                "document_id": "1fd346d3-b7cf-42b7-9dd0-b284d64d648f",
                "document_name": "iPhone List",
                "segment_id": "43f1966e-d048-4830-bbf7-7fe744e4abee",
                "score": 0.98457545,
                "content": "Model,Release Date,Display Size,Resolution,Processor,RAM,Storage,Camera,Battery,Operating System华为mate,September 24, 2021,6.7 inch,1284 x 2778,Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard),8 GB,128, 256, 512 GB, 1TB,12 MP,4000 mAh,安卓"
            }
        ]
    },
    "created_at": 1705407629
}`},{language:"streaming",title:"流式模式",code:`data: {"event": "workflow_started", "task_id": "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "workflow_id": "dfjasklfjdslag", "sequence_number": 1, "created_at": 1679586595}}
data: {"event": "node_started", "task_id": "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "node_id": "dfjasklfjdslag", "node_type": "start", "title": "Start", "index": 0, "predecessor_node_id": "fdljewklfklgejlglsd", "inputs": {}, "created_at": 1679586595}}
data: {"event": "node_finished", "task_id": "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "node_id": "dfjasklfjdslag", "node_type": "start", "title": "Start", "index": 0, "predecessor_node_id": "fdljewklfklgejlglsd", "inputs": {}, "outputs": {}, "status": "succeeded", "elapsed_time": 0.324, "execution_metadata": {"total_tokens": 63127864, "total_price": 2.378, "currency": "USD"},  "created_at": 1679586595}}
data: {"event": "workflow_finished", "task_id": "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "workflow_id": "dfjasklfjdslag", "outputs": {}, "status": "succeeded", "elapsed_time": 0.324, "total_tokens": 63127864, "total_steps": "1", "created_at": 1679586595, "finished_at": 1679976595}}
data: {"event": "message", "message_id": "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " I", "created_at": 1679586595}
data: {"event": "message", "message_id": "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": "'m", "created_at": 1679586595}
data: {"event": "message", "message_id": "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " glad", "created_at": 1679586595}
data: {"event": "message", "message_id": "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " to", "created_at": 1679586595}
data: {"event": "message", "message_id": : "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " meet", "created_at": 1679586595}
data: {"event": "message", "message_id": : "cd1cacc1-6718-424f-a1e8-45dbfb16b424", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " you", "created_at": 1679586595}
data: {"event": "message_end", "id": "5e52ce04-874b-4d27-9045-b3bc80def685", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "metadata": {"usage": {"prompt_tokens": 1033, "prompt_unit_price": "0.001", "prompt_price_unit": "0.001", "prompt_price": "0.0010330", "completion_tokens": 135, "completion_unit_price": "0.002", "completion_price_unit": "0.001", "completion_price": "0.0002700", "total_tokens": 1168, "total_price": "0.0013030", "currency": "USD", "latency": 1.381760165997548}, "retriever_resources": [{"position": 1, "dataset_id": "047f8df7-6e51-49c0-9a4a-658e2cdc7b49", "dataset_name": "iPhone", "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00", "document_name": "huawei Mate", "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a", "score": 0.98457545, "content": "Model,Release Date,Display Size,Resolution,Processor,RAM,Storage,Camera,Battery,Operating System iPhone 13 Pro Max,September 24, 2021,6.7 inch,1284 x 2778,Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard),6 GB,128, 256, 512 GB, 1TB,12 MP,4352 mAh,安卓"}]}}
data: {"event": "tts_message", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"}
data: {"event": "tts_message_end", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": ""}`}],errors:[{code:404,description:"对话不存在"},{code:400,description:"`invalid_param`，传入参数异常"},{code:400,description:"`app_unavailable`，App 配置不可用"},{code:400,description:"`provider_not_initialize`，无可用模型凭据配置"},{code:400,description:"`provider_quota_exceeded`，模型调用额度不足"},{code:400,description:"`model_currently_not_support`，当前模型不可用"},{code:400,description:"`completion_request_error`，文本生成失败"},{code:500,description:"服务内部异常"}]},{id:"files-upload",url:"/files/upload",method:"POST",title:"上传文件",description:"上传文件（目前仅支持图片）并在发送消息时使用，可实现圖文多模态理解。支持 jpg, jpeg, png, webp, gif, svg 格式。上传的文件仅供当前终端用户使用。",requestBody:[{name:"file",type:"file",required:!0,description:"要上传的文件。"},{name:"user",type:"string",required:!0,description:"用户标识，用于定义终端用户的身份，必须和发送消息接口传入 user 保持一致。"}],responseSection:{responseTypes:[{title:"UploadResponse",description:"成功上传后，服务器会返回文件的 ID 和相关信息。",fields:[{name:"id",type:"uuid",description:"ID"},{name:"name",type:"string",description:"文件名"},{name:"size",type:"int",description:"文件大小（byte）"},{name:"extension",type:"string",description:"文件后綴"},{name:"mime_type",type:"string",description:"文件 mime-type"},{name:"created_by",type:"uuid",description:"上传人 ID"},{name:"created_at",type:"timestamp",description:"上传时間"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/files/upload' \\
--header 'Authorization: Bearer {api_key}' \\
--form 'file=@"/path/to/file"'`},{language:"json",title:"Response",code:`{
  "id": "ae975f34-0e94-4c27-a7ba-f65efaf68480",
  "name": "example.png",
  "size": 1024,
  "extension": "png",
  "mime_type": "image/png",
  "created_by": 9889,
  "created_at": 1577836800
}`}],errors:[{code:400,description:"`no_file_uploaded`，必须提供文件"},{code:400,description:"`too_many_files`，目前只接受一个文件"},{code:400,description:"`unsupported_preview`，该文件不支持预览"},{code:400,description:"`unsupported_estimate`，该文件不支持估算"},{code:413,description:"`file_too_large`，文件太大"},{code:415,description:"`unsupported_file_type`，不支持的扩展名，当前只接受文文類文件"},{code:503,description:"`s3_connection_failed`，无法连接到 S3 服务"},{code:503,description:"`s3_permission_denied`，无权限上传文件到 S3"},{code:503,description:"`s3_file_too_large`，文件超出 S3 大小限制"}]},{id:"Stop",url:"/chat-messages/:task_id/stop",method:"POST",title:"停止响应",description:"仅支持流式模式。",pathParams:[{name:"task_id",type:"string",required:!0,description:"任务 ID，可在流式返回 Chunk 中获取"}],requestBody:[{name:"user",type:"string",required:!0,description:"用户标识，用于定义终端用户的身份，必须和发送消息接口传入 user 保持一致。"}],responseSection:{responseTypes:[{title:"StopResponse",description:"停止响应结果",fields:[{name:"result",type:"string",description:"固定返回 success"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/chat-messages/:task_id/stop' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json' \\
--data-raw '{ "user": "admin"}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"feedbacks",url:"/messages/:message_id/feedbacks",method:"POST",title:"消息反馈（点赞）",description:"消息终端用户反馈、点赞，方便应用开发者优化输出预期。",pathParams:[{name:"message_id",type:"string",required:!0,description:"消息 ID"}],requestBody:[{name:"rating",type:"string",required:!0,description:"点赞 like, 点踩 dislike, 撤销点赞 null"},{name:"label",type:"string",required:!1,description:'label:点踩标签选项，仅当反馈为"点踩"时填入；可选标签：答非所问,有害/不安全,虛假信息,逻辑问题,格式问题,沒有帮助'},{name:"content",type:"string",required:!1,description:'content:点踩原因自定义说明，仅当反馈为"点踩"时填入；'},{name:"user",type:"string",required:!0,description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"}],responseSection:{responseTypes:[{title:"FeedbackResponse",description:"反馈结果",fields:[{name:"result",type:"string",description:"固定返回 success"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/messages/:message_id/feedbacks' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "rating": "dislike",
    "label": "点踩选项1",
    "content": "点踩自定义说明",
    "user": "admin"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"suggested",url:"/messages/{message_id}/suggested",method:"GET",title:"获取下一轮建议问题列表",description:"获取下一轮建议问题列表。",pathParams:[{name:"message_id",type:"string",required:!0,description:"Message ID"}],queryParams:[{name:"user",type:"string",required:!0,description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"}],responseSection:{responseTypes:[{title:"SuggestedResponse",description:"建议问题列表",fields:[{name:"result",type:"string",description:"固定返回 success"},{name:"data",type:"array[string]",description:"建议问题列表"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl --location --request GET '{{appDetail.api_base_url}}/messages/{message_id}/suggested?user=admin' \\
--header 'Authorization: Bearer ENTER-YOUR-SECRET-KEY' \\
--header 'Content-Type: application/json'`},{language:"json",title:"Response",code:`{
  "result": "success",
  "data": [
    "需要我做什么？",
    "可以帮个忙吗？",
    "您好有什么事吗？"
  ]
}`}]},{id:"messages",url:"/messages",method:"GET",title:"获取会话历史消息",description:"滚动加载形式返回历史聊天记录，第一页返回最新 `limit` 条，即：倒序返回。",queryParams:[{name:"conversation_id",type:"string",required:!0,description:"会话 ID"},{name:"user",type:"string",required:!0,description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"},{name:"lead_id",type:"string",required:!1,description:"当前页第一条聊天记录的 ID，默认 null"},{name:"limit",type:"int",required:!1,description:"一次请求返回多少条聊天记录，默认 20 条。"}],responseSection:{responseTypes:[{title:"MessagesResponse",description:"",fields:[{name:"data",type:"array[object]",description:"消息列表",children:[{name:"id",type:"string",description:"消息 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"inputs",type:"array[object]",description:"用户输入参数。"},{name:"query",type:"string",description:"用户输入 / 提问内容。"},{name:"message_files",type:"array[object]",description:"消息文件",children:[{name:"id",type:"string",description:"ID"},{name:"type",type:"string",description:"文件类型，image 图片"},{name:"url",type:"string",description:"预览图片地址"},{name:"belongs_to",type:"string",description:"文件归属方，user 或 assistant"}]},{name:"answer",type:"string",description:"回答消息内容"},{name:"created_at",type:"timestamp",description:"创建时间"},{name:"feedback",type:"object",description:"反馈信息",children:[{name:"rating",type:"string",description:"点赞 like / 点踩 dislike"}]},{name:"retriever_resources",type:"array[RetrieverResource]",description:"引用和归属分段列表"}]},{name:"has_more",type:"bool",description:"是否存在下一页"},{name:"limit",type:"int",description:"返回条数，若传入超过系统限制，返回系统限制数量"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/messages?user=admin&conversation_id=' \\
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response Example",code:`{
  "limit": 20,
  "has_more": false,
  "data": [
    {
      "id": "9ba7d8ff-a3ba-4157-8f8b-23053edfe26a",
      "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2",
      "inputs": {
        "name": "test"
      },
      "query": "本田汽車",
      "answer": "动力性能：搭载 1.5T 渦轮增壓發动机或 2.0L 混合动力系統，1.5T 發动机最大功率 194 马力，峰值扭矩 260 牛・米；2.0L 混动版综合功率 215 马力，峰值扭矩 315 牛・米",
      "message_files": [],
      "feedback": null,
      "retriever_resources": [
        {
          "position": 1,
          "dataset_id": "9faeba48-b5ef-42ec-8d2c-4bf4e54616de",
          "dataset_name": "本田汽車",
          "document_id": "8dd1ad7s4-0b5f-4175-b735-7d98dbbbb4e00",
          "document_name": "本田汽車",
          "segment_id": "ed599c7f-276d6-42s94-9d1d-e5s235a61270a",
          "score": 0.98457545,
          "content": "本田汽車的动力性能如下：\\n- 搭载 1.5T 渦轮增壓發动机或 2.0L 混合动力系統\\n- 1.5T 發动机最大功率 194 马力，峰值扭矩 260 牛・米\\n- 2.0L 混动版综合功率 215 马力，峰值扭矩 315 牛・米"
        }
      ],
      "created_at": 1705569239
    }
  ]
}`},{language:"json",title:"Response Example(智能助手)",code:`{
  "limit": 20,
  "has_more": false,
  "data": [
    {
      "id": "3787ef62-5f25-4f4c-bf72-2b372df841ff",
      "conversation_id": "9faeba48-b5ef-42ec-8d2c-4bf4e54616de",
      "inputs": {},
      "query": "draw a cat",
      "answer": "I have generated an image of a cat for you. Please check your messages to view the image.",
      "message_files": [
        {
          "id": "1ef98033-44d6-4f52-9d6b-a8b0b39b31b6",
          "type": "image",
          "url": "http://127.0.0.1:5001/files/tools/976990d2-5294-47e6-8f14-7356ba9d2d76.png?timestamp=1705988524&nonce=55df3f9f7311a9acd91bf074cd524092&sign=z43nMSO1L2HBvoqADLkRxr7Biz0fkjeDstnJiCK1zh8=",
          "belongs_to": "assistant"
        }
      ],
      "feedback": null,
      "retriever_resources": [],
      "created_at": 1705988187
    }
  ]
}`}]},{id:"conversations",url:"/conversations",method:"GET",title:"获取会话列表",description:"获取当前用户的会话列表，默认返回最近的 20 条。",queryParams:[{name:"user",type:"string",required:!0,description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"},{name:"tail_id",type:"string",required:!1,description:"当前页最后面一条记录的 ID，默认 null"},{name:"limit",type:"int",required:!1,description:"一次请求返回多少条记录"},{name:"pinned",type:"bool",required:!1,description:"只返回置顶 true，只返回非置顶 false"}],responseSection:{responseTypes:[{title:"ConversationsResponse",description:"",fields:[{name:"data",type:"array[object]",description:"会话列表",children:[{name:"id",type:"string",description:"会话 ID"},{name:"name",type:"string",description:"会话名称，默认由大语言模型生成。"},{name:"inputs",type:"array[object]",description:"用户输入参数。"},{name:"introduction",type:"string",description:"开场白"},{name:"created_at",type:"timestamp",description:"创建时间"}]},{name:"has_more",type:"bool",description:""},{name:"limit",type:"int",description:"返回条数，若传入超过系统限制，返回系统限制数量"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/conversations?user=admin&tail_id=&limit=20' \\
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
  "limit": 20,
  "has_more": false,
  "data": [
    {
      "id": "1ef98033-44d6-4f52-9d6b-a8b0b39b31b6b",
      "name": "New chat",
      "inputs": {
        "book": "book",
        "myName": "Lucy"
      },
      "status": "normal",
      "created_at": 1679667915
    },
    {
      "id": "hSIhXBhNe8X1d8Et"
    }
  ]
}`}]},{id:"delete",url:"/conversations/:conversation_id",method:"DELETE",title:"删除会话",description:"删除会话。",pathParams:[{name:"conversation_id",type:"string",required:!0,description:"会话 ID"}],requestBody:[{name:"user",type:"string",required:!0,description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"}],responseSection:{responseTypes:[{title:"DeleteResponse",description:"删除结果",fields:[{name:"result",type:"string",description:"固定返回 success"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X DELETE '{{appDetail.api_base_url}}/conversations/{conversation_id}' \\
--header 'Content-Type: application/json' \\
--header 'Accept: application/json' \\
--header 'Authorization: Bearer {api_key}' \\
--data '{
    "user": "admin"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"rename",url:"/conversations/:conversation_id/name",method:"POST",title:"会话重命名",description:"对会话进行重命名，会话名称用于显示在支持多会话的客户端上。",requestBody:[{name:"conversation_name",type:"string",required:!1,description:"名称，若 `auto_generate` 为 `true` 时，该参数可不传。"},{name:"auto_generate",type:"string",required:!1,description:"自动生成标题，默认 false。",default:"false"},{name:"user",type:"string",required:!0,description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"}],responseSection:{responseTypes:[{title:"RenameResponse",description:"重命名结果",fields:[{name:"id",type:"string",description:"会话 ID"},{name:"name",type:"string",description:"会话名称"},{name:"inputs",type:"array[object]",description:"用户输入参数。"},{name:"introduction",type:"string",description:"开场白"},{name:"created_at",type:"timestamp",description:"创建时間"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/conversations/:conversation_id/name' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "conversation_name": "",
    "user": "admin"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"parameters",url:"/parameters",method:"GET",title:"获取应用配置信息",description:"用于进入页面一开始，获取功能开关、输入参数名称、类型及默认值等使用。",queryParams:[{name:"user",type:"string",required:!0,description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"}],responseSection:{responseTypes:[{title:"ParametersResponse",description:"",fields:[{name:"opening_statement",type:"string",description:"开场白"},{name:"suggested_questions",type:"array[string]",description:"开场推荐问题列表"},{name:"suggested_questions_after_answer",type:"object",description:"启用回答后给出推荐问题。",children:[{name:"enabled",type:"bool",description:"是否开启"}]},{name:"speech_to_text",type:"object",description:"语音转文本",children:[{name:"enabled",type:"bool",description:"是否开启"}]},{name:"retriever_resource",type:"object",description:"引用和归属",children:[{name:"enabled",type:"bool",description:"是否开启"}]},{name:"annotation_reply",type:"object",description:"标记回复",children:[{name:"enabled",type:"bool",description:"是否开启"}]},{name:"user_input_form",type:"array[object]",description:"用户输入表单配置",children:[{name:"text-input",type:"object",description:"文本输入控件",children:[{name:"label",type:"string",description:"控件展示标签名"},{name:"variable",type:"string",description:"控件 ID"},{name:"required",type:"bool",description:"是否必填"},{name:"default",type:"string",description:"默认值"}]},{name:"paragraph",type:"object",description:"段落文本输入控件",children:[{name:"label",type:"string",description:"控件展示标签名"},{name:"variable",type:"string",description:"控件 ID"},{name:"required",type:"bool",description:"是否必填"},{name:"default",type:"string",description:"默认值"}]},{name:"select",type:"object",description:"下拉控件",children:[{name:"label",type:"string",description:"控件展示标签名"},{name:"variable",type:"string",description:"控件 ID"},{name:"required",type:"bool",description:"是否必填"},{name:"default",type:"string",description:"默认值"},{name:"options",type:"array[string]",description:"选项值"}]}]},{name:"file_upload",type:"object",description:"文件上传配置",children:[{name:"image",type:"object",description:"图片设置。当前仅支持图片类型：`jpg`, `jpeg`, `png`, `webp`, `gif`, `svg`",children:[{name:"enabled",type:"bool",description:"是否开启"},{name:"number_limits",type:"int",description:"图片数量限制，默认 3"},{name:"transfer_methods",type:"array[string]",description:"传递方式列表，remote_url , local_file，必选一个"}]}]},{name:"system_parameters",type:"object",description:"系统参数",children:[{name:"image_file_size_limit",type:"string",description:"图片文件上传大小限制（MB）"}]}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/parameters?user=admin' \\
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
  "introduction": "nice to meet you",
  "user_input_form": [
    {
      "text-input": {
        "label": "a",
        "variable": "a",
        "required": true,
        "max_length": 48,
        "default": ""
      }
    }
  ],
  "file_upload": {
    "image": {
      "enabled": true,
      "number_limits": 3,
      "transfer_methods": [
        "remote_url",
        "local_file"
      ]
    }
  }
}`}]},{id:"meta",url:"/meta",method:"GET",title:"获取应用Meta信息",description:"用于获取工具icon",queryParams:[{name:"user",type:"string",required:!0,description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"}],responses:[{name:"tool_icons",type:"object[string]",description:"工具图标",children:[{name:"工具名称",type:"string",description:"",children:[{name:"icon",type:"object|string",description:"",children:[{name:"(object)",type:"",description:"图标",children:[{name:"background",type:"string",description:"hex格式的背景色"},{name:"content",type:"string",description:"emoji"}]},{name:"(string)",type:"",description:"图标URL"}]}]}]}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/meta?user=admin' \\
-H 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
  "tool_icons": {
    "dalle2": "http://cloud.itbg2.ffcs.cn:20361/console/api/workspaces/current/tool-provider/builtin/dalle/icon",
    "api_tool": {
      "background": "#252525",
      "content": "😁"
    }
  }
}`}]}]},F={title:"Advanced Chat App API",description:"Chat applications support session persistence, allowing previous chat history to be used as context for responses. This can be applicable for chatbot, customer service AI, etc.",baseUrl:"{{appDetail.api_base_url}}",authentication:{type:"Bearer Token",description:"The Service API uses `API-Key` authentication. **Strongly recommend storing your API Key on the server-side, not shared or stored on the client-side, to avoid possible API-Key leakage that can lead to serious consequences.** For all API requests, include your API Key in the `Authorization`HTTP Header, as shown below:",example:"Authorization: Bearer {API_KEY}"},labels:{baseUrl:"Base URL",authentication:"Authentication",pathParams:"Path Params",queryParams:"Query",requestBody:"Request Body",response:"Response",errors:"Errors",requestExample:"Request Example",default:"Default",options:"Options",streamingStructureDiffers:"The structure of the streaming chunks varies depending on the event:",errorInformation:"Error Information",errorCodeReturned:"Returned error code",errorStatusReturned:"Returned error status",errorMessageReturned:"Returned error message",errorTableCode:"code",errorTableStatus:"status",errorTableMessage:"message",interfaceDefinition:"Interface Definition",path:"Path",method:"Method",contentType:"Content-Type",authorization:"Authorization",basicInfo:"Basic Information"},endpoints:[{id:"Send-Chat-Message",url:"/chat-messages",method:"POST",title:"Send Chat Message",description:"Send a request to the chat application.",requestBody:[{name:"query",type:"string",required:!0,description:"User Input/Question content"},{name:"inputs",type:"object",required:!1,description:"Allows the entry of various variable values defined by the App. The `inputs` parameter contains multiple key/value pairs, with each key corresponding to a specific variable and each value being the specific value for that variable. Default `{}`"},{name:"response_mode",type:"string",required:!0,description:"- `streaming` Streaming mode (recommended), implements a typewriter-like output through SSE (**[Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)**). \n- `blocking` Blocking mode, returns result after execution is complete. (Requests may be interrupted if the process is long)\n*Due to Cloudflare restrictions, the request will be interrupted without a return after 100 seconds.*"},{name:"user",type:"string",required:!0,description:"User identifier, used to define the identity of the end-user for retrieval and statistics. Should be uniquely defined by the developer within the application."},{name:"conversation_id",type:"string",required:!1,description:"Conversation ID, to continue the conversation based on previous chat records, it is necessary to pass the previous message's conversation_id."},{name:"files",type:"array[object]",required:!1,description:"File list, suitable for inputting files (images) combined with text understanding and answering questions, available only when the model supports Vision capability.",children:[{name:"type",type:"string",description:"Supported type:",children:[{name:"image",type:"string",description:"currently only supports image type"}]},{name:"transfer_method",type:"string",description:"Transfer method:",children:[{name:"remote_url",type:"string",description:"for image URL"},{name:"local_file",type:"string",description:"for file upload"}]},{name:"url",type:"string",required:!1,description:"Image URL (when the transfer method is `remote_url`)"},{name:"upload_file_id",type:"string",required:!1,description:"Uploaded file ID, which must be obtained by uploading through the File Upload API in advance (when the transfer method is `local_file`)"}]},{name:"auto_generate_name",type:"bool",required:!1,description:"Auto-generate title, default is `true`. If set to `false`, can achieve async title generation by calling the conversation rename API and setting `auto_generate` to `true`."}],responseSection:{generalDescription:"When response_mode is blocking, return a CompletionResponse object. When response_mode is streaming, return a ChunkCompletionResponse stream.",responseTypes:[{title:"ChatCompletionResponse",description:"Returns the complete App result, `Content-Type` is `application/json`.",fields:[{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"mode",type:"string",description:"App mode, fixed as `chat`"},{name:"answer",type:"string",description:"Complete response content"},{name:"metadata",type:"object",description:"Metadata",children:[{name:"usage",type:"Usage",description:"Model usage information"},{name:"retriever_resources",type:"array[RetrieverResource]",description:"Citation and Attribution List"}]},{name:"created_at",type:"int",description:"Message creation timestamp, e.g., 1705395332"}]},{title:"ChunkChatCompletionResponse",description:"Returns the stream chunks outputted by the App, `Content-Type` is `text/event-stream`. Each streaming chunk starts with `data:`, separated by two newline characters `\\n\\n`, as shown below:",events:[{name:"event: message",description:"LLM returns text chunk event, i.e., the complete text is output in a chunked fashion.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"answer",type:"string",description:"LLM returned text chunk content"},{name:"created_at",type:"int",description:"Creation timestamp, e.g., 1705395332"}]},{name:"event: message_file",description:"Message file event, a new file has created by tool",fields:[{name:"id",type:"string",description:"File unique ID"},{name:"type",type:"string",description:'File type，only allow "image" currently'},{name:"belongs_to",type:"string",description:"Belongs to, it will only be an 'assistant' here"},{name:"url",type:"string",description:"Remote url of file"},{name:"conversation_id",type:"string",description:"Conversation ID"}]},{name:"event: message_end",description:"Message end event, receiving this event means streaming has ended.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"metadata",type:"object",description:"Metadata",children:[{name:"usage",type:"Usage",description:"Model usage information"},{name:"retriever_resources",type:"array[RetrieverResource]",description:"Citation and Attribution List"}]}]},{name:"event: tts_message",description:"TTS audio stream event, that is, speech synthesis output. The content is an audio block in Mp3 format, encoded as a base64 string. When playing, simply decode the base64 and feed it into the player. (This message is available only when auto-play is enabled)",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the stop response interface below"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"audio",type:"string",description:"The audio after speech synthesis, encoded in base64 text content, when playing, simply decode the base64 and feed it into the player"},{name:"created_at",type:"int",description:"Creation timestamp, e.g.: 1705395332"}]},{name:"event: tts_message_end",description:"TTS audio stream end event, receiving this event indicates the end of the audio stream.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the stop response interface below"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"audio",type:"string",description:"The end event has no audio, so this is an empty string"},{name:"created_at",type:"int",description:"Creation timestamp, e.g.: 1705395332"}]},{name:"event: message_replace",description:"Message content replacement event. When output content moderation is enabled, if the content is flagged, then the message content will be replaced with a preset reply through this event.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"answer",type:"string",description:"Replacement content (directly replaces all LLM reply text)"},{name:"created_at",type:"int",description:"Creation timestamp, e.g., 1705395332"}]},{name:"event: workflow_started",description:"workflow starts execution",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"event",type:"string",description:"fixed to `workflow_started`"},{name:"data",type:"object",description:"detail",children:[{name:"id",type:"string",description:"Unique ID of workflow execution"},{name:"workflow_id",type:"string",description:"ID of related workflow"},{name:"sequence_number",type:"int",description:"Self-increasing serial number, self-increasing in the App, starting from 1"},{name:"created_at",type:"timestamp",description:"Creation timestamp, e.g., 1705395332"}]}]},{name:"event: node_started",description:"node execution started",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"event",type:"string",description:"fixed to `node_started`"},{name:"data",type:"object",description:"detail",children:[{name:"id",type:"string",description:"Unique ID of workflow execution"},{name:"node_id",type:"string",description:"ID of node"},{name:"node_type",type:"string",description:"type of node"},{name:"title",type:"string",description:"name of node"},{name:"index",type:"int",description:"Execution sequence number, used to display Tracing Node sequence"},{name:"predecessor_node_id",type:"string",description:"optional Prefix node ID, used for canvas display execution path"},{name:"inputs",type:"array[object]",description:"Contents of all preceding node variables used in the node"},{name:"created_at",type:"timestamp",description:"timestamp of start, e.g., 1705395332"}]}]},{name:"event: node_finished",description:"node execution ends, success or failure in different states in the same event",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"event",type:"string",description:"fixed to `node_finished`"},{name:"data",type:"object",description:"detail",children:[{name:"id",type:"string",description:"Unique ID of workflow execution"},{name:"node_id",type:"string",description:"ID of node"},{name:"node_type",type:"string",description:"type of node"},{name:"title",type:"string",description:"name of node"},{name:"index",type:"int",description:"Execution sequence number, used to display Tracing Node sequence"},{name:"predecessor_node_id",type:"string",description:"optional Prefix node ID, used for canvas display execution path"},{name:"inputs",type:"array[object]",description:"Contents of all preceding node variables used in the node"},{name:"process_data",type:"json",description:"Optional node process data"},{name:"outputs",type:"json",description:"Optional content of output"},{name:"status",type:"string",description:"status of execution, `running` / `succeeded` / `failed` / `stopped`"},{name:"error",type:"string",description:"Optional reason of error"},{name:"elapsed_time",type:"float",description:"Optional total seconds to be used"},{name:"execution_metadata",type:"json",description:"meta data",children:[{name:"total_tokens",type:"int",description:"optional tokens to be used"},{name:"total_price",type:"decimal",description:"optional Total cost"},{name:"currency",type:"string",description:"optional e.g. `USD` / `RMB`"}]},{name:"created_at",type:"timestamp",description:"timestamp of start, e.g., 1705395332"}]}]},{name:"event: workflow_finished",description:"workflow execution ends, success or failure in different states in the same event",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"event",type:"string",description:"fixed to `workflow_finished`"},{name:"data",type:"object",description:"detail",children:[{name:"id",type:"string",description:"ID of workflow execution"},{name:"workflow_id",type:"string",description:"ID of related workflow"},{name:"status",type:"string",description:"status of execution, `running` / `succeeded` / `failed` / `stopped`"},{name:"outputs",type:"json",description:"Optional content of output"},{name:"error",type:"string",description:"Optional reason of error"},{name:"elapsed_time",type:"float",description:"Optional total seconds to be used"},{name:"total_tokens",type:"int",description:"Optional tokens to be used"},{name:"total_steps",type:"int",description:"default 0"},{name:"created_at",type:"timestamp",description:"start time"},{name:"finished_at",type:"timestamp",description:"end time"}]}]},{name:"event: error",description:"Exceptions that occur during the streaming process will be output in the form of stream events, and reception of an error event will end the stream.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"status",type:"int",description:"HTTP status code"},{name:"code",type:"string",description:"Error code"},{name:"message",type:"string",description:"Error message"}]},{name:"event: ping",description:"Ping event every 10 seconds to keep the connection alive.",fields:[]}]}],streamingExample:{language:"streaming",title:"Response",code:'data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\\n\\n'}},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/chat-messages' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "inputs": {{inputs}},
    "query": "What are the specs of the iPhone 13 Pro Max?",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "abc-123",
    "files": [
      {
        "type": "image",
        "transfer_method": "remote_url",
        "url": "https://cloud.ai/logo/logo-site.png"
      }
    ]
}'`},{language:"json",title:"Blocking Mode",code:`{
    "event": "message",
    "message_id": "9da23599-e713-473b-982c-4328d4f5c78a",
    "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2",
    "mode": "chat",
    "answer": "iPhone 13 Pro Max specs are listed here:...",
    "metadata": {
        "usage": {
            "prompt_tokens": 1033,
            "prompt_unit_price": "0.001",
            "prompt_price_unit": "0.001",
            "prompt_price": "0.0010330",
            "completion_tokens": 128,
            "completion_unit_price": "0.002",
            "completion_price_unit": "0.001",
            "completion_price": "0.0002560",
            "total_tokens": 1161,
            "total_price": "0.0012890",
            "currency": "USD",
            "latency": 0.7682376249867957
        },
        "retriever_resources": [
            {
                "position": 1,
                "dataset_id": "101b4c97-fc2e-463c-90b1-5261a4cdcafb",
                "dataset_name": "iPhone",
                "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00",
                "document_name": "iPhone List",
                "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a",
                "score": 0.98457545,
                "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"iPhone 13 Pro Max\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"6 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"12 MP\\",\\"4352 mAh\\",\\"iOS 15\\""
            }
        ]
    },
    "created_at": 1705407629
}`},{language:"streaming",title:"Streaming Mode",code:`data: {"event": "workflow_started", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "workflow_id": "dfjasklfjdslag", "sequence_number": 1, "created_at": 1679586595}}
data: {"event": "node_started", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "node_id": "dfjasklfjdslag", "node_type": "start", "title": "Start", "index": 0, "predecessor_node_id": "fdljewklfklgejlglsd", "inputs": {}, "created_at": 1679586595}}
data: {"event": "node_finished", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "node_id": "dfjasklfjdslag", "node_type": "start", "title": "Start", "index": 0, "predecessor_node_id": "fdljewklfklgejlglsd", "inputs": {}, "outputs": {}, "status": "succeeded", "elapsed_time": 0.324, "execution_metadata": {"total_tokens": 63127864, "total_price": 2.378, "currency": "USD"},  "created_at": 1679586595}}
data: {"event": "workflow_finished", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "workflow_id": "dfjasklfjdslag", "outputs": {}, "status": "succeeded", "elapsed_time": 0.324, "total_tokens": 63127864, "total_steps": "1", "created_at": 1679586595, "finished_at": 1679976595}}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " I", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": "'m", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " glad", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " to", "created_at": 1679586595}
data: {"event": "message", "message_id": : "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " meet", "created_at": 1679586595}
data: {"event": "message", "message_id": : "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " you", "created_at": 1679586595}
data: {"event": "message_end", "id": "5e52ce04-874b-4d27-9045-b3bc80def685", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "metadata": {"usage": {"prompt_tokens": 1033, "prompt_unit_price": "0.001", "prompt_price_unit": "0.001", "prompt_price": "0.0010330", "completion_tokens": 135, "completion_unit_price": "0.002", "completion_price_unit": "0.001", "completion_price": "0.0002700", "total_tokens": 1168, "total_price": "0.0013030", "currency": "USD", "latency": 1.381760165997548}, "retriever_resources": [{"position": 1, "dataset_id": "101b4c97-fc2e-463c-90b1-5261a4cdcafb", "dataset_name": "iPhone", "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00", "document_name": "iPhone List", "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a", "score": 0.98457545, "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"iPhone 13 Pro Max\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"6 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"12 MP\\",\\"4352 mAh\\",\\"iOS 15\\""}]}}
data: {"event": "tts_message", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"}
data: {"event": "tts_message_end", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": ""}`}],errors:[{code:404,description:"Conversation does not exists"},{code:400,description:"`invalid_param`, abnormal parameter input"},{code:400,description:"`app_unavailable`, App configuration unavailable"},{code:400,description:"`provider_not_initialize`, no available model credential configuration"},{code:400,description:"`provider_quota_exceeded`, model invocation quota insufficient"},{code:400,description:"`model_currently_not_support`, current model unavailable"},{code:400,description:"`completion_request_error`, text generation failed"},{code:500,description:"internal server error"}]},{id:"file-upload",url:"/files/upload",method:"POST",title:"File Upload",description:"Upload a file (currently only images are supported) for use when sending messages, enabling multimodal understanding of images and text. Supports png, jpg, jpeg, webp, gif formats. Uploaded files are for use by the current end-user only.",requestBody:[{name:"file",type:"File",required:!0,description:"The file to be uploaded."},{name:"user",type:"string",required:!0,description:"User identifier, defined by the developer's rules, must be unique within the application."}],responseSection:{responseTypes:[{title:"UploadResponse",description:"After a successful upload, the server will return the file's ID and related information.",fields:[{name:"id",type:"uuid",description:"ID"},{name:"name",type:"string",description:"File name"},{name:"size",type:"int",description:"File size (bytes)"},{name:"extension",type:"string",description:"File extension"},{name:"mime_type",type:"string",description:"File mime-type"},{name:"created_by",type:"uuid",description:"End-user ID"},{name:"created_at",type:"timestamp",description:"Creation timestamp, e.g., 1705395332"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/files/upload' \\
--header 'Authorization: Bearer {api_key}' \\
--form 'file=@"/path/to/file"'`},{language:"json",title:"Response",code:`{
  "id": "72fa9618-8f89-4a37-9b33-7e1178a24a67",
  "name": "example.png",
  "size": 1024,
  "extension": "png",
  "mime_type": "image/png",
  "created_by": "6ad1ab0a-73ff-4ac1-b9e4-cdb312f71f13",
  "created_at": 1577836800,
}`}],errors:[{code:400,description:"`no_file_uploaded`, a file must be provided"},{code:400,description:"`too_many_files`, currently only one file is accepted"},{code:400,description:"`unsupported_preview`, the file does not support preview"},{code:400,description:"`unsupported_estimate`, the file does not support estimation"},{code:413,description:"`file_too_large`, the file is too large"},{code:415,description:"`unsupported_file_type`, unsupported extension, currently only document files are accepted"},{code:503,description:"`s3_connection_failed`, unable to connect to S3 service"},{code:503,description:"`s3_permission_denied`, no permission to upload files to S3"},{code:503,description:"`s3_file_too_large`, file exceeds S3 size limit"},{code:500,description:"internal server error"}]},{id:"stop-generatebacks",url:"/chat-messages/:task_id/stop",method:"POST",title:"Stop Generate",description:"Only supported in streaming mode.",pathParams:[{name:"task_id",type:"string",required:!0,description:"Task ID, can be obtained from the streaming chunk return"}],requestBody:[{name:"user",type:"string",required:!0,description:"User identifier, used to define the identity of the end-user, must be consistent with the user passed in the send message interface."}],responseSection:{responseTypes:[{title:"StopResponse",description:"Stop response result",fields:[{name:"result",type:"string",description:'Always returns "success"'}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/chat-messages/:task_id/stop' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json' \\
--data-raw '{
    "user": "abc-123"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"feedbacks",url:"/messages/:message_id/feedbacks",method:"POST",title:"Message Feedback",description:"End-users can provide feedback messages, facilitating application developers to optimize expected outputs.",pathParams:[{name:"message_id",type:"string",required:!0,description:"Message ID"}],requestBody:[{name:"rating",type:"string",required:!0,description:"Upvote as `like`, downvote as `dislike`, revoke upvote as `null`"},{name:"user",type:"string",required:!0,description:"User identifier, defined by the developer's rules, must be unique within the application."}],responseSection:{responseTypes:[{title:"FeedbackResponse",description:"Feedback result",fields:[{name:"result",type:"string",description:'Always returns "success"'}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/messages/:message_id/feedbacks' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "rating": "like",
    "user": "abc-123"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"suggested",url:"/messages/{message_id}/suggested",method:"GET",title:"next suggested questions",description:"Get next questions suggestions for the current message",pathParams:[{name:"message_id",type:"string",required:!0,description:"Message ID"}],queryParams:[{name:"user",type:"string",required:!0,description:"User identifier, used to define the identity of the end-user for retrieval and statistics. Should be uniquely defined by the developer within the application."}],responseSection:{responseTypes:[{title:"SuggestedResponse",description:"Suggested questions list",fields:[{name:"result",type:"string",description:'Always returns "success"'},{name:"data",type:"array[string]",description:"Suggested questions list"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl --location --request GET '{{appDetail.api_base_url}}/messages/{message_id}/suggested?user=abc-123' \\
--header 'Authorization: Bearer ENTER-YOUR-SECRET-KEY' \\
--header 'Content-Type: application/json'`},{language:"json",title:"Response",code:`{
  "result": "success",
  "data": [
    "a",
    "b",
    "c"
  ]
}`}]},{id:"messages",url:"/messages",method:"GET",title:"Get Conversation History Messages",description:"Returns historical chat records in a scrolling load format, with the first page returning the latest `{limit}` messages, i.e., in reverse order.",queryParams:[{name:"conversation_id",type:"string",required:!0,description:"Conversation ID"},{name:"user",type:"string",required:!0,description:"User identifier, used to define the identity of the end-user for retrieval and statistics. Should be uniquely defined by the developer within the application."},{name:"first_id",type:"string",required:!1,description:"The ID of the first chat record on the current page, default is null."},{name:"limit",type:"int",required:!1,description:"How many chat history messages to return in one request, default is 20."}],responseSection:{responseTypes:[{title:"MessagesResponse",description:"",fields:[{name:"data",type:"array[object]",description:"Message list",children:[{name:"id",type:"string",description:"Message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"inputs",type:"array[object]",description:"User input parameters."},{name:"query",type:"string",description:"User input / question content."},{name:"message_files",type:"array[object]",description:"Message files",children:[{name:"id",type:"string",description:"ID"},{name:"type",type:"string",description:"File type, image for images"},{name:"url",type:"string",description:"Preview image URL"},{name:"belongs_to",type:"string",description:"belongs to，user or assistant"}]},{name:"answer",type:"string",description:"Response message content"},{name:"created_at",type:"timestamp",description:"Creation timestamp, e.g., 1705395332"},{name:"feedback",type:"object",description:"Feedback information",children:[{name:"rating",type:"string",description:"Upvote as `like` / Downvote as `dislike`"}]},{name:"retriever_resources",type:"array[RetrieverResource]",description:"Citation and Attribution List"}]},{name:"has_more",type:"bool",description:"Whether there is a next page"},{name:"limit",type:"int",description:"Number of returned items, if input exceeds system limit, returns system limit amount"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/messages?user=abc-123&conversation_id=' \\
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response Example",code:`{
  "limit": 20,
  "has_more": false,
  "data": [
    {
        "id": "a076a87f-31e5-48dc-b452-0061adbbc922",
        "conversation_id": "cd78daf6-f9e4-4463-9ff2-54257230a0ce",
        "inputs": {
            "name": "agent"
        },
        "query": "iphone 13 pro",
        "answer": "The iPhone 13 Pro, released on September 24, 2021, features a 6.1-inch display with a resolution of 1170 x 2532. It is equipped with a Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard) processor, 6 GB of RAM, and offers storage options of 128 GB, 256 GB, 512 GB, and 1 TB. The camera is 12 MP, the battery capacity is 3095 mAh, and it runs on iOS 15.",
        "message_files": [],
        "feedback": null,
        "retriever_resources": [
            {
                "position": 1,
                "dataset_id": "101b4c97-fc2e-463c-90b1-5261a4cdcafb",
                "dataset_name": "iPhone",
                "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00",
                "document_name": "iPhone List",
                "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a",
                "score": 0.98457545,
                "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"iPhone 13 Pro Max\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"6 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"12 MP\\",\\"4352 mAh\\",\\"iOS 15\\""
            }
        ],
        "created_at": 1705569239,
    }
  ]
}`}]},{id:"conversations",url:"/conversations",method:"GET",title:"Get Conversations",description:"Retrieve the conversation list for the current user, defaulting to the most recent 20 entries.",queryParams:[{name:"user",type:"string",required:!0,description:"User identifier, used to define the identity of the end-user for retrieval and statistics. Should be uniquely defined by the developer within the application."},{name:"last_id",type:"string",required:!1,description:"The ID of the last record on the current page, default is null."},{name:"limit",type:"int",required:!1,description:"How many records to return in one request, default is the most recent 20 entries."},{name:"pinned",type:"bool",required:!1,description:"Return only pinned conversations as `true`, only non-pinned as `false`"}],responseSection:{responseTypes:[{title:"ConversationsResponse",description:"",fields:[{name:"data",type:"array[object]",description:"List of conversations",children:[{name:"id",type:"string",description:"Conversation ID"},{name:"name",type:"string",description:"Conversation name, by default, is generated by LLM."},{name:"inputs",type:"array[object]",description:"User input parameters."},{name:"introduction",type:"string",description:"Introduction"},{name:"created_at",type:"timestamp",description:"Creation timestamp, e.g., 1705395332"}]},{name:"has_more",type:"bool",description:""},{name:"limit",type:"int",description:"Number of entries returned, if input exceeds system limit, system limit number is returned"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/conversations?user=abc-123&last_id=&limit=20' \\
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
  "limit": 20,
  "has_more": false,
  "data": [
    {
      "id": "10799fb8-64f7-4296-bbf7-b42bfbe0ae54",
      "name": "New chat",
      "inputs": {
          "book": "book",
          "myName": "Lucy"
      },
      "status": "normal",
      "created_at": 1679667915
    },
    {
      "id": "hSIhXBhNe8X1d8Et"
    }
  ]
}`}]},{id:"delete",url:"/conversations/:conversation_id",method:"DELETE",title:"Delete Conversation",description:"Delete a conversation.",pathParams:[{name:"conversation_id",type:"string",required:!0,description:"Conversation ID"}],requestBody:[{name:"user",type:"string",required:!0,description:"The user identifier, defined by the developer, must ensure uniqueness within the application."}],responseSection:{responseTypes:[{title:"DeleteResponse",description:"Delete result",fields:[{name:"result",type:"string",description:'Always returns "success"'}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X DELETE '{{appDetail.api_base_url}}/conversations/{conversation_id}' \\
--header 'Content-Type: application/json' \\
--header 'Accept: application/json' \\
--header 'Authorization: Bearer {api_key}' \\
--data '{
    "user": "abc-123"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"rename",url:"/conversations/:conversation_id/name",method:"POST",title:"Conversation Rename",description:"Rename a conversation for display in multi-session supported clients.",requestBody:[{name:"name",type:"string",required:!1,description:"The name of the conversation. This parameter can be omitted if `auto_generate` is set to `true`."},{name:"auto_generate",type:"bool",required:!1,description:"Automatically generate the title, default is `false`",default:"false"},{name:"user",type:"string",required:!0,description:"The user identifier, defined by the developer, must ensure uniqueness within the application."}],responseSection:{responseTypes:[{title:"RenameResponse",description:"Rename result",fields:[{name:"id",type:"string",description:"Conversation ID"},{name:"name",type:"string",description:"Conversation name"},{name:"inputs",type:"array[object]",description:"User input parameters."},{name:"introduction",type:"string",description:"Introduction"},{name:"created_at",type:"timestamp",description:"Creation timestamp, e.g., 1705395332"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/conversations/:conversation_id/name' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "name": "",
    "user": "abc-123"
}'`},{language:"json",title:"Response",code:`{
    "id": "cd78daf6-f9e4-4463-9ff2-54257230a0ce",
    "name": "Chat vs AI",
    "inputs": {},
    "introduction": "",
    "created_at": 1705569238
}`}]},{id:"audio",url:"/audio-to-text",method:"POST",title:"Speech to Text",description:"This endpoint requires a multipart/form-data request.",requestBody:[{name:"file",type:"file",required:!0,description:"Audio file. Supported formats: `['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']` File size limit: 15MB"},{name:"user",type:"string",required:!0,description:"User identifier, defined by the developer's rules, must be unique within the application."}],responseSection:{responseTypes:[{title:"AudioToTextResponse",description:"Speech to text result",fields:[{name:"text",type:"string",description:"Output text"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/conversations/name' \\
--header 'Authorization: Bearer {api_key}' \\
--form 'file=@localfile;type=audio/mp3'`},{language:"json",title:"Response",code:`{
  "text": ""
}`}]},{id:"text-to-audio",url:"/text-to-audio",method:"POST",title:"text to audio",description:"Text to speech.",requestBody:[{name:"message_id",type:"str",required:!1,description:"For text messages generated by agent, simply pass the generated message-id directly. The backend will use the message-id to look up the corresponding content and synthesize the voice information directly. If both message_id and text are provided simultaneously, the message_id is given priority."},{name:"text",type:"str",required:!1,description:"Speech generated content。"},{name:"user",type:"string",required:!0,description:"The user identifier, defined by the developer, must ensure uniqueness within the app."}],responseSection:{responseTypes:[{title:"TextToAudioResponse",description:"Text to audio result",fields:[{name:"Content-Type",type:"string",description:"audio/wav"}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -o text-to-audio.mp3 -X POST '{{appDetail.api_base_url}}/text-to-audio' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290",
    "text": "Hello agent",
    "user": "abc-123",
    "streaming": false
}'`},{language:"json",title:"headers",code:`{
  "Content-Type": "audio/wav"
}`}]},{id:"parameters",url:"/parameters",method:"GET",title:"Get Application Information",description:"Used at the start of entering the page to obtain information such as features, input parameter names, types, and default values.",queryParams:[{name:"user",type:"string",required:!0,description:"User identifier, defined by the developer's rules, must be unique within the application."}],responseSection:{responseTypes:[{title:"ParametersResponse",description:"",fields:[{name:"opening_statement",type:"string",description:"Opening statement"},{name:"suggested_questions",type:"array[string]",description:"List of suggested questions for the opening"},{name:"suggested_questions_after_answer",type:"object",description:"Suggest questions after enabling the answer.",children:[{name:"enabled",type:"bool",description:"Whether it is enabled"}]},{name:"speech_to_text",type:"object",description:"Speech to text",children:[{name:"enabled",type:"bool",description:"Whether it is enabled"}]},{name:"retriever_resource",type:"object",description:"Citation and Attribution",children:[{name:"enabled",type:"bool",description:"Whether it is enabled"}]},{name:"annotation_reply",type:"object",description:"Annotation reply",children:[{name:"enabled",type:"bool",description:"Whether it is enabled"}]},{name:"user_input_form",type:"array[object]",description:"User input form configuration",children:[{name:"text-input",type:"object",description:"Text input control",children:[{name:"label",type:"string",description:"Variable display label name"},{name:"variable",type:"string",description:"Variable ID"},{name:"required",type:"bool",description:"Whether it is required"},{name:"default",type:"string",description:"Default value"}]},{name:"paragraph",type:"object",description:"Paragraph text input control",children:[{name:"label",type:"string",description:"Variable display label name"},{name:"variable",type:"string",description:"Variable ID"},{name:"required",type:"bool",description:"Whether it is required"},{name:"default",type:"string",description:"Default value"}]},{name:"select",type:"object",description:"Dropdown control",children:[{name:"label",type:"string",description:"Variable display label name"},{name:"variable",type:"string",description:"Variable ID"},{name:"required",type:"bool",description:"Whether it is required"},{name:"default",type:"string",description:"Default value"},{name:"options",type:"array[string]",description:"Option values"}]}]},{name:"file_upload",type:"object",description:"File upload configuration",children:[{name:"image",type:"object",description:"Image settings. Currently only supports image types: `png`, `jpg`, `jpeg`, `webp`, `gif`",children:[{name:"enabled",type:"bool",description:"Whether it is enabled"},{name:"number_limits",type:"int",description:"Image number limit, default is 3"},{name:"transfer_methods",type:"array[string]",description:"List of transfer methods, remote_url, local_file, must choose one"}]}]},{name:"system_parameters",type:"object",description:"System parameters",children:[{name:"image_file_size_limit",type:"string",description:"Image file upload size limit (MB)"}]}]}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/parameters?user=abc-123' \\
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
  "opening_statement": "Hello!",
  "suggested_questions_after_answer": {
      "enabled": true
  },
  "speech_to_text": {
      "enabled": true
  },
  "retriever_resource": {
      "enabled": true
  },
  "annotation_reply": {
      "enabled": true
  },
  "user_input_form": [
      {
          "paragraph": {
              "label": "Query",
              "variable": "query",
              "required": true,
              "default": ""
          }
      }
  ],
  "file_upload": {
      "image": {
          "enabled": false,
          "number_limits": 3,
          "detail": "high",
          "transfer_methods": [
              "remote_url",
              "local_file"
          ]
      }
  },
  "system_parameters": {
      "image_file_size_limit": "10"
  }
}`}]},{id:"meta",url:"/meta",method:"GET",title:"Get Application Meta Information",description:"Used to get icons of tools in this application",queryParams:[{name:"user",type:"string",required:!0,description:"User identifier, defined by the developer's rules, must be unique within the application."}],responses:[{name:"tool_icons",type:"object[string]",description:"tool icons",children:[{name:"tool_name",type:"string",description:"",children:[{name:"icon",type:"object|string",description:"",children:[{name:"(object)",type:"",description:"icon object",children:[{name:"background",type:"string",description:"background color in hex format"},{name:"content",type:"string",description:"emoji"}]},{name:"(string)",type:"",description:"url of icon"}]}]}]}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/meta?user=abc-123' \\
-H 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
"tool_icons": {
    "dalle2": "https://cloud.ai/console/api/workspaces/current/tool-provider/builtin/dalle/icon",
    "api_tool": {
        "background": "#252525",
        "content": "😁"
    }
}
}`}]}]};function X(t){return e.jsx(u,{template:W,appDetail:t.appDetail,inputs:t.inputs})}function K(t){return e.jsx(u,{template:F,appDetail:t.appDetail,inputs:t.inputs})}const J={title:"Chat App API",description:"Chat applications support session persistence, allowing previous chat history to be used as context for responses. This can be applicable for chatbot, customer service AI, etc.",baseUrl:"{{appDetail.api_base_url}}",authentication:{type:"Bearer Token",description:"The Service API uses `API-Key` authentication.\n**Strongly recommend storing your API Key on the server-side, not shared or stored on the client-side, to avoid possible API-Key leakage that can lead to serious consequences.**\nFor all API requests, include your API Key in the `Authorization`HTTP Header, as shown below:",example:"Authorization: Bearer {API_KEY}"},labels:{baseUrl:"Base URL",authentication:"Authentication",pathParams:"Path Params",queryParams:"Query",requestBody:"Request Body",response:"Response",errors:"Errors",requestExample:"Request Example",default:"Default",options:"Options",streamingStructureDiffers:"The structure of the streaming chunks varies depending on the event:",errorInformation:"Error Information",errorCodeReturned:"Returned error code",errorStatusReturned:"Returned error status",errorMessageReturned:"Returned error message",errorTableCode:"code",errorTableStatus:"status",errorTableMessage:"message",interfaceDefinition:"Interface Definition",path:"Path",method:"Method",contentType:"Content-Type",authorization:"Authorization",basicInfo:"Basic Information"},endpoints:[{id:"Send-Chat-Message",url:"/chat-messages",method:"POST",title:"Send Chat Message",description:"Send a request to the chat application.",requestBody:[{name:"query",type:"string",description:"User Input/Question content"},{name:"inputs",type:"object",description:"Allows the entry of various variable values defined by the App.\nThe `inputs` parameter contains multiple key/value pairs, with each key corresponding to a specific variable and each value being the specific value for that variable. Default `{}`"},{name:"response_mode",type:"string",description:"The mode of response return, supporting:\n- `streaming` Streaming mode (recommended), implements a typewriter-like output through SSE ([Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)).\n- `blocking` Blocking mode, returns result after execution is complete. (Requests may be interrupted if the process is long)\nDue to Cloudflare restrictions, the request will be interrupted without a return after 100 seconds.\n*Note: blocking mode is not supported in Agent Assistant mode*"},{name:"user",type:"string",description:`User identifier, used to define the identity of the end-user for retrieval and statistics.
Should be uniquely defined by the developer within the application.`},{name:"conversation_id",type:"string",description:"Conversation ID, to continue the conversation based on previous chat records, it is necessary to pass the previous message's conversation_id."},{name:"files",type:"array[object]",description:"File list, suitable for inputting files (images) combined with text understanding and answering questions, available only when the model supports Vision capability.\n- `type` (string) Supported type: `image` (currently only supports image type)\n- `transfer_method` (string) Transfer method, `remote_url` for image URL / `local_file` for file upload\n- `url` (string) Image URL (when the transfer method is `remote_url`)\n- `upload_file_id` (string) Uploaded file ID, which must be obtained by uploading through the File Upload API in advance (when the transfer method is `local_file`)"},{name:"auto_generate_name",type:"bool",description:"Auto-generate title, default is `true`.\nIf set to `false`, can achieve async title generation by calling the conversation rename API and setting `auto_generate` to `true`."}],responseSection:{generalDescription:`When response_mode is blocking, return a CompletionResponse object.
When response_mode is streaming, return a ChunkCompletionResponse stream.`,responseTypes:[{title:"ChatCompletionResponse",description:"Returns the complete App result, `Content-Type` is `application/json`.",fields:[{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"mode",type:"string",description:"App mode, fixed as `chat`"},{name:"answer",type:"string",description:"Complete response content"},{name:"metadata",type:"object",description:"Metadata",children:[{name:"usage",type:"Usage",description:"Model usage information"},{name:"retriever_resources",type:"array[RetrieverResource]",description:"Citation and Attribution List"}]},{name:"created_at",type:"int",description:"Message creation timestamp, e.g., 1705395332"}]},{title:"ChunkChatCompletionResponse",description:"Returns the stream chunks outputted by the App, `Content-Type` is `text/event-stream`.\nEach streaming chunk starts with `data:`, separated by two newline characters `\\n\\n`, as shown below:",events:[{name:"event: message",description:"LLM returns text chunk event, i.e., the complete text is output in a chunked fashion.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"answer",type:"string",description:"LLM returned text chunk content"},{name:"created_at",type:"int",description:"Creation timestamp, e.g., 1705395332"}]},{name:"event: agent_message",description:"LLM returns text chunk event, i.e., with Agent Assistant enabled, the complete text is output in a chunked fashion (Only supported in Agent mode)",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"answer",type:"string",description:"LLM returned text chunk content"},{name:"created_at",type:"int",description:"Creation timestamp, e.g., 1705395332"}]},{name:"event: tts_message",description:"TTS audio stream event, that is, speech synthesis output. The content is an audio block in Mp3 format, encoded as a base64 string. When playing, simply decode the base64 and feed it into the player. (This message is available only when auto-play is enabled)",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the stop response interface below"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"audio",type:"string",description:"The audio after speech synthesis, encoded in base64 text content, when playing, simply decode the base64 and feed it into the player"},{name:"created_at",type:"int",description:"Creation timestamp, e.g.: 1705395332"}]},{name:"event: tts_message_end",description:"TTS audio stream end event, receiving this event indicates the end of the audio stream.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the stop response interface below"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"audio",type:"string",description:"The end event has no audio, so this is an empty string"},{name:"created_at",type:"int",description:"Creation timestamp, e.g.: 1705395332"}]},{name:"event: agent_thought",description:"thought of Agent, contains the thought of LLM, input and output of tool calls (Only supported in Agent mode)",fields:[{name:"id",type:"string",description:"Agent thought ID, every iteration has a unique agent thought ID"},{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"position",type:"int",description:"Position of current agent thought, each message may have multiple thoughts in order."},{name:"thought",type:"string",description:"What LLM is thinking about"},{name:"observation",type:"string",description:"Response from tool calls"},{name:"tool",type:"string",description:"A list of tools represents which tools are called，split by ;"},{name:"tool_input",type:"string",description:'Input of tools in JSON format. Like: `{"dalle3": {"prompt": "a cute cat"}}`.'},{name:"created_at",type:"int",description:"Creation timestamp, e.g., 1705395332"},{name:"message_files",type:"array[string]",description:"Refer to message_file event",children:[{name:"file_id",type:"string",description:"File ID"}]},{name:"conversation_id",type:"string",description:"Conversation ID"}]},{name:"event: message_file",description:"Message file event, a new file has created by tool",fields:[{name:"id",type:"string",description:"File unique ID"},{name:"type",type:"string",description:'File type，only allow "image" currently'},{name:"belongs_to",type:"string",description:"Belongs to, it will only be an 'assistant' here"},{name:"url",type:"string",description:"Remote url of file"},{name:"conversation_id",type:"string",description:"Conversation ID"}]},{name:"event: message_end",description:"Message end event, receiving this event means streaming has ended.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"metadata",type:"object",description:"Metadata",children:[{name:"usage",type:"Usage",description:"Model usage information"},{name:"retriever_resources",type:"array[RetrieverResource]",description:"Citation and Attribution List"}]}]},{name:"event: message_replace",description:`Message content replacement event.
When output content moderation is enabled, if the content is flagged, then the message content will be replaced with a preset reply through this event.`,fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"conversation_id",type:"string",description:"Conversation ID"},{name:"answer",type:"string",description:"Replacement content (directly replaces all LLM reply text)"},{name:"created_at",type:"int",description:"Creation timestamp, e.g., 1705395332"}]},{name:"event: error",description:"Exceptions that occur during the streaming process will be output in the form of stream events, and reception of an error event will end the stream.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"status",type:"int",description:"HTTP status code"},{name:"code",type:"string",description:"Error code"},{name:"message",type:"string",description:"Error message"}]},{name:"event: ping",description:"Ping event every 10 seconds to keep the connection alive.",fields:[]}],streamingExample:{language:"streaming",title:"Response",code:'data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\\n\\n'}}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/chat-messages' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "inputs": {},
    "query": "eh",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "abc-123"
}'`},{language:"json",title:"Blocking Mode",code:`{
    "event": "message",
    "message_id": "9da23599-e713-473b-982c-4328d4f5c78a",
    "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2",
    "mode": "chat",
    "answer": "iPhone 13 Pro Max specs are listed here:...",
    "metadata": {
        "usage": {
            "prompt_tokens": 1033,
            "prompt_unit_price": "0.001",
            "prompt_price_unit": "0.001",
            "prompt_price": "0.0010330",
            "completion_tokens": 128,
            "completion_unit_price": "0.002",
            "completion_price_unit": "0.001",
            "completion_price": "0.0002560",
            "total_tokens": 1161,
            "total_price": "0.0012890",
            "currency": "USD",
            "latency": 0.7682376249867957
        },
        "retriever_resources": [
            {
                "position": 1,
                "dataset_id": "101b4c97-fc2e-463c-90b1-5261a4cdcafb",
                "dataset_name": "iPhone",
                "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00",
                "document_name": "iPhone List",
                "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a",
                "score": 0.98457545,
                "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"iPhone 13 Pro Max\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"6 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"12 MP\\",\\"4352 mAh\\",\\"iOS 15\\""
            }
        ]
    },
    "created_at": 1705407629
}`},{language:"streaming",title:"Streaming Mode ( Basic Assistant )",code:`  data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " I", "created_at": 1679586595}
  data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": "'m", "created_at": 1679586595}
  data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " glad", "created_at": 1679586595}
  data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " to", "created_at": 1679586595}
  data: {"event": "message", "message_id": : "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " meet", "created_at": 1679586595}
  data: {"event": "message", "message_id": : "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " you", "created_at": 1679586595}
  data: {"event": "message_end", "id": "5e52ce04-874b-4d27-9045-b3bc80def685", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "metadata": {"usage": {"prompt_tokens": 1033, "prompt_unit_price": "0.001", "prompt_price_unit": "0.001", "prompt_price": "0.0010330", "completion_tokens": 135, "completion_unit_price": "0.002", "completion_price_unit": "0.001", "completion_price": "0.0002700", "total_tokens": 1168, "total_price": "0.0013030", "currency": "USD", "latency": 1.381760165997548}, "retriever_resources": [{"position": 1, "dataset_id": "101b4c97-fc2e-463c-90b1-5261a4cdcafb", "dataset_name": "iPhone", "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00", "document_name": "iPhone List", "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a", "score": 0.98457545, "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"iPhone 13 Pro Max\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"6 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"12 MP\\",\\"4352 mAh\\",\\"iOS 15\\""}]}}
  data: {"event": "tts_message", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"}
  data: {"event": "tts_message_end", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": ""}`},{language:"streaming",title:"Response Example(Agent Assistant)",code:`data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " I", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": "'m", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " glad", "created_at": 1679586595}
data: {"event": "message", "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " to", "created_at": 1679586595}
data: {"event": "message", "message_id": : "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " meet", "created_at": 1679586595}
data: {"event": "message", "message_id": : "5ad4cb98-f0c7-4085-b384-88c403be6290", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " you", "created_at": 1679586595}
data: {"event": "message_end", "id": "5e52ce04-874b-4d27-9045-b3bc80def685", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "metadata": {"usage": {"prompt_tokens": 1033, "prompt_unit_price": "0.001", "prompt_price_unit": "0.001", "prompt_price": "0.0010330", "completion_tokens": 135, "completion_unit_price": "0.002", "completion_price_unit": "0.001", "completion_price": "0.0002700", "total_tokens": 1168, "total_price": "0.0013030", "currency": "USD", "latency": 1.381760165997548}, "retriever_resources": [{"position": 1, "dataset_id": "101b4c97-fc2e-463c-90b1-5261a4cdcafb", "dataset_name": "iPhone", "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00", "document_name": "iPhone List", "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a", "score": 0.98457545, "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"iPhone 13 Pro Max\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"6 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"12 MP\\",\\"4352 mAh\\",\\"iOS 15\\""}]}}
data: {"event": "tts_message", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"}
data: {"event": "tts_message_end", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": ""}`}],errors:[{code:"404",description:"Conversation does not exists"},{code:"400",description:"`invalid_param`, abnormal parameter input"},{code:"400",description:"`app_unavailable`, App configuration unavailable"},{code:"400",description:"`provider_not_initialize`, no available model credential configuration"},{code:"400",description:"`provider_quota_exceeded`, model invocation quota insufficient"},{code:"400",description:"`model_currently_not_support`, current model unavailable"},{code:"400",description:"`completion_request_error`, text generation failed"},{code:"500",description:"internal server error"}]},{id:"file-upload",url:"/files/upload",method:"POST",title:"File Upload",description:`Upload a file (currently only images are supported) for use when sending messages, enabling multimodal understanding of images and text.
Supports png, jpg, jpeg, webp, gif formats.
Uploaded files are for use by the current end-user only.`,requestBody:[{name:"file",type:"File",description:"The file to be uploaded."},{name:"user",type:"string",description:"User identifier, defined by the developer's rules, must be unique within the application."}],responses:[{name:"id",type:"uuid",description:"ID"},{name:"name",type:"string",description:"File name"},{name:"size",type:"int",description:"File size (bytes)"},{name:"extension",type:"string",description:"File extension"},{name:"mime_type",type:"string",description:"File mime-type"},{name:"created_by",type:"uuid",description:"End-user ID"},{name:"created_at",type:"timestamp",description:"Creation timestamp, e.g., 1705395332"}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/files/upload' \\
--header 'Authorization: Bearer {api_key}' \\
--form 'file=@"/path/to/file"'`},{language:"json",title:"Response",code:`{
  "id": "72fa9618-8f89-4a37-9b33-7e1178a24a67",
  "name": "example.png",
  "size": 1024,
  "extension": "png",
  "mime_type": "image/png",
  "created_by": "6ad1ab0a-73ff-4ac1-b9e4-cdb312f71f13",
  "created_at": 1577836800,
}`}],errors:[{code:"400",description:"`no_file_uploaded`, a file must be provided"},{code:"400",description:"`too_many_files`, currently only one file is accepted"},{code:"400",description:"`unsupported_preview`, the file does not support preview"},{code:"400",description:"`unsupported_estimate`, the file does not support estimation"},{code:"413",description:"`file_too_large`, the file is too large"},{code:"415",description:"`unsupported_file_type`, unsupported extension, currently only document files are accepted"},{code:"503",description:"`s3_connection_failed`, unable to connect to S3 service"},{code:"503",description:"`s3_permission_denied`, no permission to upload files to S3"},{code:"503",description:"`s3_file_too_large`, file exceeds S3 size limit"},{code:"500",description:"internal server error"}]},{id:"stop-generatebacks",url:"/chat-messages/:task_id/stop",method:"POST",title:"Stop Generate",description:"Only supported in streaming mode.",pathParams:[{name:"task_id",type:"string",description:"Task ID, can be obtained from the streaming chunk return"}],requestBody:[{name:"user",type:"string",description:"User identifier, used to define the identity of the end-user, must be consistent with the user passed in the send message interface."}],responses:[{name:"result",type:"string",description:'Always returns "success"'}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/chat-messages/:task_id/stop' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json' \\
--data-raw '{
    "user": "abc-123"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]}]},V={title:"对话型应用 API",description:"对话应用支持会话持久化，可将之前的聊天记录作为上下进行回答，可适用于聊天/客服 AI 等。",baseUrl:"{{appDetail.api_base_url}}",authentication:{type:"Bearer Token",description:"Service API 使用 `API-Key` 进行鉴权。\n**强烈建议开发者把 `API-Key` 放在后端存储，而非分享或者放在客户端存储，以免 `API-Key` 泄露，导致财产损失。**\n所有 API 请求都应在 **`Authorization`** HTTP Header 中包含您的 `API-Key`，如下所示：",example:"Authorization: Bearer {API_KEY}"},labels:{baseUrl:"基础 URL",authentication:"鉴权",pathParams:"Path Params",queryParams:"Query",requestBody:"Request Body",response:"Response",errors:"Errors",requestExample:"Request Example",default:"默认",options:"可选值",streamingStructureDiffers:"流式块中根据 event 不同，结构也不同：",errorInformation:"错误信息",errorCodeReturned:"返回的错误代码",errorStatusReturned:"返回的错误状态",errorMessageReturned:"返回的错误消息",errorTableCode:"code",errorTableStatus:"status",errorTableMessage:"message",interfaceDefinition:"接口定义",path:"Path",method:"Method",contentType:"Content-Type",authorization:"Authorization",basicInfo:"基础信息"},endpoints:[{id:"Create-Chat-Message",url:"/chat-messages",method:"POST",title:"发送对话消息",description:"创建会话消息。",requestBody:[{name:"query",type:"string",description:"用户输入/提问内容。"},{name:"input_data",type:"object",description:"允许传入 App 定义的各变量值。\ninput_data 参数包含了多组键值对（Key/Value pairs），每组的键对应一个特定变量，每组的值则是该变量的具体值。\n默认 `{}`"},{name:"mode",type:"string",description:"- `streaming` 流式模式（推荐）。基于 SSE（**[Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)**）实现类似打字机输出方式的流式返回。\n- `blocking` 阻塞模式，等待执行完毕后返回结果。（请求若流程较长可能会被中断）。\n由于 Cloudflare 限制，请求会在 100 秒超时无返回后中断。\n"},{name:"user",type:"string",description:`用户标识，用于定义终端用户的身份，方便检索、统计。
由开发者定义规则，需保证用户标识在应用内唯一。`},{name:"conversation_id",type:"string",description:"（选填）会话 ID，需要基于之前的聊天记录继续对话，必须传之前消息的 conversation_id。"},{name:"files",type:"array[object]",description:"上传的文件。\n- `type` (string) 支持类型：图片 `image`（目前仅支持图片格式） 。\n- `transfer_method` (string)  传递方式:\n  - `remote_url`: 图片地址。\n  - `local_file`: 上传文件。\n- `url` 图片地址。（仅当传递方式为 `remote_url` 时）。\n- `upload_file_id` 上传文件 ID。（仅当传递方式为 `local_file `时）。"},{name:"is_name_auto",type:"bool",description:"（选填）自动生成标题，默认 `true`。 若设置为 `false`，则可通过调用会话重命名接口并设置 `auto_generate` 为 `true` 实现异步生成标题。"}],responseSection:{generalDescription:"当 `response_mode` 为 `blocking` 时，返回 ChatCompletionResponse object。\n当 `response_mode` 为 `streaming`时，返回 ChunkChatCompletionResponse object 流式序列。",responseTypes:[{title:"ChatCompletionResponse",description:"返回完整的 App 结果，`Content-Type` 为 `application/json`。",fields:[{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"mode",type:"string",description:"App 模式，固定为 chat"},{name:"answer",type:"string",description:"完整回复内容"},{name:"metadata",type:"object",description:"元数据",children:[{name:"usage",type:"Usage",description:"模型用量信息"},{name:"retriever_resources",type:"array[RetrieverResource]",description:"引用和归属分段列表"}]},{name:"created_at",type:"int",description:"消息创建时间戳，如：1705395332"}]},{title:"ChunkChatCompletionResponse",description:"返回 App 输出的流式块，`Content-Type` 为 `text/event-stream`。\n每个流式块均为 data: 开头，块之间以 \\n\\n 即两个换行符分隔，如下所示：",events:[{name:"event: message",description:"LLM 返回文本块事件，即：完整的文本以分块的方式输出。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"answer",type:"string",description:"LLM 返回文本块内容"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: agent_message",description:"Agent模式下返回文本块事件，即：在Agent模式下，文章的文本以分块的方式输出（仅Agent模式下使用）",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"answer",type:"string",description:"LLM 返回文本块内容"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: agent_thought",description:"Agent模式下有关Agent思考步骤的相关内容，涉及到工具调用（仅Agent模式下使用）",fields:[{name:"id",type:"string",description:"agent_thought ID，每一轮Agent迭代都会有一个唯一的id"},{name:"task_id",type:"string",description:"任务ID，用于请求跟踪下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一ID"},{name:"position",type:"int",description:"agent_thought在消息中的位置，如第一轮迭代position为1"},{name:"thought",type:"string",description:"agent的思考内容"},{name:"observation",type:"string",description:"工具调用的返回结果"},{name:"tool",type:"string",description:"使用的工具列表，以 ; 分割多个工具"},{name:"tool_input",type:"string",description:'工具的输入，JSON格式的字符串(object)。如：`{"dalle3": {"prompt": "a cute cat"}}`'},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"},{name:"message_files",type:"array[string]",description:"当前 `agent_thought` 关联的文件ID",children:[{name:"file_id",type:"string",description:"文件ID"}]},{name:"conversation_id",type:"string",description:"会话ID"}]},{name:"event: message_file",description:"文件事件，表示有新文件需要展示",fields:[{name:"id",type:"string",description:"文件唯一ID"},{name:"type",type:"string",description:"文件类型，目前仅为image"},{name:"belongs_to",type:"string",description:"文件归属，user或assistant，该接口返回仅为 `assistant`"},{name:"url",type:"string",description:"文件访问地址"},{name:"conversation_id",type:"string",description:"会话ID"}]},{name:"event: message_end",description:"消息结束事件，收到此事件则代表流式返回结束。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"metadata",type:"object",description:"元数据",children:[{name:"usage",type:"Usage",description:"模型用量信息"},{name:"retriever_resources",type:"array[RetrieverResource]",description:"引用和归属分段列表"}]}]},{name:"event: tts_message",description:"TTS 音频流事件，即：语音合成输出。内容是Mp3格式的音频块，使用 base64 编码后的字符串，播放的时候直接解码即可。(开启自动播放才有此消息)",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"audio",type:"string",description:"语音合成之后的音频块使用 Base64 编码之后的文本内容，播放的时候直接 base64 解码送入播放器即可"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: tts_message_end",description:"TTS 音频流结束事件，收到这个事件表示音频流返回结束。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"audio",type:"string",description:"结束事件是没有音频的，所以这里是空字符串"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: message_replace",description:`消息内容替换事件。
开启内容审查和审查输出内容时，若命中了审查条件，则会通过此事件替换消息内容为预设回复。`,fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"conversation_id",type:"string",description:"会话 ID"},{name:"answer",type:"string",description:"替换内容（直接替换 LLM 所有回复文本）"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: error",description:"流式输出过程中出现的异常会以 stream event 形式输出，收到异常事件后即结束。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"status",type:"int",description:"HTTP 状态码"},{name:"code",type:"string",description:"错误码"},{name:"message",type:"string",description:"错误消息"}]},{name:"event: ping",description:"每 10s 一次的 ping 事件，保持连接存活。",fields:[]}],streamingExample:{language:"streaming",title:"Response",code:'data: {"event": "message", "task_id": "aa321d77-dd8a-469b-a176-7791e44dfa1e", "id": "403f4621-5332-4fb2-85a1-a36ecac331cf", "answer": "你好", "created_at": 1705398420}\\n\\n'}}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/chat-messages' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json' \\
--data-raw '{
    "input_data": {
        "name": "test"
    },
    "query": "请介绍下华为手机",
    "conversation_id": "",
    "mode": "streaming",
    "user": "admin",
    "files": [
      {
        "type": "image",
        "transfer_method": "remote_url",
        "url": "https://agent.teleagi.cn//logo-index.png"
      }
    ]
}'`},{language:"json",title:"阻塞模式",code:`{
    "event": "message",
    "message_id": "26b1a6b9-f297-4c21-9135-c8d06d982a10",
    "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2",
    "mode": "chat",
    "answer": "华为手机的规格参数如下....",
    "metadata": {
        "usage": {
            "prompt_tokens": 1233,
            "prompt_unit_price": "0.001",
            "prompt_price_unit": "0.001",
            "prompt_price": "0.0010330",
            "completion_tokens": 124,
            "completion_unit_price": "0.002",
            "completion_price_unit": "0.001",
            "completion_price": "0.0002560",
            "total_tokens": 1161,
            "total_price": "0.0012890",
            "currency": "USD",
            "latency": 0.7682376249867957
        },
        "retriever_resources": [
            {
                "position": 1,
                "dataset_id": "7f7f7e1a-802e-4d52-9088-c8e9eeb5da0d",
                "dataset_name": "Huawei",
                "document_id": "1fd346d3-b7cf-42b7-9dd0-b284d64d648f",
                "document_name": "Huawei List",
                "segment_id": "43f1966e-d048-4830-bbf7-7fe744e4abee",
                "score": 0.98457545,
                "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"Huawei mate\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"12 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"11 MP\\",\\"5000mAh\\",\\"安卓\\""
            }
        ]
    },
    "created_at": 1705407629
}`},{language:"streaming",title:"流式模式（基础助手）",code:`  data: {"event": "message", "message_id": "9de30425-98e0-41d5-b5c4-52c3cd3aebd1", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " I", "created_at": 1679586595}
  data: {"event": "message", "message_id": "9de30425-98e0-41d5-b5c4-52c3cd3aebd1", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": "'m", "created_at": 1679586595}
  data: {"event": "message", "message_id": "9de30425-98e0-41d5-b5c4-52c3cd3aebd1", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " glad", "created_at": 1679586595}
  data: {"event": "message", "message_id": "9de30425-98e0-41d5-b5c4-52c3cd3aebd1", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " to", "created_at": 1679586595}
  data: {"event": "message", "message_id": : "9de30425-98e0-41d5-b5c4-52c3cd3aebd1", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " meet", "created_at": 1679586595}
  data: {"event": "message", "message_id": : "9de30425-98e0-41d5-b5c4-52c3cd3aebd1", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "answer": " you", "created_at": 1679586595}
  data: {"event": "message_end", "id": "5e52ce04-874b-4d27-9045-b3bc80def685", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "metadata": {"usage": {"prompt_tokens": 1033, "prompt_unit_price": "0.001", "prompt_price_unit": "0.001", "prompt_price": "0.0010330", "completion_tokens": 135, "completion_unit_price": "0.002", "completion_price_unit": "0.001", "completion_price": "0.0002700", "total_tokens": 1168, "total_price": "0.0013030", "currency": "USD", "latency": 1.381760165997548}, "retriever_resources": [{"position": 1, "dataset_id": "9faeba48-b5ef-42ec-8d2c-4bf4e54616de", "dataset_name": "iPhone", "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00", "document_name": "iPhone List", "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a", "score": 0.98457545, "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"iPhone 13 Pro Max\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"6 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"12 MP\\",\\"4352 mAh\\",\\"iOS 15\\""}]}}
  data: {"event": "tts_message", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"}
  data: {"event": "tts_message_end", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": ""}`},{language:"streaming",title:"流式模式（智能助手）",code:`  data: {"event": "agent_thought", "id": "8dcf3648-fbad-407a-85dd-73a6f43aeb9f", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "position": 1, "thought": "", "observation": "", "tool": "", "tool_input": "", "created_at": 1705639511, "message_files": [], "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "agent_thought", "id": "8dcf3648-fbad-407a-85dd-73a6f43aeb9f", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "position": 1, "thought": "", "observation": "", "tool": "dalle3", "tool_input": "{\\"dalle3\\": {\\"prompt\\": \\"cute Japanese anime girl with white hair, blue eyes, bunny girl suit\\"}}", "created_at": 1705639511, "message_files": [], "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "message_file", "id": "8dcf3648-fbad-407a-85dd-73a6f43aeb9f", "type": "image", "belongs_to": "assistant", "url": "http://127.0.0.1:5001/files/tools/d75b7a5c-ce5e-442e-ab1b-d6a5e5b557b0.png?timestamp=1705639526&nonce=70423256c60da73a9c96d1385ff78487&sign=7B5fKV9890YJuqchQvrABvW4AIupDvDvxGdu1EOJT94=", "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "agent_thought", "id": "8dcf3648-fbad-407a-85dd-73a6f43aeb9f", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "position": 1, "thought": "", "observation": "image has been created and sent to user already, you should tell user to check it now.", "tool": "dalle3", "tool_input": "{\\"dalle3\\": {\\"prompt\\": \\"cute Japanese anime girl with white hair, blue eyes, bunny girl suit\\"}}", "created_at": 1705639511, "message_files": ["d75b7a5c-ce5e-442e-ab1b-d6a5e5b557b0"], "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "agent_thought", "id": "67a99dc1-4f82-42d3-b354-18d4594840c8", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "position": 2, "thought": "", "observation": "", "tool": "", "tool_input": "", "created_at": 1705639511, "message_files": [], "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "agent_message", "id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "answer": "I have created an image of a cute Japanese", "created_at": 1705639511, "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "agent_message", "id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "answer": " anime girl with white hair and blue", "created_at": 1705639511, "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "agent_message", "id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "answer": " eyes wearing a bunny girl" ,"created_at": 1705639511, "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "agent_message", "id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "answer": " suit .", "created_at": 1705639511, "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "agent_thought", "id": "8dcf3648-fbad-407a-85dd-73a6f43aeb9f", "task_id": "85bd1552-cd0e-4871-9b04-b0c339578263", "message_id": "1fb10045-55fd-4040-99e6-d048d07cbad3", "position": 2, "thought": "I have created an image of a cute Japanese anime girl with white hair and blue eyes wearing a bunny girl suit.", "observation": "", "tool": "", "tool_input": "", "created_at": 1705639511, "message_files": [], "conversation_id": "c216c595-2d89-438c-b33c-aae5ddddd142"}
  data: {"event": "message_end", "id": "58dcf3648-fbad-407a-85dd-73a6f43aeb9f85", "conversation_id": "45701982-8118-4bc5-8e9b-64562b4555f2", "metadata": {"usage": {"prompt_tokens": 1033, "prompt_unit_price": "0.001", "prompt_price_unit": "0.001", "prompt_price": "0.0010330", "completion_tokens": 135, "completion_unit_price": "0.002", "completion_price_unit": "0.001", "completion_price": "0.0002700", "total_tokens": 1168, "total_price": "0.0013030", "currency": "USD", "latency": 1.381760165997548}, "retriever_resources": [{"position": 1, "dataset_id": "9faeba48-b5ef-42ec-8d2c-4bf4e54616de", "dataset_name": "iPhone", "document_id": "8dd1ad74-0b5f-4175-b735-7d98bbbb4e00", "document_name": "iPhone List", "segment_id": "ed599c7f-2766-4294-9d1d-e5235a61270a", "score": 0.98457545, "content": "\\"Model\\",\\"Release Date\\",\\"Display Size\\",\\"Resolution\\",\\"Processor\\",\\"RAM\\",\\"Storage\\",\\"Camera\\",\\"Battery\\",\\"Operating System\\"\\n\\"huawei mate\\",\\"September 24, 2021\\",\\"6.7 inch\\",\\"1284 x 2778\\",\\"Hexa-core (2x3.23 GHz Avalanche + 4x1.82 GHz Blizzard)\\",\\"6 GB\\",\\"128, 256, 512 GB, 1TB\\",\\"12 MP\\",\\"4352 mAh\\",\\"iOS 15\\""}]}}
  data: {"event": "tts_message", "conversation_id": "8dcf3648-fbad-s407a-85dd-73a6f43aeb9f", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "46516516516qqqscs"}
  data: {"event": "tts_message_end", "conversation_id": "8dcf3648-fbsad-407a-85dd-73a6f43aeb9f", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": ""}`}],errors:[{code:"404",description:"对话不存在"},{code:"400",description:"`invalid_param`，传入参数异常"},{code:"400",description:"`app_unavailable`，App 配置不可用"},{code:"400",description:"`provider_not_initialize`，无可用模型凭据配置"},{code:"400",description:"`provider_quota_exceeded`，模型调用额度不足"},{code:"400",description:"`model_currently_not_support`，当前模型不可用"},{code:"400",description:"`completion_request_error`，文本生成失败"},{code:"500",description:"服务内部异常"}]},{id:"files-upload",url:"/files/upload",method:"POST",title:"上传文件",description:`上传文件（目前仅支持图片）并在发送消息时使用，可实现图文多模态理解。
支持 jpg, jpeg, png, webp, gif, svg 格式。
上传的文件仅供当前终端用户使用。`,requestBody:[{name:"file",type:"file",description:"要上传的文件。"},{name:"user",type:"string",description:"用户标识，用于定义终端用户的身份，必须和发送消息接口传入 user 保持一致。"}],responses:[{name:"id",type:"uuid",description:"ID"},{name:"name",type:"string",description:"文件名"},{name:"size",type:"int",description:"文件大小（byte）"},{name:"extension",type:"string",description:"文件后缀"},{name:"mime_type",type:"string",description:"文件 mime-type"},{name:"created_by",type:"uuid",description:"上传人 ID"},{name:"created_at",type:"timestamp",description:"上传时间"}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/files/upload' \\
--header 'Authorization: Bearer {api_key}' \\
--form 'file=@"/path/to/file"'`},{language:"json",title:"Response",code:`{
  "id": "ae975f34-0e94-4c27-a7ba-f65efaf68480",
  "name": "example.png",
  "size": 1024,
  "extension": "png",
  "mime_type": "image/png",
  "created_by": "administrator",
  "created_at": 1577836800,
}`}],errors:[{code:"400",description:"`no_file_uploaded`，必须提供文件"},{code:"400",description:"`too_many_files`，目前只接受一个文件"},{code:"400",description:"`unsupported_preview`，该文件不支持预览"},{code:"400",description:"`unsupported_estimate`，该文件不支持估算"},{code:"413",description:"`file_too_large`，文件太大"},{code:"415",description:"`unsupported_file_type`，不支持的扩展名，当前只接受文档类文件"},{code:"503",description:"`s3_connection_failed`，无法连接到 S3 服务"},{code:"503",description:"`s3_permission_denied`，无权限上传文件到 S3"},{code:"503",description:"`s3_file_too_large`，文件超出 S3 大小限制"}]},{id:"Stop",url:"/chat-messages/:task_id/stop",method:"POST",title:"停止响应",description:"仅支持流式模式。",pathParams:[{name:"task_id",type:"string",description:"任务 ID，可在流式返回 Chunk 中获取"}],requestBody:[{name:"user",type:"string",description:"用户标识，用于定义终端用户的身份，必须和发送消息接口传入 user 保持一致。"}],responses:[{name:"result",type:"string",description:"固定返回 success"}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/chat-messages/:task_id/stop' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json' \\
--data-raw '{
    "user": "admin"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]}]};function $(t){return e.jsx(u,{template:J,appDetail:t.appDetail,inputs:t.inputs})}function Q(t){return e.jsx(u,{template:V,appDetail:t.appDetail,inputs:t.inputs})}const Y={title:"Workflow 应用 API",description:"Workflow 应用无会话支持，适合用于翻译/文章写作/总结 AI 等等。",baseUrl:"{{appDetail.api_base_url}}",authentication:{type:"Bearer Token",description:"Service API 使用 `API-Key` 进行鉴权。\n**强烈建议开发者把 `API-Key` 放在后端存储，而非分享或者放在客户端存储，以免 `API-Key` 泄露，导致财产损失。**\n所有 API 请求都应在 **`Authorization`** HTTP Header 中包含您的 `API-Key`，如下所示：",example:"Authorization: Bearer {API_KEY}"},labels:{baseUrl:"Base URL",authentication:"Authentication",pathParams:"Path Params",queryParams:"Query",requestBody:"Request Body",response:"Response",errors:"Errors",requestExample:"Request Example",default:"默认",options:"可选值",streamingStructureDiffers:"流式块中根据 `event` 不同，结构也不同，包含以下类型：",errorInformation:"错误信息",errorCodeReturned:"返回的错误代码",errorStatusReturned:"返回的错误状态",errorMessageReturned:"返回的错误消息",errorTableCode:"code",errorTableStatus:"status",errorTableMessage:"message",interfaceDefinition:"接口定义",path:"Path",method:"Method",contentType:"Content-Type",authorization:"Authorization",basicInfo:"基础信息"},endpoints:[{id:"Execute-Workflow",url:"/workflows/run",method:"POST",title:"执行 workflow",description:"执行 workflow，没有已发布的 workflow，不可执行。",requestBody:[{name:"inputs",type:"object",description:`允许传入 App 定义的各变量值。
inputs 参数包含了多组键值对（Key/Value pairs），每组的键对应一个特定变量，每组的值则是该变量的具体值。`},{name:"response_mode",type:"string",description:"返回响应模式，支持：\n- `streaming` 流式模式（推荐）。基于 SSE（**[Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)**）实现类似打字机输出方式的流式返回。\n- `blocking` 阻塞模式，等待执行完毕后返回结果。（请求若流程较长可能会被中断）。\n由于 Cloudflare 限制，请求会在 100 秒超时无返回后中断。"},{name:"user",type:"string",description:`用户标识，用于定义终端用户的身份，方便检索、统计。
由开发者定义规则，需保证用户标识在应用内唯一。`},{name:"files",type:"array[object]",description:"文件列表，适用于传入文件结合文本理解并回答问题，仅当模型支持 Vision 能力时可用。\n- `type` (string) 支持类型：\n  - `document` 具体类型包含：'TXT', 'MD', 'MARKDOWN', 'PDF', 'XLSX', 'XLS', 'DOC', 'DOCX', 'WPS', 'WPT', 'ET', 'ETT', 'CSV', 'EML', 'MSG', 'PPTX', 'PPT', 'XML', 'EPUB'\n  - `image` 具体类型包含：'JPG', 'JPEG', 'PNG', 'GIF', 'WEBP', 'SVG'\n  - `audio` 具体类型包含：'MP3', 'M4A', 'WAV'\n  - `video` 具体类型包含：'MP4', 'WEBM'\n- `transfer_method` (string) 传递方式，`remote_url` 图片地址 / `local_file` 上传文件\n- `url` (string) 图片地址（仅当传递方式为 `remote_url` 时）\n- `upload_file_id` (string) (string) 上传文件 ID（仅当传递方式为 `local_file` 时）"}],responseSection:{generalDescription:"当 `response_mode` 为 `blocking` 时，返回 CompletionResponse object。\n当 `response_mode` 为 `streaming`时，返回 ChunkCompletionResponse object 流式序列。",responseTypes:[{title:"CompletionResponse",description:"返回完整的 App 结果，`Content-Type` 为 `application/json` 。",fields:[{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"workflow 执行 ID"},{name:"workflow_id",type:"string",description:"关联 Workflow ID"},{name:"status",type:"string",description:"执行状态, `running` / `succeeded` / `failed` / `stopped`"},{name:"outputs",type:"json",description:"Optional 输出内容"},{name:"error",type:"string",description:"Optional 错误原因"},{name:"elapsed_time",type:"float",description:"Optional 耗时(s)"},{name:"total_tokens",type:"int",description:"Optional 总使用 tokens"},{name:"total_steps",type:"int",description:"总步数（冗余），默认 0"},{name:"created_at",type:"timestamp",description:"开始时间"},{name:"finished_at",type:"timestamp",description:"结束时间"}]}]},{title:"ChunkCompletionResponse",description:"返回 App 输出的流式块，`Content-Type` 为 `text/event-stream`。\n每个流式块均为 data: 开头，块之间以 `\\n\\n` 即两个换行符分隔，如下所示：",events:[{name:"event: workflow_started",description:"workflow 开始执行",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"event",type:"string",description:"固定为 `workflow_started`"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"workflow 执行 ID"},{name:"workflow_id",type:"string",description:"关联 Workflow ID"},{name:"sequence_number",type:"int",description:"自增序号，App 内自增，从 1 开始"},{name:"created_at",type:"timestamp",description:"开始时间"}]}]},{name:"event: node_started",description:"node 开始执行",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"event",type:"string",description:"固定为 `node_started`"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"workflow 执行 ID"},{name:"node_id",type:"string",description:"节点 ID"},{name:"node_type",type:"string",description:"节点类型"},{name:"title",type:"string",description:"节点名称"},{name:"index",type:"int",description:"执行序号，用于展示 Tracing Node 顺序"},{name:"predecessor_node_id",type:"string",description:"前置节点 ID，用于画布展示执行路径"},{name:"inputs",type:"array[object]",description:"节点中所有使用到的前置节点变量内容"},{name:"created_at",type:"timestamp",description:"开始时间"}]}]},{name:"event: node_finished",description:"node 执行结束，成功失败同一事件中不同状态",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"event",type:"string",description:"固定为 `node_finished`"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"node 执行 ID"},{name:"node_id",type:"string",description:"节点 ID"},{name:"index",type:"int",description:"执行序号，用于展示 Tracing Node 顺序"},{name:"predecessor_node_id",type:"string",description:"optional 前置节点 ID，用于画布展示执行路径"},{name:"inputs",type:"array[object]",description:"节点中所有使用到的前置节点变量内容"},{name:"process_data",type:"json",description:"Optional 节点过程数据"},{name:"outputs",type:"json",description:"Optional 输出内容"},{name:"status",type:"string",description:"执行状态 `running` / `succeeded` / `failed` / `stopped`"},{name:"error",type:"string",description:"Optional 错误原因"},{name:"elapsed_time",type:"float",description:"Optional 耗时(s)"},{name:"execution_metadata",type:"json",description:"元数据",children:[{name:"total_tokens",type:"int",description:"optional 总使用 tokens"},{name:"total_price",type:"decimal",description:"optional 总费用"},{name:"currency",type:"string",description:"optional 货币，如 `USD` / `RMB`"}]},{name:"created_at",type:"timestamp",description:"开始时间"}]}]},{name:"event: workflow_finished",description:"workflow 执行结束，成功失败同一事件中不同状态",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"workflow_run_id",type:"string",description:"workflow 执行 ID"},{name:"event",type:"string",description:"固定为 `workflow_finished`"},{name:"data",type:"object",description:"详细内容",children:[{name:"id",type:"string",description:"workflow 执行 ID"},{name:"workflow_id",type:"string",description:"关联 Workflow ID"},{name:"status",type:"string",description:"执行状态 `running` / `succeeded` / `failed` / `stopped`"},{name:"outputs",type:"json",description:"Optional 输出内容"},{name:"error",type:"string",description:"Optional 错误原因"},{name:"elapsed_time",type:"float",description:"Optional 耗时(s)"},{name:"total_tokens",type:"int",description:"Optional 总使用 tokens"},{name:"total_steps",type:"int",description:"总步数（冗余），默认 0"},{name:"created_at",type:"timestamp",description:"开始时间"},{name:"finished_at",type:"timestamp",description:"结束时间"}]}]},{name:"event: tts_message",description:"TTS 音频流事件，即：语音合成输出。内容是Mp3格式的音频块，使用 base64 编码后的字符串，播放的时候直接解码即可。(开启自动播放才有此消息)",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"audio",type:"string",description:"语音合成之后的音频块使用 Base64 编码之后的文本内容，播放的时候直接 base64 解码送入播放器即可"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: tts_message_end",description:"TTS 音频流结束事件，收到这个事件表示音频流返回结束。",fields:[{name:"task_id",type:"string",description:"任务 ID，用于请求跟踪和下方的停止响应接口"},{name:"message_id",type:"string",description:"消息唯一 ID"},{name:"audio",type:"string",description:"结束事件是没有音频的，所以这里是空字符串"},{name:"created_at",type:"int",description:"创建时间戳，如：1705395332"}]},{name:"event: ping",description:"每 10s 一次的 ping 事件，保持连接存活。",fields:[]}],streamingExample:{language:"streaming",title:"Response",code:'data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\\n\\n'}}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/workflows/run' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "inputs": {},
    "response_mode": "streaming",
    "user": "abc-123"
}'`},{language:"json",title:"Blocking Mode",code:`{
    "workflow_run_id": "djflajgkldjgd",
    "task_id": "9da23599-e713-473b-982c-4328d4f5c78a",
    "data": {
        "id": "fdlsjfjejkghjda",
        "workflow_id": "fldjaslkfjlsda",
        "status": "succeeded",
        "outputs": {
          "text": "Nice to meet you."
        },
        "error": null,
        "elapsed_time": 0.875,
        "total_tokens": 3562,
        "total_steps": 8,
        "created_at": 1705407629,
        "finished_at": 1727807631
    }
}`},{language:"streaming",title:"Streaming Mode",code:`  data: {"event": "workflow_started", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "workflow_id": "dfjasklfjdslag", "sequence_number": 1, "created_at": 1679586595}}
  data: {"event": "node_started", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "node_id": "dfjasklfjdslag", "node_type": "start", "title": "Start", "index": 0, "predecessor_node_id": "fdljewklfklgejlglsd", "inputs": {}, "created_at": 1679586595}}
  data: {"event": "node_finished", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "node_id": "dfjasklfjdslag", "node_type": "start", "title": "Start", "index": 0, "predecessor_node_id": "fdljewklfklgejlglsd", "inputs": {}, "outputs": {}, "status": "succeeded", "elapsed_time": 0.324, "execution_metadata": {"total_tokens": 63127864, "total_price": 2.378, "currency": "USD"},  "created_at": 1679586595}}
  data: {"event": "workflow_finished", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "workflow_id": "dfjasklfjdslag", "outputs": {}, "status": "succeeded", "elapsed_time": 0.324, "total_tokens": 63127864, "total_steps": "1", "created_at": 1679586595, "finished_at": 1679976595}}
  data: {"event": "tts_message", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"}
  data: {"event": "tts_message_end", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": ""}`}],errors:[{code:"400",description:"`invalid_param`，传入参数异常"},{code:"400",description:"`app_unavailable`，App 配置不可用"},{code:"400",description:"`provider_not_initialize`，无可用模型凭据配置"},{code:"400",description:"`provider_quota_exceeded`，模型调用额度不足"},{code:"400",description:"`model_currently_not_support`，当前模型不可用"},{code:"400",description:"`workflow_request_error`，workflow 执行失败"},{code:"500",description:"服务内部异常"}]},{id:"get-workflow-run-detail",url:"/workflows/run/:workflow_id",method:"GET",title:"获取workflow执行情况",description:"根据 workflow 执行 ID 获取 workflow 任务当前执行结果",pathParams:[{name:"workflow_id",type:"string",description:"workflow 执行 ID，可在流式返回 Chunk 中获取"}],responses:[{name:"id",type:"string",description:"workflow 执行 ID"},{name:"workflow_id",type:"string",description:"关联的 Workflow ID"},{name:"status",type:"string",description:"执行状态 `running` / `succeeded` / `failed` / `stopped`"},{name:"inputs",type:"json",description:"任务输入内容"},{name:"outputs",type:"json",description:"任务输出内容"},{name:"error",type:"string",description:"错误原因"},{name:"total_steps",type:"int",description:"任务执行总步数"},{name:"total_tokens",type:"int",description:"任务执行总 tokens"},{name:"created_at",type:"timestamp",description:"任务开始时间"},{name:"finished_at",type:"timestamp",description:"任务结束时间"},{name:"elapsed_time",type:"float",description:"耗时(s)"}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/workflows/run/:workflow_id' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json'`},{language:"json",title:"Response",code:`{
    "id": "b1ad3277-089e-42c6-9dff-6820d94fbc76",
    "workflow_id": "19eff89f-ec03-4f75-b0fc-897e7effea02",
    "status": "succeeded",
    "inputs": "{\\"sys.files\\": [], \\"sys.user_id\\": \\"abc-123\\"}",
    "outputs": null,
    "error": null,
    "total_steps": 3,
    "total_tokens": 0,
    "created_at": "Thu, 18 Jul 2024 03:17:40 -0000",
    "finished_at": "Thu, 18 Jul 2024 03:18:10 -0000",
    "elapsed_time": 30.098514399956912
}`}]},{id:"stop-generatebacks",url:"/workflows/tasks/:task_id/stop",method:"POST",title:"停止响应",description:"仅支持流式模式。",pathParams:[{name:"task_id",type:"string",description:"任务 ID，可在流式返回 Chunk 中获取"}],requestBody:[{name:"user",type:"string",description:"用户标识，用于定义终端用户的身份，必须和发送消息接口传入 user 保持一致。"}],responses:[{name:"result",type:"string",description:'固定返回 "success"'}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/workflows/tasks/:task_id/stop' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json' \\
--data-raw '{
    "user": "abc-123"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"parameters",url:"/parameters",method:"GET",title:"获取应用配置信息",description:"用于进入页面一开始，获取功能开关、输入参数名称、类型及默认值等使用。",queryParams:[{name:"user",type:"string",description:"用户标识，由开发者定义规则，需保证用户标识在应用内唯一。"}],responses:[{name:"user_input_form",type:"array[object]",description:"用户输入表单配置",children:[{name:"text-input",type:"object",description:"文本输入控件",children:[{name:"label",type:"string",description:"控件展示标签名"},{name:"variable",type:"string",description:"控件 ID"},{name:"required",type:"bool",description:"是否必填"},{name:"default",type:"string",description:"默认值"}]},{name:"paragraph",type:"object",description:"段落文本输入控件",children:[{name:"label",type:"string",description:"控件展示标签名"},{name:"variable",type:"string",description:"控件 ID"},{name:"required",type:"bool",description:"是否必填"},{name:"default",type:"string",description:"默认值"}]},{name:"select",type:"object",description:"下拉控件",children:[{name:"label",type:"string",description:"控件展示标签名"},{name:"variable",type:"string",description:"控件 ID"},{name:"required",type:"bool",description:"是否必填"},{name:"default",type:"string",description:"默认值"},{name:"options",type:"array[string]",description:"选项值"}]}]},{name:"file_upload",type:"object",description:"文件上传配置",children:[{name:"image",type:"object",description:"图片设置\n当前仅支持图片类型：`jpg`, `jpeg`, `png`， `webp`, `gif`, `svg`",children:[{name:"enabled",type:"bool",description:"是否开启"},{name:"number_limits",type:"int",description:"图片数量限制，默认 3"},{name:"transfer_methods",type:"array[string]",description:"传递方式列表，remote_url , local_file，必选一个"}]}]},{name:"system_parameters",type:"object",description:"系统参数",children:[{name:"image_file_size_limit",type:"string",description:"图片文件上传大小限制（MB）"}]}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/parameters?user=abc-123' \\
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
  "user_input_form": [
      {
          "paragraph": {
              "label": "Query",
              "variable": "query",
              "required": true,
              "default": ""
          }
      }
  ],
  "file_upload": {
      "image": {
          "enabled": false,
          "number_limits": 3,
          "detail": "high",
          "transfer_methods": [
              "remote_url",
              "local_file"
          ]
      }
  },
  "system_parameters": {
      "image_file_size_limit": "10"
  }
}`}]},{id:"Get-Workflow-Logs",url:"/workflows/logs",method:"GET",title:"获取 workflow 日志",description:"倒序返回workflow日志",queryParams:[{name:"keyword",type:"string",description:"关键字"},{name:"status",type:"string",description:"执行状态 succeeded/failed/stopped"},{name:"page",type:"int",description:"当前页码, 默认1."},{name:"limit",type:"int",description:"每页条数, 默认20."}],responses:[{name:"page",type:"int",description:"当前页码"},{name:"limit",type:"int",description:"每页条数"},{name:"total",type:"int",description:"总条数"},{name:"has_more",type:"bool",description:"是否还有更多数据"},{name:"data",type:"array[object]",description:"当前页码的数据",children:[{name:"id",type:"string",description:"标识"},{name:"workflow_run",type:"object",description:"Workflow 执行日志",children:[{name:"id",type:"string",description:"标识"},{name:"version",type:"string",description:"版本"},{name:"status",type:"string",description:"执行状态, `running` / `succeeded` / `failed` / `stopped`"},{name:"error",type:"string",description:"(可选) 错误"},{name:"elapsed_time",type:"float",description:"耗时，单位秒"},{name:"total_tokens",type:"int",description:"消耗的token数量"},{name:"total_steps",type:"int",description:"执行步骤长度"},{name:"created_at",type:"timestamp",description:"开始时间"},{name:"finished_at",type:"timestamp",description:"结束时间"}]},{name:"created_from",type:"string",description:"来源"},{name:"created_by_role",type:"string",description:"角色"},{name:"created_by_account",type:"string",description:"(可选) 帐号"},{name:"created_by_end_user",type:"object",description:"用户",children:[{name:"id",type:"string",description:"标识"},{name:"type",type:"string",description:"类型"},{name:"is_anonymous",type:"bool",description:"是否匿名"},{name:"session_id",type:"string",description:"会话标识"}]},{name:"created_at",type:"timestamp",description:"创建时间"}]}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/workflows/logs?limit=1'
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
    "page": 1,
    "limit": 1,
    "total": 7,
    "has_more": true,
    "data": [
        {
            "id": "e41b93f1-7ca2-40fd-b3a8-999aeb499cc0",
            "workflow_run": {
                "id": "c0640fc8-03ef-4481-a96c-8a13b732a36e",
                "version": "2024-08-01 12:17:09.771832",
                "status": "succeeded",
                "error": null,
                "elapsed_time": 1.3588523610014818,
                "total_tokens": 0,
                "total_steps": 3,
                "created_at": 1726139643,
                "finished_at": 1726139644
            },
            "created_from": "service-api",
            "created_by_role": "end_user",
            "created_by_account": null,
            "created_by_end_user": {
                "id": "7f7d9117-dd9d-441d-8970-87e5e7e687a3",
                "type": "service_api",
                "is_anonymous": false,
                "session_id": "abc-123"
            },
            "created_at": 1726139644
        }
    ]
}`}]}]},Z={title:"Workflow App API",description:"Workflow applications offers non-session support and is ideal for translation, article writing, summarization AI, and more.",baseUrl:"{{appDetail.api_base_url}}",authentication:{type:"Bearer Token",description:"The Service API uses `API-Key` authentication.\n**Strongly recommend storing your API Key on the server-side, not shared or stored on the client-side, to avoid possible API-Key leakage that can lead to serious consequences.**\nFor all API requests, include your API Key in the `Authorization` HTTP Header, as shown below:",example:"Authorization: Bearer {API_KEY}"},labels:{baseUrl:"Base URL",authentication:"Authentication",pathParams:"Path",queryParams:"Query",requestBody:"Request Body",response:"Response",errors:"Errors",requestExample:"Request Example",default:"Default",options:"Options",streamingStructureDiffers:"The structure of the streaming chunks varies depending on the `event`:",errorInformation:"Error Information",errorCodeReturned:"Returned error code",errorStatusReturned:"Returned error status",errorMessageReturned:"Returned error message",errorTableCode:"code",errorTableStatus:"status",errorTableMessage:"message",interfaceDefinition:"Interface Definition",path:"Path",method:"Method",contentType:"Content-Type",authorization:"Authorization",basicInfo:"Basic Information"},endpoints:[{id:"Execute-Workflow",url:"/workflows/run",method:"POST",title:"Execute workflow",description:"Execute workflow, cannot be executed without a published workflow.",requestBody:[{name:"inputs",type:"object",description:"Allows the entry of various variable values defined by the App.\nThe `inputs` parameter contains multiple key/value pairs, with each key corresponding to a specific variable and each value being the specific value for that variable.\nThe workflow application requires at least one key/value pair to be inputted."},{name:"response_mode",type:"string",description:"The mode of response return, supporting:\n- `streaming` Streaming mode (recommended), implements a typewriter-like output through SSE ([Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)).\n- `blocking` Blocking mode, returns result after execution is complete. (Requests may be interrupted if the process is long)\nDue to Cloudflare restrictions, the request will be interrupted without a return after 100 seconds."},{name:"user",type:"string",description:`User identifier, used to define the identity of the end-user for retrieval and statistics.
Should be uniquely defined by the developer within the application.`},{name:"files",type:"array[object]",description:"File list, suitable for inputting files (images) combined with text understanding and answering questions, available only when the model supports Vision capability.\n- `type` (string) Supported type: `image` (currently only supports image type)\n- `transfer_method` (string) Transfer method, `remote_url` for image URL / `local_file` for file upload\n- `url` (string) Image URL (when the transfer method is `remote_url`)\n- `upload_file_id` (string) Uploaded file ID, which must be obtained by uploading through the File Upload API in advance (when the transfer method is `local_file`)"}],responseSection:{generalDescription:"When `response_mode` is `blocking`, return a CompletionResponse object.\nWhen `response_mode` is `streaming`, return a ChunkCompletionResponse stream.",responseTypes:[{title:"CompletionResponse",description:"Returns the App result, `Content-Type` is `application/json`.",fields:[{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"data",type:"object",description:"detail of result",children:[{name:"id",type:"string",description:"ID of workflow execution"},{name:"workflow_id",type:"string",description:"ID of related workflow"},{name:"status",type:"string",description:"status of execution, `running` / `succeeded` / `failed` / `stopped`"},{name:"outputs",type:"json",description:"Optional content of output"},{name:"error",type:"string",description:"Optional reason of error"},{name:"elapsed_time",type:"float",description:"Optional total seconds to be used"},{name:"total_tokens",type:"int",description:"Optional tokens to be used"},{name:"total_steps",type:"int",description:"default 0"},{name:"created_at",type:"timestamp",description:"start time"},{name:"finished_at",type:"timestamp",description:"end time"}]}]},{title:"ChunkCompletionResponse",description:"Returns the stream chunks outputted by the App, `Content-Type` is `text/event-stream`.\nEach streaming chunk starts with `data:`, separated by two newline characters `\\n\\n`, as shown below:",events:[{name:"event: workflow_started",description:"workflow starts execution",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"event",type:"string",description:"fixed to `workflow_started`"},{name:"data",type:"object",description:"detail",children:[{name:"id",type:"string",description:"Unique ID of workflow execution"},{name:"workflow_id",type:"string",description:"ID of related workflow"},{name:"sequence_number",type:"int",description:"Self-increasing serial number, self-increasing in the App, starting from 1"},{name:"created_at",type:"timestamp",description:"Creation timestamp, e.g., 1705395332"}]}]},{name:"event: node_started",description:"node execution started",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"event",type:"string",description:"fixed to `node_started`"},{name:"data",type:"object",description:"detail",children:[{name:"id",type:"string",description:"Unique ID of workflow execution"},{name:"node_id",type:"string",description:"ID of node"},{name:"node_type",type:"string",description:"type of node"},{name:"title",type:"string",description:"name of node"},{name:"index",type:"int",description:"Execution sequence number, used to display Tracing Node sequence"},{name:"predecessor_node_id",type:"string",description:"optional Prefix node ID, used for canvas display execution path"},{name:"inputs",type:"array[object]",description:"Contents of all preceding node variables used in the node"},{name:"created_at",type:"timestamp",description:"timestamp of start, e.g., 1705395332"}]}]},{name:"event: node_finished",description:"node execution ends, success or failure in different states in the same event",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"event",type:"string",description:"fixed to `node_finished`"},{name:"data",type:"object",description:"detail",children:[{name:"id",type:"string",description:"Unique ID of workflow execution"},{name:"node_id",type:"string",description:"ID of node"},{name:"node_type",type:"string",description:"type of node"},{name:"title",type:"string",description:"name of node"},{name:"index",type:"int",description:"Execution sequence number, used to display Tracing Node sequence"},{name:"predecessor_node_id",type:"string",description:"optional Prefix node ID, used for canvas display execution path"},{name:"inputs",type:"array[object]",description:"Contents of all preceding node variables used in the node"},{name:"process_data",type:"json",description:"Optional node process data"},{name:"outputs",type:"json",description:"Optional content of output"},{name:"status",type:"string",description:"status of execution, `running` / `succeeded` / `failed` / `stopped`"},{name:"error",type:"string",description:"Optional reason of error"},{name:"elapsed_time",type:"float",description:"Optional total seconds to be used"},{name:"execution_metadata",type:"json",description:"meta data",children:[{name:"total_tokens",type:"int",description:"optional tokens to be used"},{name:"total_price",type:"decimal",description:"optional Total cost"},{name:"currency",type:"string",description:"optional e.g. `USD` / `RMB`"}]},{name:"created_at",type:"timestamp",description:"timestamp of start, e.g., 1705395332"}]}]},{name:"event: workflow_finished",description:"workflow execution ends, success or failure in different states in the same event",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the below Stop Generate API"},{name:"workflow_run_id",type:"string",description:"Unique ID of workflow execution"},{name:"event",type:"string",description:"fixed to `workflow_finished`"},{name:"data",type:"object",description:"detail",children:[{name:"id",type:"string",description:"ID of workflow execution"},{name:"workflow_id",type:"string",description:"ID of related workflow"},{name:"status",type:"string",description:"status of execution, `running` / `succeeded` / `failed` / `stopped`"},{name:"outputs",type:"json",description:"Optional content of output"},{name:"error",type:"string",description:"Optional reason of error"},{name:"elapsed_time",type:"float",description:"Optional total seconds to be used"},{name:"total_tokens",type:"int",description:"Optional tokens to be used"},{name:"total_steps",type:"int",description:"default 0"},{name:"created_at",type:"timestamp",description:"start time"},{name:"finished_at",type:"timestamp",description:"end time"}]}]},{name:"event: tts_message",description:"TTS audio stream event, that is, speech synthesis output. The content is an audio block in Mp3 format, encoded as a base64 string. When playing, simply decode the base64 and feed it into the player. (This message is available only when auto-play is enabled)",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the stop response interface below"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"audio",type:"string",description:"The audio after speech synthesis, encoded in base64 text content, when playing, simply decode the base64 and feed it into the player"},{name:"created_at",type:"int",description:"Creation timestamp, e.g.: 1705395332"}]},{name:"event: tts_message_end",description:"TTS audio stream end event, receiving this event indicates the end of the audio stream.",fields:[{name:"task_id",type:"string",description:"Task ID, used for request tracking and the stop response interface below"},{name:"message_id",type:"string",description:"Unique message ID"},{name:"audio",type:"string",description:"The end event has no audio, so this is an empty string"},{name:"created_at",type:"int",description:"Creation timestamp, e.g.: 1705395332"}]},{name:"event: ping",description:"Ping event every 10 seconds to keep the connection alive.",fields:[]}],streamingExample:{language:"streaming",title:"Response",code:'data: {"event": "message", "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227", "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c", "answer": "Hi", "created_at": 1705398420}\\n\\n'}}]},codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/workflows/run' \\
--header 'Authorization: Bearer {api_key}' \\
--header 'Content-Type: application/json' \\
--data-raw '{
    "inputs": {},
    "response_mode": "streaming",
    "user": "abc-123"
}'`},{language:"json",title:"Blocking Mode",code:`{
    "workflow_run_id": "djflajgkldjgd",
    "task_id": "9da23599-e713-473b-982c-4328d4f5c78a",
    "data": {
        "id": "fdlsjfjejkghjda",
        "workflow_id": "fldjaslkfjlsda",
        "status": "succeeded",
        "outputs": {
          "text": "Nice to meet you."
        },
        "error": null,
        "elapsed_time": 0.875,
        "total_tokens": 3562,
        "total_steps": 8,
        "created_at": 1705407629,
        "finished_at": 1727807631
    }
}`},{language:"streaming",title:"Streaming Mode",code:`  data: {"event": "workflow_started", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "workflow_id": "dfjasklfjdslag", "sequence_number": 1, "created_at": 1679586595}}
  data: {"event": "node_started", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "node_id": "dfjasklfjdslag", "node_type": "start", "title": "Start", "index": 0, "predecessor_node_id": "fdljewklfklgejlglsd", "inputs": {}, "created_at": 1679586595}}
  data: {"event": "node_finished", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "node_id": "dfjasklfjdslag", "node_type": "start", "title": "Start", "index": 0, "predecessor_node_id": "fdljewklfklgejlglsd", "inputs": {}, "outputs": {}, "status": "succeeded", "elapsed_time": 0.324, "execution_metadata": {"total_tokens": 63127864, "total_price": 2.378, "currency": "USD"},  "created_at": 1679586595}}
  data: {"event": "workflow_finished", "task_id": "5ad4cb98-f0c7-4085-b384-88c403be6290", "workflow_run_id": "5ad498-f0c7-4085-b384-88cbe6290", "data": {"id": "5ad498-f0c7-4085-b384-88cbe6290", "workflow_id": "dfjasklfjdslag", "outputs": {}, "status": "succeeded", "elapsed_time": 0.324, "total_tokens": 63127864, "total_steps": "1", "created_at": 1679586595, "finished_at": 1679976595}}
  data: {"event": "tts_message", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": "qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"}
  data: {"event": "tts_message_end", "conversation_id": "23dd85f3-1a41-4ea0-b7a9-062734ccfaf9", "message_id": "a8bdc41c-13b2-4c18-bfd9-054b9803038c", "created_at": 1721205487, "task_id": "3bf8a0bb-e73b-4690-9e66-4e429bad8ee7", "audio": ""}`}],errors:[{code:"400",description:"`invalid_param`, abnormal parameter input"},{code:"400",description:"`app_unavailable`, App configuration unavailable"},{code:"400",description:"`provider_not_initialize`, no available model credential configuration"},{code:"400",description:"`provider_quota_exceeded`, model invocation quota insufficient"},{code:"400",description:"`model_currently_not_support`, current model unavailable"},{code:"400",description:"`workflow_request_error`, workflow execution failed"},{code:"500",description:"internal server error"}]},{id:"get-workflow-run-detail",url:"/workflows/run/:workflow_id",method:"GET",title:"Get Workflow Run Detail",description:"Retrieve the current execution results of a workflow task based on the workflow execution ID.",pathParams:[{name:"workflow_id",type:"string",description:"Workflow ID, can be obtained from the streaming chunk return"}],responses:[{name:"id",type:"string",description:"ID of workflow execution"},{name:"workflow_id",type:"string",description:"ID of related workflow"},{name:"status",type:"string",description:"status of execution, `running` / `succeeded` / `failed` / `stopped`"},{name:"inputs",type:"json",description:"content of input"},{name:"outputs",type:"json",description:"content of output"},{name:"error",type:"string",description:"reason of error"},{name:"total_steps",type:"int",description:"total steps of task"},{name:"total_tokens",type:"int",description:"total tokens to be used"},{name:"created_at",type:"timestamp",description:"start time"},{name:"finished_at",type:"timestamp",description:"end time"},{name:"elapsed_time",type:"float",description:"total seconds to be used"}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/workflows/run/:workflow_id' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json'`},{language:"json",title:"Response",code:`{
    "id": "b1ad3277-089e-42c6-9dff-6820d94fbc76",
    "workflow_id": "19eff89f-ec03-4f75-b0fc-897e7effea02",
    "status": "succeeded",
    "inputs": "{\\"sys.files\\": [], \\"sys.user_id\\": \\"abc-123\\"}",
    "outputs": null,
    "error": null,
    "total_steps": 3,
    "total_tokens": 0,
    "created_at": "Thu, 18 Jul 2024 03:17:40 -0000",
    "finished_at": "Thu, 18 Jul 2024 03:18:10 -0000",
    "elapsed_time": 30.098514399956912
}`}]},{id:"stop-generatebacks",url:"/workflows/tasks/:task_id/stop",method:"POST",title:"Stop Generate",description:"Only supported in streaming mode.",pathParams:[{name:"task_id",type:"string",description:"Task ID, can be obtained from the streaming chunk return"}],requestBody:[{name:"user",type:"string",description:"User identifier, used to define the identity of the end-user, must be consistent with the user passed in the send message interface."}],responses:[{name:"result",type:"string",description:'Always returns "success"'}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X POST '{{appDetail.api_base_url}}/workflows/tasks/:task_id/stop' \\
-H 'Authorization: Bearer {api_key}' \\
-H 'Content-Type: application/json' \\
--data-raw '{
    "user": "abc-123"
}'`},{language:"json",title:"Response",code:`{
  "result": "success"
}`}]},{id:"parameters",url:"/parameters",method:"GET",title:"Get Application Information",description:"Used at the start of entering the page to obtain information such as features, input parameter names, types, and default values.",queryParams:[{name:"user",type:"string",description:"User identifier, defined by the developer's rules, must be unique within the application."}],responses:[{name:"user_input_form",type:"array[object]",description:"User input form configuration",children:[{name:"text-input",type:"object",description:"Text input control",children:[{name:"label",type:"string",description:"Variable display label name"},{name:"variable",type:"string",description:"Variable ID"},{name:"required",type:"bool",description:"Whether it is required"},{name:"default",type:"string",description:"Default value"}]},{name:"paragraph",type:"object",description:"Paragraph text input control",children:[{name:"label",type:"string",description:"Variable display label name"},{name:"variable",type:"string",description:"Variable ID"},{name:"required",type:"bool",description:"Whether it is required"},{name:"default",type:"string",description:"Default value"}]},{name:"select",type:"object",description:"Dropdown control",children:[{name:"label",type:"string",description:"Variable display label name"},{name:"variable",type:"string",description:"Variable ID"},{name:"required",type:"bool",description:"Whether it is required"},{name:"default",type:"string",description:"Default value"},{name:"options",type:"array[string]",description:"Option values"}]}]},{name:"file_upload",type:"object",description:"File upload configuration",children:[{name:"image",type:"object",description:"Image settings\nCurrently only supports image types: `png`, `jpg`, `jpeg`, `webp`, `gif`",children:[{name:"enabled",type:"bool",description:"Whether it is enabled"},{name:"number_limits",type:"int",description:"Image number limit, default is 3"},{name:"transfer_methods",type:"array[string]",description:"List of transfer methods, remote_url, local_file, must choose one"}]}]},{name:"system_parameters",type:"object",description:"System parameters",children:[{name:"image_file_size_limit",type:"string",description:"Image file upload size limit (MB)"}]}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/parameters?user=abc-123' \\
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
  "user_input_form": [
      {
          "paragraph": {
              "label": "Query",
              "variable": "query",
              "required": true,
              "default": ""
          }
      }
  ],
  "file_upload": {
      "image": {
          "enabled": false,
          "number_limits": 3,
          "detail": "high",
          "transfer_methods": [
              "remote_url",
              "local_file"
          ]
      }
  },
  "system_parameters": {
      "image_file_size_limit": "10"
  }
}`}]},{id:"Get-Workflow-Logs",url:"/workflows/logs",method:"GET",title:"Get workflow logs",description:"Returns workflow logs, with the first page returning the latest `{limit}` messages, i.e., in reverse order.",queryParams:[{name:"keyword",type:"string",description:"Keyword to search"},{name:"status",type:"string",description:"succeeded/failed/stopped"},{name:"page",type:"int",description:"current page, default is 1."},{name:"limit",type:"int",description:"How many chat history messages to return in one request, default is 20."}],responses:[{name:"page",type:"int",description:"Current page"},{name:"limit",type:"int",description:"Number of returned items, if input exceeds system limit, returns system limit amount"},{name:"total",type:"int",description:"Number of total items"},{name:"has_more",type:"bool",description:"Whether there is a next page"},{name:"data",type:"array[object]",description:"Log list",children:[{name:"id",type:"string",description:"ID"},{name:"workflow_run",type:"object",description:"Workflow run",children:[{name:"id",type:"string",description:"ID"},{name:"version",type:"string",description:"Version"},{name:"status",type:"string",description:"status of execution, `running` / `succeeded` / `failed` / `stopped`"},{name:"error",type:"string",description:"Optional reason of error"},{name:"elapsed_time",type:"float",description:"total seconds to be used"},{name:"total_tokens",type:"int",description:"tokens to be used"},{name:"total_steps",type:"int",description:"default 0"},{name:"created_at",type:"timestamp",description:"start time"},{name:"finished_at",type:"timestamp",description:"end time"}]},{name:"created_from",type:"string",description:"Created from"},{name:"created_by_role",type:"string",description:"Created by role"},{name:"created_by_account",type:"string",description:"Optional Created by account"},{name:"created_by_end_user",type:"object",description:"Created by end user",children:[{name:"id",type:"string",description:"ID"},{name:"type",type:"string",description:"Type"},{name:"is_anonymous",type:"bool",description:"Is anonymous"},{name:"session_id",type:"string",description:"Session ID"}]},{name:"created_at",type:"timestamp",description:"create time"}]}],codeExamples:[{language:"bash",title:"cURL",code:`curl -X GET '{{appDetail.api_base_url}}/workflows/logs?limit=1'
--header 'Authorization: Bearer {api_key}'`},{language:"json",title:"Response",code:`{
    "page": 1,
    "limit": 1,
    "total": 7,
    "has_more": true,
    "data": [
        {
            "id": "e41b93f1-7ca2-40fd-b3a8-999aeb499cc0",
            "workflow_run": {
                "id": "c0640fc8-03ef-4481-a96c-8a13b732a36e",
                "version": "2024-08-01 12:17:09.771832",
                "status": "succeeded",
                "error": null,
                "elapsed_time": 1.3588523610014818,
                "total_tokens": 0,
                "total_steps": 3,
                "created_at": 1726139643,
                "finished_at": 1726139644
            },
            "created_from": "service-api",
            "created_by_role": "end_user",
            "created_by_account": null,
            "created_by_end_user": {
                "id": "7f7d9117-dd9d-441d-8970-87e5e7e687a3",
                "type": "service_api",
                "is_anonymous": false,
                "session_id": "abc-123"
            },
            "created_at": 1726139644
        }
    ]
}`}]}]};function ee(t){return e.jsx(u,{template:Y,appDetail:t.appDetail,inputs:t.inputs})}function te(t){return e.jsx(u,{template:Z,appDetail:t.appDetail,inputs:t.inputs})}function ie(t){return e.jsx(u,{appDetail:t.appDetail,inputs:t.inputs,template:H,enableEnhancedDocs:!0,containerClassName:"bg-transparent"})}function ne(t){return e.jsx(u,{appDetail:t.appDetail,inputs:t.inputs,template:N,enableEnhancedDocs:!0,containerClassName:"bg-transparent"})}const ae=({appDetail:t,apiBaseUrl:a})=>{const{locale:o}=v(k),s=t?.model_config?.configs?.prompt_variables||[],d=s.reduce((l,g)=>(l[g.key]=g.name||"",l),{});return e.jsxs("article",{className:"prose prose-xl",children:[(t?.mode==="chat"||t?.mode==="agent-chat")&&(o!==f[1]?e.jsx($,{appDetail:t,variables:s,inputs:d}):e.jsx(Q,{appDetail:t,variables:s,inputs:d})),t?.mode==="advanced-chat"&&(o!==f[1]?e.jsx(K,{appDetail:t,variables:s,inputs:d}):e.jsx(X,{appDetail:t,variables:s,inputs:d})),t?.mode==="workflow"&&(o!==f[1]?e.jsx(te,{appDetail:t,variables:s,inputs:d}):e.jsx(ee,{appDetail:t,variables:s,inputs:d})),t?.mode==="third-party-chat"&&(o!==f[1]?e.jsx(ie,{appDetail:t,variables:s,inputs:d}):e.jsx(ne,{appDetail:t,variables:s,inputs:d}))]})},se={title:"MCP 服务 API",description:"MCP（Model Context Protocol）是一种用于智能体与外部服务通信的协议。通过 MCP，您可以将智能体连接到外部工具或服务，实现更强大的功能。",baseUrl:"{{appDetail.mcp_base_url}}",authentication:{type:"Bearer Token",description:"MCP 服务使用 `API-Key` 进行鉴权。**强烈建议开发者把 `API-Key` 放在后端存储，而非分享或者放在客户端存储，以免 `API-Key` 泄露，导致财产损失。** 所有 API 请求都应在 **`Authorization`** HTTP Header 中包含您的 `API-Key`，如下所示：",example:"Authorization: Bearer {API_KEY}"},labels:{baseUrl:"基础 URL",authentication:"鉴权",pathParams:"Path Params",queryParams:"Query",requestBody:"Request Body",response:"Response",errors:"Errors",requestExample:"Request Example",default:"默认",options:"可选值",streamingStructureDiffers:"流式块中根据 event 不同，结构也不同：",errorInformation:"错误信息",errorCodeReturned:"返回的错误代码",errorStatusReturned:"返回的错误状态",errorMessageReturned:"返回的错误消息",errorTableCode:"code",errorTableStatus:"status",errorTableMessage:"message",interfaceDefinition:"接口定义",path:"Path",method:"Method",contentType:"Content-Type",authorization:"Authorization",basicInfo:"基础信息"},endpoints:[{id:"mcp-config",url:"/v1/mcp",method:"POST",title:"配置 MCP 工具",description:"通过 JSON 格式配置文件将智能体接入 MCP 工具。将申请到的 API 密钥填入 `Authorization` 字段，即可完成工具配置。",documentation:`## 如何将智能体发布为 MCP 服务

### 操作步骤

1. **进入智能体页面**
   - 打开您创建的智能体
   - 点击右上角的「发布」按钮（如果是更新已发布的版本，点击「更新发布」）

2. **启用 MCP 功能**
   - 在发布设置页面中，勾选「MCP」选项
   - 点击「确认」完成发布

3. **申请 API 密钥**
   - 在智能体的「发布列表」中找到 MCP 选项
   - 点击申请 API 密钥（用于身份验证和访问控制）

> ⚠️ **注意**：API 密钥非常重要，请妥善保管，不要泄露给他人。

---

## 如何创建 MCP 工具

### 操作步骤

1. **进入创建页面**
   - 从「工具」页面进入 MCP 工具创建界面

2. **填写基本信息**
   - 设置工具名称
   - 编写工具描述（让用户了解工具的用途）
   - 选择服务类型

3. **配置 MCP 服务**
   - 按照以下 JSON 格式进行配置
   - 将申请到的 API 密钥填入 \`Authorization\` 字段`,documentationTitle:"使用说明",requestBody:[{name:"mcpServers",type:"object",required:!0,description:"MCP 服务配置的开始标记，包含一个或多个 MCP 服务的配置。",children:[{name:"agent-go",type:"object",required:!0,description:"服务名称（可自定义），包含该服务的连接配置。",children:[{name:"url",type:"string",required:!0,description:"MCP 服务的访问地址。固定值为 `http://agent-go:8080/v1/mcp`。"},{name:"headers",type:"object",required:!0,description:"请求头配置，用于传递身份验证信息。",children:[{name:"Authorization",type:"string",required:!0,description:"身份验证信息，格式为 `Bearer 你的API密钥`。`Bearer` 是 OAuth 2.0 认证方式的一种前缀，后面的密钥就是您的身份凭证。"}]}]}]}],codeExamples:[{language:"json",title:"MCP 配置示例",code:`{
  "mcpServers": {
    "agent-go": {
      "url": "http://agent-go:8080/v1/mcp",
      "headers": {
        "Authorization": "Bearer 你的API密钥"
      }
    }
  }
}`}],responses:[{name:"tools",type:"array",description:"成功连接后，MCP 服务返回可用工具列表。"},{name:"status",type:"string",description:"连接状态，`connected` 表示连接成功。"}]}],errors:[{code:401,description:"API 密钥无效或已过期，请重新申请 API 密钥。"},{code:403,description:"无权限访问该 MCP 服务，请检查 API 密钥是否正确。"},{code:404,description:"MCP 服务地址不存在，请检查 URL 配置是否正确。"},{code:500,description:"服务器内部错误，请稍后重试或联系管理员。"}],errorTable:[{code:"401",status:"Unauthorized",message:"API 密钥无效或已过期"},{code:"403",status:"Forbidden",message:"无权限访问该资源"},{code:"404",status:"Not Found",message:"MCP 服务地址不存在"},{code:"500",status:"Internal Server Error",message:"服务器内部错误"}]},re={title:"MCP Service API",description:"MCP (Model Context Protocol) is a protocol for communication between agents and external services. Through MCP, you can connect your agent to external tools or services, enabling more powerful functionality.",baseUrl:"{{appDetail.mcp_base_url}}",authentication:{type:"Bearer Token",description:"The MCP service uses `API-Key` for authentication. **It is strongly recommended that developers store the `API-Key` on the backend rather than sharing or storing it on the client side, to prevent `API-Key` leakage and financial losses.** All API requests should include your `API-Key` in the **`Authorization`** HTTP Header as follows:",example:"Authorization: Bearer {API_KEY}"},labels:{baseUrl:"Base URL",authentication:"Authentication",pathParams:"Path Params",queryParams:"Query",requestBody:"Request Body",response:"Response",errors:"Errors",requestExample:"Request Example",default:"Default",options:"Options",streamingStructureDiffers:"The structure differs based on the event in streaming chunks:",errorInformation:"Error Information",errorCodeReturned:"Error Code Returned",errorStatusReturned:"Error Status Returned",errorMessageReturned:"Error Message Returned",errorTableCode:"code",errorTableStatus:"status",errorTableMessage:"message",interfaceDefinition:"Interface Definition",path:"Path",method:"Method",contentType:"Content-Type",authorization:"Authorization",basicInfo:"Basic Info"},endpoints:[{id:"mcp-config",url:"/v1/mcp",method:"POST",title:"Configure MCP Tool",description:"Connect your agent to an MCP tool using a JSON configuration file. Fill in the API key you obtained into the `Authorization` field to complete the tool configuration.",documentation:`## How to Publish Agent as MCP Service

### Steps

1. **Go to the Agent Page**
   - Open the agent you created
   - Click the "Publish" button in the upper right corner (if updating an already published version, click "Update Publish")

2. **Enable MCP Feature**
   - On the publish settings page, check the "MCP" option
   - Click "Confirm" to complete the publish

3. **Apply for API Key**
   - Find the MCP option in the agent's "Publish List"
   - Click to apply for an API key (used for identity verification and access control)

> ⚠️ **Note**: The API key is very important. Please keep it safe and do not share it with others.

---

## How to Create an MCP Tool

### Steps

1. **Go to the Creation Page**
   - Enter the MCP tool creation interface from the "Tools" page

2. **Fill in Basic Information**
   - Set the tool name
   - Write a tool description (to help users understand the purpose of the tool)
   - Select the service type

3. **Configure MCP Service**
   - Configure using the following JSON format
   - Fill in the API key you obtained into the \`Authorization\` field`,documentationTitle:"Usage Guide",requestBody:[{name:"mcpServers",type:"object",required:!0,description:"The starting marker for MCP service configuration, containing configurations for one or more MCP services.",children:[{name:"agent-go",type:"object",required:!0,description:"Service name (customizable), containing the connection configuration for this service.",children:[{name:"url",type:"string",required:!0,description:"The access URL of the MCP service. Fixed value: `http://agent-go:8080/v1/mcp`."},{name:"headers",type:"object",required:!0,description:"Request header configuration for passing authentication information.",children:[{name:"Authorization",type:"string",required:!0,description:"Authentication information in the format `Bearer your_api_key`. `Bearer` is a prefix for OAuth 2.0 authentication, and the key after it is your identity credential."}]}]}]}],codeExamples:[{language:"json",title:"MCP Configuration Example",code:`{
  "mcpServers": {
    "agent-go": {
      "url": "http://agent-go:8080/v1/mcp",
      "headers": {
        "Authorization": "Bearer your_api_key"
      }
    }
  }
}`}],responses:[{name:"tools",type:"array",description:"After a successful connection, the MCP service returns a list of available tools."},{name:"status",type:"string",description:"Connection status. `connected` means the connection is successful."}]}],errors:[{code:401,description:"API key is invalid or expired. Please apply for a new API key."},{code:403,description:"No permission to access the MCP service. Please check if the API key is correct."},{code:404,description:"MCP service URL does not exist. Please check if the URL configuration is correct."},{code:500,description:"Internal server error. Please try again later or contact the administrator."}],errorTable:[{code:"401",status:"Unauthorized",message:"API key is invalid or expired"},{code:"403",status:"Forbidden",message:"No permission to access the resource"},{code:"404",status:"Not Found",message:"MCP service URL does not exist"},{code:"500",status:"Internal Server Error",message:"Internal server error"}]};function oe(t){return e.jsx(D,{template:se,mcpBaseUrl:t.appDetail.mcp_base_url})}function de(t){return e.jsx(D,{template:re,mcpBaseUrl:t.appDetail.mcp_base_url})}const pe=({appDetail:t})=>{const{t:a}=h();return e.jsxs(e.Fragment,{children:[e.jsx(w,{value:t.mcp_base_url,children:e.jsx("div",{className:`mr-2 px-[8px] py-[6px] h-[24px] rounded-sm border !border-gray-G5 bg-gray-G6 leading-[12px] text-gray-G2 ${x.customApi}`,children:a("appApi.mcpServer")})}),e.jsxs("div",{className:`flex items-center border h-[36px] px-2 py-[6px] text-xs bg-transparent leading-[20px] rounded
                     ${t.api_enable_mcp?"text-[#2FBD81] bg-[#2FBD81] border-[#2FBD81]":"text-yellow-500 bg-yellow-50 border-yellow-500"}`,children:[e.jsx("div",{className:"mr-1",children:a("common.nouns.status")}),e.jsx("div",{children:t.api_enable_mcp?`${a("appApi.ok")}`:`${a("appApi.disabled")}`})]}),e.jsx(I,{text:a("appApi.mcpKey")||"",variant:"secondary",className:"!bg-transparent",appId:t?.mcp_site?.app_id,disabled:!t?.mcp_site?.app_id})]})},ce=({appDetail:t})=>{const{locale:a}=v(k),o=t?.model_config?.configs?.prompt_variables||[],s=o.reduce((d,l)=>(d[l.key]=l.name||"",d),{});return e.jsx("article",{className:"prose prose-xl",children:a!==f[1]?e.jsx(de,{appDetail:t,variables:o,inputs:s}):e.jsx(oe,{appDetail:t,variables:o,inputs:s})})},le=({appId:t})=>{const a=B(y=>y.appDetail),{t:o}=h(),s=E(),l=U().get("from")==="mcp",g=()=>{s.push(`/apps/${t}/publish`)};return e.jsx("div",{className:"px-3  w-full h-full",children:e.jsxs("div",{className:"relative h-full w-full overflow-hidden flex flex-col cardWrap",children:[e.jsxs("div",{className:"flex items-center justify-between px-6 !shrink-0 h-[60px]",children:[e.jsxs(z,{variant:"text",className:"gap-3",onClick:g,children:[e.jsx(L,{}),e.jsx("span",{children:o("common.operation.publish")})]}),e.jsx("div",{className:"flex items-center gap-3 flex-wrap",children:l?e.jsx(pe,{appDetail:a}):e.jsxs(e.Fragment,{children:[e.jsx(w,{value:a.api_base_url,children:e.jsx("div",{className:`mr-2 px-[8px] py-[6px] h-[24px] rounded-sm border !border-gray-G5 bg-gray-G6 leading-[12px] text-gray-G2 ${x.customApi}`,children:o("appApi.apiServer")})}),e.jsxs("div",{className:`flex items-center border h-[36px] px-2 py-[6px] text-xs bg-transparent leading-[20px] rounded 
                               ${a.api_enable_api?"text-[#2FBD81] bg-[#2FBD81] border-[#2FBD81]":"text-yellow-500 bg-yellow-50 border-yellow-500"}`,children:[e.jsx("div",{className:"mr-1",children:o("common.nouns.status")}),e.jsx("div",{children:a.api_enable_api?`${o("appApi.ok")}`:`${o("appApi.disabled")}`})]}),e.jsx(I,{variant:"secondary",className:"!bg-transparent",appId:a?.api_site?.app_id,disabled:!a?.api_site?.app_id})]})})]}),e.jsx("div",{className:"mx-2 py-6 overflow-y-auto grow",children:l?e.jsx(ce,{appDetail:a}):e.jsx(ae,{appDetail:a})})]})})},me=()=>{const{appId:t}=R();return e.jsx(le,{appId:t})},xe=()=>e.jsx(me,{});export{xe as default};
