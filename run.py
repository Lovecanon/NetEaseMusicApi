import sys

from NetEaseMusicApi import api, save_song, save_album, interact_select_song

# save_song('Apologize')
# try:
#     sys_input = raw_input
# except:
#     sys_input = input
# while 1:
#     msg = sys_input('>').encode(sys.stdin.encoding).decode(sys.stdin.encoding)
#     print(interact_select_song(msg))

# print(api.comments.last_comments(420513460))
i = 556279
l = list()

while i < 558279:
    if len(l) > 200:
        print(l[-1])
        with open('./data.txt', 'w') as f:
            for song_id, t in l:
                f.write('%s %s\n' % (song_id, t))
        l.clear()
    total = api.comments.total(i)
    if isinstance(total, int) and total > 0:
        l.append((i, total))
    i += 1
