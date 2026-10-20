# ClickCPF

O ClickCpf é uma aplicação desenvolvida em Python para facilitar o acesso aos CPFs dos vendedores no dia a dia. A ideia surgiu para tornar esse processo mais rápido, permitindo localizar um vendedor pelo nome e copiar seu CPF para a área de transferência com apenas um clique, sem precisar ficar procurando os dados manualmente em arquivos.

## Telas
<img width="377" height="488" alt="Image 1" src="https://github.com/user-attachments/assets/6b7c2dea-cfee-44a2-bb35-b4759c141447" />
<img width="297" height="247" alt="Image 2" src="https://github.com/user-attachments/assets/69930993-6ef3-41f4-944d-dba11a4b4fe9" />
<img width="299" height="279" alt="Image 3" src="https://github.com/user-attachments/assets/9e5f4b1a-9c7d-4f99-81bd-d2f784561e51" />

## Como Utilizar

Caso você queira apenas utilizar a aplicação baixa apenas a pasta executavel onde vai haver o programa e o anexo de vendedores. Caso queira o code do projeto não se preocupe em baixar bibliotecas externas para utilizar a interface, pois o Tkinter normalmente já acompanha a instalação do Python. Caso ele não esteja disponível, será necessário instalá-lo conforme o sistema operacional utilizado.

- LEMBRANDO QUE O ARQUIVO DE VENDEDORES DEVE ESTAR SEMPRE NA MESMA PASTA QUE O PROGRAMA!!!

Recomendo que crie uma pasta para o programa e depois um atalho na area de trabalho.

## Arquivo Vendedores

O programa utiliza o arquivo vendedores.txt para armazenar os cadastros. Cada linha deve conter o nome e o CPF separados por uma vírgula.

Exemplo:

```python
João Silva,123.456.789-00
Maria Oliveira,987.654.321-00
```

Se o arquivo não existir, a aplicação abre com a lista vazia. Ao adicionar ou excluir vendedores, o programa atualiza o arquivo automaticamente.

