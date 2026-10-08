// Merge per-group outputs into research_output top-level files.
const fs=require("fs"),path=require("path");
const R="/mnt/project-files/research_output_cognetti", W=R+"/_work";
const rd=f=>{try{return JSON.parse(fs.readFileSync(f,"utf8"))}catch(e){return null}};
const roster=[].concat(...fs.readdirSync(W+"/worklists").map(f=>rd(W+"/worklists/"+f).map(i=>({id:i.siteRecord.id,tier:1})))); const T={}; roster.forEach(x=>T[x.id]=x);
const groups=fs.readdirSync(W+"/worklists").map(f=>f.replace(".json",""));
const all={new_people:[],stories:[],leads:[]}; const bad=[];
for(const g of groups) for(const k of Object.keys(all)){ const a=rd(`${W}/${g}/${k}.json`); if(Array.isArray(a)) a.forEach(x=>all[k].push({...x,_group:g})); }
// people
const people={}; for(const f of fs.readdirSync(R+"/people")){ if(!f.endsWith(".json"))continue; const p=rd(R+"/people/"+f); if(!p){bad.push(f);continue;} people[p.id||f.replace(".json","")]=p; }
const completed=Object.keys(people); const living=completed.filter(id=>people[id].status==="living_detected");
const rem={1:0,2:0,3:0}; for(const x of roster){ if(x.tier!=="skip"&&!people[x.id]) rem[x.tier]++; }
const inprog=groups.map(g=>{const p=rd(`${W}/${g}/progress.json`);return p&&p.inProgress?`${g}:${p.inProgress}`:null}).filter(Boolean);
const skip=[];
fs.writeFileSync(R+"/progress.json",JSON.stringify({lastUpdated:new Date().toISOString(),completed:completed.sort(),inProgress:inprog.join("; "),skippedLiving:[...skip,...living],remainingByTier:rem},null,1));
const strip=a=>a.map(({_group,...x})=>x);
fs.writeFileSync(R+"/new_people.json",JSON.stringify(strip(all.new_people),null,1));
fs.writeFileSync(R+"/stories.json",JSON.stringify(strip(all.stories),null,1));
fs.writeFileSync(R+"/leads.json",JSON.stringify(strip(all.leads),null,1));
// media manifest
const cols=["personId","type","title","date","pageUrl","directUrl","repository","rights","downloadable","downloaded","localPath","suggestedFile","people"];
const esc=v=>{v=v==null?"":Array.isArray(v)?v.join(";"):String(v); return /[",\n\r]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};
const rows=[cols.join(",")]; let nMedia=0,nDl=0; const seen=new Set();
const addMedia=(pid,m)=>{ const key=pid+"|"+(m.pageUrl||"")+"|"+(m.directUrl||"")+"|"+(m.title||""); if(seen.has(key))return; seen.add(key);
  let lp=m.localPath||""; let dl=m.downloaded===true; if(!lp&&m.suggestedFile&&fs.existsSync(R+"/"+m.suggestedFile)){lp=m.suggestedFile;dl=true;} if(lp&&!fs.existsSync(R+"/"+lp.replace(/^research_output\//,""))) dl=false;
  nMedia++; if(dl)nDl++; rows.push(cols.map(c=>esc(c==="personId"?pid:c==="downloaded"?dl:c==="localPath"?lp:c==="people"?(m.people||[pid]):m[c])).join(",")); };
let nSrc=0; const status={};
for(const [id,p] of Object.entries(people)){ status[p.status]=(status[p.status]||0)+1; nSrc+=(p.sources||[]).length; for(const m of p.media||[]) addMedia(id,m); }
for(const p of all.new_people){ nSrc+=(p.sources||[]).length; for(const m of p.media||[]) addMedia(p.id,m); }
fs.writeFileSync(R+"/media_manifest.csv",rows.join("\n")+"\n");
const byTier={1:0,2:0,3:0}; completed.forEach(id=>{const t=T[id]&&T[id].tier; if(byTier[t]!==undefined)byTier[t]++});
const stats={people:completed.length,byTier,status,newSources:nSrc,media:nMedia,downloaded:nDl,newPeople:all.new_people.length,stories:all.stories.length,leads:all.leads.length,remaining:rem,badFiles:bad,unknownIds:completed.filter(id=>!T[id])};
fs.writeFileSync(W+"/merge_stats.json",JSON.stringify(stats,null,1)); console.log(JSON.stringify(stats));
