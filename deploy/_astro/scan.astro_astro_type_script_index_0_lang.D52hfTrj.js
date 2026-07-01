var e=document.getElementById(`scan-btn`),t=document.getElementById(`form-error`),n=document.getElementById(`scan-progress`),r=document.getElementById(`progress-bar`),i=document.getElementById(`progress-count`),a=document.getElementById(`progress-status`),o=document.getElementById(`scan-results`),s=document.getElementById(`results-grid`),c=document.getElementById(`results-total`),l=document.getElementById(`scan-empty`),u=document.getElementById(`scan-error`),d=document.getElementById(`error-retry-btn`),f=!1,p=[{id:`1`,title:`Senior AI Consultant`,company:`Bewise ApS`,score:4.2,url:`https://bewise.dk/careers/ai-consultant`,location:`Hjørring`},{id:`2`,title:`Full-Stack Developer`,company:`NorthRange`,score:3.8,url:`https://northrange.io/jobs/fullstack`,location:`Aalborg`},{id:`3`,title:`ML Engineer`,company:`TechCorp`,score:4.5,url:`https://techcorp.com/jobs/ml-eng`,location:`Remote`},{id:`4`,title:`Data Platform Lead`,company:`DataFlow`,score:3.2,url:`https://dataflow.dk/careers`,location:`Copenhagen`},{id:`5`,title:`NLP Specialist`,company:`LangAI`,score:4.7,url:`https://lang.ai/jobs/nlp`,location:`Remote`},{id:`6`,title:`DevOps Engineer`,company:`CloudNordic`,score:2.9,url:`https://cloudnordic.dev/careers`,location:`Aarhus`}];function m(e){e.classList.remove(`hidden`)}function h(e){e.classList.add(`hidden`)}function g(){h(n),h(o),h(l),h(u),r.style.width=`0%`,i.textContent=`0 jobs found`,a.textContent=`Connecting to job board API…`}function _(e){let t=Math.max(0,Math.min(5,e)),n=t>=4.5?`A`:t>=3.5?`B`:t>=2.5?`C`:t>=1.5?`D`:`F`,r=t>=4?`#22c55e`:t>=3?`#eab308`:t>=2?`#f97316`:`#ef4444`,i=t>=4?`#166534`:t>=3?`#854d0e`:t>=2?`#9a3412`:`#991b1b`,a=t>=4?`#86efac`:t>=3?`#fde047`:t>=2?`#fdba74`:`#fca5a5`,o=2*Math.PI*17,s=o-t/5*o;return`
      <div class="inline-flex flex-col items-center gap-0.5" role="img" aria-label="Score: ${t.toFixed(1)} out of 5. Grade ${n}">
        <div class="relative flex items-center justify-center rounded-full" style="width:36px;height:36px;background:${i};">
          <svg width="36" height="36" class="absolute inset-0 -rotate-90" viewBox="0 0 36 36">
            <circle cx="18" cy="18" r="17" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2.5"/>
            <circle cx="18" cy="18" r="17" fill="none" stroke="${r}" stroke-width="2.5" stroke-linecap="round"
              stroke-dasharray="${o}" stroke-dashoffset="${s}" style="transition: stroke-dashoffset 600ms ease-out;"/>
          </svg>
          <span class="relative font-bold text-xs" style="color:${a};">${n}</span>
        </div>
        <span class="text-[10px] text-slate-500 font-mono">${t.toFixed(1)}</span>
      </div>
    `}function v(e){o.classList.remove(`hidden`),c.textContent=`${e.length} posting${e.length===1?``:`s`}`,s.innerHTML=e.map(e=>`
      <article class="bg-[var(--bg-secondary)] border border-slate-800 rounded-lg p-4 sm:p-5 hover:border-[var(--accent-primary)]/40 transition-colors group">
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1 min-w-0">
            <h4 class="text-sm font-semibold text-slate-100 truncate group-hover:text-[var(--accent-primary)] transition-colors">${e.title}</h4>
            <p class="text-xs text-slate-400 mt-0.5">${e.company}${e.location?` · ${e.location}`:``}</p>
          </div>
          ${_(e.score)}
        </div>
        <div class="flex items-center justify-between mt-4 pt-3 border-t border-slate-800">
          <a href="${e.url}" target="_blank" rel="noopener noreferrer" class="text-xs text-slate-500 hover:text-slate-300 font-mono truncate max-w-[180px]" title="${e.url}">
            ${e.url.replace(/^https?:\/\//,``).replace(/\/$/,``)}
          </a>
          <button
            type="button"
            class="ml-3 px-3 py-1.5 text-xs font-medium text-[var(--accent-primary)] border border-[var(--accent-primary)]/30 rounded-md hover:bg-[var(--accent-primary)]/10 transition-colors flex-shrink-0"
            onclick="window.dispatchEvent(new CustomEvent('scan:evaluate', { detail: ${JSON.stringify(e).replace(/</g,`\\u003c`)} }))"
          >
            Evaluate this posting
          </button>
        </div>
      </article>
    `).join(``)}async function y(){if(f)return;let s=document.getElementById(`board-url`),c=s.value.trim();if(!c||!c.startsWith(`http`)){m(t),s.focus();return}h(t),g(),m(n),h(o),h(l),f=!0,e.disabled=!0,e.textContent=`Scanning…`;try{for(let e of[{pct:15,count:0,status:`Connecting to job board API…`},{pct:35,count:1,status:`Fetching job listings…`},{pct:55,count:2,status:`Found 2 postings so far…`},{pct:75,count:4,status:`Found 4 postings, filtering…`},{pct:90,count:5,status:`Applying keyword and location filters…`},{pct:100,count:6,status:`Scan complete!`}])await new Promise(e=>setTimeout(e,600)),r.style.width=`${e.pct}%`,i.textContent=`${e.count} job${e.count===1?``:`s`} found`,a.textContent=e.status;await new Promise(e=>setTimeout(e,400)),h(n),v(p)}catch(e){h(n),m(u),console.error(`Scan failed:`,e)}finally{f=!1,e.disabled=!1,e.textContent=`Run Scan`}}e.addEventListener(`click`,y),d.addEventListener(`click`,y),document.querySelectorAll(`#board-url, #keyword, #location`).forEach(e=>{e.addEventListener(`keydown`,e=>{e.key===`Enter`&&y()})}),window.addEventListener(`scan:evaluate`,(e=>{console.log(`Evaluate posting:`,e.detail)}));