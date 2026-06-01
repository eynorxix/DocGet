let chatHistory = [];
let selectedSkillId = null;
let activeSection = null;

function toggleSection(h3){
  const group=h3.parentElement;
  const content=group.querySelector('.collapse-content');
  const icon=h3.querySelector('.collapse-icon');
  if(!content)return;
  if(activeSection===group){
    content.classList.remove('open');
    if(icon){icon.classList.remove('open');icon.textContent='+'}
    activeSection=null;
    return;
  }
  if(activeSection){
    const pc=activeSection.querySelector('.collapse-content');
    const pi=activeSection.querySelector('.collapse-icon');
    if(pc)pc.classList.remove('open');
    if(pi){pi.classList.remove('open');pi.textContent='+'}
  }
  content.classList.add('open');
  if(icon){icon.classList.add('open');icon.textContent='−'}
  activeSection=group;
}

function autoResize(t){t.style.height='auto';t.style.height=Math.min(t.scrollHeight,100)+'px'}

function handleKey(e){
  if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();handleSend()}
}

function escapeHtml(s){
  const d=document.createElement('div');
  d.textContent=s;
  return d.innerHTML;
}

function scrollBottom(){
  const ws=document.getElementById('workspace');
  ws.scrollTop=ws.scrollHeight;
}

function hideEmpty(){
  const es=document.getElementById('emptyState');
  if(es)es.style.display='none';
}

function addEntry(type, tag, title, bodyHTML, time){
  hideEmpty();
  const ws=document.getElementById('workspace');
  const d=document.createElement('div');
  d.className='entry '+type;
  d.innerHTML='<div class="entry-header"><span class="entry-tag">'+tag+'</span><span class="entry-title">'+title+'</span><span class="entry-time">'+(time||'ahora')+'</span></div><div class="entry-body">'+bodyHTML+'</div>';
  ws.appendChild(d);
  scrollBottom();
  return d;
}

