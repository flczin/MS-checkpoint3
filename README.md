# Instruções
Clone o repositorio e execute o `docker-compose`. Acesse [localhost](http://localhost:8000/docs) na porta 8000 no caminho /docs para acessar o swagger.
# Exemplo post curl
Este curl retorna uma key que será utlizada no endpoint de get.
```
curl -X 'POST' \
  'http://localhost:8000/generate_diploma' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nome": "Antonio",
  "nacionalidade": "brasileiro",
  "estado": "São Paulo",
  "dataNascimento": "10/10/2001",
  "documento": "12.123.213-8",
  "dataConclusao": "10/09/2023",
  "curso": "Sistemas de Informação",
  "cargaHoraria": "1000",
  "dataEmissao": "13/11/2024",
  "nomeAssinatura": "Marcelo",
  "cargo": "Diretor"
}'
```
# Exemplo get curl
Este curl retorna o arquivo se ele já foi processado ou "File still being processed or do not exist" se o arquivo na existir ou ainda estiver sendo processado pelo worker.
```
curl -X 'GET' \
  -O \
  'http://localhost:8000/retrieve_diploma/3427ca5b-60b2-34e3-b4ae-64403b02ea33' \
  -H 'accept: application/json'
```
