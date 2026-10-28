import {flushSync} from 'react-dom';
import {registerAtlasTools} from './agent-tools';
import {useEffect,useMemo,useRef,useState} from 'react';
import {Activity,ArrowUpRight,ChevronRight,Focus,Info,Layers3,Maximize,Minimize,Pause,RotateCcw,RotateCw,Search,X} from 'lucide-react';
import {Button} from '@/components/ui/button';
import {Badge} from '@/components/ui/badge';
import {Slider} from '@/components/ui/slider';
import {Switch} from '@/components/ui/switch';
import {Sheet,SheetContent,SheetTitle,SheetDescription} from '@/components/ui/sheet';
import {Combobox,ComboboxInput,ComboboxContent,ComboboxList,ComboboxItem,ComboboxEmpty} from '@/components/ui/combobox';
import {DirectionProvider} from '@base-ui/react/direction-provider';
import AnatomyScene from './scene';
import {DEFAULT_VISIBLE,SYSTEMS,getAnatomicalName,type Atlas,type Concept,type SceneState,type SystemId,type View} from './anatomy';
import {TRANSLATIONS,SYSTEM_TRANSLATIONS,EXPLANATION_TRANSLATIONS,type Lang} from './i18n';

const initial:SceneState={explode:0,visible:DEFAULT_VISIBLE,selected:[],isolate:false,view:'three-quarter',rotate:false,reset:0};

