import discord
from discord.ext import commands
import asyncio

perms = {}

def pull_perms():
    print('pulling perms')
    F = open('perms.txt')
    f_perms = F.readlines()

    for p in f_perms:
        p2 = p.split(' ----- ')
        perms[int(p2[0])] = int(p2[1])

def push_perms():
    print('pushing perms')
    F = open('perms.txt', 'w')
    for k in perms.keys():
        F.write(f'{k} ----- {perms[k]}\n')

def getperm(id):
    if id in perms.keys():
        return perms[id]
    perms[id] = 0
    return 0

def is_admin(person):
    F = open('admin.txt')
    admins = F.readlines()

    for i in range(len(admins)):
        if (admins[i] == person):
            return True
    return False

def is_mooderator(person):
    for role in person.roles:
        if role.name == 'Mooderator':
            return True
    return False

message_counts = {}
penalty = {}

def pull_penalty():
    print('pulling penalties')
    F = open('penalty.txt')
    f_penalty = F.readlines()

    for p in f_penalty:
        p2 = p.split(' ----- ')
        penalty[int(p2[0])] = int(p2[1])

def push_penalty():
    F = open('penalty.txt', 'w')
    for k in penalty.keys():
        F.write(f'{k} ----- {penalty[k]}\n')

def get_penalty(user):
    if user in penalty.keys():
        penalty[user] = min(86400, penalty[user] * 2)
        return penalty[user]
    penalty[user] = 20
    push_penalty()
    return 10

messages = []

star_started = False
spam_detected = False

client = discord.Client()