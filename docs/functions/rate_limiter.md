# bot_keydrop.system_safety.rate_limiter

Classe `RateLimiter(max_calls, period)` limita ações por chave usando janela deslizante.

Esta é a única implementação de *rate limiting* do projeto e é utilizada por componentes de segurança para evitar chamadas excessivas.

Exemplo de uso básico:

```python
from bot_keydrop.system_safety.rate_limiter import RateLimiter

rl = RateLimiter(2, 5.0)
if rl.allow("bot"):
    executar_acao()
```