function renderMarkdown(text){
  let h=escapeHtml(text);
  h=h.replace(/### (.+)/g,'<strong>$1</strong>');
  h=h.replace(/## (.+)/g,'<strong>$1</strong>');
  h=h.replace(/# (.+)/g,'<strong>$1</strong>');
  h=h.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
  h=h.replace(/\*(.+?)\*/g,'<em>$1</em>');
  h=h.replace(/`([^`]+)`/g,'<code>$1</code>');
  h=h.replace(/- (.+)/g,'<br>&bull; $1');
  h=h.replace(/\n/g,'<br>');
  return h;
}

function renderResponse(text, data, action){
  const lines=text.split('\n');
  let tag='DOCGENT';
  let html='';

  if(action==='create_skill'&&data?.skill){
    const s=data.skill;
    html='<p>✅ Skill <strong>'+escapeHtml(s.name)+'</strong> creada</p><pre>'+escapeHtml(s.content.slice(0,500))+'</pre>';
    loadSidebar();
  }
  else if(action==='update_skill'&&data?.skill){
    html='<p>✅ Skill <strong>'+escapeHtml(data.skill.name)+'</strong> actualizada</p>';
    loadSidebar();
  }
  else if(action==='delete_skill'){
    html='<p>✅ Skill eliminada</p>';
    loadSidebar();
  }
  else if(action==='generate_document'&&data?.download_url){
    html='<p><strong>'+escapeHtml(data.filename)+'</strong></p><div style="display:flex;gap:8px"><a class="btn-inline" href="'+data.download_url+'" target="_blank">descargar .docx</a><button class="btn-inline" onclick="openDocumentPreview(\''+data.download_url+'\',\''+escapeHtml(data.filename)+'\')">visualizar</button></div>';
    loadSidebar();
  }
  else if(action==='request_file_upload'){
    html='<p>Selecciona archivos para subir</p><button class="btn-inline" onclick="document.getElementById(\'fileInput\').click()">subir archivo</button>';
  }
  else if(action==='skill_select'){
    openSkillSelector();
    html='<p>Selecciona una skill de la lista para continuar.</p>';
  }
  else {
    html='<p>'+renderMarkdown(text)+'</p>';
  }

  addEntry('system',tag,'',html);
}

async function handleSend(){
  const t=document.getElementById('promptInput');
  const val=t.value.trim();
  if(!val)return;
  t.value='';t.style.height='auto';

  addEntry('system','TU','','<p>'+escapeHtml(val)+'</p>');

  chatHistory.push({role:'user',content:val});
  addEntry('system','DOCGENT','pensando...','<p class="dim">...</p>');

  try{
    const r=await fetch('/api/chat',{
      method:'POST',
      headers:getHeaders(),
      body:JSON.stringify({message:val,history:chatHistory.slice(-20)})
    });
    const d=await r.json();

    const ws=document.getElementById('workspace');
    const last=ws.lastElementChild;
    if(last&&last.querySelector('.entry-title')?.textContent==='pensando...')last.remove();

    chatHistory.push({role:'assistant',content:d.response});

    if(d.action){
      renderResponse(d.response,d.data,d.action);
    } else {
      addEntry('system','DOCGENT','',renderMarkdown(d.response));
    }
  }catch(e){
    const ws=document.getElementById('workspace');
    const last=ws.lastElementChild;
    if(last&&last.querySelector('.entry-title')?.textContent==='pensando...')last.remove();
    addEntry('error','ERROR','error','<p>No se pudo conectar con el servidor</p>');
  }
}

async function handleFileSelect(e){
  const files=e.target.files;
  if(!files.length)return;
  for(const f of files){
    const fd=new FormData();
    fd.append('file',f);
    try{
      const r=await fetch('/api/documents/upload',{method:'POST',body:fd});
      const d=await r.json();
      const msg='Archivo <strong>'+escapeHtml(d.filename)+'</strong> subido ('+d.size_kb+' KB)';
      addEntry('file','ARCHIVO','subido: '+escapeHtml(d.filename),'<p>'+msg+'</p><pre>'+escapeHtml(d.preview.slice(0,300))+'</pre>');
      chatHistory.push({role:'user',content:'SISTEMA: El usuario subió el archivo "'+d.filename+'". Contenido:\n```\n'+(d.preview||'')+'\n```'});
    }catch(e){
      addEntry('error','ERROR','no se pudo subir '+escapeHtml(f.name),'');
    }
  }
  e.target.value='';
  loadSidebar();
}

function handleSkillFileSelect(e){
  const file=e.target.files[0];
  if(!file)return;
  const reader=new FileReader();
  reader.onload=function(ev){
    const content=ev.target.result;
    document.getElementById('skillContent').value=content;
    const ext=file.name.split('.').pop().toLowerCase();
    if(ext==='py')document.getElementById('skillType').value='py';
    else if(ext==='txt')document.getElementById('skillType').value='txt';
    else document.getElementById('skillType').value='md';
    document.getElementById('skillDropZone').textContent='archivo cargado: '+file.name;
    document.getElementById('skillDropZone').style.borderColor='var(--accent)';
    document.getElementById('skillDropZone').style.color='var(--accent)';
  };
  reader.readAsText(file);
  e.target.value='';
}

function showCreateSkillModal(){
  document.getElementById('modalOverlay').classList.add('show');
  document.getElementById('skillName').value='';
  document.getElementById('skillDesc').value='';
  document.getElementById('skillContent').value='';
  const sdz=document.getElementById('skillDropZone');
  sdz.textContent='o arrastra un archivo .md / .py / .txt aqui';
  sdz.style.borderColor='var(--border)';
  sdz.style.color='var(--text3)';
}

function closeModal(){
  document.getElementById('modalOverlay').classList.remove('show');
}

function closeGenModal(){
  document.getElementById('genModal').classList.remove('show');
}

let btnTimeouts={};

function toggleBtn(e,el,action){
  if(el.classList.contains('expanded')){
    clearTimeout(btnTimeouts[action]);
    delete btnTimeouts[action];
    if(action==='file')document.getElementById('fileInput').click();
    else if(action==='skill')openSkillSelector();
  }else{
    document.querySelectorAll('.circle-btn.expanded').forEach(b=>b.classList.remove('expanded'));
    el.classList.add('expanded');
    btnTimeouts[action]=setTimeout(()=>{
      el.classList.remove('expanded');
      delete btnTimeouts[action];
    },5000);
  }
}

function openSkillSelector(){
  document.getElementById('skillSelectOverlay').classList.add('show');
  loadSkillSelector();
}

function closeSkillSelectModal(){
  document.getElementById('skillSelectOverlay').classList.remove('show');
}

async function loadSkillSelector(){
  const list=document.getElementById('skillSelectList');
  list.innerHTML='<p style="color:var(--text3)">Cargando skills...</p>';
  try{
    const skills=await fetch('/api/skills').then(r=>r.json());
    if(skills.length===0){
      list.innerHTML='<p style="color:var(--text3)">No hay skills. Crea una primero.</p>';
    }else{
      list.innerHTML=skills.map(s=>'<div class="skill-select-item" onclick="selectSkillFromSelector(\''+s.id+'\',\''+escapeHtml(s.name).replace(/'/g,"\\'")+'\')"><div class="name">'+escapeHtml(s.name)+'</div><div class="desc">'+escapeHtml(s.description||'Sin descripción')+'</div></div>').join('');
    }
  }catch(e){
    list.innerHTML='<p style="color:var(--text3)">Error al cargar skills.</p>';
  }
}

async function selectSkillFromSelector(id,name){
  closeSkillSelectModal();
  selectedSkillId=id;
  document.querySelectorAll('.sidebar-item.active').forEach(e=>e.classList.remove('active'));
  const el=document.querySelector('[data-skill="'+id+'"]');
  if(el)el.classList.add('active');

  let skillContent='';
  try{
    const sk=await fetch('/api/skills/'+id).then(r=>r.json());
    skillContent=sk.content||'';
  }catch(e){}

  const msg='SISTEMA: El usuario seleccionó la skill "'+name+'" para generar el documento. Contenido de la skill:\n```\n'+(skillContent||'')+'\n```\nSi ya tienes suficiente información, pregúntale al usuario si desea generar el documento (Y/N).';

  chatHistory.push({role:'user',content:msg});
  addEntry('system','TU','','<p>SISTEMA: Skill seleccionada: <strong>'+escapeHtml(name)+'</strong></p>');
  addEntry('system','DOCGENT','pensando...','<p class="dim">...</p>');

  try{
    const r=await fetch('/api/chat',{
      method:'POST',
      headers:getHeaders(),
      body:JSON.stringify({message:msg,history:chatHistory.slice(-20)})
    });
    const d=await r.json();
    const ws=document.getElementById('workspace');
    const last=ws.lastElementChild;
    if(last&&last.querySelector('.entry-title')?.textContent==='pensando...')last.remove();
    chatHistory.push({role:'assistant',content:d.response});
    addEntry('system','DOCGENT','',renderMarkdown(d.response));
  }catch(e){
    const ws=document.getElementById('workspace');
    const last=ws.lastElementChild;
    if(last&&last.querySelector('.entry-title')?.textContent==='pensando...')last.remove();
    addEntry('error','ERROR','error','<p>No se pudo procesar la skill</p>');
  }
}

async function createSkill(){
  const name=document.getElementById('skillName').value.trim();
  const desc=document.getElementById('skillDesc').value.trim();
  const type=document.getElementById('skillType').value;
  const content=document.getElementById('skillContent').value.trim();
  if(!name||!content){
    addEntry('error','ERROR','nombre y contenido requeridos','');
    return;
  }
  try{
    const r=await fetch('/api/skills',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({name,description:desc,type,content})
    });
    const skill=await r.json();
    closeModal();
    addEntry('skill','SKILL','creada: '+escapeHtml(name),'<pre>'+escapeHtml(content.slice(0,300))+'</pre>');
    chatHistory.push({role:'user',content:'Creé la skill: '+name});
    chatHistory.push({role:'assistant',content:'Skill '+name+' creada correctamente.'});
    loadSidebar();
  }catch(e){
    addEntry('error','ERROR','no se pudo crear la skill','');
  }
}

function getApiKeys(){
  try{return JSON.parse(sessionStorage.getItem('gemini_keys')||'[]')}catch{return []}
}

function saveApiKeys(keys){
  sessionStorage.setItem('gemini_keys',JSON.stringify(keys.filter(k=>k.trim()!=='')));
}

function getApiKey(){
  const keys=getApiKeys();
  return keys[0]||'';
}

function getHeaders(extra){
  const h={'Content-Type':'application/json',...(extra||{})};
  const keys=getApiKeys();
  if(keys.length>0)h['X-Gemini-Keys']=JSON.stringify(keys);
  const caratula=getCaratula();
  if(caratula.titulo||caratula.autor||caratula.tutor){
    h['X-Caratula']=JSON.stringify(caratula);
  }
  return h;
}

function getCaratula(){
  try{return JSON.parse(sessionStorage.getItem('docgent_caratula')||'{}')}catch{return {}}
}

function saveCaratula(){
  const d={
    titulo: document.getElementById('caratulaTitulo').value.trim(),
    autor: document.getElementById('caratulaAutor').value.trim(),
    tutor: document.getElementById('caratulaTutor').value.trim(),
  };
  sessionStorage.setItem('docgent_caratula',JSON.stringify(d));
  ['caratulaTitulo','caratulaAutor','caratulaTutor'].forEach(id=>{
    const el=document.getElementById(id);
    el.classList.toggle('filled',el.value.trim()!=='');
  });
}

function loadCaratula(){
  const d=getCaratula();
  document.getElementById('caratulaTitulo').value=d.titulo||'';
  document.getElementById('caratulaAutor').value=d.autor||'';
  document.getElementById('caratulaTutor').value=d.tutor||'';
  ['caratulaTitulo','caratulaAutor','caratulaTutor'].forEach(id=>{
    const el=document.getElementById(id);
    el.classList.toggle('filled',el.value.trim()!=='');
  });
}

async function generateDemoDoc(){
  addEntry('system','DOCGENT','generando demo...','<p class="dim">Generando documento de prueba con todas las funcionalidades...</p>');
  try{
    const r=await fetch('/api/documents/generate-demo',{method:'POST'});
    const d=await r.json();
    const ws=document.getElementById('workspace');
    const last=ws.lastElementChild;
    if(last&&last.querySelector('.entry-title')?.textContent==='generando demo...')last.remove();
    addEntry('doc','DOC','demo: '+d.filename,
      '<p><strong>'+escapeHtml(d.filename)+'</strong> — Documento de prueba con tablas, indices, viñetas, formato APA</p><div style="display:flex;gap:8px">'+
      '<a class="btn-inline" href="'+d.download_url+'" target="_blank">descargar .docx</a>'+
      '<button class="btn-inline" onclick="openDocumentPreview(\''+d.download_url+'\',\''+escapeHtml(d.filename)+'\')">visualizar</button></div>'
    );
    loadSidebar();
  }catch(e){
    const ws=document.getElementById('workspace');
    const last=ws.lastElementChild;
    if(last&&last.querySelector('.entry-title')?.textContent==='generando demo...')last.remove();
    addEntry('error','ERROR','error','<p>No se pudo generar el documento demo</p>');
  }
}

function openApiKeysModal(){
  const keys=getApiKeys();
  for(let i=0;i<4;i++){
    const inp=document.getElementById('apiKey'+(i+1));
    inp.value=keys[i]||'';
    inp.classList.toggle('filled',inp.value.trim()!=='');
  }
  document.getElementById('apiKeysOverlay').classList.add('show');
}

function closeApiKeysModal(){
  document.getElementById('apiKeysOverlay').classList.remove('show');
}

function applyApiKeys(){
  const keys=[1,2,3,4].map(i=>document.getElementById('apiKey'+i).value.trim()).filter(k=>k!=='');
  saveApiKeys(keys);
  closeApiKeysModal();
  addEntry('system','DOCGENT','API keys','<p>'+(keys.length>0?keys.length+' API key(s) guardada(s). Si una falla por cuota, se usa la siguiente.':'No se guardaron API keys.')+'</p>');
}

function acceptWelcome(){
  document.getElementById('welcomeOverlay').style.display='none';
  initApp();
}

async function loadSidebar(){
  try{
    const skills=await fetch('/api/skills').then(r=>r.json());
    const files=await fetch('/api/documents/uploads').then(r=>r.json());
    const docs=await fetch('/api/documents/list').then(r=>r.json());
    document.getElementById('fileCount').textContent=files.length;
    document.getElementById('skillCount').textContent=skills.length;
    document.getElementById('docCount').textContent=docs.length;

    const kc=getApiKeys().length;
    document.getElementById('sidebarKeyStatus').textContent=kc>0?kc+' key(s) configurada(s)':'0 keys';

    const qs=document.getElementById('quickSkills');
    if(skills.length===0){
      qs.innerHTML='<div style="font-size:11px;color:var(--text3);padding:4px 8px">sin skills</div>';
    } else {
      qs.innerHTML=skills.slice(0,8).map(s=>'<div class="sidebar-item clickable" data-skill="'+s.id+'" onclick="selectSkillFromSidebar(\''+s.id+'\',\''+escapeHtml(s.name).replace(/'/g,"\\'")+'\')"><span class="arrow">&gt;</span> '+escapeHtml(s.name.slice(0,28))+'</div>').join('');
    }
  }catch(e){}
}

let editingSkillId=null;
let deleteConfirmActive=false;

async function selectSkillFromSidebar(id,name){
  document.querySelectorAll('.sidebar-item.active').forEach(e=>e.classList.remove('active'));
  const el=document.querySelector('[data-skill="'+id+'"]');
  if(el)el.classList.add('active');
  editingSkillId=id;
  try{
    const sk=await fetch('/api/skills/'+id).then(r=>r.json());
    document.getElementById('editSkillName').value=sk.name||'';
    document.getElementById('editSkillDesc').value=sk.description||'';
    document.getElementById('editSkillType').value=sk.type||'md';
    document.getElementById('editSkillContent').value=sk.content||'';
    deleteConfirmActive=false;
    const btn=document.getElementById('deleteSkillBtn');
    btn.textContent='eliminar';
    btn.style.background='';
    document.getElementById('editSkillOverlay').classList.add('show');
  }catch(e){
    addEntry('error','ERROR','no se pudo cargar la skill','');
  }
}

function closeEditSkillModal(){
  document.getElementById('editSkillOverlay').classList.remove('show');
  deleteConfirmActive=false;
}

async function applySkillChanges(){
  const id=editingSkillId;
  const name=document.getElementById('editSkillName').value.trim();
  const desc=document.getElementById('editSkillDesc').value.trim();
  const type=document.getElementById('editSkillType').value;
  const content=document.getElementById('editSkillContent').value.trim();
  if(!name||!content)return;
  try{
    await fetch('/api/skills/'+id,{
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({name,description:desc,type,content})
    });
    closeEditSkillModal();
    loadSidebar();
    addEntry('skill','SKILL','actualizada: '+escapeHtml(name),'');
  }catch(e){
    addEntry('error','ERROR','no se pudo actualizar la skill','');
  }
}

function confirmDeleteSkill(){
  if(!deleteConfirmActive){
    deleteConfirmActive=true;
    const btn=document.getElementById('deleteSkillBtn');
    btn.textContent='confirmar eliminar';
    btn.style.background='var(--danger)';
    setTimeout(()=>{deleteConfirmActive=false;btn.textContent='eliminar';btn.style.background=''},4000);
    return;
  }
  const id=editingSkillId;
  fetch('/api/skills/'+id,{method:'DELETE'})
    .then(()=>{closeEditSkillModal();loadSidebar();addEntry('skill','SKILL','eliminada','')})
    .catch(()=>addEntry('error','ERROR','no se pudo eliminar la skill',''));
  deleteConfirmActive=false;
}

function changeGif(){
  const hint='https://giphy.com/search/anime';
  const url=prompt('Pega el enlace del GIF de Giphy (ve a '+hint+', elige uno, copia su enlace):',localStorage.getItem('sidebar_gif_url')||hint);
  if(url&&url.trim()){
    const img=document.getElementById('sidebarGif');
    if(img){
      const gifUrl=url.trim().startsWith('http')?url.trim():hint;
      img.src=gifUrl;
      localStorage.setItem('sidebar_gif_url',gifUrl);
    }
  }
}

function loadGif(){
  const saved=localStorage.getItem('sidebar_gif_url');
  if(saved){
    const img=document.getElementById('sidebarGif');
    if(img)img.src=saved;
  }
}

function initApp(){
  loadCaratula();
  loadSidebar();
  loadGif();
  addEntry('system','DOCGENT','sistema listo','<p>¡Hola! Soy DocGent, tu asistente para generar documentos <code>.docx</code>. ¿En qué puedo ayudarte?</p><p class="dim">Puedes pedirme: crear/editar skills, generar documentos, subir archivos, etc.</p>');
}

function openDonateModal(){
  document.getElementById('donateOverlay').classList.add('show');
}

function closeDonateModal(){
  document.getElementById('donateOverlay').classList.remove('show');
}

function copyCode(btn, code){
  navigator.clipboard.writeText(code).then(()=>{
    const orig=btn.textContent;
    btn.textContent='copiado';
    btn.classList.add('copied');
    setTimeout(()=>{btn.textContent=orig;btn.classList.remove('copied')},2000);
  }).catch(()=>{});
}

let lightboxTimer=null;

function openLightbox(img){
  const lb=document.getElementById('lightbox');
  const lbImg=document.getElementById('lightboxImg');
  lbImg.src=img.src;
  lb.classList.add('show');
  clearTimeout(lightboxTimer);
  lightboxTimer=setTimeout(closeLightbox,30000);
}

function closeLightbox(){
  document.getElementById('lightbox').classList.remove('show');
  clearTimeout(lightboxTimer);
}

function openDocumentPreview(downloadUrl, filename){
  const overlay=document.getElementById('previewOverlay');
  document.getElementById('previewFilename').textContent=filename;
  document.getElementById('previewDownloadBtn').href=downloadUrl;
  document.getElementById('previewContent').innerHTML='<div class="preview-empty">Cargando...</div>';
  overlay.classList.add('show');

  const previewUrl='/api/documents/preview/'+encodeURIComponent(filename);
  fetch(previewUrl)
    .then(r=>r.json())
    .then(data=>{
      document.getElementById('previewSize').textContent=data.size_kb+' KB';
      let html='';
      for(const p of data.paragraphs){
        const style=p.style||'Normal';
        if(style.startsWith('Heading')||style.startsWith('Título')){
          html+='<div class="preview-heading">'+escapeHtml(p.text)+'</div>';
        }else if(p.text.trim()){
          html+='<p>'+escapeHtml(p.text)+'</p>';
        }
      }
      for(const t of data.tables){
        if(t.length<2)continue;
        html+='<table class="preview-table">';
        html+='<tr>'+t[0].map(c=>'<th>'+escapeHtml(c)+'</th>').join('')+'</tr>';
        for(let i=1;i<t.length;i++){
          html+='<tr>'+t[i].map(c=>'<td>'+escapeHtml(c)+'</td>').join('')+'</tr>';
        }
        html+='</table>';
      }
      const content=document.getElementById('previewContent');
      content.innerHTML=html||'<div class="preview-empty">Sin contenido visible</div>';
      content.scrollTop=0;
    })
    .catch(()=>{
      document.getElementById('previewContent').innerHTML='<div class="preview-empty">Error al cargar la vista previa</div>';
    });
}

function closePreviewModal(){
  document.getElementById('previewOverlay').classList.remove('show');
}

function getLastUserMessage(){
  for(let i=chatHistory.length-1;i>=0;i--){
    if(chatHistory[i].role==='user'&&!chatHistory[i].content.startsWith('SISTEMA:')){
      return chatHistory[i].content;
    }
  }
  return '';
}

async function handleGenerateDirect(e){
  const btn=e.currentTarget;
  if(btn.classList.contains('expanded')){
    clearTimeout(btnTimeouts['gen']);
    delete btnTimeouts['gen'];
  }else{
    document.querySelectorAll('.circle-btn.expanded').forEach(b=>b.classList.remove('expanded'));
    btn.classList.add('expanded');
    btnTimeouts['gen']=setTimeout(()=>{btn.classList.remove('expanded');delete btnTimeouts['gen']},5000);
    return;
  }

  const caratula=getCaratula();
  const title=caratula.titulo||'Documento';
  const author=caratula.autor||'';
  const tutor=caratula.tutor||'';
  const topic=getLastUserMessage()||title;

  addEntry('system','DOCGENT','generando...','<p class="dim">Buscando informacion en internet y generando documento...</p>');

  try{
    const r=await fetch('/api/documents/generate-direct',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({title,author,tutor,topic})
    });
    const d=await r.json();

    const ws=document.getElementById('workspace');
    const last=ws.lastElementChild;
    if(last&&last.querySelector('.entry-title')?.textContent==='generando...')last.remove();

    addEntry('doc','DOC','generado: '+d.filename,
      '<p><strong>'+escapeHtml(d.filename)+'</strong></p><div style="display:flex;gap:8px">'+
      '<a class="btn-inline" href="'+d.download_url+'" target="_blank">descargar .docx</a>'+
      '<button class="btn-inline" onclick="openDocumentPreview(\''+d.download_url+'\',\''+escapeHtml(d.filename)+'\')">visualizar</button></div>'
    );
    loadSidebar();
  }catch(e){
    const ws=document.getElementById('workspace');
    const last=ws.lastElementChild;
    if(last&&last.querySelector('.entry-title')?.textContent==='generando...')last.remove();
    addEntry('error','ERROR','error al generar','<p>No se pudo generar el documento</p>');
  }
}

function init(){
  loadSidebar();
  const dz=document.getElementById('dropZone');
  dz.addEventListener('dragover',e=>{e.preventDefault();dz.classList.add('drag-over')});
  dz.addEventListener('dragleave',()=>dz.classList.remove('drag-over'));
  dz.addEventListener('drop',e=>{
    e.preventDefault();
    dz.classList.remove('drag-over');
    if(e.dataTransfer.files.length){
      if(!dz.classList.contains('expanded'))dz.classList.add('expanded');
      const input=document.getElementById('fileInput');
      const dt=new DataTransfer();
      for(const f of e.dataTransfer.files)dt.items.add(f);
      input.files=dt.files;
      handleFileSelect({target:input});
    }
  });
  const sdz=document.getElementById('skillDropZone');
  sdz.addEventListener('dragover',e=>{e.preventDefault();sdz.style.borderColor='var(--accent)';sdz.style.color='var(--accent)'});
  sdz.addEventListener('dragleave',()=>{sdz.style.borderColor='var(--border)';sdz.style.color='var(--text3)'});
  sdz.addEventListener('drop',e=>{
    e.preventDefault();
    sdz.style.borderColor='var(--border)';
    sdz.style.color='var(--text3)';
    if(e.dataTransfer.files.length){
      const input=document.getElementById('skillFileInput');
      input.files=e.dataTransfer.files;
      handleSkillFileSelect({target:input});
    }
  });
}
init();
