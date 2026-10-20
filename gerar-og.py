# Refaz o cartao de compartilhamento (og:image) de 1200x630.
#
# ⚠️ POR QUE ISSO EXISTE: o titulo do heroi esta GRAVADO nesta imagem. Quando o
# titulo da home muda, este arquivo tem que ser rodado de novo — senao o link
# compartilhado no WhatsApp e no direct continua anunciando a frase antiga.
# Foi o que aconteceu em 20/10/2026: a home virou "A comida da sua cidade" e o
# cartao seguia com "Aqui o dinheiro nao pega a estrada".
#
# Rodar:  python -I gerar-og.py
# Saida:  assets/og-inksa.png

import os
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630
BREU = (19, 28, 34)          # --fundo do tema escuro
BRASA = (249, 115, 22)       # #F97316, a cor da marca
NEVE = (255, 255, 255)
MUSGO = (201, 213, 219)
BARRA = (26, 37, 45)

LINHA1 = "A comida da sua cidade,"
LINHA2A = "na sua "                  # branco
LINHA2B = "porta."                   # laranja
LEMA = "O DELIVERY QUE FICA NA CIDADE"
SUB = "Lojas de Lages, entregadores daqui e a conta de cada pedido aberta."


def fonte(nome, tam):
    return ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", nome), tam)


base = Image.new("RGB", (W, H), BREU)

# Brilho quente vindo do canto inferior direito, como no cartao antigo.
# Feito com um gradiente radial calculado, nao com imagem — fica nitido em
# qualquer tamanho e pesa zero.
brilho = Image.new("RGB", (W, H), BREU)
d = ImageDraw.Draw(brilho)
cx, cy = int(W * 0.78), int(H * 0.72)
raio = int(W * 0.72)
for i in range(raio, 0, -4):
    t = 1 - (i / raio)              # 0 na borda, 1 no centro
    f = t ** 2.2 * 0.42             # suave: so 42% de mistura no nucleo
    cor = tuple(int(BREU[k] + (BRASA[k] - BREU[k]) * f) for k in range(3))
    d.ellipse([cx - i, cy - i, cx + i, cy + i], fill=cor)
base = Image.blend(base, brilho, 1.0)

d = ImageDraw.Draw(base)

# ---- Logo
logo_path = os.path.join(AQUI, "assets", "inksa-marca.png")
y = 62
if os.path.exists(logo_path):
    lg = Image.open(logo_path).convert("RGBA")
    alvo_w = 232
    lg = lg.resize((alvo_w, int(lg.height * alvo_w / lg.width)), Image.LANCZOS)
    base.paste(lg, (80, y), lg)
    y += lg.height + 38

# ---- Lema (espacado, como no site)
f_lema = fonte("arialbd.ttf", 23)
x = 82
for ch in LEMA:
    d.text((x, y), ch, font=f_lema, fill=BRASA)
    x += d.textlength(ch, font=f_lema) + 6
y += 58

# ---- Titulo
f_tit = fonte("ariblk.ttf", 72)
d.text((80, y), LINHA1, font=f_tit, fill=NEVE)
y += 92
d.text((80, y), LINHA2A, font=f_tit, fill=NEVE)
d.text((80 + d.textlength(LINHA2A, font=f_tit), y), LINHA2B, font=f_tit, fill=BRASA)
y += 104

# ---- Subtitulo
d.text((82, y), SUB, font=fonte("arial.ttf", 27), fill=MUSGO)

# ---- Barra do rodape
ALT = 74
d.rectangle([0, H - ALT, W, H], fill=BARRA)
f_pe = fonte("arialbd.ttf", 26)
d.text((80, H - ALT + 23), "inksadelivery.com.br", font=f_pe, fill=NEVE)
f_pe2 = fonte("arial.ttf", 24)
dir_txt = "Lages · Santa Catarina"
d.text((W - 80 - d.textlength(dir_txt, font=f_pe2), H - ALT + 25),
       dir_txt, font=f_pe2, fill=MUSGO)

saida = os.path.join(AQUI, "assets", "og-inksa.png")
base.save(saida, optimize=True)
print("ok", saida, base.size, os.path.getsize(saida) // 1024, "KB")
