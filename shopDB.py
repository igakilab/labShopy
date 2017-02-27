#! /usr/bin/env python
# -*- coding:utf-8 -*-

import pymongo
from datetime import datetime

class ShopDB:

    """ショップのデータベースへのアクセスを簡単にできるように各操作をメソッドにしてまとめたクラス"""
    
    def __init__(self, address = "localhost", port = 27017):
        self.__client = pymongo.MongoClient(address, port)
        self.__db = self.__client.labshop
        
    def isMember(self, memberId):
        return self.__db.member.find_one({"id": memberId}) != None
    
    def getMemberStatus(self, memberId):
        member = self.__db.member.find_one({"id": memberId})
        return MemberStatus(member["name"], member["balance"])
    
    # def addMember(self, memberId, memberName):
    #     pass
    
    def buyItem(self, memberId, itemId, count = 1):
        if count == 0 :
            return
        member = self.__db.member.find_one({"id": memberId})
        item = self.__db.item.find_one({"id": itemId})
        price = int(item["price"])
        if int(member["balance"]) < price * count :
            raise InsufficientFundsException("残高が足りません．");
        if int(item["count"]) < count :
            raise ShortageException("在庫が足りません．")
        lastAccountId = int(self.__db.account.find()[self.__db.account.count()-1]["id"])
        for i in xrange(count) :
            self.__db.account.insert_one({"id": lastAccountId + i + 1, "timestamp": datetime.utcnow(), "memberId": memberId, "itemId": itemId, "sellPrice": price})
        self.__db.member.update_one({"id": memberId}, {"$inc":{"balance":-(price * count)}})
        self.__db.item.update_one({"id": itemId}, {"$inc":{"count":-count}})

    def getFoodList(self):
        foods = self.__db.item.find({"isFood": True, "isOnSale":True})
        return [ShopItem(foods[i]["id"], foods[i]["name"], foods[i]["price"], foods[i]["count"]) for i in xrange(foods.count())]
    
    def getDrinkList(self):
        drinks = self.__db.item.find({"isDrink": True, "isOnSale":True})
        return [ShopItem(drinks[i]["id"], drinks[i]["name"], drinks[i]["price"], drinks[i]["count"]) for i in xrange(drinks.count())]

    def __del__(self):
        self.__client.close()

class MemberStatus:

    '''利用者のデータクラス　名前と残高の表示に使うべし'''
    
    def __init__(self, name, balance):
        self.name = name.encode("utf-8")
        self.balance = int(balance)
    
    def __str__(self):
        return self.name + ", 残高:" + str(self.balance) + "円"

class ShopItem:

    '''商品のデータクラス　表示用'''
    
    def __init__(self, itemId, name, price, count):
        self.itemId = int(itemId)
        self.name = name.encode("utf-8")
        self.price = int(price)
        self.count = int(count)
    
    def __str__(self):
        return str(self.itemId) + " : " + self.name + ", 金額" + str(self.price) + "円, 残り" + str(self.count) + "個"

class InsufficientFundsException(Exception):

    '''残高不足であるにもかかわらず何かを購入しようとした際にbuyItemで投げられる例外'''
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class ShortageException(Exception):

    '''在庫よりも多くのものを購入しようとした際にbuyItemで投げられる例外'''
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
