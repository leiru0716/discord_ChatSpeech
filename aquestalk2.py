# coding: utf-8
u"""AquesTalk2.dll, AquestTalk2DA.dll を用いて音声合成する

作成
    fgshun (http://d.hatena.ne.jp/fgshun/)

関数
    talk
        サウンドデバイスより発声する
    synthe
        音声データを生成して返す
    write_wav
        音声データファイルを作成するショートカット関数
    phont_from_path
        声の種類を規定する Phont データをファイルから読み込む
    AquesTalk2_Synthe
        音声記号列から音声波形を生成する
    AquesTalk2_FreeWave
        音声データの領域を開放
    AquesTalk2Da_PlaySync
        同期タイプの音声合成
    AquesTalk2Da_Create
        音声合成エンジンのインスタンスを生成（非同期タイプ）
    AquesTalk2Da_Release
        音声合成エンジンのインスタンスを解放（非同期タイプ）
    AquesTalk2Da_Play
        非同期タイプの音声合成
    AquesTalk2Da_Stop
        発声の停止
    AquesTalk2Da_IsPlay
        再生中か否か

例外
    AquesTalk2Error
        音声合成などの失敗を表す

AquesTalk2_, AquesTalk2Da_ で始まる関数は
AquesTalk2.dll AquesTalk2Da.dll の関数へのラッパーとなっている。
用いる際には AquesTalk に付属の『プログラミングガイド.pdf』、
および『音声記号列仕様』を参照のこと。
以下、これらの資料と挙動が異なる点について説明する。

AquesTalk2_Synthe
    引数は (const char *koe, int iSpeed, void *phontDat) の３つである。
    第３引数 int *pSize は無くなり、戻り値に含まれるようになっている。
    戻り値は 音声データへのポインタとその先のデータサイズのタプルである。
    音声データを Python 文字列型として得るには
        wav, size = AquesTalk2_Synthe(koe='あいうえお', iSpeed=100)
        voice = wav[0:size]
        AquesTalk2_FreeWave(wav)
    のようにする。

AquesTalk2Da_PlaySync
AquesTalk2Da_Play
    戻り値はなくなっている。異常終了した場合 AquesTalk2Error を送出する。
    ガイドに記されている本来の戻り値、エラーコード番号は
    この例外の err_code 属性に収まっている。

AquesTalk2Da_IsPlay
    戻り値は整数ではなく bool 型。
    再生中ならば True, 再生中でなければ False 。
"""

from __future__ import with_statement
import os
import sys
from ctypes import windll, POINTER, WINFUNCTYPE
from ctypes import c_ulong, c_int, c_char, c_char_p, c_void_p
from ctypes.wintypes import HWND

__all__ = [
    'talk', 'synthe', 'write_wav', 'phont_from_path', 'AquesTalk2Error',
    'AquesTalk2_Synthe', 'AquesTalk2_FreeWave',
    'AquesTalk2Da_PlaySync', 'AquesTalk2Da_Create', 'AquesTalk2Da_Release',
    'AquesTalk2Da_Play', 'AquesTalk2Da_Stop', 'AquesTalk2Da_IsPlay',]

version = '0.1.1'
version_info = (0, 1, 1)
dll_version = '10.2.21.0'
dll_version = (10, 2, 21, 0)

# 音声合成エンジンを示す型
H_AQTKDA = c_void_p

