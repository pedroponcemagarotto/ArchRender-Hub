/* ArchRender Hub 0.1: no external scripts and no cloud requests. */
'use strict';

const ICON_PATHS = {
  house:'<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M9 21v-8h6v8"/>',
  grid:'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  sparkles:'<path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="m19 15 .8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8zM4 2l.7 2L7 5l-2.3.7L4 8l-.7-2.3L1 5l2.3-1z"/>',
  archive:'<rect x="3" y="4" width="18" height="4" rx="1"/><path d="M5 8v12h14V8M10 12h4"/>',
  plus:'<path d="M12 5v14M5 12h14"/>',
  arrow:'<path d="M5 12h14m-6-6 6 6-6 6"/>',
  'arrow-right':'<path d="M5 12h14m-6-6 6 6-6 6"/>',
  'arrow-up-right':'<path d="M7 17 17 7M8 7h9v9"/>',
  layers:'<path d="m12 2 9 5-9 5-9-5zM3 12l9 5 9-5M3 17l9 5 9-5"/>',
  bookmark:'<path d="M6 4h12v17l-6-4-6 4z"/>',
  'bookmark-plus':'<path d="M6 4h12v17l-6-4-6 4z"/><path d="M12 7v6m-3-3h6"/>',
  layout:'<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 9v12"/>',
  image:'<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-5-5L5 21"/>',
  shield:'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
  'shield-check':'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
  wand:'<path d="m3 21 12-12M13 11l-3-3 3-3 3 3zM18 2v4M16 4h4M19 13v4M17 15h4"/>',
  x:'<path d="M18 6 6 18M6 6l12 12"/>',
  check:'<path d="m5 12 4 4L19 6"/>',
  'check-circle':'<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
  search:'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
  'search-x':'<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4M8 10l5 5m0-5-5 5"/>',
  'chevron-down':'<path d="m6 9 6 6 6-6"/>',
  copy:'<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3"/>',
  download:'<path d="M12 3v12m-4-4 4 4 4-4M4 17v4h16v-4"/>',
  upload:'<path d="M12 17V5m-4 4 4-4 4 4M4 17v4h16v-4"/>',
  info:'<circle cx="12" cy="12" r="9"/><path d="M12 10v7m0-10h.01"/>',
  menu:'<path d="M4 7h16M4 12h16M4 17h16"/>',
  edit:'<path d="M12 20h9M3 17l-1 4 4-1L19 7l-3-3zM14 6l4 4"/>',
  trash:'<path d="M3 6h18M8 6V4h8v2M6 6l1 15h10l1-15M10 10v7m4-7v7"/>',
  'file-text':'<path d="M5 2h10l4 4v16H5zM15 2v5h4M8 12h8M8 16h8"/>',
  duplicate:'<rect x="7" y="7" width="14" height="14" rx="2"/><path d="M17 7V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h2"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  sun:'<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  building:'<rect x="5" y="2" width="14" height="20" rx="1"/><path d="M9 6h2m4 0h1M9 10h2m4 0h1M9 14h2m4 0h1M10 22v-4h4v4"/>',
  sofa:'<path d="M5 11V8a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v3M3 12h2v7h14v-7h2v8H3zM6 20v2m12-2v2"/>',
  leaf:'<path d="M20 4C11 4 4 8 4 15a5 5 0 0 0 5 5c7 0 11-7 11-16Z"/><path d="M4 20c3-5 7-8 13-11"/>',
  ruler:'<rect x="4" y="4" width="16" height="16" rx="1" transform="rotate(45 12 12)"/><path d="m8 8 2 2m1-5 2 2m2 5 2 2"/>',
  wrench:'<path d="M21 7a6 6 0 0 1-8 6L6 20a2 2 0 0 1-3-3l7-7a6 6 0 0 1 8-8l-4 4 4 4z"/>',
  swatch:'<circle cx="13" cy="13" r="8"/><circle cx="9" cy="9" r="1"/><circle cx="15" cy="7" r="1"/><circle cx="18" cy="13" r="1"/><path d="M13 21a3 3 0 0 1-3-3 3 3 0 0 1 3-3h1"/>',
  moon:'<path d="M20 16a8 8 0 0 1-12-12 8 8 0 1 0 12 12z"/>',
  sliders:'<path d="M4 7h16M4 17h16"/><circle cx="9" cy="7" r="2" fill="currentColor"/><circle cx="16" cy="17" r="2" fill="currentColor"/>',
  folder:'<path d="M3 6h7l2 2h9v12H3z"/>',
  'external-link':'<path d="M14 4h6v6M10 14 20 4M20 14v6H4V4h6"/>'
};
function icon(name){return `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICON_PATHS[name] || ICON_PATHS.folder}</svg>`}
function setupIcons(root=document){root.querySelectorAll('[data-icon]').forEach(el=>{el.innerHTML=icon(el.dataset.icon)})}
function esc(str=''){return String(str??'').replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]))}
const $=sel=>document.querySelector(sel);
const $$=sel=>Array.from(document.querySelectorAll(sel));
const state={items:[],categories:[],tools:[],view:'inicio',filterCategory:'',filterTool:'',favoritesOnly:false,activeDetail:null,editingId:null,editorBefore:'',editorAfter:'',promptDraft:''};
const CATEGORY_ICONS={'Fachadas':'building','Interiores':'sofa','Paisagismo':'leaf','Plantas':'ruler','Reformas':'wrench','Materiais':'swatch','Iluminacao':'moon','Pos-producao':'sliders','Outros':'folder'};
const NAMES={'Iluminacao':'Iluminação','Pos-producao':'Pós-produção'};
const cName=v=>NAMES[v]||v||'Geral';
const categoryClass=v=>({'Fachadas':'fachadas','Interiores':'interiores','Paisagismo':'paisagismo','Plantas':'plantas','Reformas':'reformas','Materiais':'materiais','Iluminacao':'iluminacao','Pos-producao':'pos-producao'}[v]||'outros');
const allowedImage=src=>/^\/uploads\/[0-9a-f]{32}\.(?:jpg|png|webp)$/.test(src||'') ? src : '';
const shortDate=d=>{try{return new Intl.DateTimeFormat('pt-BR',{day:'2-digit',month:'short',year:'numeric'}).format(new Date(d))}catch{return '—'}};

