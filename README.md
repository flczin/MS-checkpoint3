# Instruções
Clone o repositorio e execute o `docker-compose`. Acesse [localhost](http://localhost:8000/docs) na porta 8000 no caminho /docs para acessar o swagger.
# Exemplo curl
```
curl -X 'POST' \
  -O \
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
