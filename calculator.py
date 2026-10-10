import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ali Jamil | Scientific Calculator", page_icon="🧮", layout="centered")

html_app = r"""
<div id="ajcalc">
<style>
  #ajcalc{font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;color:#f7faf8}
  .shell{max-width:820px;margin:0 auto}
  .brand{text-align:center;font-size:13px;font-weight:800;letter-spacing:4px;color:#e8f1eb}
  .title{text-align:center;font-size:31px;font-weight:850;line-height:1.12;margin:2px 0;color:#fff}
  .subtitle{text-align:center;font-size:10px;letter-spacing:3px;color:#b2c9bb;margin:7px 0 18px}
  .screen{background:linear-gradient(145deg,#020704,#071b10 48%,#020504);border:1px solid #254a37;border-radius:17px;padding:13px 18px;min-height:112px;box-sizing:border-box;text-align:right;box-shadow:inset 0 0 25px #000,0 7px 22px #0007;margin-bottom:10px;overflow:hidden}
  .expression{min-height:23px;color:#f3f5f4;font-size:14px;line-height:1.5;overflow-wrap:anywhere}
  .result{min-height:43px;color:#ff303f;font-size:36px;font-weight:800;line-height:1.2;text-shadow:0 0 5px #ff1429,0 0 13px #ff2639,0 0 26px #b50019;overflow-wrap:anywhere}
  .controls{display:grid;grid-template-columns:1fr 1fr 1fr 58px;gap:8px;margin-bottom:14px}
  button{cursor:pointer;border:1px solid #313a35;border-radius:10px;min-height:38px;font-size:14px;font-weight:750;transition:filter .12s,transform .12s}
  button:hover{filter:brightness(1.16);transform:translateY(-1px)}
  button:focus-visible{outline:2px solid #b4ffd0;outline-offset:2px}
  .utility{background:#252e29;color:#f7faf8;border-color:#48564d;font-size:12px}
  .power{font-size:11px;color:white;min-height:34px}
  .power.on{background:#167c45;border-color:#38e982;box-shadow:0 0 10px #20d76b66}
  .power.off{background:#9f202b;border-color:#ff4a55;box-shadow:0 0 10px #ff263955}
  .columns{display:grid;grid-template-columns:1.18fr 1fr;gap:14px}
  .section-label{font-size:11px;letter-spacing:2px;font-weight:800;color:#a9c2b1;margin:7px 0 10px}
  .science-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px}
  .keypad{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
  .science{background:#18221c;color:#f4faf5;border-color:#354b3b;min-height:36px;padding:3px 1px;font-size:12px}
  .number{background:#111412;color:#fff;border-color:#303a33}
  .operator,.equals{background:#F79422;color:#17110a;border-color:#ffb65f;font-size:18px}
  .history{margin-top:18px}
  .history-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
  .history-item{border:1px solid #273e30;background:#0b1510;border-radius:10px;padding:9px 10px;min-width:0}
  .history-expr{color:#c5d3c9;font-size:12px;overflow-wrap:anywhere}
  .history-result{color:#ff4a57;font-weight:800;font-size:17px;overflow-wrap:anywhere}
  .hint{font-size:11px;color:#809487;margin-top:9px;text-align:center}
  @media(max-width:600px){.title{font-size:25px}.columns{grid-template-columns:1fr}.science-grid{gap:6px}.keypad{gap:7px}.history-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.result{font-size:30px}}
</style>
<div class="shell">
  <div class="brand">ALI JAMIL</div>
  <div class="title">Scientific Calculator</div>
  <div class="subtitle">ADVANCED CALCULATION SYSTEM</div>
  <div class="screen" aria-live="polite">
    <div class="expression" id="expr">&nbsp;</div>
    <div class="result" id="result">&nbsp;</div>
  </div>
  <div class="controls">
    <button class="utility" data-action="delete">DEL</button>
    <button class="utility" data-action="clear-entry">CLR</button>
    <button class="utility" data-action="clear">AC</button>
    <button class="power on" id="power">● ON</button>
  </div>
  <div class="columns">
    <section>
      <div class="section-label">SCIENTIFIC FUNCTIONS</div>
      <div class="science-grid" id="science">
        <button class="science" data-value="DEG">DEG</button><button class="science" data-value="RAD">RAD</button><button class="science" data-action="second">2nd</button><button class="science" data-value="sin(">sin</button>
        <button class="science" data-value="cos(">cos</button><button class="science" data-value="tan(">tan</button><button class="science" data-value="asin(">sin⁻¹</button><button class="science" data-value="acos(">cos⁻¹</button>
        <button class="science" data-value="atan(">tan⁻¹</button><button class="science" data-value="sqrt(">√</button><button class="science" data-value="^2">x²</button><button class="science" data-value="^">xʸ</button>
        <button class="science" data-value="log(">log</button><button class="science" data-value="ln(">ln</button><button class="science" data-value="π">π</button><button class="science" data-value="e">e</button>
        <button class="science" data-value="!">!</button><button class="science" data-value="(">(</button><button class="science" data-value=")">)</button><button class="science" data-value="%">%</button>
        <button class="science" data-action="ans">ANS</button><button class="science" data-action="mplus">M+</button><button class="science" data-action="mr">MR</button><button class="science" data-action="mc">MC</button>
      </div>
    </section>
    <section>
      <div class="section-label">KEYPAD</div>
      <div class="keypad">
        <button class="number" data-value="7">7</button><button class="number" data-value="8">8</button><button class="number" data-value="9">9</button><button class="operator" data-value="+">+</button>
        <button class="number" data-value="4">4</button><button class="number" data-value="5">5</button><button class="number" data-value="6">6</button><button class="operator" data-value="-">−</button>
        <button class="number" data-value="1">1</button><button class="number" data-value="2">2</button><button class="number" data-value="3">3</button><button class="operator" data-value="*">×</button>
        <button class="number" data-value=".">.</button><button class="number" data-value="0">0</button><button class="equals" data-action="equals">=</button><button class="operator" data-value="/">÷</button>
      </div>
    </section>
  </div>
  <section class="history">
    <div class="section-label">CALCULATION HISTORY</div>
    <div class="history-grid" id="history"></div>
  </section>
  <div class="hint">Keyboard: numbers and operators · Enter = calculate · Backspace = delete · Esc = clear</div>
</div>
<script>
(function(){
 const root=document.getElementById('ajcalc');
 if(root.dataset.ready)return; root.dataset.ready='1';
 const $=id=>root.querySelector('#'+id);
 let expression='', result='', isOn=true, angle='DEG', second=false, answer=0, memory=0, history=[];
 const exprEl=$('expr'), resultEl=$('result'), powerBtn=$('power');
 function paint(){
   exprEl.textContent=expression||' ';
   resultEl.textContent=result||' ';
   powerBtn.textContent=isOn?'● ON':'● OFF';
   powerBtn.className='power '+(isOn?'on':'off');
   root.querySelectorAll('button').forEach(b=>{
     if(b!==powerBtn)b.disabled=!isOn;
   });
   $('history').innerHTML=history.map(h=>'<div class="history-item"><div class="history-expr">'+escapeHtml(h[0])+' · '+h[2]+'</div><div class="history-result">= '+escapeHtml(h[1])+'</div></div>').join('');
 }
 function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
 function add(s){if(!isOn)return;expression+=s;result='';paint();}
 function clear(){expression='';result='';paint();}
 function del(){expression=expression.slice(0,-1);result='';paint();}
 function trig(fn,x){return angle==='DEG'?fn(x*Math.PI/180):fn(x);}
 function inv(fn,x){let y=fn(x);return angle==='DEG'?y*180/Math.PI:y;}
 function fact(x){if(x<0||!Number.isInteger(x)||x>170)throw Error('Factorial needs an integer from 0 to 170');let n=1;for(let i=2;i<=x;i++)n*=i;return n;}
 function tokenizeAndEval(source){
   let s=source.replace(/×/g,'*').replace(/÷/g,'/').replace(/−/g,'-').replace(/π/g,'pi').replace(/\^/g,'**');
   s=s.replace(/sin⁻¹/g,'asin').replace(/cos⁻¹/g,'acos').replace(/tan⁻¹/g,'atan').replace(/√/g,'sqrt');
   s=s.replace(/(\b\d+(?:\.\d+)?|\bpi|\be|\))!/g,'factorial($1)');
   s=s.replace(/(\d+(?:\.\d+)?)%/g,'($1/100)');
   const funcs={sin:x=>trig(Math.sin,x),cos:x=>trig(Math.cos,x),tan:x=>trig(Math.tan,x),asin:x=>inv(Math.asin,x),acos:x=>inv(Math.acos,x),atan:x=>inv(Math.atan,x),sqrt:Math.sqrt,log:Math.log10,ln:Math.log,abs:Math.abs,factorial:fact};
   const names={pi:Math.PI,e:Math.E};
   let i=0;
   function ws(){while(/\s/.test(s[i]||'')&&i<s.length)i++;}
   function parseExpression(){let v=parseTerm();while(true){ws();if(s[i]==='+'){i++;v+=parseTerm()}else if(s[i]==='-'){i++;v-=parseTerm()}else return v;}}
   function parseTerm(){let v=parsePower();while(true){ws();if(s[i]==='*'&&s[i+1]!=='*'){i++;v*=parsePower()}else if(s[i]==='/'){i++;v/=parsePower()}else if(s[i]==='%'){i++;v%=parsePower()}else return v;}}
   function parsePower(){let v=parseUnary();ws();if(s.slice(i,i+2)==='**'){i+=2;v=Math.pow(v,parsePower())}return v;}
   function parseUnary(){ws();if(s[i]==='+'){i++;return parseUnary()}if(s[i]==='-'){i++;return -parseUnary()}return parsePrimary();}
   function parsePrimary(){
     ws();
     if(s[i]==='('){i++;let v=parseExpression();ws();if(s[i]!==')')throw Error('Missing )');i++;return v;}
     let num=s.slice(i).match(/^(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?/i);
     if(num){i+=num[0].length;return Number(num[0]);}
     let ident=s.slice(i).match(/^[A-Za-z_]+/);
     if(ident){i+=ident[0].length;let name=ident[0];ws();if(s[i]==='('){i++;let args=[];ws();if(s[i]!==')'){args.push(parseExpression());ws();while(s[i]===','){i++;args.push(parseExpression());ws();}}if(s[i]!==')')throw Error('Missing ) after '+name);i++;if(name==='factorial')return fact(args[0]);if(!(name in funcs))throw Error('Unknown function '+name);return funcs[name](...args);}if(name in names)return names[name];throw Error('Unknown name '+name);}
     throw Error('Unexpected input');
   }
   const value=parseExpression();ws();if(i<s.length)throw Error('Unexpected: '+s.slice(i));if(!Number.isFinite(value))throw Error('Result is not a finite number');return value;
 }
 function fmt(x){if(Number.isInteger(x))return String(x);return Number(x.toPrecision(12)).toString();}
 function calculate(){if(!isOn||!expression.trim())return;const original=expression;try{const n=tokenizeAndEval(expression);result=fmt(n);answer=n;history.unshift([original,result,angle]);history=history.slice(0,30);expression=result;}catch(e){result='Error: '+e.message;}paint();}
 root.addEventListener('click',e=>{
   const b=e.target.closest('button');if(!b||!root.contains(b))return;
   if(b.id==='power'){isOn=!isOn;if(!isOn)clear();paint();return;}
   if(!isOn)return;
   const a=b.dataset.action,v=b.dataset.value;
   if(a==='equals')calculate();
   else if(a==='clear')clear();
   else if(a==='clear-entry'){expression='';result='';paint();}
   else if(a==='delete')del();
   else if(a==='second'){second=!second;}
   else if(a==='ans')add(fmt(answer));
   else if(a==='mplus'){try{memory+=tokenizeAndEval(expression);}catch(e){result='Enter a valid value first';paint();}}
   else if(a==='mr')add(fmt(memory));
   else if(a==='mc'){memory=0;paint();}
   else if(v==='DEG'||v==='RAD'){angle=v;paint();}
   else if(v){if(second&&v==='sin(')add('asin(');else if(second&&v==='cos(')add('acos(');else if(second&&v==='tan(')add('atan(');else add(v);}
 });
 document.addEventListener('keydown',e=>{
   if(e.ctrlKey||e.metaKey||e.altKey)return;
   if(e.key==='Enter'||e.key==='='){e.preventDefault();calculate();return;}
   if(e.key==='Backspace'){e.preventDefault();del();return;}
   if(e.key==='Escape'){e.preventDefault();clear();return;}
   if(/^[0-9.+\-*/()%^!]$/.test(e.key)){e.preventDefault();add(e.key);}
 });
 paint();
})();
</script>
</div>
"""
components.html(html_app, height=850, scrolling=True)