async function request(url,{method='GET',data}={}){
  const options={method,cache:'no-store',headers:{}};
  if(method!=='GET'){options.headers['Content-Type']='application/json';if(data!==undefined) options.body=JSON.stringify(data)}
  let response;
  try{response=await fetch(url,options)}catch{throw new Error('Não foi possível conectar ao servidor local. Verifique se o app.py continua aberto.')}
  const payload=await response.json().catch(()=>({}));
  if(!response.ok)throw new Error(payload.error || `Falha na requisição (${response.status}).`);
  return payload;
}
function toast(message,error=false){
  const entry=document.createElement('div');entry.className=`toast ${error?'error':''}`;
  entry.innerHTML=`${icon(error?'x':'check-circle')}<span>${esc(message)}</span>`;
  $('#toastArea').appendChild(entry);setTimeout(()=>entry.remove(),4400);
}
async function loadData(){
  const [meta,records]=await Promise.all([request('/api/status'),request('/api/recipes')]);
  state.items=records.items;
  state.categories=meta.categories;
  state.tools=meta.tools;
  $('#sidebarVersion').textContent='V'+meta.version;
  renderCategoryNav();
  fillSelects();
  renderOverview();
  renderLibrary();
}
function fillSelects(){
  for(const s of ['#categoryFilter','#editorCategory']){
    const select=$(s),old=select.value;
    select.innerHTML=(s==='#categoryFilter'?'<option value="">Todas as categorias</option>':'')+state.categories.map(c=>`<option value="${esc(c)}">${esc(cName(c))}</option>`).join('');select.value=old|| (s==='#editorCategory'?'Fachadas':'');
  }
  const toolFilter=$('#toolFilter'); const old=toolFilter.value;
  const existingTools=[...new Set([...state.tools,...state.items.map(x=>x.tool)])].filter(Boolean);
  toolFilter.innerHTML='<option value="">Todas as ferramentas</option>'+existingTools.map(t=>`<option value="${esc(t)}">${esc(t)}</option>`).join('');toolFilter.value=old;
  const editorTool=$('#editorTool'),was=editorTool.value;
  editorTool.innerHTML=existingTools.map(t=>`<option value="${esc(t)}">${esc(t)}</option>`).join('');editorTool.value=was||'Universal';
}
function renderCategoryNav(){
  $('#sidebarCategories').innerHTML=state.categories.map(c=>`<button class="cat-item" type="button" data-category="${esc(c)}"><span class="cat-icon">${icon(CATEGORY_ICONS[c])}</span>${esc(cName(c))}</button>`).join('');
}
function imageCover(item){
  const image=allowedImage(item.after_image)||allowedImage(item.before_image);
  const media=image?`<img loading="lazy" src="${esc(image)}" alt="Imagem ${item.after_image?'de resultado':'de entrada'} da receita ${esc(item.title)}">`:`<div class="cover-placeholder c-${categoryClass(item.category)}"><span class="shape-one"></span><span class="shape-two"></span><span class="shape-three"></span></div>`;
  return `<div class="card-cover">${media}<span class="card-badge">${esc(cName(item.category))}</span><button type="button" class="card-favorite" data-favorite="${esc(item.id)}" aria-label="${item.favorite?'Remover dos':'Adicionar aos'} favoritos" aria-pressed="${!!item.favorite}">${icon('bookmark')}</button>${!image?'<span class="cover-info">Sem imagem vinculada</span>':''}</div>`;
}
function recipeCard(item){
  return `<article class="recipe-card" data-recipe="${esc(item.id)}">${imageCover(item)}<div class="card-inner"><div class="card-meta">${esc(cName(item.category).toUpperCase())} / ${esc(shortDate(item.created_at))}</div><h3>${esc(item.title)}</h3><p class="card-summary">${esc(item.summary||'Receita personalizada para visualização arquitetônica.')}</p><div class="card-bottom"><span class="card-tool">${icon('sparkles')} ${esc(item.tool)}</span><button class="card-open" type="button" data-open="${esc(item.id)}">Ver receita ${icon('arrow-up-right')}</button></div></div></article>`;
}
function renderOverview(){
  const withImage=state.items.filter(r=>r.after_image||r.before_image).length;
  const favorites=state.items.filter(r=>r.favorite).length;
  const stats=[['layers',state.items.length,'Receitas cadastradas'],['bookmark',favorites,'Favoritos'],['layout',new Set(state.items.map(r=>r.category)).size,'Categorias usadas'],['image',withImage,'Com imagens']];
  $('#statsGrid').innerHTML=stats.map(([sym,count,label])=>`<div class="stat-card"><span class="stat-icon">${icon(sym)}</span><strong class="stat-number">${count}</strong><span class="stat-label">${label}</span></div>`).join('');
  $('#navCount').textContent=state.items.length;
  // Show variety by category instead of only newest
  const unique=new Set(),featured=[];
  for(const r of [...state.items].sort((a,b)=>a.created_at.localeCompare(b.created_at))){if(!unique.has(r.category)){unique.add(r.category);featured.push(r)}if(featured.length===3)break}
  $('#featuredGrid').innerHTML=featured.map(recipeCard).join('')||'<p>Nenhuma receita. Comece criando a primeira!</p>';
}
function filteredItems(){
  const term=$('#searchInput').value.trim().toLocaleLowerCase('pt-BR');
  let items=state.items.filter(r=>{
    if(state.filterCategory&&r.category!==state.filterCategory)return false;
    if(state.filterTool&&r.tool!==state.filterTool)return false;
    if(state.favoritesOnly&&!r.favorite)return false;
    if(term){const hay=[r.title,r.summary,r.prompt,r.category,r.tool,r.materials,r.style,r.input_type,(r.tags||[]).join(' ')].join(' ').toLocaleLowerCase('pt-BR');if(!hay.includes(term))return false}
    return true;
  });
  const sort=$('#sortFilter').value;
  if(sort==='title')items.sort((a,b)=>a.title.localeCompare(b.title,'pt-BR'));
  else if(sort==='favorite')items.sort((a,b)=>Number(b.favorite)-Number(a.favorite)||b.updated_at.localeCompare(a.updated_at));
  else items.sort((a,b)=>b.updated_at.localeCompare(a.updated_at)||b.id.localeCompare(a.id));
  return items;
}
function renderLibrary(){
  const list=filteredItems();
  $('#libraryGrid').innerHTML=list.map(recipeCard).join('');
  $('#resultsCount').textContent=`${list.length} ${list.length===1?'receita encontrada':'receitas encontradas'}`;
  const filtered=!!(state.filterCategory||state.filterTool||state.favoritesOnly||$('#searchInput').value.trim());
  $('#clearFilters').hidden=!filtered;
  $('#emptyState').hidden=list.length!==0;
}
function setView(name){
  if(!['inicio','biblioteca','criador','backup'].includes(name))name='inicio';
  state.view=name;
  $$('.view').forEach(el=>el.hidden=el.id!==`view-${name}`);
  $$('.nav-item').forEach(el=>{const active=el.dataset.nav===name;el.classList.toggle('active',active);if(active)el.setAttribute('aria-current','page');else el.removeAttribute('aria-current')});
  $('#currentSection').textContent=({'inicio':'Visão geral','biblioteca':'Biblioteca de prompts','criador':'Criador de prompts','backup':'Backup e dados'})[name];
  if(window.location.hash!=='#'+name) history.replaceState(null,'','#'+name);
  closeMenu();window.scrollTo({top:0,behavior:'instant'});
}
function closeMenu(){$('#sidebar').classList.remove('open');$('#sidebarScrim').hidden=true}
function toggleMenu(){const open=$('#sidebar').classList.toggle('open');$('#sidebarScrim').hidden=!open}
function closeDialog(id){$(id.startsWith('#')?id:'#'+id).close()}

