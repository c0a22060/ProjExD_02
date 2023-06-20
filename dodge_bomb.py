import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
vector = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def direction_kk(mv, img):  #追加機能1
    """
    それぞれの回転反転した画像を代入
    方向に合わせて辞書化する
    0.0の時は何も代入しないのでFalse
    """
    kk_img_ogin = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.flip(kk_img_ogin, True, False)
    kk_img1 = pg.transform.rotozoom(kk_img_ogin, 0, 2.0)
    kk_img2 = pg.transform.rotozoom(kk_img_ogin, 45, 2.0)
    kk_img3 = pg.transform.rotozoom(kk_img_ogin, -45, 2.0)
    kk_img4 = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img5 = pg.transform.rotozoom(kk_img, 45, 2.0)
    kk_img6 = pg.transform.rotozoom(kk_img, -45, 2.0)
    kk_img7 = pg.transform.rotozoom(kk_img, 90, 2.0)
    kk_img8 = pg.transform.rotozoom(kk_img, -90, 2.0)
    if mv == [0, 0]:
        return False
    kk_img_way = {
        (+5, 0):kk_img4,
        (+5, +5):kk_img6,
        (0, +5):kk_img8,
        (-5, +5):kk_img2,
        (-5, 0):kk_img1,
        (-5, -5):kk_img3,
        (0, -5):kk_img7,
        (+5, -5):kk_img5,
    }
    return kk_img_way[tuple(mv)]

def inout(Rect:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんが画面の中か外かを判定する関数
    引数:爆弾orこうかとんrect
    """
    yoko, tate = True, True
    if Rect.left < 0 or WIDTH < Rect.right: 
        yoko = False
    if Rect.top < 0 or HEIGHT < Rect.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img_cry = pg.image.load("ex02/fig/8.png")
    kk_img_cry = pg.transform.rotozoom(kk_img_cry, 0, 2.0)  #追加機能3
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))  #練習1
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    bd_rct = bd_img.get_rect()
    bd_rct.center = x, y
    #爆弾の座標を決める
    vx, vy = +5, +5  #練習2
    clock = pg.time.Clock()
    tmr = 0
    accs = [a for a in range(1, 11)]  #追加機能2
    acshon = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):
            if acshon == 0:
                acshon = 1
        """
        ぶつかったら数値を1にして泣き始める準備をする
        """
            
            
        key_1st = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, mv in vector.items():
            if key_1st[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if tmr == 0:
            kk_img_new = kk_img
        if direction_kk(sum_mv, kk_img) != False:
            kk_img_new = direction_kk(sum_mv, kk_img)
        """
        追加機能1
        こうかとんの画像を
        direction_kkにsum_mvを代入し帰ってきた画像を代入する
        向きを残るようにしたいので0, 0を入れても更新されない
        最初だけ画像を代入する
        """
        ac = accs[min(tmr//500,9)]  #独自機能
        sum_mv[0] *= ac
        sum_mv[1] *= ac

        kk_rct.move_ip(sum_mv)  #練習3
        if inout(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        if acshon > 0:
            acshon += 1
            kk_img_new = kk_img_cry
        if acshon > 100:
            return  #ゲームオーバー処理
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img_new, kk_rct)

        avx, avy = vx*accs[min(tmr//500,9)], vy*accs[min(tmr//500,9)]  #追加機能2
        #時間によって爆弾のそくどがあがる
        bd_rct.move_ip(avx, avy)  #練習3
        yoko, tate = inout(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bd_img, bd_rct)  
        pg.display.update()
        
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()