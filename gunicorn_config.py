# Arquivo de configuração do Gunicorn

# Número de processos de trabalho (ajuste conforme necessário)
workers = 2

# Endereço e porta para vincular (não altere a variável $PORT)
bind = "0.0.0.0:${PORT}"
