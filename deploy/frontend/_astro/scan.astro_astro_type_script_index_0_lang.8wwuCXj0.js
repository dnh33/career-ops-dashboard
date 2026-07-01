import{n as e,r as t}from"./colors.D4fb9LWo.js";var n=document.getElementById(`scan-btn`),r=document.getElementById(`form-error`),i=document.getElementById(`scan-progress`),a=document.getElementById(`progress-bar`),o=document.getElementById(`progress-count`),s=document.getElementById(`progress-status`),c=document.getElementById(`scan-results`),l=document.getElementById(`results-grid`),u=document.getElementById(`results-total`),d=document.getElementById(`scan-empty`),f=document.getElementById(`scan-error`),p=document.getElementById(`error-retry-btn`),m=!1;function h(e){e.classList.remove(`hidden`)}function g(e){e.classList.add(`hidden`)}function _(){g(i),g(c),g(d),g(f),a.style.width=`0%`,o.textContent=`0 jobs found`,s.textContent=`Connecting to job board API…`}function v(n){let r=t(n),i=e(r),a=2*Math.PI*17,o=a-Math.max(0,Math.min(5,n))/5*a;return`
      <div class="inline-flex flex-col items-center gap-0.5" role="img" aria-label="Score: ${n.toFixed(1)} out of 5. Grade ${r}">
        <div class="relative flex items-center justify-center rounded-full" style="width:36px;height:36px;background:${i.bg};">
          <svg width="36" height="36" class="absolute inset-0 -rotate-90" viewBox="0 0 36 36">
            <circle cx="18" cy="18" r="17" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2.5"/>
            <circle cx="18" cy="18" r="17" fill="none" stroke="${i.stroke}" stroke-width="2.5" stroke-linecap="round"
              stroke-dasharray="${a}" stroke-dashoffset="${o}" style="transition: stroke-dashoffset 600ms ease-out;"/>
          </svg>
          <span class="relative font-bold text-xs" style="color:${i.text};">${r}</span>
        </div>
        <span class="text-[10px] text-[var(--text-muted)] font-mono">${n.toFixed(1)}</span>
      </div>
    `}function y(e){c.classList.remove(`hidden`),u.textContent=`${e.length} posting${e.length===1?``:`s`}`,l.innerHTML=e.map(e=>`
      <article class="bg-[var(--bg-secondary)] border border-[var(--border-default)] rounded-lg p-4 sm:p-5 hover:border-[var(--accent-primary)]/40 transition-colors group cursor-pointer card-interactive">
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1 min-w-0">
            <h4 class="text-sm font-semibold text-[var(--text-primary)] truncate group-hover:text-[var(--accent-primary)] transition-colors">${e.title}</h4>
            <p class="text-xs text-[var(--text-secondary)] mt-0.5">${e.company}${e.location?` · ${e.location}`:``}</p>
          </div>
          ${v(e.score)}
        </div>
        <div class="flex items-center justify-between mt-4 pt-3 border-t border-[var(--border-default)]">
          <a href="${e.url}" target="_blank" rel="noopener noreferrer" class="text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)] font-mono truncate max-w-[180px]" title="${e.url}">
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
    `).join(``)}async function b(){if(m)return;let e=document.getElementById(`board-url`),t=e.value.trim();if(!t||!t.startsWith(`http`)){h(r),e.focus();return}g(r),_(),h(i),g(c),g(d),m=!0,n.disabled=!0,n.textContent=`Scanning…`;try{a.style.width=`15%`,o.textContent=`Starting scan…`,s.textContent=`Triggering job board scanner…`;let e=await fetch(`/api/scan`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({dry_run:!1})});if(!e.ok)throw Error(`Scan request failed: `+e.status);for(let e=0;e<60;e++){await new Promise(e=>setTimeout(e,2e3));let t=await(await fetch(`/api/scan/status`)).json(),n=Math.min(15+e*1.5,95);if(a.style.width=`${n}%`,s.textContent=t.status===`running`?`Scanning job boards…`:t.status===`completed`?`Scan complete!`:t.status===`error`?`Scan failed`:`Waiting…`,t.results&&t.results.length>0&&(o.textContent=`${t.results.length} result${t.results.length===1?``:`s`}`),t.status===`completed`||t.status===`error`){if(t.status===`error`)throw Error(t.error||`Scan failed`);a.style.width=`100%`,o.textContent=`${t.results.length} result${t.results.length===1?``:`s`}`;let e=t.results.filter(e=>e&&!e.startsWith(`#`)&&!e.startsWith(`---`)).map((e,t)=>{let n=e.split(`|`).map(e=>e.trim());return n.length>=3?{id:String(t+1),title:n[0],company:n[1],score:0,url:n[2],location:n[3]||``}:{id:String(t+1),title:e,company:``,score:0,url:``,location:``}});await new Promise(e=>setTimeout(e,400)),g(i),e.length>0?y(e):h(d);break}}}catch(e){g(i),h(f),console.error(`Scan failed:`,e)}finally{m=!1,n.disabled=!1,n.textContent=`Run Scan`}}n.addEventListener(`click`,b),p.addEventListener(`click`,b),document.querySelectorAll(`#board-url, #keyword, #location`).forEach(e=>{e.addEventListener(`keydown`,e=>{e.key===`Enter`&&b()})}),window.addEventListener(`scan:evaluate`,(e=>{let t=e.detail;t&&t.url?window.location.href=`/evaluate?url=`+encodeURIComponent(t.url):window.location.href=`/evaluate`}));