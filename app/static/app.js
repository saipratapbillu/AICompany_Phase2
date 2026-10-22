(() => {
  const $ = id => document.getElementById(id);
  let requirements = [], selected = null;
  const esc = value => String(value ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
  async function api(url, options={}) {
    const response = await fetch(url, {headers:{'Content-Type':'application/json',...(options.headers||{})},...options});
    let body = null; try { body = await response.json(); } catch { body = {}; }
    if (!response.ok) throw new Error(body.detail || `Request failed (${response.status})`);
    return body;
  }
  async function checkHealth(){
    const card=$('healthCard'), text=$('healthText'); card.className='health'; text.textContent='Checking...';
    try { const x=await api('/health'); card.classList.add('ok'); text.textContent=`${x.database} on ${x.server} is ready`; }
    catch(e){card.classList.add('bad');text.textContent=e.message;}
  }
  async function loadRequirements(){
    $('requirementsList').innerHTML='<div class="empty">Loading requirements...</div>';
    try { requirements=await api('/requirements'); renderList(); if(selected){ const fresh=requirements.find(x=>x.requirement_id===selected.requirement_id); if(fresh) showDetails(fresh); } }
    catch(e){$('requirementsList').innerHTML=`<div class="empty">${esc(e.message)}</div>`;}
  }
  function renderList(){
    const q=$('search').value.trim().toLowerCase(), status=$('statusFilter').value;
    const items=requirements.filter(x=>(!q || `${x.title} ${x.description}`.toLowerCase().includes(q)) && (!status || x.status===status));
    $('requirementsList').innerHTML=items.length?items.map(x=>`<article class="req-card ${selected?.requirement_id===x.requirement_id?'selected':''}" data-id="${x.requirement_id}" tabindex="0"><h3>${esc(x.title)}</h3><div class="meta"><span class="badge ${esc(x.status)}">${esc(x.status)}</span><span>${esc(x.priority)} priority</span><span>${esc(x.requested_by)}</span></div></article>`).join(''):'<div class="empty">No requirements found. Create one using the form.</div>';
    document.querySelectorAll('.req-card').forEach(card=>{ const open=()=>showDetails(requirements.find(x=>x.requirement_id===card.dataset.id)); card.addEventListener('click',open); card.addEventListener('keydown',e=>{if(e.key==='Enter')open();}); });
  }
  function showDetails(item){
    selected=item; $('details').hidden=false; $('detailTitle').textContent=item.title; $('detailPriority').textContent=item.priority; $('detailOwner').textContent=item.requested_by; $('detailRisk').textContent=item.risk_level; $('detailDescription').textContent=item.description; $('detailStatus').textContent=item.status; $('detailStatus').className=`badge ${item.status}`; $('assessmentResult').innerHTML=''; renderList(); $('details').scrollIntoView({behavior:'smooth',block:'start'});
  }
  function resetForm(){ $('requirementForm').reset(); $('requirementId').value=''; $('requestedBy').value='HumanOwner'; $('priority').value='Medium'; $('formTitle').textContent='Create requirement'; $('saveBtn').textContent='Submit requirement'; $('formMessage').textContent=''; }
  $('requirementForm').addEventListener('submit',async e=>{
    e.preventDefault(); const id=$('requirementId').value; const body={title:$('title').value.trim(),description:$('description').value.trim(),requested_by:$('requestedBy').value.trim(),priority:$('priority').value}; if(id) body.modified_by=body.requested_by;
    const btn=$('saveBtn'), msg=$('formMessage'); btn.disabled=true; btn.innerHTML='<span class="spinner"></span>Saving'; msg.className='message';
    try { const saved=await api(id?`/requirements/${id}`:'/requirements',{method:id?'PUT':'POST',body:JSON.stringify(body)}); msg.className='message success'; msg.textContent=id?'Requirement updated successfully.':'Requirement created successfully.'; selected=saved; await loadRequirements(); showDetails(saved); if(!id) resetForm(); }
    catch(err){msg.className='message error';msg.textContent=err.message;}
    finally{btn.disabled=false;btn.textContent=id?'Update requirement':'Submit requirement';}
  });
  $('editBtn').addEventListener('click',()=>{if(!selected)return;$('requirementId').value=selected.requirement_id;$('title').value=selected.title;$('description').value=selected.description;$('requestedBy').value=selected.requested_by;$('priority').value=selected.priority;$('formTitle').textContent='Update requirement';$('saveBtn').textContent='Update requirement';window.scrollTo({top:220,behavior:'smooth'});});
  $('assessBtn').addEventListener('click',async()=>{
    if(!selected)return; const btn=$('assessBtn'); btn.disabled=true; btn.innerHTML='<span class="spinner"></span>AI CEO is assessing'; $('assessmentResult').innerHTML='';
    try { const r=await api(`/requirements/${selected.requirement_id}/assess`,{method:'POST',body:JSON.stringify({requested_by:selected.requested_by,force_reassessment:true})}); const a=r.assessment; $('assessmentResult').innerHTML=`<div class="assessment-card"><h3>Assessment completed</h3><p><b>${esc(a.classification)}</b> · ${esc(a.business_domain||'General')} · ${esc(a.complexity)} complexity</p><p>${esc(a.executive_summary)}</p><p><b>Risk:</b> ${esc(a.risk_level)} &nbsp; <b>Feasibility:</b> ${esc(a.feasibility)} &nbsp; <b>Human approval:</b> ${a.human_approval_required?'Required':'Not required'}</p><b>Departments</b><ul>${a.departments.map(d=>`<li>${esc(d.department_name)}${d.is_lead_department?' (Lead)':''}</li>`).join('')}</ul></div>`; await loadRequirements(); }
    catch(err){$('assessmentResult').innerHTML=`<div class="message error">${esc(err.message)}</div>`;}
    finally{btn.disabled=false;btn.textContent='Send to AI CEO for assessment';}
  });
  $('resetBtn').addEventListener('click',resetForm); $('refreshBtn').addEventListener('click',loadRequirements); $('healthBtn').addEventListener('click',checkHealth); $('search').addEventListener('input',renderList); $('statusFilter').addEventListener('change',renderList);
  checkHealth(); loadRequirements();
})();
