# Decision Intelligence Platform Frontend

Aplicação web responsiva da DIP, construída com React, Vite, TypeScript strict,
Tailwind CSS, React Router, Vitest e React Testing Library.

## Instalação e execução

```powershell
cd frontend
npm install
npm run dev
```

Por padrão, a aplicação abre em `http://localhost:5173`.

```powershell
npm run lint
npm run test -- --run
npm run build
```

## Conexão com o backend

Copie `.env.example` para `.env.local` quando precisar alterar a URL:

```dotenv
VITE_API_BASE_URL=
```

Vazio, o valor usa mesma origem; em desenvolvimento, o Vite encaminha `/api`
para `http://localhost:8000`. Defina uma URL absoluta somente quando frontend e
backend estiverem em origens distintas. Nenhum secret deve ser definido em
variáveis `VITE_*`, pois elas são públicas no bundle. O Dashboard consulta somente `/api/v1/health` e
`/api/v1/readiness` neste bloco.

## Estrutura

- `src/app`: bootstrap da aplicação
- `src/components/layout`: shell e navegação responsiva
- `src/components/ui`: design system mínimo
- `src/features/platform-status`: integração inicial de status
- `src/lib/api`: cliente Fetch tipado, timeout e erros
- `src/pages`: páginas do produto e 404
- `src/routes`: mapa de rotas
- `src/styles`: Tailwind e estilos globais
- `src/test`: configuração, fixtures e testes

## Providers e exportação

A preferência entre `mock`, `amadeus` e `duffel` é armazenada localmente no
navegador e enviada ao backend pelo header `X-Travel-Provider`. O frontend nunca
recebe ou armazena credenciais; elas pertencem exclusivamente ao ambiente do
backend. `mock` permanece como opção segura quando nenhuma preferência existe.

Snapshots podem ser baixados em Parquet pelo Histórico e pelas Comparações. O
download usa o conteúdo binário e o nome indicado em `Content-Disposition`, sem
interpretar ou converter o arquivo no navegador.

## Fluxo do produto e testes

Use Configurações para escolher um provider local, realize a busca, consulte a
recomendação e acompanhe snapshots no Histórico. Duas buscas persistidas podem
ser comparadas, e seus snapshots podem ser baixados em Parquet. Decisões e IA
assistiva refletem apenas capacidades realmente expostas pelo backend.

```powershell
npm run lint
npm run test -- --run
npm run build
npm run test:e2e
```

O E2E inicia frontend e backend automaticamente, usa Chromium, provider mock e
bancos descartáveis em `.tmp/`. Instale o navegador uma vez com
`npx playwright install chromium`.

Limitações: não há autenticação, armazenamento de credenciais, editor de
contexto para IA ou gráficos fabricados sem série temporal.
