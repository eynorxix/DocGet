# Proyect

- **Package manager**: Use `pnpm` ONLY. Never use npm, yarn, or bun.
- **Run on web (localhost)**: `pnpm web`
- **Run on Android**: `pnpm android`
- **Run on iOS**: `pnpm ios`
- **Start dev server**: `pnpm start`
- **TypeScript check**: `npx tsc --noEmit`
- **Expo SDK**: v56 — exact docs at https://docs.expo.dev/versions/v56.0.0/

## Tema / Estilo

- Tema único **dark mode** estilo X/Grok.
- Los colores se definen en `src/constants/theme.ts` (`Colors`).
- **NUNCA** usar colores hardcodeados (`#fff`, `#3C9FFE`, etc.) en ningún componente.
- Siempre importar `Colors` desde `@/constants/theme` y usar `Colors.xxx`.
- Paleta:
  - Fondo: `Colors.background` (`#000000`)
  - Card: `Colors.card` (`#16181c`)
  - Borde: `Colors.cardBorder` (`#2f3336`)
  - Texto: `Colors.text` (`#e7e9ea`)
  - Texto secundario: `Colors.textSecondary` (`#71767b`)
  - **Acento verde teal**: `Colors.accent` (`#22C5AF`)
  - Input bg: `Colors.inputBg` (`#1a1a1a`)
  - Peligro: `Colors.danger` (`#ef4444`)

## Documentación

- Todo cambio en el sistema debe documentarse en la carpeta `/doc`.
- Crear archivos separados por tema (no un solo archivo gigante).
- Mantener `doc/README.md` como índice general.
- Actualizar `doc/comand/comandos.md` si se agregan nuevos comandos.
- Cada nuevo módulo debe tener su documentación correspondiente.