export default function Home(){
 const detailTitle=useRef<HTMLHeadingElement>(null);
 const [lang,setLang]=useState<Lang>('en');
 const [atlas,setAtlas]=useState<Atlas|null>(null);
 const [state,setState]=useState(initial);
 const [progress,setProgress]=useState(0);
 const [error,setError]=useState('');
 const [panel,setPanel]=useState<'layers'|'search'|null>(null);
 const [details,setDetails]=useState(false);
 const [about,setAbout]=useState(false);
 const [query,setQuery]=useState('');
 const [chosen,setChosen]=useState<Concept|null>(null);
 const [isFullscreen,setIsFullscreen]=useState(false);

 useEffect(()=>{
  const handleFsChange=()=>setIsFullscreen(Boolean(document.fullscreenElement));
  document.addEventListener('fullscreenchange',handleFsChange);
  return()=>document.removeEventListener('fullscreenchange',handleFsChange);
 },[]);

 const toggleFullscreen=()=>{
  if(!document.fullscreenElement){
   document.documentElement.requestFullscreen().catch(()=>{});
  }else{
   document.exitFullscreen().catch(()=>{});
  }
 };

 const t=TRANSLATIONS[lang];

 useEffect(()=>{
  const abort=new AbortController();
  setProgress(0);
  setError('');
  setAtlas(null);
  setChosen(null);
  setDetails(false);
  setState({...initial,visible:DEFAULT_VISIBLE});
  fetch('/models/atlas.json',{signal:abort.signal})
   .then(r=>{if(!r.ok)throw new Error('The anatomy catalogue could not be loaded.');return r.json();})
   .then(data=>setAtlas(data as Atlas))
   .catch(e=>{if(e.name!=='AbortError')setError(e.message);});
  return()=>abort.abort();
 },[]);

 useEffect(()=>{
  const key=(e:KeyboardEvent)=>{
   if(e.key==='/'&&!(e.target instanceof HTMLInputElement)&&!(e.target instanceof HTMLTextAreaElement)){
    e.preventDefault();
    setPanel('search');
    setDetails(false);
   }
  };
  window.addEventListener('keydown',key);
  return()=>window.removeEventListener('keydown',key);
 },[]);

 const parts=useMemo(()=>new Map(atlas?.parts.map(p=>[p.id,p])),[atlas]);
 const counts=useMemo(()=>Object.fromEntries(SYSTEMS.map(s=>[s.id,atlas?.parts.filter(p=>p.system===s.id).length??0])),[atlas]);
 const activeSystems=SYSTEMS.filter(s=>counts[s.id]>0);
 const selectedParts=state.selected.map(id=>parts.get(id)).filter(p=>!!p),selected=selectedParts[0],system=SYSTEMS.find(s=>s.id===selected?.system);
 const visibleCount=atlas?.parts.filter(p=>state.isolate?state.selected.includes(p.id):state.visible.includes(p.system)||state.selected.includes(p.id)).length??0;

 const results=useMemo(()=>{
  if(!atlas)return[];
  const term=query.toLowerCase().trim();
  if(!term){
   return ['heart','brain','liver','stomach','spleen','pancreas','urinary bladder','trachea']
     .map(name=>atlas.concepts.find(c=>c.name.toLowerCase()===name))
     .filter((x):x is Concept=>!!x);
  }
  return atlas.concepts
   .filter(c=>
     c.name.toLowerCase().includes(term) ||
     (c.name_fr && c.name_fr.toLowerCase().includes(term)) ||
     (c.name_ar && c.name_ar.includes(term)) ||
     c.id.toLowerCase().includes(term)
   )
   .sort((a,b)=>{
     const nameA = getAnatomicalName(a, lang).toLowerCase();
     const nameB = getAnatomicalName(b, lang).toLowerCase();
     const matchA = nameA.startsWith(term);
     const matchB = nameB.startsWith(term);
     if(matchA && !matchB) return -1;
     if(!matchA && matchB) return 1;
     return nameA.length - nameB.length;
   })
   .slice(0,80);
 },[atlas,query,lang]);

 const choose=(c:Concept)=>{
  setChosen(c);
  setState(s=>({...s,selected:c.elements,isolate:false,rotate:false}));
  setDetails(true);
  setPanel(null);
 };

 useEffect(()=>{
  if(!atlas)return;
  return registerAtlasTools(atlas,c=>flushSync(()=>choose(c)));
 },[atlas]);

 const choosePart=(id:string)=>{
  const p=parts.get(id);
  if(!p)return;
  setChosen({id:p.conceptId,name:p.name,name_fr:p.name_fr,name_ar:p.name_ar,elements:[id]});
  setState(s=>({...s,selected:[id],isolate:false,rotate:false}));
  setDetails(true);
  setPanel(null);
 };

 const toggle=(id:SystemId)=>{
  setDetails(false);
  setState(s=>({...s,selected:[],isolate:false,visible:s.visible.includes(id)?s.visible.filter(x=>x!==id):[...s.visible,id]}));
 };

 const reset=()=>{
  setState(s=>({...initial,visible:DEFAULT_VISIBLE,reset:s.reset+1}));
  setChosen(null);
  setDetails(false);
  setPanel(null);
 };

 const openPanel=(next:'layers'|'search')=>{
  setDetails(false);
  setPanel(p=>p===next?null:next);
 };

 const getSystemName=(id:SystemId)=>{
  return SYSTEM_TRANSLATIONS[id]?.[lang]?.name || SYSTEMS.find(s=>s.id===id)?.name || id;
 };

 const getExplanation=(name:string,system:SystemId)=>{
  const key=name.toLowerCase();
  if(EXPLANATION_TRANSLATIONS[key]?.[lang]) {
   return EXPLANATION_TRANSLATIONS[key][lang];
  }
  return SYSTEM_TRANSLATIONS[system]?.[lang]?.desc || '';
 };

 return (
  <DirectionProvider direction={lang==='ar'?'rtl':'ltr'}>
   <main className="studio" dir={lang==='ar'?'rtl':'ltr'}>
   {atlas&&<AnatomyScene atlas={atlas} state={{...state,lang,inspectorOpen:details&&selectedParts.length>0}} onSelect={choosePart} onProgress={n=>{setProgress(n);if(n===100)setError('');}} onError={setError}/>}
   <div className="vignette"/>
   
   <header className="studio-header">
    <div className="header-identity">
     <div className="header-title">{t.appTitle}</div>
     <div className="header-meta">{atlas?atlas.parts.length.toLocaleString():'2,234'} {t.modeledPieces} <span>·</span> {t.sourceCredit}</div>
    </div>

    <div className="atlas-logo-anchor">
     <div className="atlas-logo-badge">
      <svg className="atlas-logo-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
       <circle cx="12" cy="12" r="10"/>
       <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
       <path d="M2 12h20"/>
      </svg>
      <span className="atlas-logo-text">ATLAS</span>
      <span className="atlas-logo-dot"/>
     </div>
    </div>

    <div className="header-languages">
     <div className="lang-group">
      {(['en','fr','ar'] as Lang[]).map(l=>(
       <button
        key={l}
        onClick={()=>setLang(l)}
        className={`lang-btn ${lang===l?'active':''}`}
        aria-label={`Switch to ${l.toUpperCase()}`}
        aria-pressed={lang===l}
       >
        {l.toUpperCase()}
       </button>
      ))}
     </div>
    </div>
   </header>

   <aside className="unified-control-panel glass" role="toolbar" aria-label="Controls and search">
    <Button
     variant="ghost"
     className={`unified-search-btn ${panel==='search'?'active':''}`}
     onClick={()=>openPanel('search')}
     aria-label={t.findStructure}
     title={`${t.findStructure} ( / )`}
    >
     <Search size={16}/>
     <span className="search-label">{t.findStructure}</span>
     <kbd className="search-kbd">/</kbd>
    </Button>

    <div className="panel-divider" aria-hidden="true"/>

    <div className="view-preset-group" role="group" aria-label="Camera angles">
     {(['three-quarter','front','side','back'] as View[]).map((v,i)=>(
      <Button
       variant="ghost"
       key={v}
       className={`unified-tool-btn ${state.view===v?'active':''}`}
       aria-pressed={state.view===v}
       disabled={state.explode>.8&&v!=='front'}
       onClick={()=>setState(s=>({...s,view:v,reset:s.reset+1,rotate:false}))}
       title={[t.viewThreeQuarter,t.viewFront,t.viewSide,t.viewBack][i]}
       aria-label={[t.viewThreeQuarter,t.viewFront,t.viewSide,t.viewBack][i]}
      >
       <span>{['¾','F','S','B'][i]}</span>
      </Button>
     ))}
    </div>

    <div className="panel-divider" aria-hidden="true"/>

    <Button
     variant="ghost"
     disabled={state.explode>=.4}
     aria-label={state.rotate?t.pauseRotation:t.rotateBody}
     title={state.rotate?t.pauseRotation:t.rotateBody}
     className={`unified-tool-btn ${state.rotate?'active':''}`}
     onClick={()=>setState(s=>({...s,rotate:!s.rotate}))}
    >
     {state.rotate?<Pause size={16}/>:<RotateCw size={16}/>}
    </Button>

    <Button
     variant="ghost"
     className="unified-tool-btn"
     aria-label={t.reset}
     title={t.reset}
     onClick={reset}
    >
     <RotateCcw size={16}/>
    </Button>

    <Button
     variant="ghost"
     className={`unified-tool-btn ${isFullscreen?'active':''}`}
     aria-label={isFullscreen?t.exitFullscreen:t.fullscreen}
     title={isFullscreen?t.exitFullscreen:t.fullscreen}
     onClick={toggleFullscreen}
    >
     {isFullscreen?<Minimize size={16}/>:<Maximize size={16}/>}
    </Button>

    <Button
     variant="ghost"
     className="unified-tool-btn"
     aria-label={t.aboutAtlas}
     title={t.aboutAtlas}
     onClick={()=>{setDetails(false);setPanel(null);setAbout(true);}}
    >
     <Info size={16}/>
    </Button>
   </aside>

   <section className={`layers-panel glass ${panel==='layers'?'mobile-open':''}`} aria-label="Anatomical layers">
    <div className="panel-heading">
     <span>{t.systems}</span>
     <Button variant="ghost" className="mobile-only icon-button" onClick={()=>setPanel(null)} aria-label="Close systems"><X size={18}/></Button>
     <Badge variant="secondary" className="desktop-only small-number">{activeSystems.length}</Badge>
    </div>
    <div className="layer-presets">
     <Button variant="ghost" aria-pressed={activeSystems.every(x=>state.visible.includes(x.id))} onClick={()=>setState(s=>({...s,selected:[],isolate:false,visible:activeSystems.map(x=>x.id)}))}>{t.all}</Button>
     <Button variant="ghost" aria-pressed={state.visible.length===1&&state.visible[0]==='skeletal'} onClick={()=>setState(s=>({...s,selected:[],isolate:false,visible:['skeletal']}))}>{t.skeleton}</Button>
     <Button variant="ghost" aria-pressed={state.visible.length===6&&['cardiac','respiratory','digestive','urinary','endocrine','reproductive'].every(id=>state.visible.includes(id as SystemId))} onClick={()=>setState(s=>({...s,selected:[],isolate:false,visible:['cardiac','respiratory','digestive','urinary','endocrine','reproductive']}))}>{t.organs}</Button>
    </div>
    <div className="system-list">
     {activeSystems.map(s=>(
      <div className={`system-row ${state.visible.includes(s.id)?'enabled':''}`} key={s.id}>
       <Button variant="ghost" className="system-name" title={getSystemName(s.id)} onClick={()=>setState(v=>({...v,visible:[s.id],isolate:false,selected:[]}))}>
        <span className="system-dot" style={{background:s.color}}/>
        {getSystemName(s.id)}
        <span className="system-count">{counts[s.id]}</span>
       </Button>
       <Switch checked={state.visible.includes(s.id)} onCheckedChange={()=>toggle(s.id)} aria-label={getSystemName(s.id)} />
      </div>
     ))}
    </div>
    <div className="panel-foot">
     <span>{visibleCount.toLocaleString()} {t.piecesVisible}</span>
     <Button variant="ghost" onClick={()=>setState(s=>({...s,visible:[],selected:[],isolate:false}))}>{t.hideAll}</Button>
    </div>
   </section>

   {panel==='search'&&(
    <section className="search-panel glass" aria-label="Find anatomy">
     <div className="panel-heading">
      <span>{t.findStructure}</span>
      <Button variant="ghost" className="icon-button" onClick={()=>setPanel(null)} aria-label="Close search"><X size={18}/></Button>
     </div>
     <Combobox<Concept> items={results} value={null} onValueChange={value=>{if(value)choose(value);}} inputValue={query} onInputValueChange={setQuery} itemToStringLabel={c=>getAnatomicalName(c,lang)} filter={null} open onOpenChange={open=>{if(!open)setPanel(null);}}>
      <ComboboxInput autoFocus placeholder={t.searchPlaceholder} aria-label={t.searchPlaceholder} showTrigger={false}/>
      <ComboboxContent className="anatomy-search-results">
       <ComboboxEmpty>{t.noResults}</ComboboxEmpty>
       <ComboboxList>
        {(c:Concept)=>(
         <ComboboxItem key={c.id} value={c}>
          <span className="search-result-name">{getAnatomicalName(c,lang)}</span>
          <span className="small-number">{c.elements.length} {c.elements.length===1?t.piece:t.pieces}</span>
         </ComboboxItem>
        )}
       </ComboboxList>
      </ComboboxContent>
     </Combobox>
     <p className="search-note">{query?t.showingMatches(80):t.searchNote}</p>
    </section>
   )}


   <div className="scene-caption">
    <span className="caption-line"/>
    <span>{state.isolate?(chosen?getAnatomicalName(chosen,lang):(lang==='ar'?'الهيكل المحدد':lang==='fr'?'STRUCTURE SÉLECTIONNÉE':'SELECTED STRUCTURE')):state.explode>.95?(lang==='ar'?'المخزون التشريحي':lang==='fr'?'INVENTAIRE ANATOMIQUE':'ANATOMICAL INVENTORY'):state.explode>.05?(lang==='ar'?'الهياكل المفككة':lang==='fr'?'STRUCTURES SÉPARÉES':'SEPARATED STRUCTURES'):(lang==='ar'?'الإنسان البالغ · ذكر':lang==='fr'?'ADULTE HUMAIN · HOMME':'ADULT HUMAN · MALE')}</span>
    <span className="caption-line"/>
   </div>

   <div className="bottom-dock glass">
    <Button variant="ghost" className="mobile-only dock-layers" onClick={()=>openPanel('layers')} aria-label={t.systems}>
     <Layers3 size={20}/>
     <span>{t.systems}</span>
    </Button>
    <div className="explode-control">
     <div className="explode-label">
      <label id="explode-label">{t.explodeAnatomy}</label>
      <output dir="ltr">{Math.round(state.explode*100)}<span>%</span></output>
     </div>
     <Slider dir={lang==='ar'?'rtl':'ltr'} aria-labelledby="explode-label" min={0} max={100} step={1} value={[state.explode*100]} onValueChange={v=>setState(s=>({...s,explode:(Array.isArray(v)?v[0]:v)/100,view:(Array.isArray(v)?v[0]:v)>80?'front':s.view,rotate:false}))}/>
     <div className="slider-endpoints">
      <span>{t.assembled}</span>
      <span>{t.everyPiece}</span>
     </div>
    </div>
    <Button variant="ghost" className="dock-reset" onClick={reset} aria-label={t.reset}>
     <RotateCcw size={18}/>
     <span>{t.reset}</span>
    </Button>
   </div>

   <footer className="studio-footer">
    <span>{t.controlsHint}</span>
    <Button variant="ghost" onClick={()=>{setDetails(false);setPanel(null);setAbout(true);}}>{t.sourceCreditsBtn} <ArrowUpRight size={12}/></Button>
   </footer>

   {progress<100&&!error&&(
    <div className="loading glass" role="status">
     <Activity size={18}/>
     <div>
      <strong>{t.preparingAnatomy}</strong>
      <span>{t.loadingPiece(progress, atlas?.parts.length.toLocaleString()??'2,234')}</span>
      <div className="loading-track"><i style={{width:`${progress}%`}}/></div>
     </div>
    </div>
   )}

   {error&&(
    <div className="loading glass error" role="alert">
     <p>{error}</p>
     <Button variant="ghost" onClick={()=>location.reload()}>{t.reloadViewer}</Button>
    </div>
   )}

   <Sheet open={details&&selectedParts.length>0} modal={false} disablePointerDismissal onOpenChange={setDetails}>
    <SheetContent initialFocus={detailTitle} className={`detail-sheet glass ${state.isolate?'is-isolated':''}`} showCloseButton={true}>
     <div className="detail-header">
      <div className="detail-accent" style={{background:system?.color}}/>
      <div className="eyebrow">{system?getSystemName(system.id):(lang==='ar'?'التشريح':lang==='fr'?'ANATOMIE':'ANATOMY')}</div>
      <SheetTitle ref={detailTitle} tabIndex={-1} className="structure-title">{chosen?getAnatomicalName(chosen,lang):''}</SheetTitle>
     </div>
     <div className="detail-scroll" key={`${chosen?.id}-${state.isolate}`}>
      <SheetDescription className="structure-description">
       {chosen&&selected?getExplanation(chosen.name,selected.system):''}
      </SheetDescription>
      <div className="structure-meta">
       <span>{t.atlasReference}<strong>{chosen?.id}</strong></span>
       <span>{t.selectedPieces}<strong>{state.selected.length.toLocaleString()}</strong></span>
      </div>
      {selectedParts.length>1&&(
       <div className="member-list">
        <h3>{t.includedStructures}</h3>
        {selectedParts.slice(0,50).map(p=>(
         <Button variant="ghost" key={p.id} onClick={()=>choosePart(p.id)}>
          <span>{getAnatomicalName(p,lang)}</span>
          <ChevronRight size={14} className={lang==='ar'?'rotate-180':''}/>
         </Button>
        ))}
        {selectedParts.length>50&&<p>{t.morePieces(selectedParts.length-50)}</p>}
       </div>
      )}
      <a className="source-link" href="https://lifesciencedb.jp/bp3d/" target="_blank" rel="noreferrer">
       {t.viewAnatomicalSource} <ArrowUpRight size={14}/>
      </a>
     </div>
     <div className="detail-actions">
      <Button className={`primary-action ${state.isolate?'active':''}`} onClick={()=>setState(s=>({...s,isolate:!s.isolate,explode:0}))}>
       <Focus size={18}/>
       {state.isolate?t.showSurrounding:t.isolateStructure}
       <ChevronRight size={16} className={lang==='ar'?'rotate-180':''}/>
      </Button>
      <Button variant="ghost" className="secondary-action" onClick={()=>{setState(s=>({...s,selected:[],isolate:false}));setDetails(false);}}>
       {t.clearSelection}
      </Button>
     </div>
    </SheetContent>
   </Sheet>

   <Sheet open={about} onOpenChange={setAbout}>
    <SheetContent className="about-sheet glass">
     <div className="eyebrow">{t.aboutEyebrow}</div>
     <SheetTitle className="structure-title">{t.aboutTitle}</SheetTitle>
     <SheetDescription>{t.aboutDesc}</SheetDescription>
     <div className="about-copy">
      <p><strong>{t.aboutCopyMale}</strong><br/>{t.aboutCopyBody}</p>
      <p>{t.aboutCopyDisclaimer}</p>
      <p>{t.aboutCopyColors}</p>
      <h3>{t.sourceHeading}</h3>
      <p>{t.licenseText}</p>
      <a href="https://dbarchive.biosciencedbc.jp/en/bodyparts3d/lic.html" target="_blank" rel="noreferrer">{t.datasetLicense} <ArrowUpRight size={14}/></a>
      <a href="https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html" target="_blank" rel="noreferrer">{t.originalGeometry} <ArrowUpRight size={14}/></a>
      <a href="https://academic.oup.com/nar/article/37/suppl_1/D782/1000752" target="_blank" rel="noreferrer">{t.sourcePublication} <ArrowUpRight size={14}/></a>
     </div>
    </SheetContent>
   </Sheet>
  </main>
 </DirectionProvider>
 );
}
