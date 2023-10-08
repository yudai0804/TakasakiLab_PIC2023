import unicodedata
def getStringLendth(text):
    """
    参考:https://note.nkmk.me/python-unicodedata-east-asian-width-count/
    """
    count = 0
    for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
            count += 2
        else:
            count += 1
    mod = count % 2
    count = count //2 + mod
    return count

def convertHalfWordToWord(text):
    """
    半角から全角に変換する
    参考:https://qiita.com/YuukiMiyoshi/items/6ce77bf402a29a99f1bf#%E5%8D%8A%E8%A7%92---%E5%85%A8%E8%A7%92
    """
    return text.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))

def printBitMatrix(mat):
    """ビットで表された行列を表示する"""
    for i in range(len(mat)):
        s = ''
        for j in range(len(mat[0])):
            if mat[i][j] == 1:
                s += '・'
            else:
                s += '　'
        print(s)

def printByteMatrix(mat):
    """8バイトに圧縮された8x8の行列を表示する"""
    for i in range(len(mat)):
        s = ''
        for j in range(8):
            if mat[i] & (0x80 >> j) == (0x80 >> j):
                s += '・'
            else:
                s += '　'
        print(s)
