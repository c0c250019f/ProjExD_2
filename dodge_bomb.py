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
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or rect.right > WIDTH: # 横方向判定
        yoko =  False
    if rect.top < 0 or rect.bottom > HEIGHT: # 縦方向判定
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
    go_img.blit(text, (text.get_rect(center=screen_center))) #フォントを表示
    go_img.blit(k8_ing, (310, 290)) #左のこうかとんを表示
    go_img.blit(k8_ing, (760, 290)) #右のこうかとんを表示
    screen.blit(go_img, (0, 0))
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：爆弾の大きさ、爆弾の速度のリストをまとめたタプル
    爆弾のサイズと速度を変更して返す
    """
    bb_imgs = []
    bb_rads = []
    for r in range(1, 11): #爆弾の大きさを決定  
        bb_img = pg.Surface((20*r, 20*r)) 
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r) 
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)] #爆弾の速度を決定
    return bb_imgs, bb_accs
    

def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数：なし
    戻り値：移動量タプルと対応する画像Surfaceの辞書
    移動量に応じて向きと角度を変更した画像を返す
    """

    kk_dict = { 
        ( 0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
        (+5, 0): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"),True, False), 0, 0.9),
        (+5,-5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"),True, False), 45, 0.9), 
        ( 0,-5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"),True, False), 90, 0.9),
        (-5,-5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9), 
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9), 
        (-5,+5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),
        ( 0,+5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"),True, False), -90, 0.9),
        (+5,+5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"),True, False), -45, 0.9),
        }
    return kk_dict


def calc_orientation(org: pg.Rect, dst: pg.Rect,current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    引数：爆弾のRectとこうかとんのRectと現在の移動方向
    戻り値：爆弾の移動方向
    orgからdstへの差ベクトルを求め、ベクトルの長さが√50になるように正規化する。距離が300未満なら現在の移動方向をそのまま返す。
    """
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    norm = (dx**2 + dy**2) ** 0.5 #正規化
    if norm < 300: #速度を判定
        return current_xy
    target_norm = 50 ** 0.5
    vx = dx / norm * target_norm
    vy = dy / norm * target_norm
    return vx, vy
   

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) # 練習2：空のSurface
    pg.draw.circle(bb_img,(255, 0, 0), (10, 10), 10) # 練習2：赤い爆弾
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH), random.randint(0, HEIGHT) #練習2：横縦の乱数
    bb_img.set_colorkey((0,0,0)) # 練習2：四隅の黒い部分を透過する
    bb_imgs, bb_accs = init_bb_imgs()
    vx, vy = +5, +5 # 練習2：爆弾の初期速度
    tmr = 0
    clock = pg.time.Clock()
    kk_imgs = get_kk_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0] # 横方向移動量
                sum_mv[1] += tpl[1] # 縦方向移動量
        kk_img = kk_imgs[tuple(sum_mv)]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # どこからしらはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 先程の動きをキャンセルする
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        avx = vx*bb_accs[min(tmr//500, 9)] 
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy) # 練習2：爆弾動く
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct) # 練習2：爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if kk_rct.colliderect(bb_rct): # 練習4：kkとbbのrectが重なっていたら
            print("game over")
            gameover(screen)
            return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