class AquesTalk2Error(Exception):
    u"""
    音声合成などの失敗を表す

    属性
        err_code 失敗理由をあらわす整数
    """
    err_messages = {
            100: u'その他のエラー',
            101: u'メモリ不足',
            102: u'音声記号列に未定義の読み記号が指定された',
            103: u'韻律データの時間長がマイナスなっている',
            104: u'内部エラー',
            105: u'音声記号列に未定義の読み記号が指定された',
            106: u'音声記号列のタグの指定が正しくない',
            107: u'タグの長さが制限を越えている',
            108: u'タグ内の値の指定が正しくない',
            109: u'WAVE 再生ができない',
            110: u'WAVE 再生ができない',
            111: u'発声すべきデータがない',
            200: u'音声記号列が長すぎる',
            201: u'１つのフレーズ中の読み記号が多すぎる',
            202: u'音声記号列が長い',
            203: u'ヒープメモリ不足',
            204: u'音声記号列が長い',
            1000: u'Phont データが正しくない',
            1001: u'Phont データが正しくない',
            1002: u'Phont データが正しくない',
            1003: u'Phont データが正しくない',
            1004: u'Phont データが正しくない',
            1005: u'Phont データが正しくない',
            1006: u'Phont データが正しくない',
            1007: u'Phont データが正しくない',
            1008: u'Phont データが正しくない',
            }

    def __init__(self, err_code):
        self.err_code = err_code
        err_message = self.err_messages.get(self.err_code, '')
        if err_message:
            self.err_message = u'%d %s' % (
                    self.err_code, err_message)
        else:
            self.err_message = u'%d' % self.err_code

    def __unicode__(self):
        return self.err_message

    def __str__(self):
        return str(self.__unicode__())


def _errcheck(result, func, args):
    u"""戻り値として正常 0 異常 非0 を返す外部関数用の err_check 関数"""

    if result != 0:
        raise AquesTalk2Error(result)
    return None

def _synthecheck(result, func, args):
    u"""AquesTalk2_Synthe 外部関数用の err_check 関数"""

    if not result:
        raise AquesTalk2Error(args[2].value)
    return result, args[2].value

def _isplaycheck(result, func, args):
    u"""AquesTalk2Da_IsPlay 外部関数用の err_check 関数"""

    return bool(result)


# AquesTalk2.dll wav 生成担当
try:
    _AquesTalk2 = windll.LoadLibrary(
            os.path.join(os.path.dirname(__file__), 'AquesTalk2'))
except WindowsError:
    _AquesTalk2 = windll.AquesTalk2

# 音声記号列から音声波形を生成する
_prototype = (POINTER(c_char), c_char_p, c_int, POINTER(c_int), c_void_p)
_paramflags = (
        (1, 'koe'), (1, 'iSpeed', 100), (2, 'pSize'),
        (1, 'phontDat', None))
AquesTalk2_Synthe = WINFUNCTYPE(*_prototype)(
        ('AquesTalk2_Synthe', _AquesTalk2), _paramflags)
AquesTalk2_Synthe.errcheck = _synthecheck

# 音声データの領域を開放
_prototype = (None, c_char_p)
_paramflags = ((1, 'wav'),)
AquesTalk2_FreeWave = WINFUNCTYPE(*_prototype)(
        ('AquesTalk2_FreeWave', _AquesTalk2), _paramflags)

# AquesTalk2Da.dll サウンドデバイス出力担当
try:
    _AquesTalk2Da = windll.LoadLibrary(
            os.path.join(os.path.dirname(__file__), 'AquesTalk2Da'))
except WindowsError:
    _AquesTalk2Da = windll.AquesTalk2Da

# 同期タイプの音声合成
_prototype = (c_int, c_char_p, c_int, c_void_p)
_paramflags = ((1, 'koe'), (1, 'iSpeed', 100), (1, 'phontDat', None))
AquesTalk2Da_PlaySync = WINFUNCTYPE(*_prototype)(
        ('AquesTalk2Da_PlaySync', _AquesTalk2Da), _paramflags)
AquesTalk2Da_PlaySync.errcheck = _errcheck

# 音声合成エンジンのインスタンスを生成（非同期タイプ）
_prototype = (H_AQTKDA,)
_paramflags = ()
AquesTalk2Da_Create = WINFUNCTYPE(*_prototype)(
        ('AquesTalk2Da_Create', _AquesTalk2Da), _paramflags)

