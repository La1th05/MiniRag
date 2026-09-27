# MiniRag
This is a implementation for a RAG system

# Requirments

python == 3.10.11
 
# installation 

## install required packges 
```bash
uv pip install -r requirements.txt
```

### setup Environment varivles
```bash
$ cp .env.example .env 
```


set your Environment varible in `.env` file like `.env.example`
# Run the applecation

```bash
uvicorn main:app --reload
```