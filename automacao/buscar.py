"""Consulta pública limitada, sem login, candidaturas ou ferramentas pagas."""
import argparse,datetime,json,re,time,urllib.request,urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

class Pagina(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.texto=[];self.anchor=None;self.title=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
  if tag=='a':self.anchor=dict(attrs).get('href');self.title=[]
 def handle_data(self,data):
  if self.skip:return
  if data.strip():self.texto.append(data.strip())
  if self.anchor is not None:self.title.append(data)
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
  if tag=='a' and self.anchor is not None:
   self.links.append((self.anchor,' '.join(''.join(self.title).split())))
   self.anchor=None;self.title=[]

def baixar(url):
 req=urllib.request.Request(url,headers={'User-Agent':'Codex-Money-Public-Research/1.0 (Python urllib)'})
 with urllib.request.urlopen(req,timeout=20) as r:
  if r.status!=200:raise ValueError(f'HTTP {r.status}')
  data=r.read(2_000_001)
  if len(data)>2_000_000:raise ValueError('Página excedeu o limite de tamanho')
  p=Pagina();p.feed(data.decode('utf-8',errors='replace'));return p

def candidatos(pagina):
 found={}
 for href,title in pagina.links:
  path=urllib.parse.urlsplit(href).path
  if re.fullmatch(r'/project/[^/]+-\d+',path) and title:
   found.setdefault(path,{'titulo':title,'url':'https://www.99freelas.com.br'+path})
 return list(found.values())

def avaliar(item):
 s=item['titulo'].casefold()
 if any(x in s for x in ['tráfego','trafego','vendas','prospec','curso','saas','fintech','full-stack','depoimento']):
  return None # geralmente requer operação comercial, custo ou escopo extenso
 if any(x in s for x in ['planilh','cadastro','conferência','conferencia']):return 'Dados e planilhas'
 if any(x in s for x in ['site portf','landing page','site para','blog','catálogo','catalogo']):return 'Sites e páginas'
 return None

def executar(destino,limite=6):
 agora=datetime.datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(timespec='seconds')
 found={};falhas=[];consultas=[]
 for termo in ['excel','site','landing']:
  url='https://www.99freelas.com.br/projects?'+urllib.parse.urlencode({'q':termo})
  try:
   items=candidatos(baixar(url));consultas.append({'url':url,'anuncios_extraidos':len(items)})
   if not items:falhas.append({'url':url,'erro':'Nenhum anúncio extraído; estrutura ou acesso precisa de revisão'})
   for i in items:
    categoria=avaliar(i)
    if categoria:found.setdefault(i['url'],{**i,'categoria':categoria})
  except Exception as e:falhas.append({'url':url,'erro':str(e)[:200]})
  time.sleep(1)
 oportunidades=[]
 grupos=[[x for x in found.values() if x['categoria']==cat] for cat in ['Dados e planilhas','Sites e páginas']]
 selecionados=[]
 while any(grupos) and len(selecionados)<limite:
  for grupo in grupos:
   if grupo and len(selecionados)<limite:selecionados.append(grupo.pop(0))
 for item in selecionados:
  try:
   p=baixar(item['url']);texto='\n'.join(p.texto);resumo=texto[:6000]
   encerrado=bool(re.search(r'este projeto foi (?:cancelado|encerrado|fechado)|projeto cancelado',resumo,re.I))
   count=re.search(r'Propostas:\s*(\d+)',resumo)
   item.update(propostas=int(count.group(1)) if count else None,estado='Encerramento informado na página' if encerrado else 'Página consultada; disponibilidade e contratação não confirmadas')
   if not encerrado:oportunidades.append(item)
  except Exception as e:falhas.append({'url':item['url'],'erro':str(e)[:200]})
  time.sleep(1)
 oportunidades.sort(key=lambda x:x['propostas'] if x['propostas'] is not None else 10**9)
 resultado={'consultado_em_sao_paulo':agora,'consultas':consultas,'oportunidades':oportunidades,'falhas':falhas,'candidaturas_enviadas':0,'receita_confirmada_brl':0,'observacao':'Filtro por títulos e contagem pública, sem IA e sem promessa de renda; nenhum login ou contato realizado.'}
 destino=Path(destino);destino.mkdir(parents=True,exist_ok=True)
 (destino/'oportunidades.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2))
 lines=['# Pesquisa pública de oportunidades','',f'Consulta: {agora}', '', 'Nenhuma candidatura enviada ou receita confirmada. A lista não confirma disponibilidade, elegibilidade ou contratação.','']
 for i in oportunidades:
  title=i['titulo'].replace('[','').replace(']','').replace('\n',' ')
  lines.extend([f"- [{title}]({i['url']}) — {i['categoria']}; propostas observadas: {i['propostas'] if i['propostas'] is not None else 'não informadas'}."])
 if not oportunidades:lines.append('Nenhuma oportunidade verificável nesta execução; consultar as falhas registradas.')
 if falhas:
  lines.extend(['','## Limitações',''])
  for e in falhas:lines.append(f"- {e['url']}: {e['erro']}")
 lines.extend(['','Não comprar pontos, assinaturas, publicidade ou ferramentas. As propostas dependem da revisão de Du e de acesso autenticado.'])
 (destino/'oportunidades.md').write_text('\n'.join(lines)+'\n')
 return resultado

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--saida',default='relatorios');parser.add_argument('--limite',type=int,default=6);args=parser.parse_args()
 if not 1<=args.limite<=6:parser.error('--limite deve estar entre 1 e 6')
 result=executar(args.saida,args.limite)
 print(f"{len(result['oportunidades'])} oportunidades consultadas; {len(result['falhas'])} limitações. Nenhum envio.")
 # Falhas parciais ficam visíveis no relatório; fracasso total não gera execução verde.
 raise SystemExit(0 if result['oportunidades'] else 1)