# 音声合成エンジンのインスタンスを解放（非同期タイプ）
_prototype = (None, H_AQTKDA)
_paramflags = ((1, 'hMe'),)
AquesTalk2Da_Release = WINFUNCTYPE(*_prototype)(
        ('AquesTalk2Da_Release', _AquesTalk2Da), _paramflags)

# 非同期タイプの音声合成
_prototype = (
        c_int, H_AQTKDA, c_char_p, c_int, c_void_p, HWND, c_ulong, c_ulong)
_paramflags = (
        (1, 'hMe'), (1, 'koe'), (1, 'iSpeed', 100), (1, 'phontDat', None),
        (1, 'hWnd', 0), (1, 'msg', 0), (1, 'dwUser', 0))
AquesTalk2Da_Play = WINFUNCTYPE(*_prototype)(
        ('AquesTalk2Da_Play', _AquesTalk2Da), _paramflags)
AquesTalk2Da_Play.errcheck = _errcheck

# 発声の停止
_prototype = (None, H_AQTKDA)
_paramflags = ((1, 'hMe'),)
AquesTalk2Da_Stop = WINFUNCTYPE(*_prototype)(
        ('AquesTalk2Da_Stop', _AquesTalk2Da), _paramflags)

# 再生中か否か
_prototype = (c_int, H_AQTKDA)
_paramflags = ((1, 'hMe'),)
AquesTalk2Da_IsPlay = WINFUNCTYPE(*_prototype)(
        ('AquesTalk2Da_IsPlay', _AquesTalk2Da), _paramflags)
AquesTalk2Da_IsPlay.errcheck = _isplaycheck

del _prototype
del _paramflags


def talk(sign, speed=100, phont=None):
    u"""sign 音声記号列を元にサウンドデバイスより発声する
    
    同期タイプの処理のため発声終了するまで戻らない。

    引数:
        sign 音声記号列
        speed 発音速度 50 - 300
    戻り値:
        なし
    例外：
        AquesTalk2Error 発音失敗
    """

    if isinstance(sign, unicode):
        sign = sign.encode('cp932')
    AquesTalk2Da_PlaySync(koe=sign, iSpeed=speed, phontDat=phont)

def synthe(sign, speed=100, phont=None):
    u"""sign 音声記号列より音声データを生成して返す

    フォーマットは Microsoft Wave 。

    引数:
        sign 音声記号列
        speed 発音速度 50 - 300
    戻り値:
        音声データ
    例外：
        AquesTalk2Error 音声合成失敗
    """

    if isinstance(sign, unicode):
        sign = sign.encode('cp932')
    wav, size = AquesTalk2_Synthe(koe=sign, iSpeed=speed, phontDat=phont)
    voice = wav[0:size]
    AquesTalk2_FreeWave(wav=wav)
    return voice

def write_wav(path, sign, speed=100, phont=None):
    u"""音声データファイルを作成するショートカット関数

    フォーマットは Microsoft Wave 。

    引数:
        path Wave データを保存するファイルパス
        sign 音声記号列
        speed 発音速度 50 - 300
    戻り値:
        なし
    例外：
        AquesTalk2Error 音声合成失敗
    """

    voice = synthe(sign, speed, phont)
    with open(path, 'wb') as f:
        f.write(voice)

def phont_from_path(path):
    u"""声の種類を規定する Phont データをファイルから読み込む"""

    with open(path, 'rb') as f:
        py_phont = f.read()
    c_phont = c_char_p(py_phont)
    return c_phont

def main():
    if len(sys.argv) < 2:
        exe = os.path.basename(__file__)
        sys.stderr.write(u'usage: %s voice_sign\n' % exe)
        sys.stderr.write(u'ex: %s あくえすとーくつー\n' % exe)
        sys.exit(1)

    for sign in sys.argv[1:]:
        talk(sign)

if __name__ == '__main__':
    main()
