# Pwn | Arbacoin bank

## Информация

> Мы уже давно присматривались к банку Arbalest of Siberia.
> 
> Там они хранят свои сбережения, которые используют для проведения странных мероприятий.
> 
> Мы смогли раздобыть внутренности сервисов банка.
> 
> Посмотри, может у тебя получиться найти уязвимость и проэксплуатировать что нибудь.
> 
> `nc <ip> <port>`
>
> `flag in /tmp/flag.txt`

## Запуск

Отдать командам всё из deploy/static и ip-адрес сервера

```sh
cd deploy
docker-compose up --build -d 
```


## Описание

ELF 64bit, C, no strip, no pack

Суть задания - проэксплуатировать уязвимость с созданием фейк-чанка и перезаписать GOT.


## Решение

1. Через создание и освобождение фейк-чанка в имени пользователя можно получить утечку адреса
2. По ней восстановить адреса внутри libc и найти one_gadget
3. Дальше через AW в структуре ячейки перезаписать GOT (например, функцию exit)


[Пример эксплоита](solve/exploit.py)


## Флаг

`Cup{bad9864c0db6f5be2bd95e35d5b387bb2b8edc60da469073b110800e6978f2b5}`