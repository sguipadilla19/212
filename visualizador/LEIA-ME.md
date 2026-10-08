# Visualizador 3D — Casa Padilla Maximiano

Modelo 3D navegável gerado a partir de `planta.pdf` (planta-layout, estudo preliminar de 23/09/2026, escala 1:100).

## Como abrir

1. Dê dois cliques em `index.html` (abre no navegador; precisa de internet na primeira vez, pois a biblioteca Three.js é baixada da web).
2. Clique em **Entrar na casa**. O mouse passa a controlar o olhar.

Se o navegador bloquear o arquivo local, rode `servir.bat` e abra http://localhost:8123 .

## Modos de navegação

| Modo | Tecla | O que faz |
|---|---|---|
| **Andar** | `1` | primeira pessoa, com colisão nas paredes e móveis; portas abrem ao se aproximar |
| **Voo** | `2` | voo livre sem colisão; `E`/`Q` (ou Espaço/Ctrl) sobe e desce |
| **Órbita** | `3` | casa de boneca: cobertura removida, arraste para girar, roda para aproximar |
| **Planta** | `4` | vista ortogonal de cima; arraste para mover, roda para zoom |

## Controles

| Tecla / ação | Função |
|---|---|
| `W` `A` `S` `D` ou setas | andar |
| `Shift` | correr |
| mouse | olhar (clique na tela para capturar o mouse; `Esc` libera) |
| `G` ou botão **Tour guiado** | passeio automático por todos os cômodos, com legenda; qualquer tecla de movimento interrompe |
| `R` | mostra / oculta a cobertura |
| `L` | mostra / oculta os nomes dos cômodos |
| `T` ou botão **Trena** | medição: clique em dois pontos para ver a distância (e as projeções em x, y, z) |
| `F` ou botão **Foto** | salva a imagem atual em PNG |
| `M` | amplia o minimapa |
| clique no minimapa | teletransporta para o ponto clicado |
| lista de cômodos | teletransporta para um cômodo |
| ⚙ (canto superior direito) | hora do dia (sol, céu e luzes internas automáticas), sensibilidade, campo de visão, altura dos olhos, sombras e resolução |

Em celulares e tablets: joystick virtual à esquerda move; arrastar à direita olha.

O painel central mostra o cômodo atual, a área em m² e o nível do piso. O minimapa é a própria planta com a sua posição e direção de olhar.

## Links diretos (parâmetros de URL)

`index.html?auto=1&spot=7` abre direto na suíte sem a tela inicial. Parâmetros: `spot=N`, `mode=walk|fly|orbit|plan`, `fly=ALTURA`, `x=`, `z=`, `yaw=GRAUS`, `pitch=GRAUS`, `hour=15.5`, `roof=0`, `labels=0`, `tour=1`.

Exemplos: `index.html?auto=1&mode=orbit&hour=18.5` (casa de boneca ao entardecer) · `index.html?auto=1&tour=1` (tour direto).

## O que foi modelado

- Paredes externas e internas com espessuras e posições lidas dos vetores do PDF (precisão de ~1 cm na escala da planta), rodapés, caixilhos com montantes e peitoris, portas com folha, almofadas e maçanetas.
- Dois níveis de piso: 0,00 (sala, dormitório 01, lavabo) e +0,20 (núcleo de banhos, dormitório 02, hall, cozinha, suíte), com degraus nas transições e para o jardim.
- Pilares e vigas das áreas cobertas, laje com platibanda e rufo, forro e luminárias.
- Texturas procedurais com relevo: tábuas de madeira (sala e dormitórios), porcelanato (hall, cozinha, corredor), cerâmica (banheiros), deck (varandas), concreto (calçadas), reboco, grama.
- Mobiliário do layout: camas com cabeceira e edredom, armários com portas e puxadores, sofá e poltronas, mesa de jantar com cadeiras, rack e TV, cristaleiras, bancadas com cuba e torneira, ilha com cooktop e banquetas, geladeira, armário alto, tanque, lavadora e secadora, louças, boxes de vidro, tapetes e plantas.
- Céu físico com posição solar para Embu-Guaçu (sol ao norte), sombras suaves, reflexos de ambiente; à noite as luzes internas acendem.
- Paisagismo simples: gramado, árvores, cerca viva e caminho de acesso.

## Premissas adotadas (pontos ambíguos no estudo preliminar)

- Pé-direito de 2,80 m (não cotado na planta).
- As duas faixas de 0,80 m na parede entre a sala e os dormitórios foram tratadas como portas dos dormitórios.
- A abertura de 1,20 m da sala para o núcleo de banhos foi mantida aberta, com degrau para +0,20.
- A porta de 0,80 m na parede oeste do nicho do quadro elétrico foi mantida como porta externa.
- Alturas de peitoril: 1,10 m (janelas comuns), 0,60 m (janelão da sala), 1,60 m (banheiros).
- Cores e materiais de acabamento são ilustrativos.

## Arquivos

- `index.html` — o visualizador (autossuficiente, dados embutidos).
- `dados_casa.json` — geometria em metros (paredes, aberturas, pisos, móveis, portas, rótulos, tour). Origem no canto noroeste da área coberta; X cresce para leste e Z para o sul.
- `planta_minimapa.png` — recorte da planta usado no minimapa.
- `preview_*.png` — capturas de verificação.

## Para regenerar (pasta `fonte/`)

Requer Python 3 com PyMuPDF (`pip install pymupdf`). Na pasta `fonte/`:

```
python gen_data.py   # lê ../../planta.pdf e gera casa.json + ../dados_casa.json + minimap.png
python build.py      # injeta casa.json em template.html e grava ../index.html
```

Ajustes de geometria (paredes, portas, móveis, pontos de teletransporte, roteiro do tour) ficam em `gen_data.py`, com coordenadas em pontos do PDF (1 m = 28,35 pt). Aparência, materiais e navegação ficam em `template.html`.
