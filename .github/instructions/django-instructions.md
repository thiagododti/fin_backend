# Regras para estrutura Django

## Estrutura dos apps

- Todos os apps Django devem ficar dentro do diretório `apps/`.
- Nunca criar apps diretamente na raiz do projeto.
- Nunca criar pastas vazias

Exemplo:

project/
apps/
    users/
    financial/
    authentication/


## Organização por domínio

- Os apps devem ser separados por domínio/responsabilidade.
- Cada domínio deve possuir seu próprio app.

Exemplos:

- `users` → gerenciamento de usuários
- `financial` → regras financeiras
- `authentication` → autenticação e autorização

## Estrutura interna dos apps

- Sempre separar arquivos por responsabilidade.

Exemplo:

apps/users/
    models/
    serializers/
    views/
    services/
    selectors/
    repositories/
    urls/
    admin/
    tests/
    filters/
    managers/

## Models

- Models devem ser organizadas em arquivos separados quando houver múltiplas entidades.
- Toda model criada deve ser exportada no `models/__init__.py`.

Exemplo:

```python
from .user import User
from .profile import Profile
```

## Anti-Patterns

Não criar lógica de negócio em views.
Não criar queries complexas em serializers.
Não duplicar regras de validação.
Não utilizar signals para regras críticas de negócio.
Não acessar diretamente models em múltiplas camadas sem service.
Não criar arquivos excessivamente grandes.
Não utilizar funções genéricas sem responsabilidade clara.

## Performance
Utilizar select_related e prefetch_related quando necessário.
Evitar queries N+1.
Não carregar dados desnecessários.

## Código limpo
Remover imports não utilizados.
Remover código comentado.
Evitar duplicação.
Priorizar reutilização através de services e shared.