function openEditor(existing=null){
  state.editingId=existing?.id||null;
  state.editorBefore=existing?.before_image||'';
  state.editorAfter=existing?.after_image||'';
  const form=$('#recipeForm');form.reset();
  $('#beforeFile').value='';$('#afterFile').value='';
  const values=existing||{};
  for(const field of ['title','summary','category','tool','input_type','prompt','style','lighting','camera','materials','preserve','changes','negative_prompt','tags','notes']){
    if(form.elements[field])form.elements[field].value=field==='tags'?(values.tags||[]).join(', '):(values[field]??'');
  }
  if(!existing){form.elements.category.value='Fachadas';form.elements.tool.value='Universal'}
  $('#editorTitle').textContent=existing?'Editar receita':'Nova receita';
  $('.advanced-fields').open=false;
  updateEditorPreview('before');updateEditorPreview('after');
  $('#recipeDialog').showModal();
  setTimeout(()=>form.elements.title.focus(),40);
}
function updateEditorPreview(side){
  const v=side==='before'?state.editorBefore:state.editorAfter;
  const file=$(`#${side}File`).files[0];
  const target=$(`#${side}Preview`);
  if(file){
    const objectUrl=URL.createObjectURL(file);
    target.innerHTML=`<img alt="Prévia da imagem selecionada" src="${objectUrl}">`;
    target.querySelector('img').addEventListener('load',()=>URL.revokeObjectURL(objectUrl),{once:true});
  }else if(allowedImage(v)){target.innerHTML=`<img alt="Imagem atual" src="${esc(v)}">`}
  else target.textContent='Sem imagem';
}
function readFileData(file){return new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=()=>reject(new Error('Não foi possível ler a imagem.'));reader.readAsDataURL(file)})}
async function uploadSelected(file){
  if(file.size>8*1024*1024)throw new Error('Cada imagem deve ter até 8 MB.');
  if(!['image/jpeg','image/png','image/webp'].includes(file.type))throw new Error('Formato inválido: use PNG, JPEG ou WebP.');
  const result=await request('/api/images',{method:'POST',data:{data:await readFileData(file)}});
  return result.url;
}
async function saveRecipe(event){
  event.preventDefault();
  const form=$('#recipeForm');
  if(!form.reportValidity())return;
  const button=$('#saveRecipeButton');button.disabled=true;
  try{
    const data={};
    for(const name of ['title','summary','category','tool','input_type','style','lighting','camera','materials','preserve','changes','prompt','negative_prompt','notes'])data[name]=form.elements[name].value;
    data.tags=form.elements.tags.value.split(',').map(x=>x.trim()).filter(Boolean);
    data.before_image=$('#beforeFile').files[0]?await uploadSelected($('#beforeFile').files[0]):state.editorBefore;
    data.after_image=$('#afterFile').files[0]?await uploadSelected($('#afterFile').files[0]):state.editorAfter;
    if(state.editingId){const old=state.items.find(x=>x.id===state.editingId);data.favorite=old?.favorite||false;await request(`/api/recipes/${state.editingId}`,{method:'PUT',data});toast('Receita atualizada.');}
    else{data.favorite=false;await request('/api/recipes',{method:'POST',data});toast('Receita adicionada à biblioteca.');}
    closeDialog('recipeDialog');await loadData();setView('biblioteca');
  }catch(err){toast(err.message,true)}finally{button.disabled=false}
}
function metadata(label,value){return value?`<div class="metadata-item"><span class="metadata-label">${esc(label)}</span><span class="metadata-value">${esc(value)}</span></div>`:''}
function detailMarkup(r){
  const before=allowedImage(r.before_image),after=allowedImage(r.after_image);
  let imageBlock='';
  if(before&&after){imageBlock=`<div class="comparison" id="comparison"><img class="comparison-base" src="${esc(before)}" alt="Imagem original"><img class="comparison-result" src="${esc(after)}" alt="Imagem de resultado"><div class="comparison-divider"></div><span class="comparison-handle">${icon('sliders')}</span><span class="comparison-label before">ANTES</span><span class="comparison-label after">DEPOIS</span><input id="comparisonRange" type="range" min="0" max="100" value="50" aria-label="Comparar imagem original e resultado, deslizando de antes para depois"></div>`}
  else if(before||after){imageBlock=`<div class="detail-hero"><img src="${esc(after||before)}" alt="${esc(after?'Imagem de resultado':'Imagem original')}"></div>`}
  else{imageBlock=`<div class="detail-hero"><div class="cover-placeholder c-${categoryClass(r.category)}"><span class="shape-one"></span><span class="shape-two"></span><span class="shape-three"></span></div></div>`}
  return `<div class="detail-layout">${imageBlock}<div class="detail-heading"><div><span class="overline">${esc(cName(r.category).toUpperCase())} · ${esc(r.tool.toUpperCase())}</span><h2 id="detailTitle">${esc(r.title)}</h2><p>${esc(r.summary||'Receita para visualização arquitetônica.')}</p></div><button class="icon-button" type="button" data-detail-action="favorite" title="${r.favorite?'Desfavoritar':'Favoritar'}" aria-label="${r.favorite?'Remover dos':'Adicionar aos'} favoritos" aria-pressed="${!!r.favorite}">${icon('bookmark')}</button></div><div class="detail-tags">${(r.tags||[]).map(t=>`<span class="tag">#${esc(t)}</span>`).join('')||'<span class="tag">Sem etiquetas</span>'}</div><div class="detail-metadata">${metadata('TIPO DE ENTRADA',r.input_type)}${metadata('ESTILO',r.style)}${metadata('ILUMINAÇÃO',r.lighting)}${metadata('CÂMERA',r.camera)}${metadata('MATERIAIS',r.materials)}${metadata('CRIADO EM',shortDate(r.created_at))}</div>${r.preserve?`<div class="detail-section"><h3>Elementos a preservar</h3><p>${esc(r.preserve)}</p></div>`:''}${r.changes?`<div class="detail-section"><h3>Alterações permitidas</h3><p>${esc(r.changes)}</p></div>`:''}<div class="detail-section"><h3>Prompt principal</h3><div class="detail-prompt" id="detailPrompt">${esc(r.prompt)}</div></div>${r.negative_prompt?`<div class="detail-section"><h3>Prompt negativo (quando aplicável)</h3><div class="detail-prompt">${esc(r.negative_prompt)}</div></div>`:''}${r.notes?`<div class="detail-section"><h3>Notas e testes</h3><p>${esc(r.notes)}</p></div>`:''}<div class="detail-actions"><button class="button button-main" data-detail-action="copy" type="button">${icon('copy')} Copiar prompt</button><button class="button button-secondary" data-detail-action="edit" type="button">${icon('edit')} Editar</button><button class="button button-plain" data-detail-action="duplicate" type="button">${icon('duplicate')} Duplicar</button><button class="button button-plain danger" data-detail-action="delete" type="button">${icon('trash')} Excluir</button></div></div>`;
}
function openDetail(id){
  const r=state.items.find(x=>x.id===id);if(!r)return;
  state.activeDetail=id;$('#detailContent').innerHTML=detailMarkup(r);
  if(!$('#detailDialog').open)$('#detailDialog').showModal();
  bindCompare();
}
function bindCompare(){
  const range=$('#comparisonRange');if(!range)return;
  const update=()=>{const n=Number(range.value);$('#comparison .comparison-result').style.clipPath=`inset(0 ${100-n}% 0 0)`;$('#comparison .comparison-divider').style.left=n+'%';$('#comparison .comparison-handle').style.left=n+'%';};
  range.addEventListener('input',update);update();
}
async function detailAction(action){
  const id=state.activeDetail,r=state.items.find(x=>x.id===id);if(!r)return;
  try{
    if(action==='copy'){await copyText(r.prompt);toast('Prompt copiado para a área de transferência.');return}
    if(action==='edit'){closeDialog('detailDialog');openEditor(r);return}
    if(action==='delete'){
      if(!confirm(`Excluir "${r.title}"? Esta ação não pode ser desfeita, exceto se você tiver um backup.`))return;
      await request('/api/recipes/'+id,{method:'DELETE'});closeDialog('detailDialog');await loadData();toast('Receita excluída.');return;
    }
    if(action==='duplicate'){
      await request('/api/recipes/'+id+'/duplicate',{method:'POST'});
      closeDialog('detailDialog');await loadData();toast('Cópia criada.');setView('biblioteca');return;
    }
    if(action==='favorite'){
      await toggleFavorite(id);openDetail(id);
    }
  }catch(err){toast(err.message,true)}
}
async function toggleFavorite(id){
  try{await request(`/api/recipes/${id}/favorite`,{method:'PATCH'});await loadData()}
  catch(err){toast(err.message,true)}
}
async function copyText(text){
  if(!text)throw new Error('Gere ou escolha um prompt para copiar.');
  try{await navigator.clipboard.writeText(text);return}
  catch{
    const box=document.createElement('textarea');box.value=text;box.style.position='fixed';box.style.opacity='0';document.body.appendChild(box);box.select();const success=document.execCommand('copy');box.remove();if(!success)throw new Error('Não foi possível copiar. Selecione o texto manualmente.');
  }
}
function buildPrompt(){
  const f=new FormData($('#composerForm'));
  const raw=n=>String(f.get(n)||'').trim();
  const base=raw('input_type');const project=raw('project_type');
  const fromText=base.startsWith('Descrição textual');
  const paragraphs=[
    `TAREFA\nCrie uma visualização arquitetônica de ${project.toLocaleLowerCase('pt-BR')}, adequada a uma apresentação profissional.${fromText?' Desenvolva um conceito a partir da descrição textual, sem tratar dimensões não informadas como medidas verificadas.':' Use a imagem fornecida como base principal e não a substitua por outro projeto.'}`,
    `ENTRADA E CONTEXTO\nTipo de entrada: ${base}.`,
    `LINGUAGEM VISUAL\nEstilo: ${raw('style')||'apresentação realista e sóbria'}. Iluminação: ${raw('lighting')}. Materiais e acabamentos: ${raw('materials')||'definir conforme a referência, com texturas em escala plausível'}.` ,
    `ELEMENTOS QUE DEVEM PERMANECER\n${fromText?'Respeite as características e requisitos explicitamente descritos, sem inventar informações técnicas.':raw('preserve')||'Preserve proporções, geometria e enquadramento da referência.'}`,
    `ALTERAÇÕES PERMITIDAS\n${raw('changes')||'Somente as alterações explicitamente solicitadas.'}`,
    `QUALIDADE E VERIFICAÇÃO\nMateriais coerentes, sombras plausíveis, composição equilibrada, verticais alinhadas quando aplicável. Evite elementos deformados, novas aberturas ou alterações não autorizadas. Confira o resultado com a base. O prompt expressa restrições desejadas; a fidelidade deve ser validada antes da aprovação.`
  ];
  if(raw('goal'))paragraphs.splice(2,0,`OBJETIVO ESPECÍFICO\n${raw('goal')}`);
  return paragraphs.join('\n\n');
}
function generatePrompt(showToast=false){state.promptDraft=buildPrompt();$('#promptPreview').textContent=state.promptDraft;if(showToast)toast('Prompt estruturado atualizado.');}
function saveComposer(){
  generatePrompt();
  const f=new FormData($('#composerForm'));const project=String(f.get('project_type'));
  const category= project.includes('Interior')?'Interiores': project.includes('Paisagismo')?'Paisagismo': project.includes('Planta')?'Plantas':project.includes('Reforma')?'Reformas':'Fachadas';
  openEditor({title:`${project} — prompt estruturado`,summary:'Receita criada no assistente de composição.',category,tool:'Universal',input_type:String(f.get('input_type')),style:String(f.get('style')),lighting:String(f.get('lighting')),materials:String(f.get('materials')),preserve:String(f.get('preserve')),changes:String(f.get('changes')),prompt:state.promptDraft,tags:['criador',category.toLocaleLowerCase('pt-BR')],notes:String(f.get('goal')||'')});
}
async function exportBackup(){
  try{
    const button=$('#exportBackup');button.disabled=true;
    const response=await fetch('/api/backup');
    if(!response.ok){const e=await response.json().catch(()=>({}));throw new Error(e.error||'Não foi possível exportar.')}
    const blob=await response.blob();const url=URL.createObjectURL(blob);
    const a=document.createElement('a');a.href=url;a.download=`archrender-hub-backup-${new Date().toISOString().slice(0,10)}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);toast('Backup gerado. Guarde o arquivo em local seguro.');
  }catch(err){toast(err.message,true)}finally{$('#exportBackup').disabled=false}
}
async function importBackup(event){
  const input=event.target;const file=input.files[0];if(!file)return;
  try{
    if(file.size>120*1024*1024)throw new Error('Arquivo acima de 120 MB.');
    const data=JSON.parse(await file.text());
    if(data.format!=='archrender-hub-v1'||!Array.isArray(data.recipes))throw new Error('Formato de backup incompatível.');
    if(!confirm(`Importar ${data.recipes.length} receitas? Identificadores já existentes serão substituídos.`))return;
    const result=await request('/api/restore',{method:'POST',data});await loadData();toast(`${result.restored} receitas restauradas com sucesso.`);setView('biblioteca');
  }catch(err){toast(err.message,true)}finally{input.value=''}
}
function clearFilters(){state.filterCategory='';state.filterTool='';state.favoritesOnly=false;$('#searchInput').value='';$('#categoryFilter').value='';$('#toolFilter').value='';$('#favoritesFilter').setAttribute('aria-pressed','false');renderLibrary()}
function setupEvents(){
  document.addEventListener('click',async event=>{
    const target=event.target.closest('[data-nav],[data-category],[data-open],[data-favorite],[data-close],[data-remove-image],[data-detail-action]');
    if(!target)return;
    if(target.matches('[data-nav]')){setView(target.dataset.nav);return}
    if(target.matches('[data-category]')){clearFilters();state.filterCategory=target.dataset.category;$('#categoryFilter').value=state.filterCategory;setView('biblioteca');renderLibrary();return}
    if(target.matches('[data-open]')){openDetail(target.dataset.open);return}
    if(target.matches('[data-favorite]')){event.stopPropagation();await toggleFavorite(target.dataset.favorite);return}
    if(target.matches('[data-close]')){closeDialog(target.dataset.close);return}
    if(target.matches('[data-remove-image]')){const side=target.dataset.removeImage.startsWith('before')?'before':'after';state[side==='before'?'editorBefore':'editorAfter']='';$(`#${side}File`).value='';updateEditorPreview(side);return}
    if(target.matches('[data-detail-action]')){await detailAction(target.dataset.detailAction)}
  });
  $('#brandLink').addEventListener('click',e=>{e.preventDefault();setView('inicio')});
  $('#menuButton').addEventListener('click',toggleMenu);
  $('#sidebarScrim').addEventListener('click',closeMenu);
  $$('#recipeDialog,#detailDialog').forEach(dialog=>{dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()})});
  ['topNewRecipe','libraryNewRecipe','emptyNewRecipe'].forEach(id=>$('#'+id).addEventListener('click',()=>openEditor()));
  $('#recipeForm').addEventListener('submit',saveRecipe);
  $('#beforeFile').addEventListener('change',()=>updateEditorPreview('before'));
  $('#afterFile').addEventListener('change',()=>updateEditorPreview('after'));
  $('#searchInput').addEventListener('input',renderLibrary);
  $('#categoryFilter').addEventListener('change',e=>{state.filterCategory=e.target.value;renderLibrary()});
  $('#toolFilter').addEventListener('change',e=>{state.filterTool=e.target.value;renderLibrary()});
  $('#sortFilter').addEventListener('change',renderLibrary);
  $('#favoritesFilter').addEventListener('click',()=>{state.favoritesOnly=!state.favoritesOnly;$('#favoritesFilter').setAttribute('aria-pressed',String(state.favoritesOnly));renderLibrary()});
  $('#clearFilters').addEventListener('click',clearFilters);
  $('#composerForm').addEventListener('input',()=>generatePrompt());
  $('#composerForm').addEventListener('change',()=>generatePrompt());
  $('#composerForm').addEventListener('reset',()=>setTimeout(()=>generatePrompt(),0));
  $('#generatePrompt').addEventListener('click',()=>generatePrompt(true));
  $('#copyComposer').addEventListener('click',async()=>{try{await copyText(state.promptDraft||buildPrompt());toast('Prompt copiado.')}catch(e){toast(e.message,true)}});
  $('#saveComposer').addEventListener('click',saveComposer);
  $('#exportBackup').addEventListener('click',exportBackup);
  $('#importBackup').addEventListener('change',importBackup);
  window.addEventListener('hashchange',()=>setView(location.hash.slice(1)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});
}
async function init(){
  setupIcons();setupEvents();
  generatePrompt();
  try{await loadData();setView(location.hash.slice(1)||'inicio')}
  catch(error){$('#featuredGrid').innerHTML=`<div class="empty-state"><h2>Servidor indisponível</h2><p>${esc(error.message)}</p></div>`;toast(error.message,true)}
}
document.addEventListener('DOMContentLoaded',init);
