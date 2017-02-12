# coding=utf8
import hashlib, base64, random, json
import requests

__all__ = ['NetEaseMusicApi', 'get_dfsId']

DEFAULT_LIMIT = 10
BASE_URL = 'http://music.163.com/api/'

headers = {
    'Cookie': 'appver=1.5.0.75771',
    'Referer': 'http://music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
}
# 为了方便，这里直接使用AES加密过后的用户名密码数据
user_data = {
    'params': 'tShDl+2GNOJ529i8REZKVnHQCBDk4bf3l5Y4rodp5lv66dbRwckzLE+UJmm5gZ3rfvedxEgzLv6XvMRwmZvGmwLFHyE7RRi6wBcT/j3B0+RJbLeL3ln3T/Nw75XSv6my6imkrvFgichcp3QUUGtvZIztP+t0BZS8IfXHr6XDrfXTJc6ONPZswcxtpqrItZ4M',
    'encSecKey': '27152af8c1016c0b103b1079db0cc1f51ae8aab9526fe7e4ded7f5c862321c1d7765da64904d77ea261f3845e5a6d5849e5878e8f4ff1a7fcdafd1b9a2305e1c38a48c90c49b0c874274642394e1689623f5a21c0a6afa1ea4f9599e75c6ed17fee49afb6abe19e0c745cb9d8e50a4c97d250dd3a4d10b9bd097f229a7'
}

_API = {
    'search': {
        'songs': (1, 'songs'),
        'albums': (10, 'albums'),
        'artists': (100, 'artists'),
        'playlists': (1000, 'playlists'),
        'userprofiles': (1002, 'userprofiles'),
        'mvs': (1004, 'mvs'),
        'lyric': (1006, 'songs'),
    },
    'download': '',
    'song': {
        'detail': ('/?id={0}&ids=%5B{0}%5D', 'songs'),
    },
    'artist': {
        'albums': ('/{0}?id={0}&limit={1}', 'hotAlbums'),
    },
    'album': ('/{0}', 'album/songs'),
    'playlist': {
        'detail': ('?id={0}', 'result'),
    },
    'comments': {
        'last_comments': 'comments',
        'total': 'total',
    }
}


def _APIProxy(key, value, chain):
    # nameOrId为调用传入的参数
    # value[0]为_API中的值，如：(1, 'songs')，value[0]为1
    if isinstance(value, dict):
        childrenList = list(value.keys())
        return lambda: '%s has %s sub functions: %s' % (key, len(childrenList), ', '.join(childrenList))
    else:
        def __APIProxy(nameOrId, limit=DEFAULT_LIMIT):
            def _get_value(json_, keyChain):
                for k in keyChain.split('/'):
                    try:
                        try:
                            k = int(k)
                        except ValueError:
                            pass
                        json_ = json_[k]
                    except:
                        return
                return json_

            if chain[0] == 'search':
                url = BASE_URL + '/'.join(chain[:-1] + ['get'])
                data = {
                    's': nameOrId,
                    'type': value[0],
                    'offset': 0,
                    'sub': 'false',
                    'limit': limit,
                }
                j = requests.post(url, data, headers=headers).json()
                return _get_value(j, 'result/' + value[1])
            elif chain[0] == 'download':
                urls = ['http://m%d.music.126.net/%s/%s.mp3' % (i, encrypted_id(nameOrId), nameOrId) for i in [1, 2, 3]]
                for url in urls:
                    r = requests.get(url, headers=headers)
                    print('[status code:%d] Song URL:%s' % (r.status_code, url))
                    if str(r.status_code)[0] == '2':
                        return r.content
                return b''
            elif chain[0] == 'comments':
                url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=' % (nameOrId,)
                r = requests.post(url, headers=headers, data=user_data)
                if r.status_code == 200 and r.text.find('comments') != -1:
                    return json.loads(r.text)[value]
                else:
                    return 'status code:%s, result:%s' % (r.status_code, r.text)
            else:
                url = BASE_URL + '/'.join(chain) + value[0].format(nameOrId, limit)
                j = requests.get(url, headers=headers).json()
                return _get_value(j, value[1])

        return __APIProxy


def _setup_apiobj(parent, apiList, chain=list()):
    # 为了通过_API中的key进行链式调用，api.search.songs()
    for k, v in apiList.items():
        setattr(parent, k, _APIProxy(k, v, chain + [k]))
        if isinstance(v, dict):
            _setup_apiobj(getattr(parent, k), v, chain + [k])


def encrypted_id(dfsId):
    byte1 = bytearray('3go8&$8*3*3h0k(2)2', 'utf8')
    byte2 = bytearray(str(dfsId), 'utf8')
    byte1_len = len(byte1)
    for i in range(len(byte2)):
        byte2[i] = byte2[i] ^ byte1[i % byte1_len]
    m = hashlib.md5(byte2).digest()
    return base64.b64encode(m).decode('utf8').replace('/', '_').replace('+', '-')


def get_dfsId(song):
    dfsId = None
    for musicIndex in ('hMusic', 'mMusic', 'lMusic', 'bMusic'):
        try:
            if not song[musicIndex]['dfsId'] is None:
                dfsId = song[musicIndex]['dfsId']
            if not dfsId is None:
                break
        except:
            pass
    return dfsId


class NetEaseMusicApi(object):
    def __init__(self):
        _setup_apiobj(self, _API)


if __name__ == '__main__':
    api = NetEaseMusicApi()
