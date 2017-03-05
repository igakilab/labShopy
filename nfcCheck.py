#! /usr/bin/env python
# -*- coding:utf-8 -*-

'''nfcタグの読み取りにはnfcCheck()を使ってください'''

import nfc
from shopDB import ShopDB

def on_connect(tag):
    # 必要なデータが格納されているのはシステムコード0xFE00なのでpollingして切り替える
    idm, pmm = tag.polling(system_code=0xFE00)
    tag.idm, tag.pmm, tag.sys = idm, pmm, 0xFE00
    # サービスコード0x1A8Bに学籍番号と名前のデータがあるのでそこにアクセスする
    sc = nfc.tag.tt3.ServiceCode(106, 0x0b)
    # ブロックコード0が学籍番号
    bc = nfc.tag.tt3.BlockCode(0, service=0)
    data = tag.read_without_encryption([sc], [bc])
    # 学科ごとのアルファベットを数値に変換し,intに直す
    studentNumber = int(data.decode("shift-jis")[2:8].replace("B", "2").replace("C", "3").replace("N", "4").replace("Q", "5"))
    # ブロックコード1が氏名だが今回は使用しない
    # bc = nfc.tag.tt3.BlockCode(1, service=0)
    # data = tag.read_without_encryption([sc], [bc])
    # print 'name:', data.decode("shift-jis")
    # mongoDBのサーバにアクセスする,IPアドレスとポートはShopDBの第一・第二引数で変更できる
    # デフォルトはlocalhost:27017
    sdb = ShopDB()
    tag.memberStatus = None
    if sdb.checkMember(studentNumber, idm, pmm) :
        tag.memberStatus = sdb.getMemberStatus(studentNumber)

def nfcCheck():
    # nfcタグを感知すると読み取った学籍番号からMemberStatusのインスタンスを返す．
    # 認識できなかった場合・タグが学生証のものでない場合はNoneを返す
    with nfc.ContactlessFrontend('usb') as clf:
        return clf.connect(rdwr={'on-connect': on_connect}).memberStatus
    
# テスト用
if __name__ == '__main__':
    memberStatus = nfcCheck()
    if memberStatus == None:
        exit()
    print memberStatus
    sdb = ShopDB()
    for food in sdb.getFoodList():
        print food
    for drink in sdb.getDrinkList():
        print drink
    sdb.buyItem(memberStatus.memberId, 100401, 1)
