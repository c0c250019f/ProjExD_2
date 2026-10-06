import time
import random
import os
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}


def check_bound(rect:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or rect.right > WIDTH:
        yoko =  False
    if rect.top < 0 or rect.bottom > HEIGHT:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数：からのSurface
    戻り値：なし
    画面をブラックアウトしてGame Overの文字列を5秒表示
    """
    go_img = pg.Surface((WIDTH, HEIGHT))
    go_img.set_alpha(200)
    fonto = pg.font.Font(None, 80)
    text = fonto.render("Game Over", True, (255, 255, 255))
    k8_ing = pg.image.load("fig/8.png")
    screen_center = WIDTH / 2, HEIGHT / 2
    go_img.blit(text, (text.get_rect(center=screen_center)))
    go_img.blit(k8_ing, (310, 290))
    go_img.blit(k8_ing, (760, 290))
    screen.blit(go_img, (0, 0))
    pg.display.update()
    time.sleep(5)


# def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
#     """
#     引数：なし
#     戻り値：ばくだん画像リスト，ばくだんの半径リスト
#     ばくだんの画像を作成し，リストに格納して返す
#     """
#     bb_imgs = []
#     bb_rads = []
#     for r in range(1, 11): 
#         bb_img = pg.Surface((20*r, 20*r)) 
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r) 
#         bb_imgs.append(bb_img)
#         bb_accs = [a for a in range(1, 11)]
    



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img,(255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0,0,0))
    vx, vy = +5, +5 
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if kk_rct.colliderect(bb_rct):
            print("game over")
            gameover(screen)
            return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
