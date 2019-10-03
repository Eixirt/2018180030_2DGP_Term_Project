import pico2d

pico2d.open_canvas()
character_player = pico2d.load_image('resource\\Character_Player.png')

x = 400
frame1 = 0
frame3 = 0
is_up = True

while x < 800:
    pico2d.clear_canvas()
    # 그림확인
    character_player.clip_draw(0 * 24, 384 - 71, 24, 23, 400, 290, 120, 115)
    character_player.clip_draw(0 * 24, (384 - 20), 24, 20, 400, 290, 120, 100)

    character_player.clip_draw(1 * 24, 384 - 71, 24, 23, 500, 289, 120, 115)
    character_player.clip_draw(1 * 24, (384 - 20), 24, 20, 500, 290, 120, 100)

    character_player.clip_draw(2 * 24, 384 - 71, 24, 23, 600, 288, 120, 115)
    character_player.clip_draw(2 * 24, (384 - 20), 24, 20, 600, 290, 120, 100)

    character_player.clip_draw(3 * 24, 384 - 71, 24, 23, 700, 289, 120, 115)
    character_player.clip_draw(3 * 24, (384 - 20), 24, 20, 700, 290, 120, 100)



    # 몸
    character_player.clip_draw(frame1 * 24, 384 - 71, 24, 23, x, 90 - 2 * frame3, 120, 115)
    # 머리
    character_player.clip_draw(frame1 * 24, 384 - 20, 24, 20, x, 92 + frame3, 120, 100)
    pico2d.update_canvas()

    frame1 = (frame1 + 1) % 4
    if is_up:
        frame3 += 1
        if frame3 == 2:
            is_up = False
    else:
        frame3 -= 1
        if frame3 == 0:
            is_up = True

    x += 5
    pico2d.delay(0.1)
    pico2d.get_events()

pico2d.close_canvas()