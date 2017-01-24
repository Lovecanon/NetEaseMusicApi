# NetEaseMusicApi

![python](https://img.shields.io/badge/python-2.7-ff69b4.svg) ![python](https://img.shields.io/badge/python-3.5-red.svg) [English Version](https://github.com/littlecodersh/NetEaseMusicApi/blob/master/README_EN.md)

完善的网易云音乐Api

## 功能简述
* api类提供了常用api的调用，根据`/api/`后的网址调用。
```python
# 例如http://music.163.com/api/song/detail的调用
# /api/song/detail -> api.song.detail
# songId = 28377211
api.song.detail(28377211) 
```
* 提供了基本的下载歌曲与专辑作为api示例。

## 安装方法

```bash
pip install NetEaseMusicApi
```

## 使用示例

```python
from NetEaseMusicApi import api, save_song, save_album
# 保存歌曲
# 会先通过名字/id查询歌曲，web页面上的搜索框也是调用该接口链接
save_song('Apologize')

# 查询最新十条评论
print(api.comments.last_comments(420513460))

# 查询歌曲总评论数
print(api.comments.total(420513460))
```
